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
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

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
	import time

	# Set the correct serial port for your Arduino (e.g., COM3, /dev/ttyACM0, etc.)
	SERIAL_PORT = '/dev/ttyACM0'  # Change this to your serial port
	BAUD_RATE = 115200

	# Establish a serial connection
	ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)


	def send_command(command):
		"""Send a command to the Arduino."""
		ser.write(f"{command}\n".encode())

	def turn_motor_on():
		"""Send command to turn the motor on."""
		send_command(1)

	def turn_motor_off():
		"""Send command to turn the motor off."""
		send_command(2)

	def set_servo_angle(angle):
		"""Send command to set the servo to a specific angle."""
		if 0 <= angle <= 180:
			send_command(3)
			send_command(round(angle))
			print(f'Angle - {round(angle)}')
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
    delta=0.03,
):
    direction = 0.0
    weight = 0.0
    # process frames until EOS or the user exits
    while True:
        await asyncio.sleep(0)
        # capture the next image
        img = input_capture.Capture()

        if img is None: # timeout
            continue
        
        # detect objects in the image (with overlay)
        detections = detect_net.Detect(img, overlay=args.overlay)

        # print the detections
        #print("detected {:d} objects in image".format(len(detections)))
        
        nearest = {}

        for detection in detections:
            if detection.ClassID not in nearest:
                nearest[detection.ClassID] = detection
            elif nearest[detection.ClassID].Area < detection.Area:
                nearest[detection.ClassID] = detection
        
        #print(nearest)
        
        if len(nearest) == 0:
            direction += delta * (0 - direction)
            weight += delta * (1 - weight)
        elif len(nearest) == 1:
            for detection in nearest.values():
                if detection.Area < 5000:
                    dx = detection.Center[0] - resolution / 2
                elif detection.Center[0] < resolution / 2:
                    dx = detection.Center[0]
                else:
                    dx = detection.Center[0] - resolution
                direction += delta * (dx - direction)
                weight += delta * (1 - weight)
        else:
            dx = 0.0
            for detection in nearest.values():
                dx += detection.Center[0] - resolution / 2
            dx /= len(nearest)
            direction += delta * (dx - direction)
            weight += delta * (1 - weight)
        
        if weight != 0.0:
            if len(nearest) == 0:
                data["direction"] = -direction / weight
            else:
                data["direction"] = direction / weight
            x = resolution / 2 + data["direction"]
            cudaDrawLine(img, (x, 0), (x, resolution - 1), (255, 127, 0, 200), 10)

        # render the image
        output_capture.Render(img)

        # update the title bar
        output_capture.SetStatus(
            "{:s} | Network {:.0f} FPS | {}".format(
                args.network,
                detect_net.GetNetworkFPS(),
                data.get("command", ""),
            )
        )

        # print out performance info
        #net.PrintProfilerTimes()

        # exit on input/output EOS
        if not input_capture.IsStreaming() or not output_capture.IsStreaming():
            break
    data["stop"] = True

async def send_commands(data, frequency=1, threshold=25):
    while not data["stop"]:
        await asyncio.sleep(frequency)
        if "direction" not in data:
            continue
        
        direction = data["direction"]
        
        if direction is None:
            break
        
        commands = []
        
        if abs(direction) < threshold:
            commands.append("straight")
        
        if direction < 0:
            commands.append("left")
            set_servo_angle(direction *4 / 10 + 90)
        else:
            commands.append("right")
            set_servo_angle(direction *4 / 10 + 90)
        commands.append(str(round(direction / 10 + 90)))
        data["command"] = " ".join(commands)

async def main():
    data = {"stop": False}
    turn_motor_on()
    await asyncio.gather(
        read_data(input_capture, output_capture, detect_net, data),
        send_commands(data),
    )
    turn_motor_off()

asyncio.run(main())


