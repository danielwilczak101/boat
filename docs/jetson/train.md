# Train and Save
The goal of this section is to retrain the `ssd-mobilenet` to recognize the objects you have labeled in your data.

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

## Training
Make sure you have a version folder in `data`` with the proper [orginized](https://danielwilczak101.github.io/boat/jetson/organize/) format.
```
python3 train.py --dataset-type=voc --data=data/v2 --model-dir=models/v2 --batch-size=2 --workers=1 --epochs=5 --resolution=640
```

## Save the model
Update the version number.
```
python3 save.py --input-model=models/mobilenet-v1-ssd-mp-0_675.pth --output-model=models/v1/ssd-mobilenet.onnx --resolution=640
```

## Run
Run the saved model to detect the objects.
```
python3 detect.py --model=models/v1/ssd-mobilenet.onnx --labels=models/v1/labels.txt --input-width=640 --input-height=640 /dev/video1
```