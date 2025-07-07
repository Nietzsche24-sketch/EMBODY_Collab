# revamp_level34.py - t-SNE Embedding Visualizer for EMBODY
import os
import json
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from datetime import datetime

INPUT_PATH = "output/revamp_level33/embody_vectors.json"
OUTPUT_DIR = "output/revamp_level34"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data
with open(INPUT_PATH, "r") as f:
    data = json.load(f)

embeddings = data.get("fused_embeddings", {})
vectors = []
labels = []

for filename, details in embeddings.items():
    prosody = details.get("prosody", {})
    vector = [
        prosody.get("duration_sec", 0),
        prosody.get("avg_rms", 0),
        prosody.get("zcr", 0),
        prosody.get("tempo_bpm", 0),
        prosody.get("silence_ratio", 0),
        prosody.get("pitch_mean", 0),
        prosody.get("pitch_std", 0),
    ]
    vectors.append(vector)
    labels.append(filename)

if not vectors:
    print("⚠️ No vectors found. Exiting.")
    exit()

# Convert to NumPy array
X = np.array(vectors)

# Apply t-SNE
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

plot_path = os.path.join(OUTPUT_DIR, "tsne_plot.png")
plt.savefig(plot_path)
print(f"✅ Level 34 complete — t-SNE plot saved to: {plot_path}")

# Save t-SNE coordinates to JSON
filenames = list(embeddings.keys())
tsne_coords = {k: [float(x), float(y)] for k, (x, y) in zip(filenames, reduced)}
with open("output/revamp_level34/tsne_plot_coords.json", "w") as f:
    json.dump(tsne_coords, f, indent=4)

# Save plot image
plt.savefig("output/revamp_level34/tsne_plot.png")

