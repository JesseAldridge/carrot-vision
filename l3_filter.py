import sys, os, math

import numpy as np
import cv2

import l0_image, l2_cluster

def filter_matches(needle, hay, max_dist_from_median=60):

  points1, points2, match_dists, kmeans, biggest_group = l2_cluster.get_match_points(needle, hay)

  if len(points1) == 0:
    return [], [], match_dists, kmeans

  # Delete outlying points.

  median_x = np.median([p[0] for i, p in biggest_group])
  median_y = np.median([p[1] for i, p in biggest_group])

  biggest_group = [
    (i, p) for i, p in biggest_group
    if math.sqrt((median_x - p[0]) ** 2 + (median_y - p[1]) ** 2) <= max_dist_from_median]
  points1 = [points1[i] for i, _ in biggest_group]
  points2 = [points2[i] for i, _ in biggest_group]
  match_dists = [match_dists[i] for i, _ in biggest_group]

  # Delete points that don't have proportianal dist in needle and hay.

  ratios = []
  for i in range(1, len(points1)):
    p1_1, p1_2 = points1[i - 1], points1[i]
    p2_1, p2_2 = points2[i - 1], points2[i]
    mag1 = (p1_2[0] - p1_1[0]) ** 2 + (p1_2[1] - p1_1[1]) ** 2
    mag2 = (p2_2[0] - p2_1[0]) ** 2 + (p2_2[1] - p2_1[1]) ** 2
    ratio = float(mag1) / mag2 if mag2 != 0 else 0
    ratios.append((i - 1, ratio))

  keep_indexes = set()
  median_ratio = np.median(ratios, axis=0)[1] if ratios else None
  for i, ratio in ratios:
    if ratio >= median_ratio * .5 and ratio <= median_ratio * 2 or median_ratio == 0:
      keep_indexes.add(i)

  points1, points2, match_dists = [
    [list_[i] for i in keep_indexes] for list_ in points1, points2, match_dists]

  if len(points1) == 1:
    points1, points2 = [], []
  return points1, points2, match_dists, kmeans

if __name__ == '__main__':
  # needle_path = 'stuff/needles/oroweat.jpeg'
  # hay_path = os.path.expanduser('~/Desktop/frames/out0144.png')
  # hay_path = '/Users/jessealdridge/Desktop/frames/out0300.png'

  # needle_path = 'stuff/needles/bud-light.jpeg'
  # hay_path = os.path.expanduser('~/Desktop/frames/out0001.png')
  # hay_path = os.path.expanduser('~/Desktop/frames/out0261.png')

  needle_path = 'stuff/needles/jb.jpg'
  hay_path = os.path.expanduser('~/Desktop/frames/out0007.png') # oh god why
  # hay_path = os.path.expanduser('~/Desktop/frames/out0077.png')
  # hay_path = os.path.expanduser('~/Desktop/frames/out0261.png')
  # hay_path = os.path.expanduser('~/Desktop/frames/out0300.png')
  # hay_path = os.path.expanduser('~/Desktop/frames/out0301.png')

  # needle_path = 'stuff/needles/therma_vid-large.mp4care.jpeg'
  # hay_path = os.path.expanduser('~/Desktop/frames/out0622.png')

  # needle_path = 'stuff/needles/frosted_flakes.jpg'
  # hay_path = os.path.expanduser('~/Desktop/frames/out1176.png')

  # needle_path = 'stuff/needles/therma_care.jpeg'
  # hay_path = os.path.expanduser('~/Desktop/frames/out0622.png')


  needle = l0_image.Image(needle_path)
  hay = l0_image.Image(hay_path, resize=.5)

  points1, points2, match_dists, kmeans = filter_matches(needle, hay)
  canvas = l2_cluster.create_match_image(
    needle.image, hay.image, points1, points2, match_dists, kmeans.cluster_centers_)
  l0_image.display(canvas)
  print 'points:', len(points1), 'inertia:', kmeans.inertia_ if kmeans else None
  print 'mean_dist:', np.mean(match_dists) if match_dists else 0
