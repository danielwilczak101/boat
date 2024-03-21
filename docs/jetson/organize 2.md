# Orginize the data

1. Create a version folder in `data/`. In this example we create `v1`.

2. Run the command below or copy your `train, test, and valid` data into the version folder.
```bash
cp -r /media/boat/wilczak/pool_buoys.v1i.voc/* ~/Desktop/boat/jetson/data/v2/
```

3. In your v1 folder updated your `labels.txt` with the labels you used. You can check by opening the xml files from your data.

4. Go back into the main directory and run `cp -r /media/boat/wilczak/pool_buoys.v1i.voc/* ~/Desktop/boat/jetson/data/v2/`.

5. Done. Your data is now in the proper format.