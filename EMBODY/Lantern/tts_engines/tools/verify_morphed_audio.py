import os
import wave

WAV_DIR = "audio_assets/arabic"
errors = []

for fn in sorted(os.listdir(WAV_DIR)):
    if not fn.endswith(".wav"): continue
    path = os.path.join(WAV_DIR, fn)
    try:
        if os.path.getsize(path) < 1024:
            errors.append(f"⚠️ File too small: {fn}")
            continue
        with wave.open(path, "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            dur = frames / float(rate)
            if dur < 0.2:
                errors.append(f"⚠️ Very short duration: {fn} ({dur:.2f}s)")
    except Exception as e:
        errors.append(f"❌ Corrupt: {fn} ({e})")

if not errors:
    print("✅ All morphed WAVs are healthy.")
else:
    print("\n".join(errors))
