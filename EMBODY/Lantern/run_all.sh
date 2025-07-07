#!/usr/bin/env bash
set -e

# 1) Make sure we’re in the right spot
cd "$(dirname "$0")"

# 2) Prepare folders
mkdir -p decoded_vectors outputs

# 3) Decode emotion vectors for clips 001…030
for i in $(seq -f "%03g" 1 30); do
  echo "🔍 Decoding clip ${i}_clean.wav …"
  python3 tools/decode_emotion.py \
    --input  audio_assets/arabic/${i}_clean.wav \
    --output decoded_vectors/${i}.json
done

# 4) Morph each clip
for i in $(seq -f "%03g" 1 30); do
  echo "🎯 Morphing clip ${i}_clean.wav → outputs/${i}_morphed.wav …"
  python3 tools/morph_audio.py \
    --input_wav   audio_assets/arabic/${i}_clean.wav \
    --vector_file decoded_vectors/${i}.json \
    --output_wav  outputs/${i}_morphed.wav
done

echo "✅ All 30 clips decoded & morphed!"
