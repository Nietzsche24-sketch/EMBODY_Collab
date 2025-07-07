import os
import shutil
import hashlib
from datetime import datetime

RAW_DIR = 'output/raw'
SORTED_DIR = 'output/sorted'
LOG_FILE = 'logs/recovery_log.txt'

# File type classification
TYPE_MAP = {
    'audio': ['.wav', '.mp3', '.m4a'],
    'video': ['.mp4', '.mov', '.avi'],
    'image': ['.jpg', '.jpeg', '.png'],
    'text': ['.txt', '.csv', '.srt'],
    'pdf': ['.pdf'],
}

def get_category(ext):
    for category, exts in TYPE_MAP.items():
        if ext in exts:
            return category
    return 'other'

def hash_file(path):
    hasher = hashlib.sha256()
    with open(path, 'rb') as afile:
        buf = afile.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(65536)
    return hasher.hexdigest()

def sort_files():
    if not os.path.exists(RAW_DIR):
        print(f"❌ No raw folder found at {RAW_DIR}")
        return

    os.makedirs(SORTED_DIR, exist_ok=True)
    seen_hashes = set()
    count = 0
    duplicates = 0

    for root, _, files in os.walk(RAW_DIR):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            full_path = os.path.join(root, file)
            if not os.path.isfile(full_path):
                continue

            file_hash = hash_file(full_path)
            if file_hash in seen_hashes:
                duplicates += 1
                continue
            seen_hashes.add(file_hash)

            category = get_category(ext)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = f"{category}_{timestamp}{ext}"
            dest_folder = os.path.join(SORTED_DIR, category)
            os.makedirs(dest_folder, exist_ok=True)
            dest_path = os.path.join(dest_folder, base_name)

            i = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_folder, f"{category}_{timestamp}_{i}{ext}")
                i += 1

            shutil.copy2(full_path, dest_path)
            count += 1

    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()}: Sorted {count} files, skipped {duplicates} duplicates.\n")

    print(f"✅ Sorted {count} new files. 🧼 Skipped {duplicates} duplicates.")

if __name__ == "__main__":
    sort_files()
