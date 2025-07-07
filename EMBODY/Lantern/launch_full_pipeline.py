#!/usr/bin/env python3

# Lantern: Full Audio Recovery Pipeline Launcher

import os
import subprocess

LEVELS = list(range(1, 36))  # Levels 1 to 35

def run_level(level):
    filename = f"revamp_levels/revamp_level{level}.py"
    print(f"\n🚀 Launching REVAMP Level {level}...")
    try:
        subprocess.run(["python3", filename], check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Error in Level {level}: {filename}\n")

def main():
    print("\n🧠 LANTERN: RUNNING FULL REVAMP PIPELINE")
    for level in LEVELS:
        run_level(level)
    print("\n✅ ALL LEVELS COMPLETE — Lantern full pipeline executed.")

if __name__ == "__main__":
    main()
