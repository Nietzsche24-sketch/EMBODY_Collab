import os
import shutil
import time
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

with open("VAULT/vault_config.json") as f:
    config = json.load(f)

class AutoBackupHandler(FileSystemEventHandler):
    def trigger_backup(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_root = os.path.join("VAULT", "backups_system", f"backup_{timestamp}")
        os.makedirs(backup_root, exist_ok=True)

        for path in config.get("paths", []):
            abs_path = os.path.expanduser(path)
            if os.path.exists(abs_path):
                folder_name = os.path.basename(abs_path.rstrip("/"))
                dest = os.path.join(backup_root, folder_name)
                try:
                    shutil.copytree(abs_path, dest)
                    print(f"✅ Auto-backed up: {abs_path}")
                except Exception as e:
                    print(f"⚠️ Failed to backup {abs_path}: {e}")

    def on_any_event(self, event):
        if not event.is_directory:
            print(f"[{event.event_type.upper()}] {event.src_path}")
            self.trigger_backup()

def main():
    event_handler = AutoBackupHandler()
    observer = Observer()

    for path in config.get("paths", []):
        abs_path = os.path.expanduser(path)
        if os.path.exists(abs_path):
            observer.schedule(event_handler, abs_path, recursive=True)

    observer.start()
    print("🔁 VAULT Auto-Backup running. Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
