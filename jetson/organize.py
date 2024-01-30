from pathlib import Path
import argparse

parser = argparse.ArgumentParser(
    description="Reorganize the images to the correct training folders."
)

# Params folder locations
parser.add_argument(
    "--folder_to_organize",
    default=None,
    type=str,
    help="Specify a specific subdirectory to organize, otherwise organize this directory.",
)

args = parser.parse_known_args()[0]
ROOT = Path().resolve()

# If the flag is set to update the directory.
if args.folder_to_organize is not None:
    ROOT /= args.folder_to_organize

# Stup the directory names.
JPEG_IMAGES = ROOT / "JPEGImages"
ANNOTATIONS = ROOT / "Annotations"
IMAGE_SETS = ROOT / "ImageSets"

# Create directories and files if they don't exist.
JPEG_IMAGES.mkdir(exist_ok=True)
ANNOTATIONS.mkdir(exist_ok=True)
(IMAGE_SETS / "Main").mkdir(exist_ok=True, parents=True)
(ROOT / "labels.txt").touch()

DIRECTORIES = dict(
    train=ROOT / "train",
    validation=ROOT / "valid",
    test=ROOT / "test",
)

file_names = {name: set() for name in ("train", "validation", "test")}

for name, directory in DIRECTORIES.items():
    files = [path for path in directory.iterdir() if path.is_file() and not path.stem.startswith(".")]
    for file in files:
        if file.suffix == ".jpg":
            file_names[name].add(file.stem)
            #file.rename(JPEG_IMAGES / file.name)
        elif file.suffix == ".xml":
            file_names[name].add(file.stem)
            #file.rename(ANNOTATIONS / file.name)

# Create the files with the image names in them. This is what
# training will use for train,test, and validation.
with open(IMAGE_SETS / "Main" / "train.txt", mode="w") as file:
    file.writelines("\n".join(file_names["train"]))

with open(IMAGE_SETS / "Main" / "val.txt", mode="w") as file:
    file.writelines("\n".join(file_names["validation"]))

with open(IMAGE_SETS / "Main" / "trainval.txt", mode="w") as file:
    file.writelines("\n".join(file_names["train"] | file_names["validation"]))

with open(IMAGE_SETS / "Main" / "test.txt", mode="w") as file:
    file.writelines("\n".join(file_names["test"]))