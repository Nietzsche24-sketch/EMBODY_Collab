set -euo pipefail

# choose either a HuggingFace model name...
MODEL_NAME="tts_models/multilingual/multi-dataset/vits"
# ...or point at your local checkpoint:
# MODEL_PATH="tools/harvester/harvest_output/checkpoint.pth.tar"

OUTDIR="tools/harvester/harvest_output/generated_wavs"
LIST="tools/harvester/harvest_output/train_filelist_final.txt"

mkdir -p "$OUTDIR"

while IFS="|" read -r WAV_PATH ARABIC_TEXT SPEAKER EMOTION; do
  CLIP=$(basename "$WAV_PATH" .wav)
  echo "→ Synthesizing $CLIP (speaker=$SPEAKER)"
  tts \
    --text       "$ARABIC_TEXT" \
    --model_name "$MODEL_NAME" \
    # --model_path "$MODEL_PATH" \    # if you want to use a local checkpoint
    --config_path config/your_config.json \
    --speaker_idx "$SPEAKER" \
    --out_path   "$OUTDIR/${CLIP}.wav" \
    --use_cuda   false
done < "$LIST"
