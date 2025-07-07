import os
import time
import shutil
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CONFIG_PATH = "/Users/peteryoussef/Development/Projects/EMBODY/VAULT/vault_config.json"
BACKUP_BASE = "VAULT/backups_system"
LOG_FILE = "VAULT/vault.log"

def copy_contents(src, dst):
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_contents(s, d)
        else:
            shutil.copy2(s, d)

def clean_old_backups(base_dir, days=7):
    now = time.time()
    cutoff = now - (days * 86400)
    for entry in os.listdir(base_dir):
        path = os.path.join(base_dir, entry)
        if os.path.isdir(path) and os.path.getmtime(path) < cutoff:
            shutil.rmtree(path)
            print(f"[VAULT] 🧹 Deleted old backup: {entry}")

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def perform_backup():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = os.path.join(BACKUP_BASE, f"auto_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    for path in config.get("folders", []):
        abs_path = os.path.expanduser(path)
        try:
            if os.path.exists(abs_path):
                dst = os.path.join(backup_dir, os.path.basename(abs_path))
                copy_contents(abs_path, dst)
                print(f"✅ Auto-backed up: {abs_path}")
                log_event(f"Backed up: {abs_path}")
        except Exception as e:
            print(f"⚠️ Failed to backup {abs_path}: {e}")
            log_event(f"Failed to backup {abs_path}: {e}")

    clean_old_backups(BACKUP_BASE)

class AutoBackupHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        perform_backup()

def main():
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    observer = Observer()
    for path in config.get("folders", []):
        abs_path = os.path.expanduser(path)
        if os.path.exists(abs_path):
            observer.schedule(AutoBackupHandler(), abs_path, recursive=True)

    observer.start()
    print("🛡️ VAULT Auto-Backup running. Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
