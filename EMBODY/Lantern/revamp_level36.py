# revamp_level36.py — Cluster Evaluation & Voting Prep
import os
import json
from collections import defaultdict

CLUSTER_LOG = "output/revamp_level35/clusters/cluster_log.json"
AUDIO_DIR = "output/revamp_level35/clusters/"

# Load cluster assignments
with open(CLUSTER_LOG, "r") as f:
    assignments = json.load(f)

# Organize into clusters
clusters = defaultdict(list)
for fname, cid in assignments.items():
    clusters[cid].append(fname)

# Show summary
print("📊 Cluster Summary:")
for cid, files in clusters.items():
    print(f"\n🧩 Cluster {cid} — {len(files)} files")
    for f in files[:3]:  # show sample of 3 files
        print(f"   • {f}")
    if len(files) > 3:
        print("   ...")

# Save cluster summary to JSON
summary = {str(cid): files for cid, files in clusters.items()}
with open("output/revamp_level36/cluster_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\n✅ Level 36 complete — summary saved to: output/revamp_level36/cluster_summary.json")
