import os, json
from datetime import datetime
from public_tools.firm_module import inspect_audio

SEGMENT_DIR = "output/revamp_level13/chunks"
REPORT_DIR = "output/revamp_level14"
os.makedirs(REPORT_DIR, exist_ok=True)

print(f"\n🧬 REVAMP Level 14 — {datetime.now().isoformat()}\n")

report = {}

for f in os.listdir(SEGMENT_DIR):
    if f.endswith(".wav"):
        path = os.path.join(SEGMENT_DIR, f)
        result = inspect_audio(path)
        report[f] = result
        print(f"🧠 Analyzed: {f} → {result['🧪 Status']}")

out_path = os.path.join(REPORT_DIR, "segment_scores.json")
with open(out_path, "w") as f:
    json.dump(report, f, indent=2)

print(f"\n📊 Segment health report saved to: {out_path}")
print("✅ Level 14 complete.\n")
