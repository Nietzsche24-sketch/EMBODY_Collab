import time
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load config
with open("vault_config.json") as f:
    config = json.load(f)

class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        event_type = event.event_type
        src = event.src_path
        print(f"[{event_type.upper()}] {src}")

def main():
    paths = config.get("paths", [])
    observer = Observer()

    for path in paths:
        abs_path = os.path.expanduser(path)
        if os.path.exists(abs_path):
            print(f"👁️  Watching: {abs_path}")
            observer.schedule(ChangeHandler(), abs_path, recursive=True)
        else:
            print(f"⚠️  Skipped (not found): {abs_path}")

    observer.start()
    print("🚨 VAULT Watchdog Active. Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 VAULT Watchdog Stopped.")

    observer.join()

if __name__ == "__main__":
    main()
