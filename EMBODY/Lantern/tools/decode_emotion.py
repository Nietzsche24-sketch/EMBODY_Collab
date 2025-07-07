import sys
import json
import librosa

def extract_features(wav_path):
    y, sr = librosa.load(wav_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    pitch = librosa.yin(y, fmin=80, fmax=400).mean()
    intensity = abs(y).mean()

    # Simple heuristic classifier
    if pitch > 1.8 and intensity > 0.02:
        emotion = "angry"
    elif pitch < 1.2 and tempo < 1.0:
        emotion = "sad"
    elif tempo > 1.5 and intensity > 0.02:
        emotion = "excited"
    elif intensity < 0.01 and pitch < 1.0:
        emotion = "calm"
    elif pitch > 1.6 and tempo < 1.0:
        emotion = "sarcastic"
    else:
        emotion = "neutral"

    return {
        "emotion": emotion,
        "pitch": round(pitch, 2),
        "tempo": round(tempo / 100, 2),
        "formant": [1.0, 1.0, 1.0],  # Placeholder
        "intensity": round(intensity, 5)
    }

if __name__ == "__main__":
    input_wav = sys.argv[sys.argv.index("--input") + 1]
    output_json = sys.argv[sys.argv.index("--output") + 1]
    features = extract_features(input_wav)
    with open(output_json, "w") as f:
        json.dump(features, f, indent=2, default=lambda o: float(o))
    print(f"✅ Emotion vector saved to {output_json}")
