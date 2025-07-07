#!/usr/bin/env python3
"""
vault_monitor.py ▸ Watches all backup targets and triggers vault_backup.py
whenever a file changes. Requires watchdog (`pip install watchdog`).
"""

import json, time, subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

VAULT_DIR = Path(__file__).parent
CONFIG    = json.load(open(VAULT_DIR / "vault_config.json"))
TARGETS   = CONFIG["backup_targets"]

class BackupTrigger(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f"📡 Change detected: {event.src_path}")
        subprocess.run(["python", str(VAULT_DIR / "vault_backup.py")])

observer = Observer()
for path in TARGETS:
    p = Path(path)
    if p.exists():
        observer.schedule(BackupTrigger(), str(p), recursive=True)

print("👀 Vault Monitor running... (Ctrl+C to stop)")
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    observer.join()
