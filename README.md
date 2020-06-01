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

- `left`/`right` arrow (&larr;/&rarr;) - next/previous frame
- `PgUp`/`PgDn` - next/previous 24 frames
- `j`/`k` - next/previous 200 frames


## Getting Images from Video

```
ffmpeg -i input.avi -q:v 2 -f image2 output_dir/img%06d.jpg
```

## Example of a landmark file

- one frame per line

```
filename mean.x mean.y face_lms eyebrow1_lms eyebrow2_lms nose_lms nostril_lms eye1_lms eye2_lms lips_lms teeth_lms 
```

`_lms` stands for landmarks

