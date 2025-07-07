import os
import subprocess

def harvest_clip(video_path, subtitle_path, output_dir):
    print(f"[HARVESTER] 📼 Video: {video_path}")
    print(f"[HARVESTER] 📜 Subtitle: {subtitle_path}")
    print(f"[HARVESTER] 💾 Output dir: {output_dir}")

    os.makedirs(output_dir, exist_ok=True)

    audio_path = os.path.join(output_dir, "full.wav")

    print("[HARVESTER] 🎙️ Extracting audio from video...")
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-ar", "22050", "-ac", "1", "-vn",
        audio_path
    ], check=True)

    print("[HARVESTER] ✂️ Slicing audio...")
    subprocess.run([
        "sox", audio_path,
        os.path.join(output_dir, "slice.wav"),
        "trim", "0", "5"
    ], check=True)

    print("[HARVESTER] 🧠 Extracting subtitle lines...")
    with open(subtitle_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    output_txt = os.path.join(output_dir, "train_filelist.txt")
    with open(output_txt, "w", encoding="utf-8") as out:
        for i, line in enumerate(lines):
            if "-->" not in line and line.strip() and not line.strip().isdigit():
                wav_path = os.path.join(output_dir, f"{i:03d}.wav")
                subprocess.run([
                    "sox", audio_path, wav_path,
                    "trim", str(i * 5), "5"
                ])
                out.write(f"{wav_path}|{line.strip()}\n")

    print(f"[HARVESTER] ✅ Done. Saved filelist to: {output_txt}")
