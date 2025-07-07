import os
import json
import shutil

# Load config
with open("vault_config.json") as f:
    config = json.load(f)

BACKUP_DIR = os.path.expanduser(config.get("backup_base", "~/VaultBackups"))
RESTORE_BASE = os.path.expanduser(config.get("restore_base", "~/VAULT_RESTORED"))

def list_backups():
    if not os.path.exists(BACKUP_DIR):
        return []
    return sorted(os.listdir(BACKUP_DIR))

def copy_contents(src, dst):
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_contents(s, d)
        else:
            try:
                shutil.copy2(s, d)
            except Exception as e:
                print(f"❌ Failed to copy {s} -> {d}: {e}")

def restore_backup(backup_name):
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    print(f"\n🟢 Restoring from: {backup_path}")
    for item in os.listdir(backup_path):
        src = os.path.join(backup_path, item)
        dst = os.path.join(RESTORE_BASE, item)
        print(f"📁 Restoring: {item} -> {dst}")
        copy_contents(src, dst)

def main():
    backups = list_backups()
    if not backups:
        print("⚠️ No backups found.")
        return

    print("\n📦 Available backups:")
    for i, name in enumerate(backups):
        print(f"{i + 1}. {name}")

    try:
        choice = int(input("\n❓ Which backup number to restore? ")) - 1
        if not (0 <= choice < len(backups)):
            raise ValueError
    except ValueError:
        print("❌ Invalid choice.")
        return

    restore_backup(backups[choice])
    print("\n✅ Restore complete.")

if __name__ == "__main__":
    main()
