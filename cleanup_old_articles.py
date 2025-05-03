import os
from datetime import datetime, timedelta

# ===== CONFIGURATION =====
OUTPUT_DIR = "outputs"
DAYS_TO_KEEP = 3  # Change this to 14, 30, etc.
ARCHIVE_DIR = "archive"  # Optional: move instead of delete

def get_folder_date(folder_name):
    try:
        return datetime.strptime(folder_name, "%Y-%m-%d")
    except ValueError:
        return None

def is_old_folder(folder_path):
    folder_name = os.path.basename(folder_path)
    folder_date = get_folder_date(folder_name)
    if not folder_date:
        return False
    return (datetime.now() - folder_date).days > DAYS_TO_KEEP

def delete_or_archive_folder(folder_path):
    print(f"\n🗑️ Processing folder: {folder_path}")
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)

    folder_name = os.path.basename(folder_path)
    archive_dest = os.path.join(ARCHIVE_DIR, folder_name)

    try:
        # Move to archive (optional)
        os.rename(folder_path, archive_dest)
        print(f"📦 Moved to archive: {archive_dest}")

        # If you prefer to DELETE instead of archive:
        # import shutil
        # shutil.rmtree(folder_path)
        # print(f"✅ Deleted folder: {folder_path}")

    except Exception as e:
        print(f"❌ Error processing {folder_path}: {e}")

def run_cleanup():
    print("🧹 Starting cleanup process...")
    for folder in os.listdir(OUTPUT_DIR):
        full_path = os.path.join(OUTPUT_DIR, folder)
        if os.path.isdir(full_path) and get_folder_date(folder):
            if is_old_folder(full_path):
                delete_or_archive_folder(full_path)

    print("✅ Cleanup complete.")

if __name__ == "__main__":
    run_cleanup()