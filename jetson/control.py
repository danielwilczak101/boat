#!/usr/bin/env python3

import sys
import argparse
import asyncio

from jetson_inference import detectNet
from jetson_utils import cudaDrawLine, videoSource, videoOutput, Log

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
    model="models/v1/ssd-mobilenet.onnx",
    labels="models/v1/labels.txt", 
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

async def read_data(
    input_capture,
    output_capture,
    detect_net,
    data,
    resolution=640.0,
    delta=0.1,
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
        
        if len(nearest) == 1:
            for detection in nearest.values():
                if detection.Center[0] < resolution / 2:
                    dx = detection.Center[0]
                else:
                    dx = detection.Center[0] - resolution
                direction += delta * (dx - direction)
                weight += delta * (1 - weight)
        elif len(nearest) > 1:
            dx = 0.0
            for detection in nearest.values():
                dx += detection.Center[0] - resolution / 2
            dx /= len(nearest)
            direction += delta * (dx - direction)
            weight += delta * (1 - weight)
        
        if weight != 0.0:
            data[:] = [direction / weight]
            x = resolution / 2 + data[0]
            cudaDrawLine(img, (x, 0), (x, resolution - 1), (255, 127, 0, 200), 10)

        # render the image
        output_capture.Render(img)

        # update the title bar
        output_capture.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, detect_net.GetNetworkFPS()))

        # print out performance info
        #net.PrintProfilerTimes()

        # exit on input/output EOS
        if not input_capture.IsStreaming() or not output_capture.IsStreaming():
            break
    data[:] = [None]

async def send_commands(data, frequency=1, threshold=25):
    command = ""
    while True:
        await asyncio.sleep(frequency)
        if not data:
            continue
        
        direction = data[0]
        
        if direction is None:
            break
        
        new_command = []
        if abs(direction) < threshold:
            new_command.append("straight")
        if direction < 0:
            new_command.append("left")
        else:
            new_command.append("right")
        new_command = " ".join(new_command)
        
        if command != new_command:
            print(new_command)
        command = new_command

async def main():
    data = []
    await asyncio.gather(
        read_data(input_capture, output_capture, detect_net, data),
        send_commands(data),
    )

asyncio.run(main())

