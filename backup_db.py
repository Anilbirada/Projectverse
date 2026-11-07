"""
PROJECTVERSE - Automated Production SQLite Database Backup Script
Creates timestamped point-in-time snapshots with WAL checkpointing and retention pruning.
"""

import os
import shutil
import sqlite3
from datetime import datetime

DB_PATH = "projectverse.db"
BACKUP_DIR = "backups"
MAX_BACKUPS = 14  # Keep last 14 backups

def perform_backup():
    if not os.path.exists(DB_PATH):
        print(f"[Error]: Database {DB_PATH} not found.")
        return False

    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"projectverse_backup_{timestamp}.db")

    print(f"Starting database backup: {DB_PATH} -> {backup_file}")

    try:
        # Checkpoint WAL mode before backup
        conn = sqlite3.connect(DB_PATH, timeout=30.0)
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        conn.close()

        # Copy database file
        shutil.copyfile(DB_PATH, backup_file)
        file_size_kb = os.path.getsize(backup_file) / 1024
        print(f"[Success]: Backup created successfully ({file_size_kb:.2f} KB).")

        # Prune old backups
        backups = sorted([os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR) if f.startswith("projectverse_backup_") and f.endswith(".db")])
        if len(backups) > MAX_BACKUPS:
            to_remove = backups[:-MAX_BACKUPS]
            for old in to_remove:
                os.remove(old)
                print(f"[Pruned]: Removed aged backup {old}")

        return True
    except Exception as e:
        print(f"[Error]: Backup failed: {e}")
        return False

if __name__ == "__main__":
    perform_backup()
