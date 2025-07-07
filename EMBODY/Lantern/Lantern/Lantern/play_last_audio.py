import os
import glob
import subprocess

AUDIO_DIR = "output/sorted/audio"

def get_latest_file(folder):
    files = glob.glob(os.path.join(folder, "*"))
    if not files:
        print("🚫 No audio files found.")
        return None
    latest = max(files, key=os.path.getmtime)
    return latest

def main():
    latest_file = get_latest_file(AUDIO_DIR)
    if latest_file:
        print(f"🎧 Opening: {os.path.basename(latest_file)}")
        subprocess.run(["open", latest_file])

if __name__ == "__main__":
    main()
