import glob, sys, os

import numpy as np

import l0_image, l3_filter

# Load needles and frames.

needles_path = os.path.join(os.path.dirname(__file__), 'stuff/needles')
filenames = os.listdir(needles_path)
needles = [l0_image.Image(os.path.join(needles_path, filename)) for filename in filenames]

frame_paths = glob.glob(os.path.expanduser('~/Desktop/frames/out030*.png'))
if len(sys.argv) > 1:
  frame_paths = sys.argv[2:]

# Compare each needle against each frame.

printed_col_labels = False
for frame_path in frame_paths:
  hay = l0_image.Image(frame_path, resize=.5)
  matches = {}
  for needle in needles:
    needle_name = os.path.basename(needle.path).rsplit('.', 1)[0]
    ps1, ps2, dists, kmeans = l3_filter.filter_matches(needle, hay)
    matches[needle_name] = {
      'count': len(ps1), 'inertia': round(kmeans.inertia_) if kmeans else -1}

  # Dump the results to a csv file.

  keys = ['count']
  col_labels = ['frame_path']
  values = [os.path.basename(frame_path)]
  for needle_index, item in enumerate(sorted(matches.iteritems(), key=lambda t: t[0])):
    needle_name, match_dict = item
    col_labels += [' '.join([needle_name, key]) for key in keys]
    values += [str(match_dict[k]) for k in keys]
  if not printed_col_labels:
    print ','.join(col_labels)
    printed_col_labels = True
  print ','.join(values)
