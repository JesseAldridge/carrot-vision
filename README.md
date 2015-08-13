
Carrot Vision
-------------

![Example](stuff/example.png)

Setup
-------

Install opencv:

    brew install opencv

  Look for this in the output of the above command.  If you see it, run the commands it tells you to run:

    ==> Caveats
    Python modules have been installed and Homebrew's site-packages is not
    in your Python sys.path, so you will not be able to import the modules
    this formula installed. If you plan to develop with these modules,
    please run:
      mkdir -p /Users/Jesse/Library/Python/2.7/lib/python/site-packages
      echo 'import site; site.addsitedir("/usr/local/lib/python2.7/site-packages")' >> /Users/Jesse/Library/Python/2.7/lib/python/site-packages/homebrew.pth

Install other stuff:

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
