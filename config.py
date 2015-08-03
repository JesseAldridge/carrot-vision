import os

frames_path = os.path.expanduser("~/carrot-frames")

def get_frame(filename):
  return os.path.join(frames_path, filename)
