# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from sqlalchemy import text, func

def auto_seed_database(db: Session, engine):
    from app import models
    
    # 1. Ensure deleted_at and new elective columns exist across all tables
    try:
        if engine.dialect.name == "sqlite":
            tables = ["students", "parents", "tenants", "exam_materials", "vod_library", "attendance_logs", "tutor_profiles", "planner_blocks", "administrative_requests", "exam_paper_masters", "exam_omr_submissions"]
            for t in tables:
                try:
                    cols = [row[1] for row in db.execute(text(f"PRAGMA table_info({t})")).fetchall()]
                    if cols:
                        if "deleted_at" not in cols:
                            db.execute(text(f"ALTER TABLE {t} ADD COLUMN deleted_at DATETIME"))
                        if t in ["exam_paper_masters", "exam_omr_submissions"]:
                            if "curriculum_era" not in cols:
                                db.execute(text(f"ALTER TABLE {t} ADD COLUMN curriculum_era VARCHAR(50) DEFAULT '2022_2027'"))
                            if "elective_subject" not in cols:
                                db.execute(text(f"ALTER TABLE {t} ADD COLUMN elective_subject VARCHAR(100)"))
                        db.commit()
                except Exception:
                    db.rollback()
        elif engine.dialect.name in ("postgresql", "postgres"):
            tables = ["students", "parents", "tenants", "exam_materials", "vod_library", "attendance_logs", "tutor_profiles", "planner_blocks", "administrative_requests", "exam_paper_masters", "exam_omr_submissions"]
            for t in tables:
                try:
                    db.execute(text(f"ALTER TABLE {t} ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP WITH TIME ZONE;"))
                    if t in ["exam_paper_masters", "exam_omr_submissions"]:
                        db.execute(text(f"ALTER TABLE {t} ADD COLUMN IF NOT EXISTS curriculum_era VARCHAR(50) DEFAULT '2022_2027';"))
                        db.execute(text(f"ALTER TABLE {t} ADD COLUMN IF NOT EXISTS elective_subject VARCHAR(100);"))
                    db.commit()
                except Exception:
                    db.rollback()
    except Exception as e:
        db.rollback()
        print(f"[AUTO_SEED] Column migration warning: {e}")

    # 1.1 One-time migration: Zero out test cash for beta phase (Runs ONLY ONCE and never overwrites future real purchases)
    try:
        db.execute(text("CREATE TABLE IF NOT EXISTS system_migrations (migration_key VARCHAR(100) PRIMARY KEY, applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"))
        db.commit()
        
        mig = db.execute(text("SELECT migration_key FROM system_migrations WHERE migration_key = 'beta_cash_zero_20260910'")).fetchone()
        if not mig:
            db.query(models.Student).filter(models.Student.paid_cash > 0).update({models.Student.paid_cash: 0})
            db.execute(text("INSERT INTO system_migrations (migration_key) VALUES ('beta_cash_zero_20260910')"))
            db.commit()
            print("[AUTO_SEED] One-time beta cash reset applied successfully.")
    except Exception as e:
        db.rollback()
        print(f"[AUTO_SEED] One-time migration note: {e}")

    # 1.5 Ensure Default Real Active Tenants Exist for All 4 Industry Types
    try:
        import json
        
        def generate_default_seats():
            seats = []
            types = ["FOCUS", "FOCUS", "OPEN", "WINDOW"]
            dummy_users = [
                {"name": "김민준", "plan": "정기권 (30일)", "rem": 18, "start": "08:30", "time": "6시간 40분"},
                {"name": "이서연", "plan": "100시간권", "rem": 42, "start": "09:10", "time": "5시간 15분"},
                {"name": "박도윤", "plan": "정기권 (30일)", "rem": 5, "start": "10:00", "time": "4시간 20분"},
                {"name": "최지우", "plan": "당일권 (8시간)", "rem": 3, "start": "11:30", "time": "3시간 10분"},
                {"name": "정예은", "plan": "50시간권", "rem": 21, "start": "13:00", "time": "2시간 00분"},
                {"name": "강현우", "plan": "정기권 (60일)", "rem": 45, "start": "07:50", "time": "7시간 30분"},
                {"name": "윤서아", "plan": "100시간권", "rem": 88, "start": "14:20", "time": "1시간 20분"},
                {"name": "임지호", "plan": "당일권 (4시간)", "rem": 1, "start": "15:00", "time": "0시간 40분"},
            ]
            u_idx = 0
            for r_idx, row_char in enumerate(["A", "B", "C", "D"]):
                for col_idx in range(1, 7):
                    s_id = f"{row_char}{col_idx:02d}"
                    s_num = r_idx * 6 + col_idx
                    stype = types[r_idx]
                    status = "EMPTY"
                    student_name = ""
                    plan_type = ""
                    rem_days = 0
                    start_time = ""
                    study_time = ""
                    
                    if s_num in [1, 2, 4, 7, 8, 13, 19, 21] and u_idx < len(dummy_users):
                        u = dummy_users[u_idx]
                        status = "OCCUPIED" if s_num != 4 else "OUT_BRIEF"
                        student_name = u["name"]
                        plan_type = u["plan"]
                        rem_days = u["rem"]
                        start_time = u["start"]
                        study_time = u["time"]
                        u_idx += 1
                    elif s_num == 12:
                        status = "RESERVED"
                        student_name = "예약 대기"

                    seats.append({
                        "seat_id": s_id,
                        "seat_num": s_num,
                        "seat_type": stype,
                        "status": status,
                        "student_name": student_name,
                        "plan_type": plan_type,
                        "remaining_days": rem_days,
                        "start_time": start_time,
                        "study_time_today": study_time
                    })
            return json.dumps(seats, ensure_ascii=False)

        default_tenants = [
            {
                "code": "ILWON-2027",
                "name": "일원 대입전문학원",
                "director_name": "김철훈 원장",
                "director_email": "1286orbital21@gmail.com",
                "director_pin": "12Yonsei21*",
                "tier": 3,
                "license_tier": 3,
                "business_type": "HIGH_ACADEMY",
                "subject_desc": "수능국어, 대치동 대입직강, 모의고사 OMR 처방",
                "seats": "[]"
            },
            {
                "code": "MID-TOP01",
                "name": "대치 탑클래스 중등학원",
                "director_name": "박중등 원장",
                "director_email": "mid_top@palin.com",
                "director_pin": "1286",
                "tier": 2,
                "license_tier": 2,
                "business_type": "MID_ACADEMY",
                "subject_desc": "중등 5대과목 내신 올A, 특목자사고(외대부고/하나고) 진학",
                "seats": "[]"
            },
            {
                "code": "ELEM-PET01",
                "name": "아이꿈 초등 보습·어학원",
                "director_name": "이지은 원장",
                "director_email": "elem_pet@palin.com",
                "director_pin": "1286",
                "tier": 2,
                "license_tier": 2,
                "business_type": "ELEM_ACADEMY",
                "subject_desc": "초등 3대 바른 루틴, 펫 성장 칭찬케어, 영재 어학",
                "seats": "[]"
            },
            {
                "code": "CAFE-STUDY01",
                "name": "일원 프리미엄 스터디카페",
                "director_name": "정스카 대표",
                "director_email": "study_cafe@palin.com",
                "director_pin": "1286",
                "tier": 2,
                "license_tier": 2,
                "business_type": "STUDY_CAFE",
                "subject_desc": "24시간 2D 좌석관제, 전연령 순공 랭킹, 이용권 자동관리",
                "seats": generate_default_seats()
            }
        ]

        for dt in default_tenants:
            t_exist = db.query(models.Tenant).filter(models.Tenant.code == dt["code"]).first()
            if not t_exist:
                db.add(models.Tenant(
                    code=dt["code"],
                    name=dt["name"],
                    director_name=dt["director_name"],
                    director_email=dt["director_email"],
                    director_phone="010-1286-2386",
                    director_pin=dt["director_pin"],
                    tier=dt["tier"],
                    license_tier=dt["license_tier"],
                    business_type=dt["business_type"],
                    seat_layout_json=dt.get("seats", "[]"),
                    max_students=99999,
                    royalty_rate=15.0,
                    monthly_revenue=0,
                    subject_desc=dt["subject_desc"],
                    is_active=True,
                    deleted_at=None
                ))
                db.commit()
            else:
                t_exist.tier = dt["tier"]
                t_exist.license_tier = dt["license_tier"]
                t_exist.name = dt["name"]
                t_exist.director_name = dt["director_name"]
                t_exist.director_pin = dt["director_pin"]
                t_exist.director_email = dt["director_email"]
                if not getattr(t_exist, "business_type", None) or t_exist.business_type == "HIGH_ACADEMY" and dt["business_type"] != "HIGH_ACADEMY":
                    t_exist.business_type = dt["business_type"]
                if dt["business_type"] == "STUDY_CAFE" and (not getattr(t_exist, "seat_layout_json", None) or t_exist.seat_layout_json == "[]"):
                    t_exist.seat_layout_json = dt.get("seats", "[]")
                db.commit()
    except Exception as e:
        db.rollback()
        print(f"[AUTO_SEED] Tenant seed warning: {e}")

    # 1.6 Scan and synchronize authentic exam materials from static/downloads folder structure
    try:
        from app.exam_file_sync import scan_and_sync_downloads
        scan_and_sync_downloads(db)
    except Exception as em_err:
        db.rollback()
        print(f"[AUTO_SEED] Exam folder sync note: {em_err}")

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

    # STEP C: Ensure Study Sessions exist for students
    try:
        from datetime import timedelta
        import random
        now = datetime.now()
        for st in db.query(models.Student).all():
            if db.query(models.StudySession).filter(models.StudySession.student_id == st.id).count() == 0:
                total_sec = 0
                for _ in range(random.randint(6, 15)):
                    days_ago = random.randint(0, 7)
                    hours_ago = random.randint(1, 12)
                    start_dt = (now - timedelta(days=days_ago, hours=hours_ago)).replace(minute=random.randint(0, 50), second=0)
                    dur_sec = random.randint(45, 150) * 60
                    end_dt = start_dt + timedelta(seconds=dur_sec)
                    total_sec += dur_sec
                    db.add(models.StudySession(
                        student_id=st.id,
                        start_time=start_dt,
                        end_time=end_dt,
                        duration_sec=dur_sec,
                        is_distracted=False,
                        created_at=start_dt,
                        deleted_at=None
                    ))
                total_mins = total_sec // 60
                st.diligence_score = (st.diligence_score or 0) + total_mins
                st.weekly_diligence_points = (st.weekly_diligence_points or 0) + total_mins
                if not st.streak_days:
                    st.streak_days = random.randint(3, 10)
                st.last_streak_date = now.date()
        db.commit()
    except Exception as se_err:
        db.rollback()
        print(f"[AUTO_SEED] Study session seed warning: {se_err}")

    print("[AUTO_SEED] Seeding completed.")
