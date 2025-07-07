import os
import shutil

BACKUP_DIR = "VAULT/backups_system"

def list_backups():
    return sorted(os.listdir(BACKUP_DIR))

def restore_backup(backup_name):
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    print(f"\n📦 Restoring from: {backup_path}")

    for item in os.listdir(backup_path):
        src = os.path.join(backup_path, item)
        dst = os.path.expanduser(f"~/VAULT_RESTORED/{item}")
        print(f"📁 Restoring {item} ➜ {dst}")
        try:
            if os.path.isdir(src):
                if not os.path.exists(dst):
                    os.makedirs(dst)
                for file in os.listdir(src):
                    s = os.path.join(src, file)
                    d = os.path.join(dst, file)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)
            else:
                shutil.copy2(src, dst)
        except Exception as e:
            print(f"❌ Failed to restore {item}: {e}")

def main():
    backups = list_backups()
    if not backups:
        print("No backups found.")
        return

    print("\n📂 Available backups:")
    for i, name in enumerate(backups):
        print(f"{i+1}. {name}")

    choice = int(input("\n❓ Which backup number to restore? ")) - 1
    selected = backups[choice]
    restore_backup(selected)

if __name__ == "__main__":
    main()
