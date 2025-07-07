import os
for i in range(1, 31):
    fn = f"audio_assets/raw/{i:03}_clean.wav"
    if not os.path.exists(fn):
        print(f"❌ Missing WAV: {fn}")
