#!/bin/bash

# FROSTBYTE — RAM & Disk Pressure Monitor with Auto Cleanup + DALL·ALERT sound

# === CONFIG ===
MIN_FREE_MB=2000           # Min acceptable free RAM in MB
MAX_SWAP_MB=1024           # Max acceptable swap usage
MAX_COMP_MB=2500           # Max acceptable RAM compression
MIN_DISK_GB=10             # Min acceptable disk space

LOG_FILE="$HOME/Development/Projects/Frostbyte/logs/frostbyte.log"
SOUND="/System/Library/Sounds/Glass.aiff"  # Or your custom DALL·ALERT

# === FUNCTIONS ===

log() {
  echo "$(date): $1" | tee -a "$LOG_FILE"
}

get_ram_stats() {
  FREE_MB=$(vm_stat | awk '/Pages free/ {free=$3} /Pages speculative/ {spec=$3} END {print int((free + spec)*4096/1048576)}')
  COMPRESSED_MB=$(vm_stat | awk '/Pages occupied by compressor/ {print int($5 * 4096 / 1048576)}')
  SWAP_RAW=$(sysctl vm.swapusage | awk '{print $7}' | sed 's/M//')
  SWAP=$(printf "%.0f" "$SWAP_RAW")
}

get_disk_stats() {
  DISK_FREE_GB=$(df -g ~ | tail -1 | awk '{print $4}')
}

play_alert() {
  afplay "$SOUND"
}

cleanup_ram() {
  log "🔴 RAM pressure high. Triggering purge..."
  play_alert
  sudo purge
}

cleanup_disk() {
  log "🔴 Disk space low ($DISK_FREE_GB GB left). Manual cleanup may be needed."
  play_alert
}

# === MAIN ===

get_ram_stats
get_disk_stats

log "🔎 RAM: $FREE_MB MB free, $SWAP MB swap, $COMPRESSED_MB MB compressed. Disk: $DISK_FREE_GB GB free."

if [ "$FREE_MB" -lt "$MIN_FREE_MB" ] || [ "$SWAP" -gt "$MAX_SWAP_MB" ] || [ "$COMPRESSED_MB" -gt "$MAX_COMP_MB" ]; then
  cleanup_ram
else
  log "✅ RAM is healthy."
fi

if [ "$DISK_FREE_GB" -lt "$MIN_DISK_GB" ]; then
  cleanup_disk
else
  log "✅ Disk space is healthy."
fi
