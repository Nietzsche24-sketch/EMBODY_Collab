import os
import subprocess

SORTED_DIR = 'output/sorted'

def list_files(folder):
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    return sorted(files)

def preview_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ['.wav', '.mp3', '.m4a', '.mp4', '.mov', '.avi', '.jpg', '.jpeg', '.png']:
        subprocess.run(['open', filepath])  # use GUI viewer
    else:
        print("⚠️ Preview not supported for this file type.")

def run_preview():
    print("🧭 Preview folders:")
    folders = [d for d in os.listdir(SORTED_DIR) if os.path.isdir(os.path.join(SORTED_DIR, d))]
    for i, f in enumerate(folders):
        print(f"{i + 1}. {f}")

    choice = input("\nEnter number to preview: ").strip()
    try:
        selected_folder = folders[int(choice) - 1]
    except:
        print("❌ Invalid choice.")
        return

    folder_path = os.path.join(SORTED_DIR, selected_folder)
    files = list_files(folder_path)

    if not files:
        print("🚫 No files to preview.")
        return

    print(f"\n🎧 Previewing {len(files)} files in: {selected_folder}")
    for file in files:
        full_path = os.path.join(folder_path, file)
        print(f"\n▶️ {file}")
        preview_file(full_path)

if __name__ == "__main__":
    run_preview()
