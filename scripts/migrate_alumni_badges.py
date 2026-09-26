# -*- coding: utf-8 -*-
from app.database import SessionLocal, engine
from sqlalchemy import text

db = SessionLocal()
print("[MIGRATION] Applying Alumni Verification & Admission Track Columns...")

columns_to_add_students = [
    ("passed_univ", "VARCHAR(255)"),
    ("passed_major", "VARCHAR(255)"),
    ("admission_track", "VARCHAR(50)"),
    ("alumni_academy_verified", "BOOLEAN DEFAULT FALSE"),
    ("alumni_school_verified", "BOOLEAN DEFAULT FALSE"),
    ("alumni_univ_verified", "BOOLEAN DEFAULT FALSE"),
    ("badge_academy_equipped", "BOOLEAN DEFAULT TRUE"),
    ("badge_school_equipped", "BOOLEAN DEFAULT TRUE"),
    ("badge_univ_equipped", "BOOLEAN DEFAULT TRUE"),
]

for col_name, col_type in columns_to_add_students:
    try:
        db.execute(text(f"ALTER TABLE students ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
        db.commit()
        print(f"  + students.{col_name} checked/added.")
    except Exception as e:
        db.rollback()
        print(f"  - students.{col_name} note: {e}")

try:
    db.execute(text("ALTER TABLE tutor_profiles ADD COLUMN IF NOT EXISTS admission_track VARCHAR(50)"))
    db.commit()
    print("  + tutor_profiles.admission_track checked/added.")
except Exception as e:
    db.rollback()
    print(f"  - tutor_profiles.admission_track note: {e}")

db.close()
print("[MIGRATION] Done successfully!")
