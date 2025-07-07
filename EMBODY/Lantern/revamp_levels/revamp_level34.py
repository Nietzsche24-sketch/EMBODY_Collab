# revamp_level34.py – t-SNE Dimensionality Reduction + Plot
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

INPUT_PATH = "output/revamp_level33/embody_vectors.json"
OUTPUT_DIR = "output/revamp_level34"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data
with open(INPUT_PATH, "r") as f:
    data = json.load(f)

vectors = []
labels = []
filenames = []

for fname, entry in data["fused_embeddings"].items():
    prosody = entry.get("prosody", {})
    vector = [
        prosody.get("duration_sec", 0),
        prosody.get("avg_rms", 0),
        prosody.get("zcr", 0),
        prosody.get("silence_ratio", 0),
        prosody.get("pitch_mean", 0),
        prosody.get("pitch_std", 0),
    ]
    vectors.append(vector)
    labels.append(fname)
    filenames.append(fname)

if not vectors:
    print("⚠️ No vectors found. Exiting.")
    exit()

X = np.array(vectors)
tsne = TSNE(n_components=2, perplexity=2, random_state=42)
reduced = tsne.fit_transform(X)

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(reduced[:, 0], reduced[:, 1], c="blue", s=50)
for i, label in enumerate(labels):
    plt.annotate(label, (reduced[i, 0], reduced[i, 1]), fontsize=8, alpha=0.7)

plt.title("t-SNE Projection of Prosody Embeddings")
plt.xlabel("Component 1")
plt.ylabel("Component 2")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "tsne_plot.png"))

# Save coordinates
tsne_coords = {k: [float(x), float(y)] for k, (x, y) in zip(filenames, reduced)}
with open(os.path.join(OUTPUT_DIR, "tsne_plot_coords.json"), "w") as f:
    json.dump(tsne_coords, f, indent=4)

print(f"✅ Level 34 complete — t-SNE plot saved to: {os.path.join(OUTPUT_DIR, 'tsne_plot.png')}")
