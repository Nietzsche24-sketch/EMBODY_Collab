import os
import json
import shutil
from datetime import datetime

# === Load Config ===
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "vault_config.json")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

folders = config.get("folders", [])
backup_base = os.path.expanduser(config.get("backup_base", "~/VaultBackups"))
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_dir = os.path.join(backup_base, f"backup_{timestamp}")

# === Create Backup Directory ===
os.makedirs(backup_dir, exist_ok=True)
print(f"\n💾 Creating deep system backup at:\n{backup_dir}\n")

# === Copy Each Folder ===
for folder in folders:
    folder = os.path.expanduser(folder)
    if not os.path.exists(folder):
        print(f"⚠️ Skipped (not found): {folder}")
        continue

    folder_name = os.path.basename(folder.rstrip("/"))
    dest = os.path.join(backup_dir, folder_name)

    try:
        shutil.copytree(folder, dest, dirs_exist_ok=True)
        print(f"✅ Backed up: {folder_name}")
    except Exception as e:
        print(f"❌ Failed to back up {folder_name}: {e}")

print("\n✅ Deep Backup Complete.\n")
