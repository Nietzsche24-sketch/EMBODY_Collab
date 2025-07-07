import os
import shutil
from datetime import datetime

INPUT_DIR = "input_audio"
LOG_PATH = "output/revamp_level22/sort_log.json"

# Ensure output directory exists
os.makedirs("output/revamp_level22", exist_ok=True)

log = []
now = datetime.now().isoformat()

for filename in os.listdir(INPUT_DIR):
    file_path = os.path.join(INPUT_DIR, filename)
    
    if not os.path.isfile(file_path) or not filename.endswith(".wav"):
        continue

    # Expect prefix like en_filename.wav
    parts = filename.split("_", 1)
    if len(parts) != 2:
        continue  # Skip files without prefix

    lang_prefix = parts[0]
    lang_folder = os.path.join(INPUT_DIR, lang_prefix)
    os.makedirs(lang_folder, exist_ok=True)

    new_path = os.path.join(lang_folder, filename)
    shutil.move(file_path, new_path)

    log.append({
        "original": file_path,
        "moved_to": new_path,
        "language": lang_prefix,
        "timestamp": now
    })

# Save log
import json
with open(LOG_PATH, "w") as f:
    json.dump(log, f, indent=2)

print(f"📂 Sorted {len(log)} files by language.")
print(f"📄 Sort log saved to: {LOG_PATH}")
print("✅ Level 22 complete.")
