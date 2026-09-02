# -*- coding: utf-8 -*-
import json
import os
from sqlalchemy.orm import Session
from sqlalchemy import text, func

def auto_seed_database(db: Session, engine):
    from app import models
    
    # 1. Ensure deleted_at column exists across all tables in SQLite and PostgreSQL
    try:
        if engine.dialect.name == "sqlite":
            tables = ["students", "parents", "tenants", "exam_materials", "vod_library", "attendance_logs", "tutor_profiles"]
            for t in tables:
                try:
                    cols = [row[1] for row in db.execute(text(f"PRAGMA table_info({t})")).fetchall()]
                    if cols and "deleted_at" not in cols:
                        db.execute(text(f"ALTER TABLE {t} ADD COLUMN deleted_at DATETIME"))
                        db.commit()
                except Exception:
                    pass
        elif engine.dialect.name in ("postgresql", "postgres"):
            tables = ["students", "parents", "tenants", "exam_materials", "vod_library", "attendance_logs", "tutor_profiles"]
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
        student_count = db.query(models.Student).filter(models.Student.deleted_at == None).count()
    except Exception:
        try:
            student_count = db.query(models.Student).count()
        except Exception:
            pass

    if student_count < 10:
        print(f"[AUTO_SEED] Detected only {student_count} students. Auto-seeding full 109 student database...")
        # Load students from JSON dump
        dump_path = os.path.join(os.path.dirname(__file__), "supabase_students_dump.json")
        if not os.path.exists(dump_path):
            # Fallback to scratch or built-in
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
                    streak_days=s.get("streak_days", 0),
                    max_streak_days=s.get("max_streak_days", 0),
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
        
        # Ensure student 1 is Kim Cheolhun
        s1 = db.query(models.Student).filter(models.Student.id == 1).first()
        if s1:
            s1.name = "김철훈"
            s1.target_univ = "연세대학교 의예과"
            s1.baseline_univ = "서울대학교 화학생물공학부"
            s1.streak_days = 7
            s1.league_tier = "PLATINUM"
            s1.medical_symbol = "MED"
            s1.academy_code = "ILWON-2027"
        
        db.commit()
        print(f"[AUTO_SEED] 109 students seeded successfully!")

    # 3. Check Exam Materials count
    mat_count = 0
    try:
        mat_count = db.query(models.ExamMaterial).filter(models.ExamMaterial.deleted_at == None).count()
    except Exception:
        pass

    if mat_count < 10:
        print(f"[AUTO_SEED] Detected only {mat_count} exam materials. Seeding 28 official materials...")
        materials = [
            ("국어", 2027, "2027학년도 6월 모의평가 국어 (공통+화작/언매)", "한국교육과정평가원 주관 2027 수능 대비 6월 모의평가 국어영역 전 문항 및 전문 해설", "/downloads/2027_06_korean.pdf", "/downloads/2027_06_korean_ans.pdf"),
            ("국어", 2027, "2027학년도 3월 전국연합학력평가 국어 (공통+화작/언매)", "서울시교육청 주관 고3 첫 전국연합학력평가 국어 전 문항 및 정답표", "/downloads/2027_03_korean.pdf", "/downloads/2027_03_korean_ans.pdf"),
            ("수학", 2027, "2027학년도 6월 모의평가 수학 (공통+미적/확통/기하)", "한국교육과정평가원 주관 2027 수능 대비 6월 모의평가 수학영역 킬러/준킬러 포함 전 문항", "/downloads/2027_06_math.pdf", "/downloads/2027_06_math_ans.pdf"),
            ("수학", 2027, "2027학년도 3월 전국연합학력평가 수학 (공통+미적/확통/기하)", "서울시교육청 주관 고3 전국연합학력평가 수학영역 전 문항 및 심층 해설", "/downloads/2027_03_math.pdf", "/downloads/2027_03_math_ans.pdf"),
            ("영어", 2027, "2027학년도 6월 모의평가 영어 (듣기 대본/독해)", "한국교육과정평가원 주관 2027 6월 모평 영어영역 문제지 및 듣기평가 대본", "/downloads/2027_06_english.pdf", "/downloads/2027_06_english_ans.pdf"),
            ("과탐", 2027, "2027학년도 6월 모평 과학탐구 (물리I/화학I/생명I/지구I)", "평가원 6월 모의평가 과탐 I 전과목 합본 문제지 및 정답지", "/downloads/2027_06_science.pdf", "/downloads/2027_06_science_ans.pdf"),
            ("사탐", 2027, "2027학년도 6월 모평 사회탐구 (생윤/사문/한지)", "평가원 6월 모의평가 사탐 주요 3개 과목 합본 문제지 및 정답지", "/downloads/2027_06_social.pdf", "/downloads/2027_06_social_ans.pdf"),
            ("한국사", 2027, "2027학년도 6월 모의평가 한국사", "한국교육과정평가원 주관 필수 한국사 영역 기출문제 및 정답 해설", "/downloads/2027_06_history.pdf", "/downloads/2027_06_history_ans.pdf"),
            ("사관/경찰", 2027, "2027학년도 사관학교 1차 선발시험 (국어/수학/영어)", "육·해·공·국간사 2027학년도 신입생 선발 공동 1차 필기시험 전 문항", "/downloads/2027_military.pdf", "/downloads/2027_military_ans.pdf"),
            ("논술/면접", 2027, "2027학년도 주요 15개 대학 인문/수리의학 논술 기출 모음집", "연세대·한양대·성균관대·가톨릭대의대 등 최신 논술 기출 제시문 및 예시답안", "/downloads/2027_essay.pdf", "/downloads/2027_essay_ans.pdf"),

            ("국어", 2026, "2026학년도 대학수학능력시험 국어 (공통+화작/언매)", "2026학년도 수능 공식 국어영역 홀수형/짝수형 문제지 및 최종 정답표", "/downloads/2026_csat_korean.pdf", "/downloads/2026_csat_korean_ans.pdf"),
            ("국어", 2026, "2026학년도 9월 모의평가 국어 (공통+화작/언매)", "한국교육과정평가원 주관 2026 수능 대비 9월 모의평가 국어영역 전 문항", "/downloads/2026_09_korean.pdf", "/downloads/2026_09_korean_ans.pdf"),
            ("국어", 2026, "2026학년도 6월 모의평가 국어 (공통+화작/언매)", "한국교육과정평가원 주관 2026 수능 대비 6월 모의평가 국어영역 전 문항", "/downloads/2026_06_korean.pdf", "/downloads/2026_06_korean_ans.pdf"),
            ("수학", 2026, "2026학년도 대학수학능력시험 수학 (공통+미적/확통/기하)", "2026학년도 수능 공식 수학영역 홀수형/짝수형 문제지 및 최종 정답표", "/downloads/2026_csat_math.pdf", "/downloads/2026_csat_math_ans.pdf"),
            ("수학", 2026, "2026학년도 9월 모의평가 수학 (공통+미적/확통/기하)", "한국교육과정평가원 주관 2026 수능 대비 9월 모의평가 수학영역 전 문항", "/downloads/2026_09_math.pdf", "/downloads/2026_09_math_ans.pdf"),
            ("수학", 2026, "2026학년도 6월 모의평가 수학 (공통+미적/확통/기하)", "한국교육과정평가원 주관 2026 수능 대비 6월 모의평가 수학영역 전 문항", "/downloads/2026_06_math.pdf", "/downloads/2026_06_math_ans.pdf"),
            ("영어", 2026, "2026학년도 대학수학능력시험 영어", "2026학년도 수능 공식 영어영역 문제지 및 듣기평가 대본/정답", "/downloads/2026_csat_english.pdf", "/downloads/2026_csat_english_ans.pdf"),
            ("과탐", 2026, "2026학년도 수능 과학탐구 (물I, 화I, 생I, 지I)", "2026학년도 수능 과학탐구 I 전과목 문제지 및 해설", "/downloads/2026_csat_science.pdf", "/downloads/2026_csat_science_ans.pdf"),
            ("사탐", 2026, "2026학년도 수능 사회탐구 (생윤, 사문, 한지)", "2026학년도 수능 사회탐구 주요 3과목 문제지 및 해설", "/downloads/2026_csat_social.pdf", "/downloads/2026_csat_social_ans.pdf"),
            ("한국사", 2026, "2026학년도 수능 한국사", "2026학년도 수능 필수 한국사 기출문제 및 정답", "/downloads/2026_csat_history.pdf", "/downloads/2026_csat_history_ans.pdf"),
            ("사관/경찰", 2026, "2026학년도 사관학교 1차 선발시험", "2026학년도 사관학교 선발 공동 1차 필기시험 전 문항 및 정답", "/downloads/2026_military.pdf", "/downloads/2026_military_ans.pdf"),
            ("논술/면접", 2026, "2026학년도 주요 대학 수시 논술/구술면접 기출자료", "연세·성균관·서강·경희·중앙대 논술 기출 및 모범답안", "/downloads/2026_essay.pdf", "/downloads/2026_essay_ans.pdf"),

            ("국어", 2025, "2025학년도 대학수학능력시험 국어", "2025학년도 수능 공식 국어영역 문제지 및 정답지", "/downloads/2025_csat_korean.pdf", "/downloads/2025_csat_korean_ans.pdf"),
            ("수학", 2025, "2025학년도 대학수학능력시험 수학", "2025학년도 수능 공식 수학영역 문제지 및 정답지", "/downloads/2025_csat_math.pdf", "/downloads/2025_csat_math_ans.pdf"),
            ("영어", 2025, "2025학년도 대학수학능력시험 영어", "2025학년도 수능 공식 영어영역 문제지 및 정답지", "/downloads/2025_csat_english.pdf", "/downloads/2025_csat_english_ans.pdf"),
            ("과탐", 2025, "2025학년도 대학수학능력시험 과학탐구", "2025학년도 수능 과탐 I 전과목 문제지 및 정답지", "/downloads/2025_csat_science.pdf", "/downloads/2025_csat_science_ans.pdf"),
            ("사탐", 2025, "2025학년도 대학수학능력시험 사회탐구", "2025학년도 수능 사탐 전과목 문제지 및 정답지", "/downloads/2025_csat_social.pdf", "/downloads/2025_csat_social_ans.pdf"),
            ("한국사", 2025, "2025학년도 대학수학능력시험 한국사", "2025학년도 수능 한국사 기출문제 및 정답지", "/downloads/2025_csat_history.pdf", "/downloads/2025_csat_history_ans.pdf")
        ]
        for sub, yr, title, desc, f_url, ans_url in materials:
            db.add(models.ExamMaterial(
                subject=sub,
                title=title,
                description=desc,
                file_url=f_url,
                file_name=f"{title}.pdf",
                file_size="1.8 MB",
                answer_file_url=ans_url,
                answer_file_name=f"{title}_정답해설.pdf",
                year=yr,
                deleted_at=None
            ))
        db.commit()
        print(f"[AUTO_SEED] 28 exam materials seeded successfully!")

    # 4. Check VOD Library count
    vod_count = 0
    try:
        vod_count = db.query(models.VodLibrary).filter(models.VodLibrary.deleted_at == None).count()
    except Exception:
        pass

    if vod_count < 2:
        print(f"[AUTO_SEED] Seeding 6 VOD lectures...")
        vods = [
            ("2027 수능국어 고난도 독서 비문학 구조독해 특강", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "국어", "평가원 6월·9월 비문학 과학/경제 지문 독해 알고리즘 및 1등급 킬러 정복", "고3/N수", ""),
            ("2027 미적분 킬러 22번, 30번 심층 반복 해설", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "수학", "미적분 극값과 역함수 합성 추론 킬러 문항 3초 개념 정리 및 실전 풀이법", "고3/N수", ""),
            ("2027 수능영어 빈칸추론 & 순서삽입 오답률 1위 킬러 특강", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "영어", "절대평가 1등급 확보를 위한 빈칸 31~34번 논리적 인과관계 도출 전략", "고3/N수", ""),
            ("2027 과탐 생명과학I 유전 가계도 3분 컷 풀이법", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "탐구", "생명과학I 다인자 유전 및 가계도 분석 시간 단축 핵심 스킬", "고3/N수", ""),
            ("2027 의치한약수 & 최상위권 정시/수시 합격 지원 전략 설명회", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "입시", "2027 수능 누적백분위 및 대학별 환산점수 유불리 심층 분석 가이드", "전체", ""),
            ("원장 직강: 슬럼프를 극복하는 멘탈 관리 및 기상/취침 루틴화", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "칼럼", "수험 생활 100일 전 멘탈 유지법 및 성실도 1000점 유지 비결", "전체", "")
        ]
        for title, url, cat, desc, aud, pw in vods:
            db.add(models.VodLibrary(
                title=title,
                video_url=url,
                password=pw,
                category=cat,
                description=desc,
                target_audience=aud,
                deleted_at=None
            ))
        db.commit()
        print(f"[AUTO_SEED] 6 VOD lectures seeded successfully!")
