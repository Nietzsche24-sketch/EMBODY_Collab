#!/usr/bin/env python3
import os
import shutil
import datetime
from pathlib import Path

LOG_FILE = Path.home() / "Library" / "Logs" / "vault_autoclean.log"

def log(msg):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} {msg}\n")

def remove_if_exists(path):
    if path.exists():
        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            log(f"Removed {path}")
        except Exception as e:
            log(f"Failed to remove {path}: {e}")

TARGETS = [
    Path.home() / ".Trash",
    Path("/private/var/folders"),
    Path("/var/folders"),
    Path("/tmp"),
    Path.home() / "Library" / "Caches",
]

log("===== Starting vault auto-clean =====")
for target in TARGETS:
    if target.exists():
        for item in target.glob("*"):
            remove_if_exists(item)
log("===== Finished vault auto-clean =====\n")
