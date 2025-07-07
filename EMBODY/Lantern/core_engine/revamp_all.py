import os
import subprocess

LEVELS = list(range(1, 21))

for level in LEVELS:
    filename = f"revamp_level{level}.py"
    if os.path.exists(filename):
        print(f"\n🚀 Launching REVAMP Level {level}...\n")
        subprocess.run(["python3", filename])
    else:
        print(f"⚠️ Skipped: {filename} not found.")
