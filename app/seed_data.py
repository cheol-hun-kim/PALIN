# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from sqlalchemy import text, func

def auto_seed_database(db: Session, engine):
    from app import models
    
    # 1. Ensure deleted_at column exists across all tables
    try:
        if engine.dialect.name == "sqlite":
            tables = ["students", "parents", "tenants", "exam_materials", "vod_library", "attendance_logs", "tutor_profiles", "planner_blocks", "administrative_requests"]
            for t in tables:
                try:
                    cols = [row[1] for row in db.execute(text(f"PRAGMA table_info({t})")).fetchall()]
                    if cols and "deleted_at" not in cols:
                        db.execute(text(f"ALTER TABLE {t} ADD COLUMN deleted_at DATETIME"))
                        db.commit()
                except Exception:
                    db.rollback()
        elif engine.dialect.name in ("postgresql", "postgres"):
            tables = ["students", "parents", "tenants", "exam_materials", "vod_library", "attendance_logs", "tutor_profiles", "planner_blocks", "administrative_requests"]
            for t in tables:
                try:
                    db.execute(text(f"ALTER TABLE {t} ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP WITH TIME ZONE;"))
                    db.commit()
                except Exception:
                    db.rollback()
    except Exception as e:
        db.rollback()
        print(f"[AUTO_SEED] Column migration warning: {e}")

    # 1.5 Ensure Default Tenants Exist & Synchronize Pilot Tier 3
    try:
        default_tenants = [
            {"code": "ILWON-2027", "name": "일원학원", "director_name": "일원 원장", "director_pin": "1286", "tier": 3, "license_tier": 3},
            {"code": "PALIN-2027", "name": "팰린 마스터 학원", "director_name": "팰린 총괄", "director_pin": "1286", "tier": 3, "license_tier": 3},
            {"code": "DAECH1", "name": "팰린 대치본원", "director_name": "대치 원장", "director_pin": "1286", "tier": 3, "license_tier": 3},
            {"code": "ACAD-2027", "name": "대치 미래탐구", "director_name": "미탐 원장", "director_pin": "1286", "tier": 3, "license_tier": 3}
        ]
        for dt in default_tenants:
            t_exist = db.query(models.Tenant).filter(models.Tenant.code == dt["code"]).first()
            if not t_exist:
                db.add(models.Tenant(
                    code=dt["code"],
                    name=dt["name"],
                    director_name=dt["director_name"],
                    director_pin=dt["director_pin"],
                    tier=dt["tier"],
                    license_tier=dt["license_tier"],
                    is_active=True,
                    deleted_at=None
                ))
                db.commit()
            else:
                if t_exist.tier != dt["tier"] or t_exist.license_tier != dt["license_tier"]:
                    t_exist.tier = dt["tier"]
                    t_exist.license_tier = dt["license_tier"]
                    db.commit()
    except Exception as e:
        db.rollback()
        print(f"[AUTO_SEED] Tenant seed warning: {e}")

    # 2. Check student count
    student_count = 0
    try:
        student_count = db.query(models.Student).count()
    except Exception:
        db.rollback()

    if student_count >= 10:
        print(f"[AUTO_SEED] Database already has {student_count} students. Preserving all user data.")
        return

    print("[AUTO_SEED] Initializing 109 students and parents into database...")
    from app.students_data_builtin import BUILTIN_STUDENTS_LIST
    students_list = BUILTIN_STUDENTS_LIST

    # STEP A: Insert all Parents FIRST with duplicate deduplication
    seen_pids = set()
    for s in students_list:
        pid = s.get("parent_id")
        if pid and pid not in seen_pids:
            seen_pids.add(pid)
            try:
                p_exist = db.query(models.Parent).filter(models.Parent.id == pid).first()
                if not p_exist:
                    db.add(models.Parent(
                        id=pid,
                        name=f"{s.get('name', '학생')} 학부모",
                        phone=f"010-{pid:04d}-5678",
                        is_premium_subscribed=True,
                        email=f"parent_{pid}@palin.com",
                        role="PARENT",
                        wallet_balance=0,
                        deleted_at=None
                    ))
                    db.commit()
            except Exception:
                db.rollback()

    # STEP B: Insert Students
    for s in students_list:
        try:
            s_exist = db.query(models.Student).filter(models.Student.id == s["id"]).first()
            if not s_exist:
                p_id = s.get("parent_id")
                if p_id:
                    p_match = db.query(models.Parent).filter(models.Parent.id == p_id).first()
                    if not p_match:
                        p_id = None
                
                db.add(models.Student(
                    id=s["id"],
                    email=s.get("email", f"student_{s['id']}@palin.com"),
                    name=s.get("name", f"학생{s['id']}"),
                    phone=s.get("phone", f"010-0000-{s['id']:04d}"),
                    grade=s.get("grade", 3),
                    region=s.get("region", "경기도 성남시 분당구"),
                    high_school=s.get("high_school", "낙생고등학교"),
                    target_univ=s.get("target_univ", "연세대학교 의예과"),
                    baseline_univ=s.get("baseline_univ", "고려대학교 의과대학"),
                    wake_target_time=s.get("wake_target_time", "06:30"),
                    sleep_target_time=s.get("sleep_target_time", "23:30"),
                    current_points=s.get("current_points", 100),
                    league_tier=s.get("league_tier", "BRONZE"),
                    point_multiplier=s.get("point_multiplier", 1),
                    diligence_score=s.get("diligence_score", 0),
                    dday_date=s.get("dday_date", "2026-11-19"),
                    dday_title=s.get("dday_title", "2027 수능"),
                    parent_id=p_id,
                    referral_code=s.get("referral_code"),
                    has_unlimited_chat=s.get("has_unlimited_chat", False),
                    role="STUDENT",
                    deleted_at=None
                ))
                db.commit()
        except Exception:
            db.rollback()

    print("[AUTO_SEED] Seeding completed.")
