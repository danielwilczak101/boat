## Setup:
Open a terminal and run this commands.
```
cd Desktop/jetson-inference/
```
```
docker/run.sh --volume /home/boat/Desktop/boat/:/jetson-inference/boat/
```       
```
cd boat
```   

## Detect
Detect is if you just want to see the model bounding boxes without an control operations. Good for new labeled dataset testing.
```
python3 detect.py --model=models/v1/ssd-mobilenet.onnx --labels=models/v1/labels.txt --input-width=640 --input-height=640 /dev/video1
```

## Control
```
python3 control.py --model=models/v1/ssd-mobilenet.onnx --labels=models/v1/labels.txt --input-width=640 --input-height=640 /dev/video1
```