import os
import json
import librosa
import numpy as np

input_dir = "output/revamp_level26/sorted"
output_file = "output/revamp_level27/prosody_features.json"

features = {}

def extract_features(filepath):
    y, sr = librosa.load(filepath)
    duration = librosa.get_duration(y=y, sr=sr)
    rms = float(np.mean(librosa.feature.rms(y=y)))
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y=y)))
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    silence_ratio = float(np.sum(np.abs(y) < 1e-4) / len(y))
    pitch = librosa.yin(y, fmin=80, fmax=400, sr=sr)
    pitch_mean = float(np.mean(pitch))
    pitch_std = float(np.std(pitch))

    return {
        "duration_sec": round(duration, 2),
        "avg_rms": round(rms, 5),
        "zcr": round(zcr, 5),
        "tempo_bpm": round(tempo, 2),
        "silence_ratio": round(silence_ratio, 4),
        "pitch_mean": round(pitch_mean, 2),
        "pitch_std": round(pitch_std, 2)
    }

for emotion in os.listdir(input_dir):
    emotion_path = os.path.join(input_dir, emotion)
    for fname in os.listdir(emotion_path):
        if fname.endswith(".wav"):
            fpath = os.path.join(emotion_path, fname)
            features[fname] = extract_features(fpath)

os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w") as f:
    json.dump({ "features": features }, f, indent=2)

print(f"✅ Level 27 complete — features saved to: {output_file}")
