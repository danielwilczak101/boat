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
Select the model you want to use. Look through your training results.
```
python3 save.py --input=models/v2/mb1-ssd-Epoch-3-Loss-2.3346897708045113.pth --output=models/v2/ssd-mobilenet.onnx --labels=models/v2/labels.txt  --resolution=640
```

## Run
Run the saved model to detect the objects.
```
python3 detect.py --model=models/v3/mb1-ssd-Epoch-28-Loss-1.924500224325392.pth --labels=models/v3/labels.txt --input-width=640 --input-height=640 --input-blob=input_0 --output-cvg=scores --output-bbox=boxes --threshold=.15 /jetson-inference/boat/tasks/run4.mp4
```

