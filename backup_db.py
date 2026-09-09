import os
import sys
import json
import time
from datetime import datetime
from sqlalchemy import inspect, text

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Import core database engine
from app.database import engine, DATABASE_URL, BASE_DIR

BACKUP_DIR = os.path.join(BASE_DIR, "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

def run_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_backup_folder = os.path.join(BACKUP_DIR, f"backup_{timestamp}")
    os.makedirs(target_backup_folder, exist_ok=True)

    print("=" * 60)
    print(f"🛡️ [PALIN OS] Database Automated Backup & Snapshot Engine")
    print(f"   Target DB: {DATABASE_URL}")
    print(f"   Destination: {target_backup_folder}")
    print("=" * 60)

    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    print(f"📦 Found {len(table_names)} tables in database: {table_names}")

    backup_manifest = {
        "timestamp": timestamp,
        "database_url": DATABASE_URL,
        "tables": {},
        "total_rows": 0
    }

    with engine.connect() as conn:
        for table in table_names:
            try:
                res = conn.execute(text(f"SELECT * FROM {table}"))
                cols = res.keys()
                rows = [dict(zip(cols, row)) for row in res.fetchall()]
                
                cleaned_rows = []
                for row in rows:
                    cleaned_row = {}
                    for k, v in row.items():
                        if isinstance(v, (datetime, )):
                            cleaned_row[k] = v.isoformat()
                        else:
                            cleaned_row[k] = v
                    cleaned_rows.append(cleaned_row)

                table_json_path = os.path.join(target_backup_folder, f"{table}.json")
                with open(table_json_path, "w", encoding="utf-8") as f:
                    json.dump(cleaned_rows, f, ensure_ascii=False, indent=2)

                row_count = len(cleaned_rows)
                backup_manifest["tables"][table] = row_count
                backup_manifest["total_rows"] += row_count
                print(f"   ✅ [{table}] -> {row_count} rows backed up.")
            except Exception as e:
                print(f"   ⚠️ Error backing up table {table}: {e}")

    manifest_path = os.path.join(target_backup_folder, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(backup_manifest, f, ensure_ascii=False, indent=2)

    print("-" * 60)
    print(f"🎉 Backup successfully completed! Total rows archived: {backup_manifest['total_rows']}")
    print(f"   Manifest: {manifest_path}")
    print("=" * 60)

if __name__ == "__main__":
    run_backup()
