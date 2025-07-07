import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

WATCH_PATHS = [
    "/Users/peteryoussef/Documents",
    "/Users/peteryoussef/Downloads",
    "/Users/peteryoussef/Desktop"
]  # Add more dirs if you want

class VaultDeepHandler(FileSystemEventHandler):
    def on_modified(self, event):
        logging.info(f"[MODIFIED] {event.src_path}")

    def on_created(self, event):
        logging.info(f"[CREATED] {event.src_path}")

    def on_deleted(self, event):
        logging.info(f"[DELETED] {event.src_path}")

def start_deep_monitor():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(message)s")

    observer = Observer()
    handler = VaultDeepHandler()

    for path in WATCH_PATHS:
        if Path(path).exists():
            observer.schedule(handler, path, recursive=True)
            print(f"🔍 Watching: {path}")
        else:
            print(f"⚠️ Path does not exist: {path}")

    observer.start()
    print("🚨 VAULT Deep Monitor running. Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_deep_monitor()
