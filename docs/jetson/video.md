# Videos
The goal of this page is to show users how to run the controls code using a video. This is good for dry run testing to see how the controls would work without having to be in the water.

YOUTUBE VIDEO EXAMPLE HERE

## Setup
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
## Run
Put your video in the `videos/` folder and run the code below.

```
python3 detect.py --model=models/v1/ssd-mobilenet.onnx --labels=models/v1/labels.txt --input-width=640 --input-height=640 /video/<VIDEO FILE NAME>.mp4
```