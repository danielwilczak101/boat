## Setup:
Open a terminal and run this commands. To ssh `ssh boat@192.168.0.196`.       

## Control
Controls is when you want the craft to run it's control operations for the compitions. Make sure to. Need to rebuild containe to fix this but that takes a hot minute. You can also run using the camera `/dev/video0`.

```
cd Desktop/jetson-inference/

docker/run.sh --volume /home/boat/Desktop/boat/:/jetson-inference/boat/

cd boat/

pip3 install pyserial-3.5-py2.py3-none-any.whl

cd jetson

python3 control.py --model=models/v3/mb1-ssd-Epoch-28-Loss-1.924500224325392.pth --labels=models/v3/labels.txt --input-width=640 --input-height=640 --input-blob=input_0 --output-cvg=scores --output-bbox=boxes --threshold=.15 --motor=1400 /dev/video0
```


## Web Viewer with Controls
Give the output to a server to view via a browser `webrtc://@:8554/output`.

```
cd Desktop/jetson-inference/

docker/run.sh --volume /home/boat/Desktop/boat/:/jetson-inference/boat/

cd boat/

pip3 install pyserial-3.5-py2.py3-none-any.whl

cd jetson

python3 control.py --model=models/v3/mb1-ssd-Epoch-28-Loss-1.924500224325392.pth --labels=models/v3/labels.txt --input-width=640 --input-height=640 --input-blob=input_0 --output-cvg=scores --output-bbox=boxes --threshold=.15 --motor=1400 /jetson-inference/boat/tasks/run4.mp4 webrtc://@:8554/output
```

## Videos
The goal of this page is to show users how to run the controls code using a video. This is good for dry run testing to see how the controls would work without having to be in the water. Example video is `/jetson-inference/boat/tasks/run4.mp4`. Put your video in the `tasks/` folder and run the code below.

```
cd Desktop/jetson-inference/

docker/run.sh --volume /home/boat/Desktop/boat/:/jetson-inference/boat/

cd jetson-inference/boat/jetson

python3 control.py --model=models/v3/mb1-ssd-Epoch-28-Loss-1.924500224325392.pth --labels=models/v3/labels.txt --input-width=640 --input-height=640 --input-blob=input_0 --output-cvg=scores --output-bbox=boxes --threshold=.15 --motor=1400 /jetson-inference/boat/tasks/run4.mp4
```