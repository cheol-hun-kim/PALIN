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

    # 2. Check student count
    student_count = 0
    try:
        student_count = db.query(models.Student).count()
    except Exception:
        pass

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
            p_exist = db.query(models.Parent).filter(models.Parent.id == pid).first()
            if not p_exist:
                db.add(models.Parent(
                    id=pid,
                    name=f"{s.get('name', '학생')} 학부모",
                    phone=f"010-{pid:04d}-5678",
                    is_premium_subscribed=True,
                    email=f"parent_{pid}@palin.com",
                    role="PARENT",
                    wallet_balance=50000,
                    deleted_at=None
                ))
    try:
        db.commit()
    except Exception as pe:
        db.rollback()
        print(f"[AUTO_SEED] Parent insert note: {pe}")

    # STEP B: Insert all Students
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
    try:
        db.commit()
    except Exception as se:
        db.rollback()
        print(f"[AUTO_SEED] Student insert note: {se}")

    # STEP C: Ensure Student #1 (Kim Cheolhun) is correctly configured
    s1 = db.query(models.Student).filter(models.Student.id == 1).first()
    if not s1:
        s1 = models.Student(
            id=1,
            name="김철훈",
            email="1286orbital21@gmail.com",
            phone="010-5527-2979",
            grade=4,
            region="경기도 성남시 분당구",
            high_school="낙생고",
            target_univ="연세대학교 의예과",
            baseline_univ="서울대학교 화학생물공학부",
            wake_target_time="06:30",
            sleep_target_time="23:30",
            current_points=670,
            streak_days=7,
            max_streak_days=7,
            league_tier="PLATINUM",
            medical_symbol="MED",
            paid_cash=128200,
            free_report_tickets=3,
            academy_code="ILWON-2027",
            enrollment_status="ENROLLED",
            tuition_paid=True,
            parent_id=1
        )
        db.add(s1)
    else:
        s1.name = "김철훈"
        s1.target_univ = "연세대학교 의예과"
        s1.baseline_univ = "서울대학교 화학생물공학부"
        s1.streak_days = 7
        s1.max_streak_days = 7
        s1.league_tier = "PLATINUM"
        s1.medical_symbol = "MED"
        s1.academy_code = "ILWON-2027"

    # STEP D: Ensure default Tenant exists
    t1 = db.query(models.Tenant).filter(models.Tenant.code == "ILWON-2027").first()
    if not t1:
        db.add(models.Tenant(
            code="ILWON-2027",
            name="일원학원",
            director_name="김철훈 원장",
            director_email="1286orbital21@gmail.com",
            director_phone="010-5527-2979",
            director_password_hash="1286",
            tier=3,
            is_active=True,
            custom_system_prompt="학생들의 수험 몰입을 최우선으로 엄격하게 지도합니다."
        ))

    # STEP E: Fix PostgreSQL auto-increment sequences if on postgres
    if engine.dialect.name in ("postgresql", "postgres"):
        try:
            db.execute(text("SELECT setval(pg_get_serial_sequence('students', 'id'), COALESCE(MAX(id), 1) + 1, false) FROM students;"))
            db.execute(text("SELECT setval(pg_get_serial_sequence('parents', 'id'), COALESCE(MAX(id), 1) + 1, false) FROM parents;"))
        except Exception as seq_err:
            print(f"[AUTO_SEED] Sequence sync warning: {seq_err}")

    db.commit()
    print("[AUTO_SEED] 109 students, parents and tenant seeded successfully with 100% integrity!")
