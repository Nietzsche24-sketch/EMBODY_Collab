#!/bin/bash

INPUT_ROOT="./harvest_batch"
OUTPUT_ROOT="./harvest_output"
LOG_FILE="./harvest_log.txt"

mkdir -p "$OUTPUT_ROOT/wavs"

echo "[🚜 HARVESTER BATCH START]" > "$LOG_FILE"

# Loop through all .mp4 files
find "$INPUT_ROOT" -type f -name '*.mp4' | while read -r VIDEO_FILE; do
    BASE_NAME=$(basename "$VIDEO_FILE" .mp4)
    DIR_NAME=$(dirname "$VIDEO_FILE")
    SUB_FILE="$DIR_NAME/${BASE_NAME}.srt"

    if [[ -f "$SUB_FILE" ]]; then
        echo "[🎬 MATCH] $VIDEO_FILE + $SUB_FILE" | tee -a "$LOG_FILE"
        bash harvest.sh --input "$VIDEO_FILE" --subs "$SUB_FILE"
    else
        echo "[❌ SKIP] No subtitle for $VIDEO_FILE" | tee -a "$LOG_FILE"
    fi
done

# Inject emotions afterward
echo "[🎭 Injecting emotions...]" | tee -a "$LOG_FILE"
bash inject_emotions.sh

echo "[✅ DONE] All clips processed." | tee -a "$LOG_FILE"
