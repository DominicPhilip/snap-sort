# Python-Sort-Image
A program that sorts JPEG and TIFF images into folders according to date of which the image was made or created.

## Features

Recursive - Gets all images from given folder.

Logging - Records files not proccessed.

Duplicate Checks - Images are checked for duplicates before being proccessed.

Space Checks - Destination Folder is checked for adequete space before being proccessed.

Colorful - Nice color coded information.
##Dependencies and Installation

[Python 3](https://www.python.org/downloads) - The language behind this program.


[ExifRead](https://pypi.python.org/pypi/ExifRead) - Gets the tags of the images.

```
$ pip install exifread
```

[Psutil](https://pypi.python.org/pypi/psutil) - Gets available file space.

```
$ pip install psutil
```
