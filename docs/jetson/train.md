# Train and Save
Go in to the bouy folder.
```
cd Desktop/bouy
```

## Training
Make sure you have a version folder in `data`` with the proper [orginized]() format.
```
python3 train.py --dataset-type=voc --data=data/v1 --model-dir=models/v1 --batch-size=2 --workers=1 --epochs=5 resolution=640
```

## Save the model
Update the version number.
```
python3 save.py --input-model=models/mobilenet-v1-ssd-mp-0_675.pth --output-model=models/v1/ssd-mobilenet.onnx --resolution=640
```

## Run detect.
```
python3 detect.py --model=models/v1/ssd-mobilenet.onnx --labels=models/v1/labels.txt --input-width=640 --input-height=640 /dev/video1
```