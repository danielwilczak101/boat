# Orginize the data

1. Create a version folder in `data/`. In this example we create `v2`.

2. Run the command below or copy your `train, test, and valid` data into the version folder.

```bash
cp -r /media/boat/wilczak/pool_buoys.v1i.voc/* ~/Desktop/boat/jetson/data/v2/
```

3. Go back into the main directory and run 
```
cd jetson-inference/jetson

python3 orginize.py --folder_to_organize=data/v2
```

4. In your v2 folder updated your `labels.txt` with the labels you used. You can check by opening the xml files from your data.

5. Done. Your data is now in the proper format.