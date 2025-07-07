#!/bin/bash

VIDEO_FILE="$1"
SUB_FILE="$2"
LANG="$3"
SPEAKER="$4"

OUTPUT_DIR="wavs"
FILELIST="train_filelist.txt"
EMOTION_VECTOR="neutral"

mkdir -p "$OUTPUT_DIR"
rm -f "$FILELIST"

awk '
BEGIN { FS="-->"; }
/^[0-9]+$/ {
  getline time;
  gsub(",", ".", time);
  split(time, a, " --> ");
  start = a[1]; end = a[2];
  getline text;
  print start "|" end "|" text;
}
' "$SUB_FILE" > temp_clips.txt

index=0
while IFS='|' read -r start end text; do
    clip_name=$(printf "clip_%04d.wav" "$index")
    out_path="$OUTPUT_DIR/$clip_name"

    ffmpeg -loglevel quiet -y -ss "$start" -to "$end" -i "$VIDEO_FILE" -ar 22050 -ac 1 -vn "$out_path"

    echo "$out_path|$text|$LANG|$SPEAKER|$EMOTION_VECTOR" >> "$FILELIST"
    echo "✅ Clip $index: $text"
    index=$((index + 1))
done < temp_clips.txt

echo "✅ Done. Created $index clips."
rm temp_clips.txt
