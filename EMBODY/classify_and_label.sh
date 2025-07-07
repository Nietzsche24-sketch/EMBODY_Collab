set -euo pipefail

MODEL="superb/wav2vec2-base-superb-er"
IN_FILE="tools/harvester/harvest_output/train_filelist_final.txt"
OUT_FILE="tools/harvester/harvest_output/train_with_emotion.tsv"
sed -i.bak 's/\r$//' "$IN_FILE"
printf "wav_path\ttext\tspeaker\tgold_emotion\tpred_emotion\tconfidence\n" > "$OUT_FILE"

while IFS='|' read -r wav text speaker gold; do

 read pred conf < <(
    python3 - <<PYCODE 2>/dev/null
from transformers import pipeline
pipe = pipeline("audio-classification", model="$MODEL", device=-1, top_k=1)
res = pipe("$wav")[0]
print(res["label"], f"{res['score']:.3f}", sep="\t")
PYCODE
  )

 printf "%s\t%s\t%s\t%s\t%s\t%s\n" \
    "$wav" "$text" "$speaker" "$gold" "$pred" "$conf" \
    >> "$OUT_FILE"

done < "$IN_FILE"

echo "✅ Done!  See $OUT_FILE"
