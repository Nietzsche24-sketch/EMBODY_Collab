import os
import shutil
import json
from pathlib import Path

# Load unified tags
with open("output/revamp_level25/unified_tags.json") as f:
    data = json.load(f)

# Create base output folder
output_base = Path("output/revamp_level26/sorted")
output_base.mkdir(parents=True, exist_ok=True)

# Process each tagged file
tagged = data.get("tagged_files", {})
for filename, tags in tagged.items():
    emotion = tags.get("emotion", "unknown")
    behavior = tags.get("behavior", "unknown")

    # Skip files with unknown emotion
    if emotion == "unknown":
        continue

    # Build destination path
    if behavior == "unknown":
        dest_folder = output_base / emotion
    else:
        dest_folder = output_base / emotion / behavior

    dest_folder.mkdir(parents=True, exist_ok=True)

    # Source and destination
    src_path = Path("input_audio") / filename
    dest_path = dest_folder / filename

    if src_path.exists():
        shutil.copy(src_path, dest_path)

# Save completion log
log = {
    "sorted_files": list(tagged.keys()),
    "timestamp": str(Path().stat().st_mtime)
}
with open("output/revamp_level26/sort_log.json", "w") as f:
    json.dump(log, f, indent=2)

print("✅ Level 26 complete — files sorted into output/revamp_level26/sorted/")
