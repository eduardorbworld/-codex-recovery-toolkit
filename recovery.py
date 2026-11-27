"""Local SQLite recovery helper. Close ChatGPT/Codex before use."""
import argparse
import hashlib
import shutil
import sqlite3
from pathlib import Path
from tempfile import mkdtemp, TemporaryDirectory

NAME = ".codex-global-state.sqlite"

def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()

def snapshot(db):
    return {p.name: digest(p) for p in (db, *(Path(str(db)+s) for s in ("-journal", "-wal", "-shm"))) if p.is_file()}

def check(db):
    with sqlite3.connect(db.resolve().as_uri()+"?mode=rw", uri=True, timeout=3) as conn:
        try:
            result = conn.execute("PRAGMA integrity_check").fetchall()
            if result != [("ok",)]:
                raise RuntimeError("Integrity check failed")
            return "ok"
        finally:
            conn.close()

def recover(db, destination, apply=False):
    db = db.resolve()
    destination = destination.resolve()
    if not db.is_file() or db.name != NAME:
        raise ValueError("Expected existing "+NAME)
    if destination == db.parent or db.parent in destination.parents:
        raise ValueError("Choose a backup destination outside the Codex directory")
    before = snapshot(db)
    backup = Path(mkdtemp(prefix="codex-backup-", dir=destination))
    for name in before:
        shutil.copy2(db.parent/name, backup/name)
    if snapshot(backup/db.name) != before or snapshot(db) != before:
        raise RuntimeError("Backup verification failed or source changed")
    with TemporaryDirectory(prefix="recovery-test-", dir=destination) as tmp:
        work = Path(tmp)
        for name in before:
            shutil.copy2(backup/name, work/name)
        check(work/db.name)
    if apply:
        if snapshot(db) != before:
            raise RuntimeError("Source changed; close all related processes")
        check(db)
        # Verify a write transaction can begin; do not change application rows.
        conn = sqlite3.connect(db.as_uri()+"?mode=rw", uri=True, timeout=3)
        try:
            conn.execute("BEGIN IMMEDIATE")
            conn.rollback()
        finally:
            conn.close()
    return backup

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--database", type=Path, default=Path.home()/".codex"/NAME)
    p.add_argument("--backup-dir", type=Path)
    p.add_argument("--apply", action="store_true")
    p.add_argument("--closed", action="store_true", help="Confirm all related processes are closed")
    args = p.parse_args()
    if not args.database.is_file():
        p.error("Database not found")
    print("Free GiB:", round(shutil.disk_usage(args.database.parent).free/2**30, 2))
    print("Sidecars:", [s for s in ("-journal","-wal","-shm") if Path(str(args.database)+s).exists()])
    if args.backup_dir:
        if not args.closed:
            p.error("Close ChatGPT and Codex, then pass --closed")
        print("Verified backup:", recover(args.database,args.backup_dir,args.apply))
        print("Integrity: OK; original recovery attempted" if args.apply else "Copy integrity: OK; original untouched")
    elif args.apply:
        p.error("--apply requires --backup-dir")
if __name__ == "__main__":
    main()
