# Annotation Vizualizator


## Installation

In a new virtual env run:

```
pip install -U pip setuptools wheel
pip install -r requirements.txt
```


## Usage

`pythom main.py <annotation-file> <directory with images corresponding to annotation-file> [<landmarks-file>]`

or

`pythom main.py -n <landmarks-file> <directory with images corresponding to landmarks-file>`


### Keyboard

- left/right arrow - next/previous frame
- PgUp/PgDn - next/previous 24 frames


## Getting Images from Video

```
ffmpeg -i input.avi -q:v 2 -f image2 output_dir/img%06d.jpg
```