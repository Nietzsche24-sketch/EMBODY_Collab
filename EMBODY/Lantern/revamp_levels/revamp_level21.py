# revamp_level21.py

import os
import whisper
import shutil
import datetime
import json

INPUT_DIR = "input_audio/"
OUTPUT_DIR = "output/revamp_level21/"
LOG_FILE = os.path.join(OUTPUT_DIR, "renaming_log.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n🌍 REVAMP Level 21 — {datetime.datetime.now().isoformat()}\n")

model = whisper.load_model("base")

renaming_log = []

def sanitize(text):
    return ''.join(c if c.isalnum() or c in "_-" else '_' for c in text).lower()

for filename in os.listdir(INPUT_DIR):
    if filename.lower().endswith(".wav"):
        path = os.path.join(INPUT_DIR, filename)
        print(f"🔍 Transcribing: {filename}")
        result = model.transcribe(path, fp16=False)
        lang = result["language"]
        first_words = ' '.join(result["text"].strip().split()[:4])
        first_words_clean = sanitize(first_words) or "untitled"
        lang_code = lang if lang else "unk"
        new_name = f"{lang_code}_{first_words_clean}.wav"
        new_path = os.path.join(INPUT_DIR, new_name)

        os.rename(path, new_path)
        print(f"✅ Renamed to: {new_name}")

        renaming_log.append({
            "original": filename,
            "new": new_name,
            "language": lang,
            "transcript": result["text"].strip()
        })

# Save log
with open(LOG_FILE, "w", encoding="utf-8") as f:
    json.dump(renaming_log, f, indent=2, ensure_ascii=False)

print(f"\n📄 Renaming log saved to: {LOG_FILE}")
print("✅ Level 21 complete.\n")
