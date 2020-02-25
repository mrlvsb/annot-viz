# Annotation Vizualizator


## Installation

In a new virtual env run:

```
$ pip install -U pip setuptools wheel
$ pip install -r requirements.txt
```


## Usage

`pythom main.py <annotation-file> <directory with images corresponding to annotation-file> [<landmarks-file>]`


## Getting images from video

```
ffmpeg -i input.avi -q:v 2 -f image2 output_dir/img%06d.jpg
```