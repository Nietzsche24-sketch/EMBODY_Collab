import os
import sys
import json
import subprocess

CONFIG_FILE = "vault_config.json"

# Load config
def load_config():
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        return {}

config = load_config()

def run_command(cmd, success_msg="", fail_msg=""):
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if success_msg:
            print(f"✅ {success_msg}")
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        print(f"❌ {fail_msg or 'Command failed'}: {e.stderr.decode().strip()}")
        return None

def enable_autoclean():
    run_command("launchctl load -w ~/Library/LaunchAgents/com.vault.autoclean.plist", 
                "Auto-clean enabled.", 
                "Failed to enable auto-clean")

def disable_autoclean():
    run_command("launchctl unload ~/Library/LaunchAgents/com.vault.autoclean.plist", 
                "Auto-clean disabled.", 
                "Failed to disable auto-clean")

def manual_clean():
    run_command("python3 vault_auto_clean.py", "Manual clean completed.")

def view_logs():
    run_command("tail -n 30 /Library/Logs/vault_autoclean.log")

def run_backup():
    run_command("python3 vault_backup.py", "Backup completed.")

def view_disk_usage():
    run_command("df -h", "Disk usage:")

def restore_backup():
    if not os.path.exists("vault_restore.py"):
        print("❌ vault_restore.py script not found.")
        return
    run_command("python3 vault_restore.py")

def menu():
    while True:
        print("\n=== VAULT CLI Pro ===")
        print("1. Manual Clean Now")
        print("2. View Cleanup Logs")
        print("3. Run Full Backup")
        print("4. Restore From Backup")
        print("5. View Top Disk Usage")
        print("6. Enable Auto-Clean")
        print("7. Disable Auto-Clean")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            manual_clean()
        elif choice == '2':
            view_logs()
        elif choice == '3':
            run_backup()
        elif choice == '4':
            restore_backup()
        elif choice == '5':
            view_disk_usage()
        elif choice == '6':
            enable_autoclean()
        elif choice == '7':
            disable_autoclean()
        elif choice == '8':
            print("Goodbye.")
            sys.exit(0)
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    menu()
