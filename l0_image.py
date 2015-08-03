import os, colorsys

import cv2
import numpy as np

'''
Load an image, run SIFT, and draw some test lines on it.
'''

detector = cv2.SIFT()

class BadImageException(Exception):
  pass

class Image:
  def __init__(self, path, resize=None):
    if not os.path.exists(path):
      raise Exception('image not found: {}'.format(path))
    self.path = path
    self.image = cv2.imread(path)
    if self.image is None:
      raise BadImageException()
    h, w, _ = self.image.shape
    if resize and resize != 1:
      self.image = cv2.resize(
        self.image, (int(round(w * resize)), int(round(h * resize))))
    self.features = Features(self.image)

class Features:
  def __init__(self, image):
    self.kp, self.desc = detector.detectAndCompute(image, None)

def draw_lines(canvas, points1, points2, line_strengths):
  min_strength = min(line_strengths) if line_strengths else 0
  max_strength = max(line_strengths) if line_strengths else 0

  for p1, p2, line_strength in zip(points1, points2, line_strengths):
    x1, y1 = p1
    x2, y2 = p2
    x1, y1, x2, y2 = [int(round(x)) for x in x1, y1, x2, y2]
    hue = 0
    if (max_strength - min_strength) != 0:
      hue = .5 * (line_strength - min_strength) / float(max_strength - min_strength)
    color = tuple(x * 255 for x in colorsys.hsv_to_rgb(hue, 1, 1))
    cv2.circle(canvas, (x1, y1), 2, color, -1)
    cv2.circle(canvas, (x2, y2), 2, color, -1)
    cv2.line(canvas, (x1, y1), (x2, y2), color)
  return canvas.copy()

def display(image):
  cv2.imwrite("stuff/out.png", image)
  os.system("open -a Preview stuff/out.png")

if __name__ == '__main__':
  image = Image('stuff/test_frames/bud-light-04_22.png', resize=.5)
  canvas = draw_lines(
    image.image, [(10,10), (20,20), (30,30)], [(100,10), (100,100), (100,200)], [1,2,3])
  display(canvas)
