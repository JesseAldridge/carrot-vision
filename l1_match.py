import sys, os

import cv2
import numpy as np

import config
import l0_image

'''
Find and display the corresponding keypoints between the two images.
'''

norm = cv2.NORM_L2
matcher = cv2.BFMatcher(norm)

def get_match_points(needle, hay):

  # Turn raw matches into lists of points.

  raw_matches = matcher.match(needle.features.desc, hay.features.desc)
  match_points1, match_points2, match_dists = [], [], []
  for match in raw_matches:
    if match.distance < 175:
      match_dists.append(match.distance)
      match_points1.append(needle.features.kp[match.queryIdx])
      match_points2.append(hay.features.kp[match.trainIdx])
  points1 = np.float32([keypoints.pt for keypoints in match_points1])
  points2 = np.float32([keypoints.pt for keypoints in match_points2])
  return points1, points2, match_dists

def create_match_image(img1, img2, points1, points2, match_dists):

  # Combine both images into a new one.  Draw lines.

  h1, w1 = img1.shape[:2]
  h2, w2 = img2.shape[:2]
  canvas = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
  canvas[:h1, :w1] = img1
  canvas[:h2, w1:w1+w2] = img2
  for i in range(len(points2)):
    points2[i][0] += w1

  return l0_image.draw_lines(canvas, points1, points2, match_dists)

if __name__ == '__main__':
  if len(sys.argv) == 1:

    needle_path = 'stuff/needles/oroweat.jpeg'
    hay_path = os.path.expanduser(config.get_frame('out0144.png'))
    # hay_path = '/Users/jessealdridge/Desktop/frames/out0302.png'

    # needle_path = 'stuff/needles/bud-light.jpeg'
    # hay_path = os.path.expanduser('~/Desktop/frames/out0001.png')
    # hay_path = os.path.expanduser('~/Desktop/frames/out0261.png')

    # needle_path = 'stuff/needles/jb.jpg'
    # hay_path = os.path.expanduser('~/Desktop/frames/out0077.png')
    # hay_path = os.path.expanduser('~/Desktop/frames/out0261.png')

    # needle_path = 'stuff/needles/therma_care.jpeg'
    # hay_path = os.path.expanduser('~/Desktop/frames/out0622.png')

  needle = l0_image.Image(needle_path)
  hay = l0_image.Image(hay_path)

  points1, points2, match_dists = get_match_points(needle, hay)
  canvas = create_match_image(needle.image, hay.image, points1, points2, match_dists)
  l0_image.display(canvas)
