#!/usr/bin/env python3
import argparse
import librosa
import soundfile as sf
import json
import numpy as np
import math

def apply_morph(wav_path, vec_path, out_path):
    print(f"🎧 Loading WAV: {wav_path}")
    y, sr = librosa.load(wav_path, sr=48000)
    if y.size == 0:
        raise ValueError("❌ Loaded audio is empty — please re-record full phrase.")

    vec = json.load(open(vec_path, "r"))

    # 🎵 Pitch shift
    raw_pitch = vec.get("pitch", 1.0)
    if math.isnan(raw_pitch):
        raw_pitch = 1.0
    # Map [0.9⇾1.1] to roughly ±0.2 semitones then clamp ±0.1
    steps = (raw_pitch - 1.0) * 2
    steps = max(min(steps,  0.10), -0.10)
    print(f"🔊 pitch shift: {steps:+.3f} semitones")
    if abs(steps) > 0.005:
        # Note: your librosa version requires sr and n_steps as keyword args
        y = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=steps)

    # ⚡ Intensity adjust
    iv = vec.get("intensity", 0.0)
    if math.isnan(iv):
        iv = 0.0
    iv = max(min(iv, 0.03), -0.03)
    print(f"⚡ intensity adj: {iv:+.3f}")
    if abs(iv) > 0.005:
        y = np.clip(y * (1 + iv * 10), -1.0, 1.0)

    # ✍️ Write output (WAV, 48 kHz)
    sf.write(out_path, y, sr, format="WAV")
    print(f"✅ Morphed and saved: {out_path}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Apply morph using decoded vector")
    p.add_argument("--input_wav",    required=True, help="Path to input WAV")
    p.add_argument("--vector_file",  required=True, help="Path to decoded JSON vector")
    p.add_argument("--output_wav",   required=True, help="Path for morphed output WAV")
    args = p.parse_args()
    apply_morph(args.input_wav, args.vector_file, args.output_wav)
