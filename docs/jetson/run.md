# Run code:
```
docker/run.sh --volume /home/boat/Desktop/bouy/:/jetson-inference/bouy/;
cd bouy;
```           

## Detect
```
python3 detect.py --model=models/v1/ssd-mobilenet.onnx --labels=models/v1/labels.txt --input-width=640 --input-height=640 /dev/video1
```

## Control
```
python3 control.py --model=models/v1/ssd-mobilenet.onnx --labels=models/v1/labels.txt --input-width=640 --input-height=640 /dev/video1
```