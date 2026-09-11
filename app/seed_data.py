# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import random
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
            sample_invoices = [
                {
                    "student_id": 1, "student_name": "김철훈", "parent_phone": "010-8888-1286",
                    "item_title": "2026년 9월 고3 파이널 수능국어 정규반 & 특수교재",
                    "amount": 550000, "discount": 50000, "final": 500000, "due": "2026-09-25",
                    "status": "PAID", "paid_at": datetime.now() - timedelta(days=2), "method": "CARD", "card": "신한카드 (개인일시불)",
                    "split_saas": 16500, "split_sms": 15, "split_payout": 483485
                },
                {
                    "student_id": 2, "student_name": "이수아", "parent_phone": "010-2345-6789",
                    "item_title": "2026년 9월 고3 메디컬 심화반 수강료",
                    "amount": 480000, "discount": 0, "final": 480000, "due": "2026-09-25",
                    "status": "PAID", "paid_at": datetime.now() - timedelta(days=3), "method": "EASY_PAY", "card": "카카오페이 (머니)",
                    "split_saas": 15840, "split_sms": 15, "split_payout": 464145
                },
                {
                    "student_id": 3, "student_name": "박민준", "parent_phone": "010-3456-7890",
                    "item_title": "2026년 9월 수능국어 킬러문항 집중반",
                    "amount": 450000, "discount": 0, "final": 450000, "due": "2026-09-25",
                    "status": "PAID", "paid_at": datetime.now() - timedelta(days=1), "method": "CARD", "card": "현대카드 (M포인트)",
                    "split_saas": 14850, "split_sms": 15, "split_payout": 435135
                },
                {
                    "student_id": 4, "student_name": "정다은", "parent_phone": "010-4567-8901",
                    "item_title": "2026년 9월 고3 실전 모의고사 파이널반",
                    "amount": 520000, "discount": 20000, "final": 500000, "due": "2026-09-25",
                    "status": "SENT", "paid_at": None, "method": None, "card": None,
                    "split_saas": 16500, "split_sms": 15, "split_payout": 483485
                },
                {
                    "student_id": 5, "student_name": "강태우", "parent_phone": "010-5678-9012",
                    "item_title": "2026년 9월 고3 국어 정규반 수강료",
                    "amount": 450000, "discount": 0, "final": 450000, "due": "2026-09-25",
                    "status": "SENT", "paid_at": None, "method": None, "card": None,
                    "split_saas": 14850, "split_sms": 15, "split_payout": 435135
                },
                {
                    "student_id": 6, "student_name": "최서윤", "parent_phone": "010-6789-0123",
                    "item_title": "2026년 8월분 수강료 및 특별교재비 (연체)",
                    "amount": 450000, "discount": 0, "final": 450000, "due": "2026-08-25",
                    "status": "OVERDUE", "paid_at": None, "method": None, "card": None,
                    "split_saas": 14850, "split_sms": 15, "split_payout": 435135
                }
            ]
            for idx, inv in enumerate(sample_invoices, 1):
                inv_code = f"INV-202609-{idx:04d}"
                db.add(models.BillingInvoice(
                    invoice_code=inv_code,
                    tenant_code="ILWON-2027",
                    student_id=inv["student_id"],
                    student_name=inv["student_name"],
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

    # STEP D: Seed Authentic Crowdsourced Exam Source Questions & Accepted Answers
    try:
        if db.query(models.ExamSourceQuestion).count() == 0:
            sample_qa = [
                {
                    "school": "낙생고등학교", "grade": 2, "subject": "수학", "exam": "1학기 기말", "q_num": "19번",
                    "text": "최고차항 계수가 음수인 삼차함수 f(x)와 실수 t에 대하여 g(t)가 불연속이 되는 점의 개수를 구하는 킬러 문항 출처가 어디인가요?",
                    "bounty": 500, "resolved": True,
                    "ans_author": "연세대 의예과 튜터", "is_tutor": True,
                    "book": "블랙라벨", "detail": "수학II p.42 8번 최고난도 문항 변형",
                    "notes": "원문항의 최고차항 계수 1을 -2로 바꾸고, (나) 조건을 역함수 미분가능성 조건으로 비틀어 출제함"
                },
                {
                    "school": "낙생고등학교", "grade": 1, "subject": "수학", "exam": "1학기 중간", "q_num": "17번",
                    "text": "원 x^2 + y^2 + 2x - 8y + 8 = 0 위의 점 P와 직선 3x - 4y - 5 = 0 사이의 거리의 최댓값/최솟값 곱을 구하는 문제 출처 알려주세요!",
                    "bounty": 500, "resolved": True,
                    "ans_author": "서울대 수리과학부 멘토", "is_tutor": True,
                    "book": "평가원/교육청 기출", "detail": "2023년 6월 고1 학평 21번 킬러 변형",
                    "notes": "중심 좌표를 (2,3)에서 (-1,4)로 평행이동하고 반지름을 미지수 r로 변형하여 선지 계산량을 2배 늘림"
                },
                {
                    "school": "낙생고등학교", "grade": 2, "subject": "수학", "exam": "2학기 중간", "q_num": "20번",
                    "text": "정적분으로 정의된 함수 F(x) = ∫_{x}^{x+1} (t^3 - 3t) dt 의 극값과 접선 교점 방정식 문항 출처 제보 부탁드립니다.",
                    "bounty": 500, "resolved": True,
                    "ans_author": "낙생고 졸업생 전교1등", "is_tutor": True,
                    "book": "평가원/교육청 기출", "detail": "2022년 고3 10월 교육청 22번 킬러 변형",
                    "notes": "피적분함수 적분 구간을 [0, x]에서 [x, x+1]로 변형하여 도함수 부호 판정을 복합적으로 비틈"
                },
                {
                    "school": "낙생고등학교", "grade": 1, "subject": "수학", "exam": "1학기 중간", "q_num": "14번",
                    "text": "모든 실수 x에 대하여 이차부등식 (k-1)x^2 + 2(k-1)x + 3 > 0 이 항상 성립하도록 하는 정수 k의 개수 문제",
                    "bounty": 500, "resolved": True,
                    "ans_author": "카이스트 수리멘토", "is_tutor": True,
                    "book": "일품", "detail": "고등수학(상) 1단원 최고수준 4번 문항",
                    "notes": "k=1일 때 최고차항이 0이 되는 함정 조건을 일품 원문항 그대로 출제함"
                },
                {
                    "school": "낙생고등학교", "grade": 2, "subject": "국어", "exam": "1학기 중간", "q_num": "22번",
                    "text": "독서 비문학 외부지문 [헤겔의 미학 이론과 절대정신의 변증법적 전개] 관련 3점 킬러 <보기> 적용 문제 출처 어디인가요?",
                    "bounty": 500, "resolved": True,
                    "ans_author": "고려대 국문과 선배", "is_tutor": True,
                    "book": "EBS 수능특강", "detail": "EBS 수능특강 독서 인문·예술 03강(헤겔 미학)",
                    "notes": "EBS 원문 지문에 2024 9월 모평 인문 제재 선지 패턴을 융합하여 서술형 3번으로 출제함"
                },
                {
                    "school": "분당대진고등학교", "grade": 2, "subject": "통합과학", "exam": "1학기 중간", "q_num": "18번",
                    "text": "물리학I 역학적 에너지 보존 법칙에서 마찰이 있는 빗면 구간을 통과할 때의 속력 비 문제",
                    "bounty": 500, "resolved": True,
                    "ans_author": "포스텍 멘토", "is_tutor": True,
                    "book": "평가원/교육청 기출", "detail": "2023 수능 물리학I 20번 킬러 변형",
                    "notes": "용수철 상수를 k에서 2k로 변경하고 마찰구간 길이를 d에서 2d로 변형함"
                },
                {
                    "school": "분당대진고등학교", "grade": 1, "subject": "수학", "exam": "1학기 기말", "q_num": "16번",
                    "text": "함수 y = f(x) 와 역함수 y = f^{-1}(x) 의 교점 사이의 거리가 최소가 되도록 하는 상수 m의 값 구하기",
                    "bounty": 500, "resolved": True,
                    "ans_author": "의대 재학생 튜터", "is_tutor": True,
                    "book": "쎈", "detail": "쎈 고등수학(하) C단계 84p 541번",
                    "notes": "쎈 C단계 발문에 2021년 9월 학평 19번 그래프 개형을 합성하여 출제함"
                },
                {
                    "school": "휘문고등학교", "grade": 2, "subject": "수학", "exam": "1학기 기말", "q_num": "21번",
                    "text": "미적분 f(x) = (x^2 - a)e^{-x} 의 변곡점 접선과 x축 사이의 둘러싸인 넓이 킬러 문항",
                    "bounty": 500, "resolved": True,
                    "ans_author": "서울대 의대 멘토", "is_tutor": True,
                    "book": "블랙라벨", "detail": "블랙라벨 미적분 64p Step 3 5번",
                    "notes": "블랙라벨 Step 3 최고난도 문항과 2024 6월 모평 28번을 융합하여 서술형 배점 10점으로 출제함"
                },
                {
                    "school": "대원외국어고등학교", "grade": 1, "subject": "영어", "exam": "1학기 중간", "q_num": "25번",
                    "text": "심화영어 외부 빈칸추론 [인공지능 윤리와 알고리즘 편향성] 지문 출처가 어디인가요?",
                    "bounty": 500, "resolved": True,
                    "ans_author": "대원외고 34기 졸업생", "is_tutor": True,
                    "book": "기타 학술/사설", "detail": "The Economist 2024년 2월호 테크 특집 사설",
                    "notes": "Economist 원문 3개 단락을 발췌하여 빈칸 2개를 뚫고 어휘를 고급 수능 어휘로 패러프레이징함"
                }
            ]

            for item in sample_qa:
                q = models.ExamSourceQuestion(
                    school_name=item["school"],
                    grade=item["grade"],
                    subject=item["subject"],
                    exam_type=item["exam"],
                    question_num=item["q_num"],
                    question_text=item["text"],
                    bounty_points=item["bounty"],
                    is_resolved=item["resolved"],
                    author_name="낙생고 수험생" if "낙생" in item["school"] else "재원생 수험생"
                )
                db.add(q)
                db.commit()
                db.refresh(q)

                ans = models.ExamSourceAnswer(
                    question_id=q.id,
                    author_name=item["ans_author"],
                    is_alumni_tutor=item["is_tutor"],
                    source_book_name=item["book"],
                    source_detail=item["detail"],
                    adaptation_notes=item["notes"],
                    is_accepted=True
                )
                db.add(ans)
                db.commit()
                db.refresh(ans)

                q.accepted_answer_id = ans.id
                db.commit()

            print(f"[AUTO_SEED] Seeded {len(sample_qa)} authentic crowdsourced exam source Q&A and accepted answers.")
    except Exception as q_err:
        db.rollback()
        print(f"[AUTO_SEED] Exam source QA seed warning: {q_err}")

    print("[AUTO_SEED] Seeding completed.")
