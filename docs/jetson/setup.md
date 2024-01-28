## Setup:

### Install operating system
Install Jetpack Ubuntu OS using the [jetpack jdk]().

!!! Warning

    Make sure `/dev/mmcblk0p1` has more then 28gb of space or download wont work. Install gpart, **remove all the non root partitions** and then resize the root partition.

### Fix Partitions (Optional)
```
sudo apt-get install gparted
```

Open gpart and find the drive with all the partitions. Delete everything evcept the root partition. Once that happens resive the root partition to take advantage of the whole hard drive.

### Setup code / Docker.
Open a terminal and grab the code.
```
cd Desktop
git clone --recursive https://github.com/dusty-nv/jetson-inference
```

Docker setup script. (Takes ~30mins on shitty lab wifi.)
```
cd jetson-inference
docker/run.sh
```

### Basic testing.
Check what the camera name is:
```
ls /dev/video*
```

Open the camera feed:
```
video-viewer /dev/video0
```

Run your first object detection example (It will first install the model ~5mins):
```
detectnet /dev/video0
```
