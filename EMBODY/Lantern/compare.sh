#!/usr/bin/env bash
set -e

for i in $(seq -f "%03g" 1 30); do
  echo "▶️ $i: original → morphed"
  afplay audio_assets/arabic/${i}_clean.wav &
  sleep 4
  killall afplay || true

  afplay outputs/${i}_morphed.wav &
  sleep 4
  killall afplay || true
done
