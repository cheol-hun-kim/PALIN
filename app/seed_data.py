# -*- coding: utf-8 -*-
import json
import os
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
                    pass
        elif engine.dialect.name in ("postgresql", "postgres"):
            tables = ["students", "parents", "tenants", "exam_materials", "vod_library", "attendance_logs", "tutor_profiles", "planner_blocks", "administrative_requests"]
            for t in tables:
                try:
                    db.execute(text(f"ALTER TABLE {t} ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP WITH TIME ZONE;"))
                    db.commit()
                except Exception:
                    pass
    except Exception as e:
        print(f"[AUTO_SEED] Column migration warning: {e}")

    # 2. Check if DB already has students. If YES, NEVER overwrite or re-seed anything!
    student_count = 0
    try:
        student_count = db.query(models.Student).count()
    except Exception:
        pass

    if student_count > 0:
        print(f"[AUTO_SEED] Database already has {student_count} students. Preserving all user data and deletions.")
        return

    print("[AUTO_SEED] Empty database detected. Initializing first-time baseline data...")
    # Load students from JSON dump
    dump_path = os.path.join(os.path.dirname(__file__), "supabase_students_dump.json")
    if not os.path.exists(dump_path):
        dump_path = r'C:\Users\1286o\.gemini\antigravity\brain\d3a9304a-a387-45ed-ba1c-8d4ce5ea0a56\scratch\supabase_students_dump.json'
    
    students_list = []
    if os.path.exists(dump_path):
        try:
            with open(dump_path, "r", encoding="utf-8") as f:
                raw = f.read()
            start = raw.find('[')
            end = raw.rfind(']') + 1
            parsed = json.loads(raw[start:end])
            students_list = parsed[0]["json_agg"]
        except Exception as e:
            print(f"[AUTO_SEED] Error parsing dump: {e}")

    for s in students_list:
        sid = s["id"]
        existing = db.query(models.Student).filter(models.Student.id == sid).first()
        if not existing:
            student = models.Student(
                id=sid,
                email=s.get("email"),
                name=s.get("name"),
                phone=s.get("phone", ""),
                grade=s.get("grade", 3),
                region=s.get("region", "성남시 분당구"),
                sido=s.get("sido", "경기도"),
                sigungu=s.get("sigungu", "성남시 분당구"),
                high_school=s.get("high_school", "-"),
                high_school_type=s.get("high_school_type", "일반고"),
                target_univ=s.get("target_univ", "-"),
                baseline_univ=s.get("baseline_univ", "-"),
                wake_target_time=s.get("wake_target_time", "06:30"),
                sleep_target_time=s.get("sleep_target_time", "23:30"),
                current_points=s.get("current_points", 100),
                password_hash=s.get("password_hash"),
                role=s.get("role", "STUDENT"),
                parent_invite_code=s.get("parent_invite_code"),
                league_tier=s.get("league_tier", "BRONZE"),
                point_multiplier=s.get("point_multiplier", 1.0),
                referrer_id=s.get("referrer_id"),
                diligence_score=s.get("diligence_score", 0),
                is_vip=bool(s.get("is_vip")),
                is_banned=bool(s.get("is_banned")),
                ban_reason=s.get("ban_reason"),
                escrow_deposit=s.get("escrow_deposit", 50000),
                escrow_deductions=s.get("escrow_deductions", 0),
                dday_date=s.get("dday_date", "2026-11-19"),
                dday_title=s.get("dday_title", "2027 수능"),
                streak_days=s.get("streak_days", 7 if sid == 1 else 0),
                max_streak_days=s.get("max_streak_days", 7 if sid == 1 else 0),
                medical_symbol=s.get("medical_symbol", "GENERAL"),
                paid_cash=s.get("paid_cash", 0),
                free_report_tickets=s.get("free_report_tickets", 0),
                referral_code=s.get("referral_code"),
                referred_by=s.get("referred_by"),
                has_unlimited_chat=bool(s.get("has_unlimited_chat")),
                previous_b2c_tier=s.get("previous_b2c_tier", "B2C_FREE"),
                academy_code="ILWON-2027",
                ai_level=s.get("ai_level", "B2B_PREMIUM"),
                tuition_paid=bool(s.get("tuition_paid")),
                textbook_paid=bool(s.get("textbook_paid")),
                textbooks_distributed=s.get("textbooks_distributed", ""),
                enrollment_status=s.get("enrollment_status", "ENROLLED"),
                leave_reason=s.get("leave_reason"),
                deleted_at=None,
                parent_id=s.get("parent_id")
            )
            db.add(student)
            
            # Seed parent
            pid = s.get("parent_id")
            if pid:
                p_exist = db.query(models.Parent).filter(models.Parent.id == pid).first()
                if not p_exist:
                    db.add(models.Parent(
                        id=pid,
                        name=f"{s.get('name')} 학부모",
                        phone=f"010-{pid:04d}-5678",
                        is_premium_subscribed=True,
                        email=f"parent_{pid}@palin.com",
                        role="PARENT",
                        wallet_balance=50000,
                        deleted_at=None
                    ))
    
    # Ensure student 1 is Kim Cheolhun with 7-day streak
    s1 = db.query(models.Student).filter(models.Student.id == 1).first()
    if s1:
        s1.name = "김철훈"
        s1.target_univ = "연세대학교 의예과"
        s1.baseline_univ = "서울대학교 화학생물공학부"
        s1.streak_days = 7
        s1.max_streak_days = 7
        s1.league_tier = "PLATINUM"
        s1.medical_symbol = "MED"
        s1.academy_code = "ILWON-2027"
    
    db.commit()
    print("[AUTO_SEED] Initial baseline seed completed.")
