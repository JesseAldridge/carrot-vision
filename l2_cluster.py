import sys, os

import numpy as np
import cv2
from sklearn import cluster

import l0_image
import l1_match

'''
Find the biggest cluster of matched points.
'''

def get_match_points(needle, hay):

  # Group each point by its nearest mean.

  points1, points2, dists = l1_match.get_match_points(needle, hay)
  kmeans, biggest_group = None, []
  if len(points2) > 0:
    kmeans = progressive_kmeans(points2)
    groups = {}
    for point_index, point in enumerate(points2):
      group = kmeans.predict(point)[0]
      groups.setdefault(group, [])
      groups[group].append((point_index, point))
    biggest_group = max(groups.values(), key=lambda x: len(x))
  return points1, points2, dists, kmeans, biggest_group

def progressive_kmeans(points):

  # Find k-means with an increasing k until improvement slows.

  prev_kmeans = None
  for i in range(1, 9):
    kmeans = cluster.KMeans(n_clusters=i)
    kmeans.fit(points)
    if kmeans.inertia_ == 0:
      return kmeans
    prev_inertia = prev_kmeans.inertia_ if prev_kmeans else None
    improvement = None if prev_inertia is None else prev_inertia / kmeans.inertia_
    if improvement is not None and improvement < 2:
      break
    prev_kmeans = kmeans
  return prev_kmeans

def create_match_image(img1, img2, points1, points2, match_dists, ring_points):

  # Draw thick rings at each cluster centroid.

  canvas = l1_match.create_match_image(img1, img2, points1, points2, match_dists)
  h1, w1 = img1.shape[:2]
  for x, y in ring_points:
    cv2.circle(canvas, (int(x + w1), int(y)), 10, (0,255,0), 4)
  return canvas

if __name__ == '__main__':
  # needle = l0_image.Image('stuff/needles/jb.jpg')
  # hay_path = os.path.expanduser('~/Desktop/frames/out0301.png')

  needle = l0_image.Image('stuff/needles/bud-light.jpeg')
  hay_path = os.path.expanduser('~/Desktop/frames/out0271.png')

  hay = l0_image.Image(hay_path)
  points1, points2, sdists, kmeans, biggest_group = get_match_points(needle, hay)
  canvas = create_match_image(needle.image, hay.image, points1, points2, sdists, kmeans.cluster_centers_)
  l0_image.display(canvas)
