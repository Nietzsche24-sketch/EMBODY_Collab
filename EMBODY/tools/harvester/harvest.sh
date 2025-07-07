#!/bin/bash

# HARVESTER: Emotional Data Builder for EMBODY
# By CTO Orders — Full Bash Pipeline

# === CONFIG ===
VIDEO_FILE="input_video.mp4"
SUBTITLE_FILE="input_subs.srt"
OUT_DIR="harvest_output"
WAV_DIR="$OUT_DIR/wavs"
TXT_DIR="$OUT_DIR/txt"
FILELIST="$OUT_DIR/train_filelist.txt"
SPEAKER="egyptian_movie"
DURATION=5  # clip length in seconds

# === PREP ===
mkdir -p "$WAV_DIR" "$TXT_DIR"
rm -f "$FILELIST"

# === STEP 1: Slice WAVs from video ===
echo "[HARVESTER] Extracting audio from video..."
ffmpeg -y -i "$VIDEO_FILE" -ar 22050 -ac 1 "$OUT_DIR/full.wav"

echo "[HARVESTER] Slicing audio..."
sox "$OUT_DIR/full.wav" "$WAV_DIR/chunk.wav" trim 0 "$DURATION" : newfile : restart

# === STEP 2: Extract text from subtitle (assumes SRT format) ===
echo "[HARVESTER] Extracting lines from subtitle..."
grep -vE '^[0-9]+$' "$SUBTITLE_FILE" | grep -vE '^-->' | grep -v '^$' > "$TXT_DIR/lines.txt"

# === STEP 3: Pair audio clips with subtitle lines ===
echo "[HARVESTER] Pairing audio with text..."
audiocount=$(ls "$WAV_DIR" | grep '.wav' | wc -l)
linecount=$(wc -l < "$TXT_DIR/lines.txt")
count=$((audiocount<linecount ? audiocount : linecount))

for i in $(seq -f "%03g" 1 "$count"); do
    wav="$WAV_DIR/chunk${i}.wav"
    text=$(sed -n "${i}p" "$TXT_DIR/lines.txt")
    echo "${wav}|${text}|${SPEAKER}" >> "$FILELIST"
done

echo "[HARVESTER] ✅ Done. Filelist ready: $FILELIST"
