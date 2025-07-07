# revamp_level35.py — Cluster t-SNE Coordinates
import os
import json
import numpy as np
from sklearn.cluster import DBSCAN
import shutil

INPUT_JSON = "output/revamp_level34/tsne_plot_coords.json"
INPUT_AUDIO = "output/revamp_level31/sliced/"
OUTPUT_DIR = "output/revamp_level35/clusters/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load 2D coords
with open(INPUT_JSON, "r") as f:
    coords = json.load(f)

filenames = list(coords.keys())
points = np.array([coords[f] for f in filenames])

# DBSCAN clustering
clustering = DBSCAN(eps=50, min_samples=1).fit(points)
labels = clustering.labels_

# Save into folders by cluster
for fname, cluster_id in zip(filenames, labels):
    cluster_folder = os.path.join(OUTPUT_DIR, f"cluster_{cluster_id}")
    os.makedirs(cluster_folder, exist_ok=True)
    
    src = os.path.join(INPUT_AUDIO, fname)
    dst = os.path.join(cluster_folder, fname)
    shutil.copyfile(src, dst)

# Save cluster log
log = {fname: int(cid) for fname, cid in zip(filenames, labels)}
with open(os.path.join(OUTPUT_DIR, "cluster_log.json"), "w") as f:
    json.dump(log, f, indent=2)

print(f"✅ Level 35 complete — clusters saved to: {OUTPUT_DIR}")
