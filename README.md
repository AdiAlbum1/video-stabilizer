# Video Stabilizer

Video Stabilization algorithm implementation using OpenCV

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#Examples)

## Installation

```sh
git clone https://github.com/AdiAlbum1/video_stabilizer
cd video_stabilizer
pip install -r requirments.txt
```

## Usage

```sh
python stabilize_video.py -i in_vid.mp4 -o out_vid.mp4
```

1. press 'a' when you've setup and ready to go
2. select Region of Interest, the rest of the image will be cropped out
3. select number of points which should be veritcal, this is our global stablization point of view
4. Enjoy the stable video

## Examples

Side by side:
<br/><br/>
![](gifs/vid4/out_vid.gif)
