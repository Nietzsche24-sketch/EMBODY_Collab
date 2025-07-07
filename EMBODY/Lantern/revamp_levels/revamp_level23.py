# revamp_level23.py – Behavior Tagging Layer (Private for EMBODY)

import os, json
import whisper
from datetime import datetime

INPUT_DIR = "input_audio"
OUTPUT_DIR = "output/revamp_level23"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 🧠 Basic placeholder logic for behavior detection
def detect_behavior_tags(text):
    tags = []
    lower = text.lower()
    if "?" in text or lower.startswith(("do you", "what", "why")):
        tags.append("questioning")
    if "maybe" in lower or "i think" in lower:
        tags.append("uncertain")
    if "go now" in lower or "do it" in lower:
        tags.append("commanding")
    if "again?" in lower or "really?" in lower:
        tags.append("mocking")
    if not tags:
        tags.append("neutral")
    return tags

# 🎤 Load Whisper model
model = whisper.load_model("base")

# 🧾 Store results
results = {}

# 🔄 Process all WAV files
for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".wav"):
        filepath = os.path.join(INPUT_DIR, filename)
        print(f"🔍 Transcribing: {filename}")
        result = model.transcribe(filepath, fp16=False, language="en")
        text = result["text"].strip()
        tags = detect_behavior_tags(text)
        print(f"✅ Tags for '{filename}': {tags}")
        results[filename] = {
            "text": text,
            "behavior_tags": tags
        }

# 💾 Save behavior tag log
log_path = os.path.join(OUTPUT_DIR, "behavior_tags.json")
with open(log_path, "w") as f:
    json.dump({
        "timestamp": str(datetime.now()),
        "tagged_files": results
    }, f, indent=2)

print(f"\n✅ Behavior tags saved to: {log_path}")
