import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict

# Load data
with open("output/revamp_level28/vectorized_tags.json", "r") as f:
    data = json.load(f)

files = data.get("tagged_files", {})
emotions = [v.get("emotion") for v in files.values() if "emotion" in v]
behaviors = [v.get("behavior") for v in files.values() if "behavior" in v]

# Plot 1: Emotion distribution
plt.figure(figsize=(6, 4))
sns.countplot(x=emotions)
plt.title("Emotion Distribution")
plt.ylabel("Count")
plt.xlabel("Emotion")
plt.tight_layout()
os.makedirs("output/revamp_level30", exist_ok=True)
plt.savefig("output/revamp_level30/emotion_distribution.png")
plt.close()

# Plot 2: Behavior distribution
plt.figure(figsize=(6, 4))
sns.countplot(x=behaviors)
plt.title("Behavior Distribution")
plt.ylabel("Count")
plt.xlabel("Behavior")
plt.tight_layout()
plt.savefig("output/revamp_level30/behavior_distribution.png")
plt.close()

# Plot 3: Emotion x Behavior heatmap
# Only plot if both emotion + behavior present and non-empty
combo = defaultdict(int)
for v in files.values():
    e = v.get("emotion")
    b = v.get("behavior")
    if e and b:
        combo[(e, b)] += 1

if combo:
    all_emotions = sorted(set(e for e, _ in combo.keys()))
    all_behaviors = sorted(set(b for _, b in combo.keys()))
    heat_data = [[combo.get((e, b), 0) for b in all_behaviors] for e in all_emotions]

    plt.figure(figsize=(8, 6))
    sns.heatmap(heat_data, annot=True, fmt="d", xticklabels=all_behaviors, yticklabels=all_emotions, cmap="Blues")
    plt.title("Emotion vs. Behavior Matrix")
    plt.ylabel("Emotion")
    plt.xlabel("Behavior")
    plt.tight_layout()
    plt.savefig("output/revamp_level30/emotion_behavior_matrix.png")
    plt.close()
else:
    print("ℹ️ Skipped heatmap — no valid emotion/behavior pairs found.")

print("📊 Diagnostic Summary — Level 30 Complete")
