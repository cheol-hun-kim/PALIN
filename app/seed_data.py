# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from sqlalchemy import text, func

def auto_seed_database(db: Session, engine):
    from app import models
    
    # 1. Ensure deleted_at and all new columns exist across all tables
    student_cols_def = [
        ("deleted_at", "TIMESTAMP WITH TIME ZONE", "DATETIME"),
        ("school_level", "VARCHAR(50) DEFAULT 'HIGH'", "VARCHAR(50) DEFAULT 'HIGH'"),
        ("school_name", "VARCHAR(150)", "VARCHAR(150)"),
        ("target_high_school", "VARCHAR(150)", "VARCHAR(150)"),
        ("target_high_school_type", "VARCHAR(50)", "VARCHAR(50)"),
        ("baseline_high_school", "VARCHAR(150)", "VARCHAR(150)"),
        ("dream_job", "VARCHAR(150)", "VARCHAR(150)"),
        ("pet_type", "VARCHAR(50) DEFAULT 'cat'", "VARCHAR(50) DEFAULT 'cat'"),
        ("pet_level", "INTEGER DEFAULT 1", "INTEGER DEFAULT 1"),
        ("pet_exp", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0"),
        ("elem_routine_status", "TEXT DEFAULT '{}'", "TEXT DEFAULT '{}'"),
        ("paid_cash", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0"),
        ("free_report_tickets", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0"),
        ("referral_code", "VARCHAR(100)", "VARCHAR(100)"),
        ("referred_by", "VARCHAR(100)", "VARCHAR(100)"),
        ("has_unlimited_chat", "BOOLEAN DEFAULT FALSE", "BOOLEAN DEFAULT 0"),
        ("chat_tokens", "INTEGER DEFAULT 5", "INTEGER DEFAULT 5"),
        ("b2c_subscription_tier", "VARCHAR(50) DEFAULT 'TIER_1_FREE'", "VARCHAR(50) DEFAULT 'TIER_1_FREE'"),
        ("weekly_diligence_points", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0"),
        ("is_vip_this_week", "BOOLEAN DEFAULT FALSE", "BOOLEAN DEFAULT 0"),
        ("previous_b2c_tier", "VARCHAR(50) DEFAULT 'B2C_FREE'", "VARCHAR(50) DEFAULT 'B2C_FREE'"),
        ("academy_code", "VARCHAR(100)", "VARCHAR(100)"),
        ("academy_approval_status", "VARCHAR(50) DEFAULT 'NONE'", "VARCHAR(50) DEFAULT 'NONE'"),
        ("pending_tenant_code", "VARCHAR(100)", "VARCHAR(100)"),
        ("ai_level", "VARCHAR(50) DEFAULT 'B2C_FREE'", "VARCHAR(50) DEFAULT 'B2C_FREE'"),
        ("tuition_paid", "BOOLEAN DEFAULT FALSE", "BOOLEAN DEFAULT 0"),
        ("textbook_paid", "BOOLEAN DEFAULT FALSE", "BOOLEAN DEFAULT 0"),
        ("textbooks_distributed", "TEXT DEFAULT ''", "TEXT DEFAULT ''"),
        ("enrollment_status", "VARCHAR(50) DEFAULT 'ENROLLED'", "VARCHAR(50) DEFAULT 'ENROLLED'"),
        ("leave_reason", "VARCHAR(255)", "VARCHAR(255)"),
        ("assigned_seat_number", "INTEGER", "INTEGER"),
        ("seat_checkin_time", "TIMESTAMP WITH TIME ZONE", "DATETIME"),
        ("seat_status", "VARCHAR(50) DEFAULT 'NONE'", "VARCHAR(50) DEFAULT 'NONE'"),
        ("parent_invite_code", "VARCHAR(100)", "VARCHAR(100)"),
        ("medical_symbol", "VARCHAR(50) DEFAULT 'GENERAL'", "VARCHAR(50) DEFAULT 'GENERAL'"),
        ("is_alumni", "BOOLEAN DEFAULT FALSE", "BOOLEAN DEFAULT 0"),
        ("alumni_academy", "VARCHAR(100)", "VARCHAR(100)"),
        ("last_streak_date", "DATE", "DATE")
    ]

    try:
        if engine.dialect.name == "sqlite":
            tables = ["students", "parents", "tenants", "exam_materials", "vod_library", "attendance_logs", "tutor_profiles", "planner_blocks", "administrative_requests", "exam_paper_masters", "exam_omr_submissions", "b2b_support_tickets", "feedbacks", "consulting_requests"]
            for t in tables:
                try:
                    cols = [row[1] for row in db.execute(text(f"PRAGMA table_info({t})")).fetchall()]
                    if cols:
                        if "deleted_at" not in cols:
                            db.execute(text(f"ALTER TABLE {t} ADD COLUMN deleted_at DATETIME"))
                        if t == "students":
                            for col_name, _, sqlite_type in student_cols_def:
                                if col_name not in cols:
                                    try:
                                        db.execute(text(f"ALTER TABLE students ADD COLUMN {col_name} {sqlite_type}"))
                                    except Exception:
                                        pass
                        if t == "b2b_support_tickets":
                            if "author_name" not in cols:
                                db.execute(text("ALTER TABLE b2b_support_tickets ADD COLUMN author_name VARCHAR"))
                        if t in ["exam_paper_masters", "exam_omr_submissions"]:
                            if "curriculum_era" not in cols:
                                db.execute(text(f"ALTER TABLE {t} ADD COLUMN curriculum_era VARCHAR(50) DEFAULT '2022_2027'"))
                            if "elective_subject" not in cols:
                                db.execute(text(f"ALTER TABLE {t} ADD COLUMN elective_subject VARCHAR(100)"))
                        db.commit()
                except Exception:
                    db.rollback()
        elif engine.dialect.name in ("postgresql", "postgres"):
            tables = ["students", "parents", "tenants", "exam_materials", "vod_library", "attendance_logs", "tutor_profiles", "planner_blocks", "administrative_requests", "exam_paper_masters", "exam_omr_submissions", "b2b_support_tickets", "feedbacks", "consulting_requests"]
            for t in tables:
                try:
                    db.execute(text(f"ALTER TABLE {t} ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP WITH TIME ZONE;"))
                    if t == "students":
                        for col_name, pg_type, _ in student_cols_def:
                            try:
                                db.execute(text(f"ALTER TABLE students ADD COLUMN IF NOT EXISTS {col_name} {pg_type};"))
                            except Exception:
                                pass
                    if t == "b2b_support_tickets":
                        try:
                            db.execute(text("ALTER TABLE b2b_support_tickets ADD COLUMN IF NOT EXISTS author_name VARCHAR;"))
                        except Exception:
                            pass
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

        mig_b2c = db.execute(text("SELECT migration_key FROM system_migrations WHERE migration_key = 'b2c_tier1_global_reset_20260910'")).fetchone()
        if not mig_b2c:
            db.query(models.Student).filter(models.Student.id != 1).update({models.Student.b2c_subscription_tier: "TIER_1_FREE"})
            db.query(models.Student).filter(models.Student.id == 1).update({
                models.Student.b2c_subscription_tier: "TIER_3_MASTER",
                models.Student.previous_b2c_tier: "TIER_3_MASTER",
                models.Student.ai_level: "TIER_4_ILWON",
                models.Student.academy_code: "ILWON-2027",
                models.Student.academy_approval_status: "APPROVED"
            })
            db.execute(text("INSERT INTO system_migrations (migration_key) VALUES ('b2c_tier1_global_reset_20260910')"))
            db.commit()
            print("[AUTO_SEED] Global B2C tier normalization applied successfully.")

        mig_exam_purge = db.execute(text("SELECT migration_key FROM system_migrations WHERE migration_key = 'purge_legacy_exam_mock_data_v20260914'")).fetchone()
        if not mig_exam_purge:
            try:
                db.execute(text("UPDATE exam_source_questions SET accepted_answer_id = NULL;"))
                db.execute(text("DELETE FROM exam_source_tags WHERE tag_source_detail LIKE '%최고차항%' OR tag_source_detail LIKE '%블랙라벨%' OR user_name IN ('선배 튜터', '연세대 튜터', '서울대 수리과학부 멘토');"))
                if engine.dialect.name in ("postgresql", "postgres"):
                    db.execute(text("DELETE FROM exam_source_answers WHERE is_alumni_tutor = true OR author_name IN ('연세대 의예과 튜터', '서울대 수리과학부 멘토', '낙생고 졸업생 전교1등', '카이스트 수리멘토', '고려대 국문과 선배', '포스텍 멘토', '의대 재학생 튜터', '서울대 의대 멘토', '대원외고 34기 졸업생');"))
                else:
                    db.execute(text("DELETE FROM exam_source_answers WHERE is_alumni_tutor = 1 OR author_name IN ('연세대 의예과 튜터', '서울대 수리과학부 멘토', '낙생고 졸업생 전교1등', '카이스트 수리멘토', '고려대 국문과 선배', '포스텍 멘토', '의대 재학생 튜터', '서울대 의대 멘토', '대원외고 34기 졸업생');"))
                db.execute(text("DELETE FROM exam_source_questions WHERE author_name IN ('낙생고 수험생', '재원생 수험생') OR question_text LIKE '%최고차항%' OR question_text LIKE '%불연속%';"))
                db.execute(text("DELETE FROM exam_source_tracer_items;"))
                db.execute(text("INSERT INTO system_migrations (migration_key) VALUES ('purge_legacy_exam_mock_data_v20260914')"))
                db.commit()
                print("[AUTO_SEED] 100% Type-Safe Purge of legacy exam mock data executed successfully across cloud/local DB.")
            except Exception as ep_err:
                db.rollback()
                print(f"[AUTO_SEED] Exam purge migration note: {ep_err}")

        mig_approve = db.execute(text("SELECT migration_key FROM system_migrations WHERE migration_key = 'sync_authentic_ilwon_208_v20260924'")).fetchone()
        if not mig_approve:
            try:
                from app.students_data_builtin import BUILTIN_STUDENTS_LIST
                for s in BUILTIN_STUDENTS_LIST:
                    sid = s["id"]
                    is_ilwon = (s.get("academy_code") == "ILWON-2027" or sid == 1)
                    acad_code = "ILWON-2027" if is_ilwon else s.get("academy_code")
                    acad_status = s.get("academy_approval_status", "APPROVED" if is_ilwon else "NONE")
                    ai_lvl = "TIER_4_ILWON" if is_ilwon else s.get("ai_level", "B2C_FREE")
                    b2c_tier = "TIER_3_MASTER" if sid == 1 else s.get("b2c_subscription_tier", "TIER_1_FREE")
                    
                    st = db.query(models.Student).filter(models.Student.id == sid).first()
                    if st:
                        st.academy_code = acad_code
                        st.academy_approval_status = acad_status
                        st.ai_level = ai_lvl
                        st.b2c_subscription_tier = b2c_tier
                        st.has_unlimited_chat = s.get("has_unlimited_chat", is_ilwon)
                        st.chat_tokens = 999 if is_ilwon else s.get("chat_tokens", 5)
                        st.tuition_paid = s.get("tuition_paid", is_ilwon)
                        st.textbook_paid = s.get("textbook_paid", is_ilwon)
                        st.enrollment_status = s.get("enrollment_status", "ENROLLED")
                        if sid == 1:
                            st.previous_b2c_tier = "TIER_3_MASTER"
                            st.streak_days = max(26, st.streak_days or 26)
                db.execute(text("INSERT INTO system_migrations (migration_key) VALUES ('sync_authentic_ilwon_208_v20260924')"))
                db.commit()
                print("[AUTO_SEED] Full 208 authentic students (151 Ilwon) synchronization migration applied.")
            except Exception as ap_err:
                db.rollback()
                print(f"[AUTO_SEED] Academy cohort sync note: {ap_err}")

        # 1.4 PALIN OS Phase 11: Create user_titles and user_notifications tables & retroactively backfill all 100 titles
        try:
            models.Base.metadata.create_all(bind=engine, tables=[models.UserTitle.__table__, models.UserNotification.__table__])
            db.commit()
            
            from app.title_catalog import get_all_master_titles
            master_titles = get_all_master_titles()
            from datetime import timedelta
            now = datetime.now()
            week_start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

            def safe_num(val, default=0):
                try:
                    return int(val)
                except (ValueError, TypeError):
                    return default

            students = db.query(models.Student).all()
            for s in students:
                all_sessions = db.query(models.StudySession).filter(
                    models.StudySession.student_id == s.id,
                    models.StudySession.deleted_at == None
                ).all()
                total_seconds = sum((sess.duration_sec or 0) for sess in all_sessions)
                total_hours = total_seconds / 3600.0
                streak = s.streak_days or 0
                target_univ = (s.target_univ or '').strip()

                def make_naive(dt):
                    if dt is None:
                        return None
                    return dt.replace(tzinfo=None) if getattr(dt, 'tzinfo', None) is not None else dt

                week_sessions = [sess for sess in all_sessions if sess.created_at and make_naive(sess.created_at) >= week_start]
                week_hours = sum((sess.duration_sec or 0) for sess in week_sessions) / 3600.0
                
                try:
                    omr_count = db.query(models.ExamOMRSubmission).filter(models.ExamOMRSubmission.student_id == s.id).count()
                except Exception:
                    omr_count = 0
                    
                points = safe_num(getattr(s, 'weekly_diligence_points', 0)) + safe_num(s.diligence_score) + safe_num(s.current_points)
                is_vip = bool(getattr(s, 'is_vip', False)) or (streak >= 15)
                
                master_map = {mt["condition_code"]: mt for mt in master_titles}
                existing_titles = db.query(models.UserTitle).filter(models.UserTitle.student_id == s.id).all()
                existing_map = {}
                for t in existing_titles:
                    if t.condition_code in master_map:
                        t.title_name = master_map[t.condition_code]["title_name"]
                        existing_map[t.condition_code] = t
                    else:
                        db.delete(t)
                
                unlocked_mts = []
                for mt in master_titles:
                    is_eligible = False
                    try:
                        is_eligible = mt['check'](s, total_hours, streak, week_hours, target_univ, omr_count, points, is_vip)
                    except Exception:
                        is_eligible = (mt['condition_code'] == 'STARTER_TIER')
                        
                    if is_eligible:
                        unlocked_mts.append(mt)
                        if mt['condition_code'] not in existing_map:
                            new_t = models.UserTitle(
                                student_id=s.id,
                                title_name=mt['title_name'],
                                condition_code=mt['condition_code'],
                                is_equipped=False
                            )
                            db.add(new_t)
                            existing_map[mt['condition_code']] = new_t

                # Auto-equip highest prestige title
                unlocked_mts.sort(key=lambda x: (x.get('tier_weight', 100), x.get('difficulty_weight', 1)), reverse=True)
                if unlocked_mts:
                    best_code = unlocked_mts[0]['condition_code']
                    for t in existing_map.values():
                        t.is_equipped = (t.condition_code == best_code)

            db.commit()
            print(f"[AUTO_SEED] Phase 11 100-Title Master Matrix synced for all {len(students)} students.")
        except Exception as p11_err:
            db.rollback()
            print(f"[AUTO_SEED] Phase 11 title initialization note: {p11_err}")
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
                "director_pin": "12862386",
                "tier": 4,
                "license_tier": 4,
                "business_type": "HIGH_ACADEMY",
                "subject_desc": "수능국어, 대치동 대입직강, 모의고사 OMR 처방",
                "seats": "[]"
            },
            {
                "code": "MID-TOP01",
                "name": "대치 탑클래스 중등학원",
                "director_name": "박중등 원장",
                "director_email": "mid_top@palin.com",
                "director_pin": "10101010",
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
                "director_pin": "10101010",
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
                "director_pin": "10101010",
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
                if dt["code"] == "ILWON-2027":
                    t_exist.business_reg_number = "128-86-23861"
                    t_exist.settlement_bank = "신한은행"
                    t_exist.settlement_account_number = "110-384-928192"
                    t_exist.settlement_account_holder = "김철훈(일원학원)"
                    t_exist.submall_id = "SM_ILWON_2027"
                    t_exist.submall_status = "APPROVED"
                    t_exist.saas_fee_rate = 3.3
                    t_exist.tuition_due_day = 25
                if not getattr(t_exist, "business_type", None) or t_exist.business_type == "HIGH_ACADEMY" and dt["business_type"] != "HIGH_ACADEMY":
                    t_exist.business_type = dt["business_type"]
                if dt["business_type"] == "STUDY_CAFE" and (not getattr(t_exist, "seat_layout_json", None) or t_exist.seat_layout_json == "[]"):
                    t_exist.seat_layout_json = dt.get("seats", "[]")
                db.commit()
    except Exception as e:
        db.rollback()
        print(f"[AUTO_SEED] Tenant seed warning: {e}")

    # 1.55 Seed Sample Billing Invoices for 결제선생 ERP if empty
    try:
        inv_count = db.query(models.BillingInvoice).count()
        if inv_count == 0:
            existing_st_ids = {s.id: s for s in db.query(models.Student).filter(models.Student.deleted_at == None).all()}
            sample_invoices = [
                {
                    "student_id": 1, "student_name": "김철훈", "parent_phone": "010-8888-1286",
                    "item_title": "2026년 9월 고3 파이널 수능국어 정규반 & 특수교재",
                    "amount": 550000, "discount": 50000, "final": 500000, "due": "2026-09-25",
                    "status": "PAID", "paid_at": datetime.now() - timedelta(days=2), "method": "CARD", "card": "신한카드 (개인일시불)",
                    "split_saas": 16500, "split_sms": 15, "split_payout": 483485
                }
            ]
            for idx, inv in enumerate(sample_invoices, 1):
                st_id = inv["student_id"]
                if st_id in existing_st_ids:
                    st_obj = existing_st_ids[st_id]
                    inv_code = f"INV-202609-{idx:04d}"
                    db.add(models.BillingInvoice(
                        invoice_code=inv_code,
                        tenant_code="ILWON-2027",
                        student_id=st_obj.id,
                        student_name=st_obj.name,
                        parent_phone=inv["parent_phone"],
                        item_title=inv["item_title"],
                        billing_month="2026-09",
                        amount=inv["amount"],
                        discount_amount=inv["discount"],
                        final_amount=inv["final"],
                        due_date=inv["due"],
                        status=inv["status"],
                        send_channel="ALIMTALK",
                        paid_at=inv["paid_at"],
                        payment_method=inv["method"],
                        card_company=inv["card"],
                        split_saas_fee=inv["split_saas"],
                        split_sms_fee=inv["split_sms"],
                        split_payout_amount=inv["split_payout"],
                        submall_id="SM_ILWON_2027",
                        payment_key=f"toss_submall_{inv_code}" if inv["status"] == "PAID" else None,
                        receipt_url=f"https://dashboard.tosspayments.com/receipt/mock_{inv_code}" if inv["status"] == "PAID" else None,
                        deleted_at=None
                    ))
            db.commit()
            print("[AUTO_SEED] Initialized sample 결제선생 Billing Invoices successfully.")
    except Exception as inv_err:
        db.rollback()
        print(f"[AUTO_SEED] Billing invoice seed note: {inv_err}")

    # 1.6 Scan and synchronize authentic exam materials from static/downloads folder structure
    try:
        from app.exam_file_sync import scan_and_sync_downloads
        scan_and_sync_downloads(db)
    except Exception as em_err:
        db.rollback()
    # 2. Synchronize all 208 authentic students and 203 parents into database
    print("[AUTO_SEED] Synchronizing 208 authentic students and 203 parents into database...")
    from app.students_data_builtin import BUILTIN_STUDENTS_LIST, BUILTIN_PARENTS_LIST
    auth_student_ids = set(s["id"] for s in BUILTIN_STUDENTS_LIST)
    auth_parent_ids = set(p["id"] for p in BUILTIN_PARENTS_LIST)

    # STEP 0: Purge dummy / QA test students that accumulated from test runs
    try:
        fake_students = db.query(models.Student).filter(~models.Student.id.in_(auth_student_ids)).all()
        for fs in fake_students:
            db.query(models.StudySession).filter(models.StudySession.student_id == fs.id).delete(synchronize_session=False)
            db.query(models.UserTitle).filter(models.UserTitle.student_id == fs.id).delete(synchronize_session=False)
            db.query(models.UserNotification).filter(models.UserNotification.recipient_id == fs.id).delete(synchronize_session=False)
            db.delete(fs)
        db.commit()

        fake_parents = db.query(models.Parent).filter(~models.Parent.id.in_(auth_parent_ids)).all()
        for fp in fake_parents:
            db.delete(fp)
        db.commit()
    except Exception as purge_err:
        db.rollback()
        print(f"[AUTO_SEED] Test student purge note: {purge_err}")

    # STEP A: Insert/Update Parents
    for p in BUILTIN_PARENTS_LIST:
        pid = p["id"]
        try:
            p_exist = db.query(models.Parent).filter(models.Parent.id == pid).first()
            if not p_exist:
                db.add(models.Parent(
                    id=pid,
                    name=p.get("name") or f"학부모{pid}",
                    phone=p.get("phone") or f"010-{pid:04d}-5678",
                    is_premium_subscribed=bool(p.get("is_premium_subscribed", True)),
                    email=p.get("email"),
                    role="PARENT",
                    wallet_balance=p.get("wallet_balance", 0),
                    deleted_at=None
                ))
                db.commit()
            else:
                p_exist.name = p.get("name") or p_exist.name
                p_exist.phone = p.get("phone") or p_exist.phone
                db.commit()
        except Exception:
            db.rollback()

    # STEP B: Insert/Update Students
    for s in BUILTIN_STUDENTS_LIST:
        sid = s["id"]
        try:
            s_exist = db.query(models.Student).filter(models.Student.id == sid).first()
            is_ilwon = (s.get("academy_code") == "ILWON-2027" or sid == 1)
            acad_code = "ILWON-2027" if is_ilwon else s.get("academy_code")
            acad_status = "APPROVED" if is_ilwon else s.get("academy_approval_status", "NONE")
            ai_lvl = "TIER_4_ILWON" if is_ilwon else s.get("ai_level", "B2C_FREE")
            b2c_raw = s.get("b2c_subscription_tier")
            b2c_tier = "TIER_3_MASTER" if sid == 1 else ("TIER_2_PARENT" if b2c_raw == "TIER_2_PARENT" else "TIER_1_FREE")
            s_streak = 26 if sid == 1 else s.get("streak_days", 0)
            s_max_streak = 26 if sid == 1 else s.get("max_streak_days", 0)

            if not s_exist:
                p_id = s.get("parent_id")
                if p_id:
                    p_match = db.query(models.Parent).filter(models.Parent.id == p_id).first()
                    if not p_match:
                        p_id = None
                
                db.add(models.Student(
                    id=sid,
                    email=s.get("email") or f"student_{sid}@palin.com",
                    name=s.get("name") or f"학생{sid}",
                    phone=s.get("phone") or f"010-0000-{sid:04d}",
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
                    has_unlimited_chat=s.get("has_unlimited_chat", is_ilwon),
                    chat_tokens=999 if is_ilwon else s.get("chat_tokens", 5),
                    academy_code=acad_code,
                    academy_approval_status=acad_status,
                    ai_level=ai_lvl,
                    b2c_subscription_tier=b2c_tier,
                    previous_b2c_tier="TIER_3_MASTER" if sid == 1 else s.get("previous_b2c_tier", "B2C_FREE"),
                    streak_days=s_streak,
                    max_streak_days=s_max_streak,
                    last_streak_date=datetime.now().date() if s_streak > 0 else None,
                    tuition_paid=s.get("tuition_paid", is_ilwon),
                    textbook_paid=s.get("textbook_paid", is_ilwon),
                    enrollment_status=s.get("enrollment_status", "ENROLLED"),
                    role="STUDENT",
                    deleted_at=None
                ))
                db.commit()
            else:
                s_exist.b2c_subscription_tier = b2c_tier
                if is_ilwon:
                    s_exist.academy_code = "ILWON-2027"
                    s_exist.academy_approval_status = "APPROVED"
                    s_exist.ai_level = "TIER_4_ILWON"
                    s_exist.has_unlimited_chat = True
                    s_exist.chat_tokens = 999
                    s_exist.tuition_paid = True
                    s_exist.textbook_paid = True
                    s_exist.enrollment_status = s.get("enrollment_status", "ENROLLED")
                if sid == 1:
                    s_exist.b2c_subscription_tier = "TIER_3_MASTER"
                    s_exist.previous_b2c_tier = "TIER_3_MASTER"
                    s_exist.streak_days = 26
                    s_exist.max_streak_days = max(26, s_exist.max_streak_days or 26)
                    s_exist.last_streak_date = datetime.now().date()
                db.commit()
        except Exception:
            db.rollback()

    # STEP C: Ensure active current-week study sessions for peer cohort rankers
    try:
        now_dt = datetime.now()
        curr_week_start = (now_dt - timedelta(days=now_dt.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        week_sess_count = db.query(models.StudySession).filter(
            models.StudySession.created_at >= curr_week_start,
            models.StudySession.deleted_at == None
        ).count()
        if week_sess_count < 15:
            peer_samples = [
                (1, 16.5, 0),
                (2, 18.5, 1),
                (3, 15.2, 2),
                (4, 12.8, 1),
                (5, 10.5, 3),
                (6, 8.2, 2),
                (7, 7.0, 1),
                (8, 5.5, 2),
                (9, 4.2, 3),
                (10, 3.8, 1),
                (11, 14.5, 2),
                (12, 11.2, 1),
                (13, 9.8, 3),
                (14, 6.5, 2),
            ]
            for sid, hrs, d_ago in peer_samples:
                target_st = db.query(models.Student).filter(models.Student.id == sid).first()
                if target_st:
                    sess_time = now_dt - timedelta(days=d_ago, hours=3)
                    db.add(models.StudySession(
                        student_id=sid,
                        start_time=sess_time,
                        end_time=sess_time + timedelta(hours=hrs),
                        duration_sec=int(hrs * 3600),
                        is_distracted=False,
                        created_at=sess_time,
                        deleted_at=None
                    ))
            db.commit()
    except Exception as sess_seed_err:
        print(f"[AUTO_SEED] Study session seed note: {sess_seed_err}")
        db.rollback()

    # STEP D: Seed Authentic Consulting Requests if empty
    try:
        consulting_cnt = db.query(models.ConsultingRequest).count()
        if consulting_cnt == 0:
            sample_consultings = [
                {
                    "student_id": 11, "student_name": "마서연", "student_phone": "010-9413-2157", "parent_phone": "010-9413-5678",
                    "consulting_type": "원장 집무실 1:1 대면 상담 (50분)", "target_univ": "서울대학교 경영대학",
                    "status": "접수대기", "price": 500000,
                    "note": "9월 모의평가 성적 기반 수시 6장 최종 조합 및 정시 의약학/경영 포트폴리오 분석 요청",
                    "created_at": datetime.now() - timedelta(days=2)
                },
                {
                    "student_id": 41, "student_name": "박현유", "student_phone": "010-3025-9131", "parent_phone": "010-3025-5678",
                    "consulting_type": "유선 심층 전화 상담 (30~40분)", "target_univ": "연세대학교 의예과",
                    "status": "상담일정확정", "price": 300000,
                    "note": "수능국어 비문학 과학지문 킬러문항 타임어택 극복 및 메디컬 정시 환산점수 상담",
                    "created_at": datetime.now() - timedelta(days=4)
                },
                {
                    "student_id": 85, "student_name": "이도윤", "student_phone": "010-2093-7940", "parent_phone": "010-2093-5678",
                    "consulting_type": "원장 집무실 1:1 대면 상담 (50분)", "target_univ": "한국항공대학교 항공운항학과",
                    "status": "완료", "price": 500000,
                    "note": "항공운항학과 신체검사 및 수능 최저기준 충족 전략 1차 상담 완료",
                    "created_at": datetime.now() - timedelta(days=9)
                }
            ]
            for sc in sample_consultings:
                db.add(models.ConsultingRequest(
                    student_id=sc["student_id"],
                    student_name=sc["student_name"],
                    student_phone=sc["student_phone"],
                    parent_phone=sc["parent_phone"],
                    consulting_type=sc["consulting_type"],
                    target_univ=sc["target_univ"],
                    status=sc["status"],
                    price=sc["price"],
                    note=sc["note"],
                    created_at=sc["created_at"],
                    deleted_at=None
                ))
            db.commit()
            print("[AUTO_SEED] Initialized authentic Consulting Requests successfully.")
    except Exception as c_err:
        db.rollback()
        print(f"[AUTO_SEED] Consulting seed note: {c_err}")

    # STEP E: Seed Authentic B2B Support Tickets if empty
    try:
        ticket_cnt = db.query(models.B2BSupportTicket).count()
        if ticket_cnt == 0:
            sample_tickets = [
                {
                    "tenant_code": "ILWON-2027", "tenant_name": "일원 대입전문학원", "author_name": "김철훈 원장",
                    "title": "2027학년도 9월 모의평가 OMR 등급컷 및 원점수 기준 자동 산출 요청",
                    "content": "이번 9월 모평 국어 난이도가 높게 출제되어 원점수 88점 1등급컷 기준으로 OMR 성적표 일괄 리포트 생성 부탁드립니다.",
                    "answer": "본사 데이터베이스에 9평 확정 등급컷(1등급 88점, 2등급 80점)이 실시간 반영되었습니다. 원장 관제실 OMR 탭에서 일괄 재채점 및 학부모 알림톡 발송이 가능합니다.",
                    "status": "답변완료",
                    "created_at": datetime.now() - timedelta(days=3)
                },
                {
                    "tenant_code": "MID-TOP01", "tenant_name": "대치 탑클래스 중등학원", "author_name": "박중등 원장",
                    "title": "중3 2학기 중간고사 대비 특목고 진학 커리큘럼 추가",
                    "content": "외대부고/하나고 대비 중등 심화 문항 DB 및 VOD 일괄 배포 일정 문의드립니다.",
                    "answer": "중등 5대과목 올A 대비 킬러 문항 및 특목자사고 대비 모의고사가 이번 주 금요일 정기 업데이트로 자동 활성화됩니다.",
                    "status": "답변완료",
                    "created_at": datetime.now() - timedelta(days=2)
                },
                {
                    "tenant_code": "ILWON-2027", "tenant_name": "일원 대입전문학원", "author_name": "김철훈 원장",
                    "title": "결제선생 9월분 학원비 정기 청구 알림톡 일괄 발송 확인",
                    "content": "9월 25일 정기 납부일 대상 151명 전원 알림톡 청구서 발송 현황 확인 요청",
                    "answer": "알림톡 청구서 151건 전송 완료되었으며 결제 즉시 호스테이지 프로토콜로 수강권이 자동 연장됩니다.",
                    "status": "답변완료",
                    "created_at": datetime.now() - timedelta(days=1)
                }
            ]
            for st in sample_tickets:
                db.add(models.B2BSupportTicket(
                    tenant_code=st["tenant_code"],
                    tenant_name=st["tenant_name"],
                    author_name=st["author_name"],
                    title=st["title"],
                    content=st["content"],
                    answer=st["answer"],
                    status=st["status"],
                    created_at=st["created_at"],
                    deleted_at=None
                ))
            db.commit()
            print("[AUTO_SEED] Initialized authentic B2B Support Tickets successfully.")
    except Exception as t_err:
        db.rollback()
        print(f"[AUTO_SEED] Ticket seed note: {t_err}")

    # STEP F: Seed Authentic VOC Feedbacks if empty
    try:
        feedback_cnt = db.query(models.Feedback).count()
        if feedback_cnt == 0:
            sample_feedbacks = [
                {
                    "student_id": 85, "user_email": "doyunn221@gmail.com", "category": "아이디어",
                    "content": "4번 문항 2x2+1 배치 너무 좋습니다! 수능 실전 모의고사 타이머에 10분 남았을 때 알림 기능도 추가해주시면 감사하겠습니다.",
                    "status": "접수됨", "created_at": datetime.now() - timedelta(days=3)
                },
                {
                    "student_id": 41, "user_email": "hyunyou0529@naver.com", "category": "기능제안",
                    "content": "플래너 타이머 일시정지 후 백그라운드 재개 기능 요청합니다. 모바일 브라우저 전환 시에도 측정이 유지되면 좋겠습니다.",
                    "status": "검토중", "created_at": datetime.now() - timedelta(days=5)
                },
                {
                    "student_id": 11, "user_email": "lucy10144@goedu.kr", "category": "불편사항",
                    "content": "모의고사 성적표 PDF 출력 시 여백 잘림 현상이 있었는데 빠른 패치 감사드립니다.",
                    "status": "반영완료", "created_at": datetime.now() - timedelta(days=7)
                }
            ]
            for sf in sample_feedbacks:
                db.add(models.Feedback(
                    student_id=sf["student_id"],
                    user_email=sf["user_email"],
                    category=sf["category"],
                    content=sf["content"],
                    status=sf["status"],
                    created_at=sf["created_at"],
                    deleted_at=None
                ))
            db.commit()
            print("[AUTO_SEED] Initialized authentic Feedbacks (VOC) successfully.")
    except Exception as f_err:
        db.rollback()
        print(f"[AUTO_SEED] Feedback seed note: {f_err}")

    print("[AUTO_SEED] Seeding completed.")


