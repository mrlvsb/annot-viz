# anot-viz

## Getting images

```
ffmpeg -i face-5.avi -q:v 2 -f image2 face-5_out/img%06d.jpg
```