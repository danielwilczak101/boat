#!/usr/bin/env python3

import sys
import argparse
import asyncio

from jetson_inference import detectNet
from jetson_utils import cudaDrawLine, videoSource, videoOutput, Log

# True if running on the boat, false if on shadow mode.
ROBOT_CONNECTED = True

# parse the command line
parser = argparse.ArgumentParser(
    description="Locate objects in a live camera stream using an object detection DNN.", 
    formatter_class=argparse.RawTextHelpFormatter, 
    epilog=detectNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage(),
)

parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="Minimum detection threshold to use.")
parser.add_argument("--motor", type=float, default=1450, help="Speed of the motor to run on.")

try:
    args = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)

# create video sources and outputs
input_capture = videoSource(args.input, argv=sys.argv)
output_capture = videoOutput(args.output, argv=sys.argv)

# note: to hard-code the paths to load a model, the following API can be used:
#
detect_net = detectNet(
    model="models/v3/ssd-mobilenet.onnx",
    labels="models/v3/labels.txt", 
    input_blob="input_0",
    output_cvg="scores",
    output_bbox="boxes", 
    threshold=args.threshold,
)

RESOLUTION: float = 640.0
DELTA: float = 0.1
THRESHOLD: float = 25

direction: float = 0.0
weight: float = 0.0

if ROBOT_CONNECTED:
    import serial
    arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)

    def send_command(command, value):
        """
        Sends a command followed by an integer value to the Arduino.
        """
        command_str = f"{command},{value}\n"  # Format command string
        arduino.write(bytes(command_str, 'utf-8'))  # Send command

    def turn_motor_on():
        """Send command to turn the motor on."""
        print(f'motor on {round(args.motor)}')
        send_command(1, round(args.motor))

    def turn_motor_off():
        """Send command to turn the motor off."""
        send_command(2, 0)

    def set_servo_angle(angle, threshold=10):
        """Send command to set the servo to a specific angle."""
        
        # Set angle thresholds.
        if angle < -threshold:
            angle = -threshold
        elif angle > threshold:
            angle = threshold
        
        # Adjust: 100 = straight.
        angle += 100
        
        if 0 <= angle <= 180:
            angle = round(angle)
            send_command(3, angle)
            print(f"Angle {angle}")
        else:
            print("Invalid angle. Please enter a value between 0 and 180.")
    
else:
    def turn_motor_on():
        pass
    def turn_motor_off():
        pass
    def set_servo_angle(angle):
        pass


async def read_data(
    input_capture,
    output_capture,
    detect_net,
    data,
    resolution=640.0,
    delta=0.01,
    ensure_stop=True
):
    if ensure_stop:
        try:
            return await read_data(
                input_capture,
                output_capture,
                detect_net,
                data,
                resolution,
                delta,
                False,
            )
        finally:
            data["stop"] = True
    
    # Calculate the average direction over time.
    direction = 0.0
    weight = 0.0
    
    # Process frames until EOS or the user exits.
    while True:
        
        # Run other asynchronous code.
        await asyncio.sleep(0)
        
        # Capture the next image.
        img = input_capture.Capture()
        
        # Capture timed out, try again.
        if img is None:
            continue
        
        # Detect objects in the image (with overlay).
        detections = detect_net.Detect(img, overlay=args.overlay)
        
        # Calculate the nearest bouy of each color.
        nearest = {}

        for detection in detections:
            if detection.ClassID not in nearest:
                nearest[detection.ClassID] = detection
            elif nearest[detection.ClassID].Area < detection.Area:
                nearest[detection.ClassID] = detection
        
        # Calculate the direction to go.
        dx = 0.0
        
        for detection in nearest.values():
            # Really far bouy, go towards it.
            if detection.Area < 2000:
                dx += detection.Center[0] - resolution / 2
            # White bouy, go right.
            elif detection.ClassID == 1:
                dx += 100
            # Blue bouy, go left.
            elif detection.ClassID == 2:
                dx -= 100
            # Far bouy, go towards it.
            elif detection.Area < 4000:
                dx += detection.Center[0] - resolution / 2
            # Close bouy on the left, go right.
            elif detection.Center[0] < resolution / 2:
                dx += detection.Center[0]
            # Close bouy on the right, go left.
            else:
                dx += detection.Center[0] - resolution
        
        # Take the average of all of the directions.
        if len(nearest) > 0:
            dx /= len(nearest)
        
        # Update direction calculation.
        direction += delta * (dx - direction)
        weight += delta * (1 - weight)
        
        data["dx"] = dx
        # If no bouys seen, go in the opposite direction that it last went.
        # Roomba algorithm.
        if len(nearest) == 0:
            data["direction"] = -direction / weight
        
        # If bouys detected, follow the direction.
        else:
            data["direction"] = direction / weight
        
        # Draw the estimate of where to go on the image.
        x = resolution / 2 + data["direction"]
        cudaDrawLine(img, (x, 0), (x, resolution - 1), (255, 127, 0, 200), 10)

        # Render the image.
        output_capture.Render(img)

        # Update the title bar.
        output_capture.SetStatus(
            "{:s} | Network {:.0f} FPS | {}".format(
                args.network,
                detect_net.GetNetworkFPS(),
                data.get("command", ""),
            )
        )

        # Print out performance info.
        #net.PrintProfilerTimes()

        # Exit on input/output EOS.
        if not input_capture.IsStreaming() or not output_capture.IsStreaming():
            break

async def send_commands(data, frequency=1, threshold=25):
    # Loop until no new capture data.
    while not data["stop"]:
        
        # Run other asynchronous code.
        await asyncio.sleep(frequency)
        
        # Wait until first direction input.
        if "direction" not in data:
            continue
        
        # Get the next direction to go in.
        direction = 0.7 * data["direction"] + 0.3 * data["dx"]
        
        # Track recommended directions 
        commands = []
        
        # Only for printing purposes.
        if abs(direction) < threshold:
            commands.append("straight")
        
        # Only for printing purposes.
        if direction < 0:
            commands.append("left")
        else:
            commands.append("right")
        
        # Convert pixel direction to angle direction by dampening.
        direction /= 4
        
        commands.append(str(round(direction)))
        data["command"] = " ".join(commands)
        
        set_servo_angle(direction)
        await asyncio.sleep(0.3)
        set_servo_angle(0.0)

async def main():
    data = {"stop": False}
    
    try:
        turn_motor_on()
        
        # Read the data and send commands to the boat.
        await asyncio.gather(
            read_data(input_capture, output_capture, detect_net, data),
            send_commands(data),
        )
    
    finally:
        turn_motor_off()

asyncio.run(main())
