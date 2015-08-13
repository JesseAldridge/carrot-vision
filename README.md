
Carrot Vision
-------------

![Example](stuff/example.png)

Setup
-------

Install libs:

    brew install opencv
    brew install ffmpeg
    brew install youtube-dl
    sudo pip install sklearn
    sudo pip install numpy

Get the test video (500 MB):

    youtube-dl https://www.youtube.com/watch?v=Bs5zfeKced8

Split the video into frames:

    mkdir ~/carrot-frames
    ffmpeg -i "path/to/video.mp4" -vf fps=1 ~/carrot-frames/out%03d.png

Run the analysis and dump to csv:

    python -u l4_frames.py ~/carrot-frames/out*.png | tee out.csv
