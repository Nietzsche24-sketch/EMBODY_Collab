import os
import json
import datetime

INPUT_DIR = "input_audio"
OUTPUT_PATH = "output/revamp_level24/emotion_tags.json"

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Simulated tagging function
def tag_emotion(filename):
    base = os.path.basename(filename)
    # Dummy logic: assign emotion based on filename length
    return "neutral" if len(base) % 2 == 0 else "angry"

# Walk through input_audio and find all .wav files
tagged = {}
for root, _, files in os.walk(INPUT_DIR):
    for f in files:
        if f.lower().endswith(".wav"):
            full_path = os.path.join(root, f)
            emotion = tag_emotion(f)
            tagged[f] = emotion
            print(f"🧠 Tagged {f} as {emotion}")

# Save results
with open(OUTPUT_PATH, "w") as f:
    json.dump({
        "tagged_files": tagged,
        "timestamp": str(datetime.datetime.now())
    }, f, indent=2)

print(f"✅ Emotion tags saved to: {OUTPUT_PATH}")
