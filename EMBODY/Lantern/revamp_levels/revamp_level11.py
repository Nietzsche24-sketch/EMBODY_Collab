import json
import os
import matplotlib.pyplot as plt
from datetime import datetime

REPORT_PATH = "output/revamp_level10/report_v10.json"
CHART_PATH = "output/revamp_level11/summary_chart.png"

# ✅ Make sure output dir exists
os.makedirs(os.path.dirname(CHART_PATH), exist_ok=True)

print(f"\n📊 REVAMP Level 11 — {datetime.now().isoformat()}\n")

# ✅ Load data
with open(REPORT_PATH) as f:
    data = json.load(f)

files = list(data.keys())
durations = [data[f]["duration_seconds"] for f in files]
word_counts = [data[f]["word_count"] for f in files]

# ✅ Plot side-by-side bars
plt.figure(figsize=(10, 6))
bars1 = plt.bar(files, durations, label="Duration (sec)", alpha=0.6)
bars2 = plt.bar(files, word_counts, label="Word Count", alpha=0.6)

# ✅ Label and save
plt.title("🔎 Audio Analysis Summary — Level 11")
plt.ylabel("Value")
plt.legend()
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(CHART_PATH)
plt.close()

print(f"📊 Chart saved to: {CHART_PATH}")
print("✅ Level 11 complete.\n")
