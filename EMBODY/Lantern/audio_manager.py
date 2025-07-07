import argparse
import json
import os
import subprocess

METADATA_PATH = "audio_assets/metadata.json"

def load_metadata():
    with open(METADATA_PATH, "r") as f:
        return json.load(f)

def save_metadata(data):
    with open(METADATA_PATH, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_clip(clip_id, language, text, emotion, path):
    data = load_metadata()
    entry = {
        "id": clip_id,
        "language": language,
        "text": text,
        "emotion": emotion,
        "processed": True,
        "final_path": path
    }
    data.append(entry)
    save_metadata(data)
    print(f"✅ Added clip {clip_id}")

def play_clip(clip_id):
    data = load_metadata()
    match = next((item for item in data if item["id"] == clip_id), None)
    if not match:
        print(f"❌ Clip {clip_id} not found in metadata.")
        return
    path = match["final_path"]
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return
    print(f"▶️ Playing {clip_id}: {path}")
    subprocess.call(["afplay", path])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--add", nargs=5, metavar=("id", "lang", "text", "emotion", "path"), help="Add new clip")
    parser.add_argument("--play", metavar="id", help="Play clip by ID")
    args = parser.parse_args()

    if args.add:
        add_clip(*args.add)
    elif args.play:
        play_clip(args.play)
    else:
        print("❌ No action specified. Use --add or --play")

if __name__ == "__main__":
    main()
