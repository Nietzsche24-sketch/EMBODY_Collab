import sys
import json

from pathlib import Path

def load_emotion_tags(emotion_tag_file):
    tag_map = {}
    with open(emotion_tag_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) != 3:
                continue  # Skip malformed lines
            path, _, emotion = parts
            tag_map[path.strip('"')] = emotion
    return tag_map

def inject_emotions(tag_path, jsonl_path):
    tag_map = load_emotion_tags(tag_path)
    enriched_lines = []

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            wav_path = entry["wav"]
            emotion = tag_map.get(wav_path, entry.get("emotion", None))
            entry["emotion"] = emotion
            enriched_lines.append(entry)

    with open(jsonl_path, "w", encoding="utf-8") as f:
        for entry in enriched_lines:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    inject_emotions(sys.argv[1], sys.argv[2])
