#!/bin/bash

INPUT_FILE="harvest_output/train_filelist.txt"
OUTPUT_FILE="harvest_output/train_filelist_emotion.txt"

# Define available emotions
EMOTIONS=("angry" "happy" "sad" "calm" "excited" "confused")

echo "🎭 Injecting emotions into: $INPUT_FILE"
echo "💾 Saving output to: $OUTPUT_FILE"

> "$OUTPUT_FILE"  # Clear output file

while IFS= read -r line; do
    emotion="${EMOTIONS[$RANDOM % ${#EMOTIONS[@]}]}"
    modified=$(echo "$line" | awk -F '|' -v emo="$emotion" '{print $1 "|" $2 "|{" emo "} " $3 "|" $4}')
    echo "$modified" >> "$OUTPUT_FILE"
done < "$INPUT_FILE"

echo "✅ Done. Emotion-wrapped file ready: $OUTPUT_FILE"
