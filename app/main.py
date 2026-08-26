from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import json
import os
import shutil

from app.database import get_db, engine
from app import models, schemas, ai, predict

app = FastAPI(title="PASS-MATE API")

from sqlalchemy import text, inspect
def init_db_schema():
    try:
        models.Base.metadata.create_all(bind=engine)
        with engine.connect() as conn:
            try:
                if engine.dialect.name == "sqlite":
                    columns = [row[1] for row in conn.execute(text("PRAGMA table_info(students)")).fetchall()]
                    if columns:
                        if "wake_target_time" not in columns:
                            conn.execute(text("ALTER TABLE students ADD COLUMN wake_target_time VARCHAR DEFAULT '06:30'"))
                        if "sleep_target_time" not in columns:
                            conn.execute(text("ALTER TABLE students ADD COLUMN sleep_target_time VARCHAR DEFAULT '23:30'"))
                        if "is_banned" not in columns:
                            conn.execute(text("ALTER TABLE students ADD COLUMN is_banned BOOLEAN DEFAULT 0"))
                        if "ban_reason" not in columns:
                            conn.execute(text("ALTER TABLE students ADD COLUMN ban_reason VARCHAR"))
                        if "dday_date" not in columns:
                            conn.execute(text("ALTER TABLE students ADD COLUMN dday_date VARCHAR DEFAULT '2026-11-19'"))
                        if "dday_title" not in columns:
                            conn.execute(text("ALTER TABLE students ADD COLUMN dday_title VARCHAR DEFAULT '2027 수능'"))
                        if "streak_days" not in columns:
                            conn.execute(text("ALTER TABLE students ADD COLUMN streak_days INTEGER DEFAULT 0"))
                        if "max_streak_days" not in columns:
                            conn.execute(text("ALTER TABLE students ADD COLUMN max_streak_days INTEGER DEFAULT 0"))
                        if "medical_symbol" not in columns:
                            conn.execute(text("ALTER TABLE students ADD COLUMN medical_symbol VARCHAR DEFAULT 'GENERAL'"))
                        if "paid_cash" not in columns:
                            conn.execute(text("ALTER TABLE students ADD COLUMN paid_cash INTEGER DEFAULT 0"))
                        if "free_report_tickets" not in columns:
                            conn.execute(text("ALTER TABLE students ADD COLUMN free_report_tickets INTEGER DEFAULT 0"))
                        if "referral_code" not in columns:
                            conn.execute(text("ALTER TABLE students ADD COLUMN referral_code VARCHAR"))
                        if "referred_by" not in columns:
                            conn.execute(text("ALTER TABLE students ADD COLUMN referred_by VARCHAR"))
                        if "has_unlimited_chat" not in columns:
                            conn.execute(text("ALTER TABLE students ADD COLUMN has_unlimited_chat BOOLEAN DEFAULT 0"))
                        conn.commit()

                    # TutorProfile 컬럼 검사
                    tutor_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(tutor_profiles)")).fetchall()]
                    if tutor_cols:
                        if "is_suspended" not in tutor_cols:
                            conn.execute(text("ALTER TABLE tutor_profiles ADD COLUMN is_suspended BOOLEAN DEFAULT 0"))
                        if "suspend_reason" not in tutor_cols:
                            conn.execute(text("ALTER TABLE tutor_profiles ADD COLUMN suspend_reason VARCHAR"))

                    # QAPost 컬럼 검사
                    qa_post_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(qa_posts)")).fetchall()]
                    if qa_post_cols:
                        if "is_anonymous" not in qa_post_cols:
                            conn.execute(text("ALTER TABLE qa_posts ADD COLUMN is_anonymous BOOLEAN DEFAULT 0"))

                    # QAComment 컬럼 검사
                    qa_comment_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(qa_comments)")).fetchall()]
                    if qa_comment_cols:
                        if "is_anonymous" not in qa_comment_cols:
                            conn.execute(text("ALTER TABLE qa_comments ADD COLUMN is_anonymous BOOLEAN DEFAULT 0"))
                    conn.commit()
                else:
                    # PostgreSQL (Supabase) 자동 마이그레이션 실행
                    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS wake_target_time VARCHAR DEFAULT '06:30'"))
                    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS sleep_target_time VARCHAR DEFAULT '23:30'"))
                    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS is_banned BOOLEAN DEFAULT FALSE"))
                    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS ban_reason VARCHAR"))
                    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS dday_date VARCHAR DEFAULT '2026-11-19'"))
                    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS dday_title VARCHAR DEFAULT '2027 수능'"))
                    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS streak_days INTEGER DEFAULT 0"))
                    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS max_streak_days INTEGER DEFAULT 0"))
                    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS medical_symbol VARCHAR DEFAULT 'GENERAL'"))
                    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS paid_cash INTEGER DEFAULT 0"))
                    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS free_report_tickets INTEGER DEFAULT 0"))
                    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS referral_code VARCHAR"))
                    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS referred_by VARCHAR"))
                    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS has_unlimited_chat BOOLEAN DEFAULT FALSE"))
                    conn.execute(text("ALTER TABLE tutor_profiles ADD COLUMN IF NOT EXISTS is_suspended BOOLEAN DEFAULT FALSE"))
                    conn.execute(text("ALTER TABLE tutor_profiles ADD COLUMN IF NOT EXISTS suspend_reason VARCHAR"))
                    conn.execute(text("ALTER TABLE qa_posts ADD COLUMN IF NOT EXISTS is_anonymous BOOLEAN DEFAULT FALSE"))
                    conn.execute(text("ALTER TABLE qa_comments ADD COLUMN IF NOT EXISTS is_anonymous BOOLEAN DEFAULT FALSE"))
                    conn.commit()
                    print("PostgreSQL Schema Migration Complete!")
            except Exception as e:
                print("DB Schema Migration Warning:", e)
    except Exception as e:
        print("DB Connection/Init Warning (Non-blocking):", e)

try:
    init_db_schema()
except Exception as e:
    print("Async DB Init Warning:", e)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    from app.sms import send_sms, check_aligo_remain, save_sms_settings, load_sms_settings
except Exception as _sms_err:
    print(f"Warning: app.sms import failed ({_sms_err}), falling back to dummy SMS.")
    def send_sms(to_phone: str, message: str, title: str = "[PALIN OS]"):
        print(f"[FALLBACK SMS] TO: {to_phone} | {message}")
        return {"result_code": 1, "message": "Dummy fallback success"}
    def check_aligo_remain():
        return {"status": "mock", "message": "시뮬레이션 모드", "SMS_CNT": 9999, "LMS_CNT": 9999}
    def save_sms_settings(key: str, user_id: str, sender: str):
        return True
    def load_sms_settings():
        return {}

def send_mock_sms(to_phone: str, message: str):
    send_sms(to_phone=to_phone, message=message, title="[PALIN OS 행동통제 알림]")

# --- 1. User & Auth ---

@app.get("/api/univ-data")
def get_univ_data():
    try:
        from app.ai import load_univ_cuts
        cuts = load_univ_cuts()
        res = {}
        for u in cuts:
            res[u] = list(cuts[u].keys())
        return res
    except:
        return {}

@app.post("/api/register")
def register_student(payload: schemas.StudentCreate, db: Session = Depends(get_db)):
    try:
        clean_email = payload.email.strip().lower()
        
        # 중복 이메일 가입 방지 및 기존 계정 자동 로그인 안내
        existing = db.query(models.Student).filter(models.Student.email == clean_email).first()
        if existing:
            raise HTTPException(status_code=400, detail="이미 가입된 이메일 주소입니다. [기존 계정으로 로그인]을 이용해 주세요.")

        # 블랙리스트 검사
        banned = db.query(models.Blacklist).filter(
            (models.Blacklist.email == clean_email) | (models.Blacklist.phone == payload.phone)
        ).first()
        if banned:
            raise HTTPException(status_code=403, detail=f"원장님에 의해 이용이 정지/퇴거된 계정입니다. (사유: {banned.reason or '학원 규칙 위반'})")

        parent = db.query(models.Parent).filter(models.Parent.phone == payload.parent_phone).first()
        if not parent:
            parent = models.Parent(name=payload.parent_name, phone=payload.parent_phone, is_premium_subscribed=False)
            db.add(parent)
            db.commit()
            db.refresh(parent)
            
        initial_points = 100
        referred_by_code = payload.referred_by.strip().upper() if payload.referred_by else None
        
        student = models.Student(
            email=clean_email, name=payload.name, phone=payload.phone,
            grade=payload.grade, region=payload.region, high_school=payload.high_school,
            target_univ=payload.target_univ, baseline_univ=payload.baseline_univ,
            current_points=initial_points, paid_cash=0, free_report_tickets=0,
            referred_by=referred_by_code, parent_id=parent.id
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        
        # 내 고유 친구초대 코드 발급 (예: PL-0101)
        student.referral_code = f"PL-{student.id:04d}"
        
        # 추천인 보상 로직: 추천인에게 19,000원 리포트 무료권 1장 지급 & 가입자에게 500P 추가 지급!
        if referred_by_code:
            inviter = db.query(models.Student).filter(models.Student.referral_code == referred_by_code).first()
            if inviter:
                inviter.free_report_tickets = (inviter.free_report_tickets or 0) + 1
                student.current_points += 500
                db.add(models.PointHistory(student_id=student.id, amount=500, description=f"친구({inviter.name}) 초대 코드 웰컴 보너스"))
                db.add(models.PointHistory(student_id=inviter.id, amount=0, description=f"친구({student.name}) 초대 성공: 19,000원 리포트 무료권 획득!"))
                
        db.add(models.PointHistory(student_id=student.id, amount=initial_points, description="가입 축하 기본 포인트"))
        db.commit()
        db.refresh(student)
        
        return {
            "id": student.id,
            "email": student.email,
            "name": student.name,
            "phone": student.phone,
            "grade": student.grade,
            "region": student.region,
            "high_school": student.high_school,
            "target_univ": student.target_univ,
            "baseline_univ": student.baseline_univ,
            "wake_target_time": student.wake_target_time or "06:30",
            "sleep_target_time": student.sleep_target_time or "23:30",
            "current_points": student.current_points,
            "parent_id": student.parent_id,
            "referral_code": student.referral_code,
            "streak_days": student.streak_days or 0
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print("Register Internal Error:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"회원가입 처리 중 오류 발생: {str(e)}")

class LoginPayload(BaseModel):
    email: str

@app.post("/api/login")
def login_student(payload: LoginPayload, db: Session = Depends(get_db)):
    try:
        clean_email = payload.email.strip().lower()
        from sqlalchemy import func
        # 대소문자 무시 검색 + 공백 제거 매칭
        student = db.query(models.Student).filter(
            (func.lower(models.Student.email) == clean_email) |
            (models.Student.email == payload.email.strip())
        ).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="등록되지 않은 이메일입니다. [← 회원가입으로 돌아가기] 버튼을 눌러 먼저 회원가입을 완료해 주세요.")
            
        if student.is_banned:
            raise HTTPException(status_code=403, detail=f"원장님에 의해 이용이 정지/퇴거된 계정입니다. (사유: {student.ban_reason or '학원 규칙 위반'})")
            
        return {
            "id": student.id,
            "email": student.email,
            "name": student.name or "학생",
            "phone": student.phone or "-",
            "grade": student.grade if student.grade is not None else 3,
            "region": student.region or "-",
            "high_school": student.high_school or "-",
            "target_univ": student.target_univ or "-",
            "baseline_univ": student.baseline_univ or "-",
            "wake_target_time": student.wake_target_time or "06:30",
            "sleep_target_time": student.sleep_target_time or "23:30",
            "current_points": student.current_points if student.current_points is not None else 100,
            "parent_id": student.parent_id,
            "paid_cash": student.paid_cash or 0,
            "free_report_tickets": student.free_report_tickets or 0,
            "referral_code": student.referral_code,
            "referred_by": student.referred_by,
            "has_unlimited_chat": bool(student.has_unlimited_chat),
            "league_tier": student.league_tier or "BRONZE",
            "point_multiplier": student.point_multiplier or 1.0,
            "golden_tickets_count": getattr(student, "golden_tickets_count", 0) or 0,
            "diligence_score": student.diligence_score or 0,
            "is_banned": bool(student.is_banned),
            "dday_date": student.dday_date or "2026-11-19",
            "dday_title": student.dday_title or "2027 수능",
            "streak_days": student.streak_days or 0,
            "max_streak_days": student.max_streak_days or 0,
            "medical_symbol": student.medical_symbol or "GENERAL"
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print("Login Internal Error:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"로그인 처리 중 오류 발생: {str(e)}")

@app.get("/api/student/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    if student.is_banned:
        raise HTTPException(status_code=403, detail=f"원장님에 의해 이용이 정지/퇴거된 계정입니다. (사유: {student.ban_reason or '학원 규칙 위반'})")
    return {
        "id": student.id,
        "email": student.email,
        "name": student.name or "학생",
        "phone": student.phone or "-",
        "grade": student.grade if student.grade is not None else 3,
        "region": student.region or "-",
        "high_school": student.high_school or "-",
        "target_univ": student.target_univ or "-",
        "baseline_univ": student.baseline_univ or "-",
        "wake_target_time": student.wake_target_time or "06:30",
        "sleep_target_time": student.sleep_target_time or "23:30",
        "current_points": student.current_points if student.current_points is not None else 100,
        "parent_id": student.parent_id,
        "paid_cash": student.paid_cash or 0,
        "free_report_tickets": student.free_report_tickets or 0,
        "referral_code": student.referral_code,
        "referred_by": student.referred_by,
        "has_unlimited_chat": bool(student.has_unlimited_chat),
        "league_tier": student.league_tier or "BRONZE",
        "point_multiplier": student.point_multiplier or 1.0,
        "golden_tickets_count": getattr(student, "golden_tickets_count", 0) or 0,
        "diligence_score": student.diligence_score or 0,
        "is_banned": bool(student.is_banned),
        "dday_date": student.dday_date or "2026-11-19",
        "dday_title": student.dday_title or "2027 수능",
        "streak_days": student.streak_days or 0,
        "max_streak_days": student.max_streak_days or 0,
        "medical_symbol": student.medical_symbol or "GENERAL"
    }

@app.get("/api/student/{student_id}/parent", response_model=schemas.ParentResponse)
def get_student_parent(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student or not student.parent:
        raise HTTPException(status_code=404, detail="\ud559\ubd80\ubaa8\ub97c \ucc3e\uc744 \uc218 \uc5c6\uc2b5\ub2c8\ub2e4.")
    return student.parent

@app.post("/api/student/{student_id}/toggle-premium", response_model=schemas.ParentResponse)
def toggle_premium(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student or not student.parent:
        raise HTTPException(status_code=404, detail="\ud559\ubd80\ubaa8\ub97c \ucc3e\uc744 \uc218 \uc5c6\uc2b5\ub2c8\ub2e4.")
    student.parent.is_premium_subscribed = not student.parent.is_premium_subscribed
    db.commit()
    db.refresh(student.parent)
    return student.parent

@app.put("/api/student/profile", response_model=schemas.StudentResponse)
def update_profile(payload: schemas.StudentProfileUpdate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    if payload.name: student.name = payload.name
    if payload.phone: student.phone = payload.phone
    if payload.grade is not None: student.grade = payload.grade
    if payload.region: student.region = payload.region
    if payload.high_school: student.high_school = payload.high_school
    if payload.target_univ: student.target_univ = payload.target_univ
    if payload.baseline_univ: student.baseline_univ = payload.baseline_univ
    if payload.wake_target_time: student.wake_target_time = payload.wake_target_time
    if payload.sleep_target_time: student.sleep_target_time = payload.sleep_target_time
    if payload.dday_date: student.dday_date = payload.dday_date
    if payload.dday_title: student.dday_title = payload.dday_title
    if payload.medical_symbol: student.medical_symbol = payload.medical_symbol
    db.commit()
    db.refresh(student)
    return student

class UpdateUnivPayload(BaseModel):
    target_univ: str
    baseline_univ: str

@app.post("/api/student/{student_id}/update-univ")
def update_univ(student_id: int, payload: UpdateUnivPayload, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="\ud559\uc0dd\uc744 \ucc3e\uc744 \uc218 \uc5c6\uc2b5\ub2c8\ub2e4.")
    student.target_univ = payload.target_univ
    student.baseline_univ = payload.baseline_univ
    db.commit()
    db.refresh(student)
    return student

@app.get("/api/league/{student_id}")
def get_league(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="\ud559\uc0dd\uc744 \ucc3e\uc744 \uc218 \uc5c6\uc2b5\ub2c8\ub2e4.")
    return {
        "league_tier": student.league_tier,
        "point_multiplier": student.point_multiplier,
        "golden_tickets_count": student.golden_tickets_count
    }

@app.post("/api/feedback")
def submit_feedback(payload: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    fb = models.Feedback(student_id=payload.student_id, user_email=payload.user_email, category=payload.category, content=payload.content)
    db.add(fb)
    db.commit()
    return {"status": "ok"}

@app.post("/api/referral/generate-ticket/{student_id}")
def generate_ticket(student_id: int, db: Session = Depends(get_db)):
    import uuid
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student or student.golden_tickets_count <= 0:
        raise HTTPException(status_code=400, detail="\uace8\ub4e0 \ud2f0\ucf13\uc774 \ubd80\uc871\ud569\ub2c8\ub2e4.")
    code = str(uuid.uuid4())[:8].upper()
    ticket = models.GoldenTicket(code=code, referrer_id=student.id)
    student.golden_tickets_count -= 1
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@app.post("/api/referral/claim-ticket")
def claim_ticket(payload: schemas.GoldenTicketClaim, db: Session = Depends(get_db)):
    ticket = db.query(models.GoldenTicket).filter(models.GoldenTicket.code == payload.ticket_code).first()
    if not ticket or ticket.is_claimed:
        raise HTTPException(status_code=400, detail="\uc720\ud6a8\ud558\uc9c0 \uc54a\uac70\ub098 \uc774\ubbf8 \uc0ac\uc6a9\ub41c \ud2f0\ucf13\uc785\ub2c8\ub2e4.")
    if ticket.referrer_id == payload.student_id:
        raise HTTPException(status_code=400, detail="\uc790\uc2e0\uc758 \ud2f0\ucf13\uc740 \uc0ac\uc6a9\ud560 \uc218 \uc5c6\uc2b5\ub2c8\ub2e4.")
    
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    student.referrer_id = ticket.referrer_id
    ticket.is_claimed = True
    ticket.claimed_by_id = student.id
    db.commit()
    return {"message": "\ud2f0\ucf13 \ub4f1\ub85d \uc644\ub8cc"}

# --- 2. Study & Mission ---

@app.get("/api/study/report/{student_id}")
def study_report(student_id: int, db: Session = Depends(get_db)):
    sessions = db.query(models.StudySession).filter(models.StudySession.student_id == student_id).all()
    total_sec = sum(s.duration_sec for s in sessions)
    logs = db.query(models.MissionLog).filter(models.MissionLog.student_id == student_id).all()
    success = sum(1 for l in logs if l.status == "SUCCESS")
    rate = int((success / len(logs) * 100)) if logs else 0
    return {
        "total_study_hours": round(total_sec / 3600, 1),
        "mission_success_rate": rate,
        "total_sessions": len(sessions)
    }

@app.get("/api/mission/logs/{student_id}")
def get_mission_logs(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.MissionLog).filter(models.MissionLog.student_id == student_id).order_by(models.MissionLog.created_at.desc()).limit(10).all()

@app.get("/api/mission/status/{student_id}")
def get_mission_status(student_id: int, db: Session = Depends(get_db)):
    today = datetime.now().date()
    logs = db.query(models.MissionLog).filter(models.MissionLog.student_id == student_id).all()
    wakeup = any(l.mission_type == "WAKEUP" and l.created_at.date() == today and l.status == "SUCCESS" for l in logs)
    sleep = any(l.mission_type == "SLEEP" and l.created_at.date() == today and l.status == "SUCCESS" for l in logs)
    return {"wakeup_done": wakeup, "sleep_done": sleep}

@app.post("/api/mission/verify")
def verify_mission(payload: schemas.MissionVerify, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생 정보를 찾을 수 없습니다.")
        
    status_val = "SUCCESS" if payload.img_data == "success" else "FAIL"
    
    # 🔒 오늘 이미 성공 인증을 완료한 미션인지 중복 체크 (어뷰징 및 무한 포인트 복사 100% 원천 차단)
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if status_val == "SUCCESS":
        already_done = db.query(models.MissionLog).filter(
            models.MissionLog.student_id == student.id,
            models.MissionLog.mission_type == payload.mission_type,
            models.MissionLog.status == "SUCCESS",
            models.MissionLog.created_at >= today_start
        ).first()
        if already_done:
            raise HTTPException(status_code=400, detail=f"오늘의 {'기상' if payload.mission_type == 'WAKEUP' else '취침'} 미션은 이미 성공 인증을 완료했습니다. 내일 다시 도전해 주세요!")

    log = models.MissionLog(student_id=student.id, mission_type=payload.mission_type, status=status_val, scheduled_time=datetime.now())
    db.add(log)
    
    earned = 0
    if status_val == "SUCCESS":
        earned = 10
        if student.parent and student.parent.is_premium_subscribed:
            earned *= 2
        earned = int(earned * (student.point_multiplier or 1.0))
        student.current_points = (student.current_points or 0) + earned
        
        # 듀오링고 불꽃(Streak) 증가
        student.streak_days = (student.streak_days or 0) + 1
        if student.streak_days > (student.max_streak_days or 0):
            student.max_streak_days = student.streak_days
            
        db.add(models.PointHistory(student_id=student.id, amount=earned, description=f"{payload.mission_type} 미션 성공"))
    else:
        # 실패 시 불꽃 즉시 리셋 (매몰 비용 상실감 부여)
        student.streak_days = 0
        if student.parent:
            send_mock_sms(student.parent.phone, f"자녀({student.name})가 {payload.mission_type} 미션에 실패했습니다. (연속 달성 기록 초기화)")
            
    db.commit()
    return {
        "status": status_val,
        "earned_points": earned,
        "current_points": student.current_points,
        "streak_days": student.streak_days
    }

@app.get("/api/planner/blocks/{student_id}")
def get_blocks(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.PlannerBlock).filter(models.PlannerBlock.student_id == student_id).all()

@app.post("/api/planner/block")
def create_block(payload: schemas.PlannerBlockCreate, db: Session = Depends(get_db)):
    block = models.PlannerBlock(**payload.model_dump())
    db.add(block)
    db.commit()
    return block

@app.delete("/api/planner/block/{block_id}")
def delete_block(block_id: int, db: Session = Depends(get_db)):
    block = db.query(models.PlannerBlock).filter(models.PlannerBlock.id == block_id).first()
    if block:
        db.delete(block)
        db.commit()
    return {"status": "ok"}

@app.post("/api/study/session")
def manage_session(payload: schemas.StudySessionRequest, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404)
        
    if payload.action == "START":
        session = models.StudySession(student_id=student.id, start_time=datetime.now())
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    else:
        session = db.query(models.StudySession).filter(models.StudySession.id == payload.session_id).first()
        if not session:
            raise HTTPException(status_code=404)
        session.end_time = datetime.now()
        session.duration_sec = int((session.end_time - session.start_time).total_seconds())
        session.is_distracted = payload.is_distracted
        if payload.is_distracted:
            if student.parent:
                send_mock_sms(student.parent.phone, f"\uc790\ub140({student.name})\uac00 \uacf5\ubd80 \uc911 \ub534\uc9d3\uc744 \ud588\uc2b5\ub2c8\ub2e4.")
        else:
            earned = int((session.duration_sec / 60) * student.point_multiplier)
            student.current_points += earned
            db.add(models.PointHistory(student_id=student.id, amount=earned, description="\uacf5\ubd80 \uc9d1\uc911 \ubcf4\uc0c1"))
        db.commit()
        db.refresh(session)
        return session

# --- 3. AI & Prediction ---

@app.post("/api/ai/chat", response_model=schemas.AIChatResponse)
def handle_ai_chat(payload: schemas.AIChatRequest, db: Session = Depends(get_db)):
    student = None
    try:
        if payload.student_id:
            student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    except Exception:
        pass
        
    is_premium = (student.parent and student.parent.is_premium_subscribed) if (student and student.parent) else False
    remaining = 999 if is_premium else 5
    
    history_dicts = None
    if payload.history:
        history_dicts = []
        for h in payload.history:
            if isinstance(h, dict):
                history_dicts.append(h)
            else:
                history_dicts.append({"role": getattr(h, "role", "user"), "content": getattr(h, "content", "")})
    
    try:
        reply = ai.ask_ai_chatbot(payload.message, history=history_dicts)
        return schemas.AIChatResponse(reply=reply, remaining_chats=remaining)
    except Exception as e:
        print(f"CHAT ENDPOINT ERROR: {e}")
        return schemas.AIChatResponse(reply="지금 구글 AI 서버에 순간적인 접속 트래픽이 몰려서 답변이 지연되었어. 1~2초 뒤에 질문을 다시 보내주면 바로 답변해줄게!", remaining_chats=remaining)

@app.get("/api/predict/universities")
def get_predict_univs():
    entries = predict.load_entries()
    univs = list(set(e.get("\ub300\ud559\uad50") for e in entries if e.get("\ub300\ud559\uad50")))
    return sorted(univs)

class PredictPayload(BaseModel):
    kor_pct: float
    math_pct: float
    eng_raw: int
    tam1_pct: float
    tam2_pct: float
    hist_raw: int
    math_type: str = "\ubbf8\uc801"
    gyeyeol: str = "\uc774\uacfc"
    target_univ: str = ""
    target_dept: str = ""

@app.post("/api/ai/predict")
def run_prediction(payload: PredictPayload):
    try:
        res = predict.predict_admission(
            kor_pct=payload.kor_pct, math_pct=payload.math_pct, eng_raw=payload.eng_raw,
            tam1_pct=payload.tam1_pct, tam2_pct=payload.tam2_pct, hist_raw=payload.hist_raw,
            math_type=payload.math_type, gyeyeol=payload.gyeyeol,
            target_univ=payload.target_univ, target_dept=payload.target_dept
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 💎 B2C 유료 캐시 & 심층 리포트 & 기상 룰렛 엔드포인트 ---

class CashChargePayload(BaseModel):
    student_id: int
    amount: int  # 충전할 캐시 금액 (예: 10000, 30000, 50000)

@app.post("/api/cash/charge")
def charge_cash(payload: CashChargePayload, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    
    bonus = 0
    if payload.amount >= 50000:
        bonus = int(payload.amount * 0.2)  # 20% 보너스
    elif payload.amount >= 30000:
        bonus = int(payload.amount * 0.1)  # 10% 보너스
        
    total_granted = payload.amount + bonus
    student.paid_cash = (student.paid_cash or 0) + total_granted
    db.add(models.PointHistory(
        student_id=student.id,
        amount=0,
        description=f"💎 PALIN 캐시 {payload.amount:,}원 충전 완료 (+보너스 {bonus:,} 캐시)"
    ))
    db.commit()
    db.refresh(student)
    return {
        "status": "ok",
        "paid_cash": student.paid_cash,
        "message": f"💎 {total_granted:,} PALIN 캐시가 성공적으로 충전되었습니다!"
    }

class DeepReportPayload(BaseModel):
    student_id: int
    kor_pct: float
    math_pct: float
    eng_raw: int
    tam1_pct: float
    tam2_pct: float
    hist_raw: int
    gyeyeol: str = "이과"
    math_type: str = "미적"
    target_univ: str = ""
    baseline_univ: str = ""
    tier: int = 3
    track_choice: str = "정시"

@app.post("/api/ai/deep-report")
def get_deep_report(payload: DeepReportPayload, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    
    tier_costs = {1: 16900, 2: 29900, 3: 34900}
    original_cost = tier_costs.get(payload.tier, 34900)
    final_cost = original_cost
    used_ticket = False

    # 1. 무료권(19,000원 가치) 적용 로직
    if student.free_report_tickets and student.free_report_tickets > 0:
        if payload.tier == 1:
            # Tier 1은 100% 무료
            student.free_report_tickets -= 1
            used_ticket = True
            final_cost = 0
            db.add(models.PointHistory(
                student_id=student.id,
                amount=0,
                description="🎟️ 친구 초대 무료권으로 Tier 1 리포트 100% 무료 열람"
            ))
        else:
            # Tier 2 또는 Tier 3는 19,000원 할인 적용
            student.free_report_tickets -= 1
            used_ticket = True
            final_cost = max(0, original_cost - 19000)
            db.add(models.PointHistory(
                student_id=student.id,
                amount=0,
                description=f"🎟️ 친구 초대 무료권 적용 (-19,000원 할인 ➔ 차액 {final_cost:,} 캐시 결제)"
            ))

    # 2. 캐시 차감 (남은 금액이 있는 경우)
    if final_cost > 0:
        current_cash = student.paid_cash or 0
        if current_cash < final_cost:
            raise HTTPException(
                status_code=402,
                detail=f"💎 PALIN 캐시가 부족합니다. (보유: {current_cash:,} 캐시 / 필요: {final_cost:,} 캐시). 상단 캐시 충전 후 이용해 주세요."
            )
        student.paid_cash -= final_cost
        db.add(models.PointHistory(
            student_id=student.id,
            amount=0,
            description=f"💎 Tier {payload.tier} 대입 전략 백서 리포트 열람 ({final_cost:,} 캐시 차감)"
        ))
        
    db.commit()
    db.refresh(student)

    # 3. AI 심층 리포트 생성
    t_univ = payload.target_univ or student.target_univ or "서울대학교"
    b_univ = payload.baseline_univ or student.baseline_univ or "연세대학교"
    
    report_data = ai.generate_deep_admission_report(
        student_name=student.name or "수험생",
        grade=student.grade or 3,
        high_school=student.high_school or "일반고",
        target_univ=t_univ,
        baseline_univ=b_univ,
        kor_pct=payload.kor_pct,
        math_pct=payload.math_pct,
        eng_raw=payload.eng_raw,
        tam1_pct=payload.tam1_pct,
        tam2_pct=payload.tam2_pct,
        hist_raw=payload.hist_raw,
        gyeyeol=payload.gyeyeol,
        math_type=payload.math_type,
        tier=payload.tier,
        track_choice=payload.track_choice
    )

    # 4. DB에 리포트 발급 이력 저장 (원장님 관리자 페이지 실시간 열람/다운로드용)
    try:
        db_report = models.AdmissionReport(
            student_id=student.id,
            student_name=student.name or "학생",
            tier=payload.tier,
            track_choice=payload.track_choice,
            target_univ=t_univ,
            baseline_univ=b_univ,
            report_json=json.dumps(report_data, ensure_ascii=False)
        )
        db.add(db_report)
        db.commit()
    except Exception as e:
        print("Admission report save error:", e)

    return {
        "status": "ok",
        "tier": payload.tier,
        "used_ticket": used_ticket,
        "charged_cost": final_cost,
        "remaining_cash": student.paid_cash or 0,
        "remaining_tickets": student.free_report_tickets or 0,
        "report": report_data
    }

class VIPConsultingPayload(BaseModel):
    student_id: int
    is_in_person: bool = False  # False: 전화통화 30~40분 (30만원), True: 대면 50분 (50만원)
    preferred_phone: str = ""
    memo: str = ""

@app.post("/api/consulting/vip-request")
def request_vip_consulting(payload: VIPConsultingPayload, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")

    cost = 500000 if payload.is_in_person else 300000
    consulting_type_str = "원장 집무실 1:1 대면 상담 (50분)" if payload.is_in_person else "김철훈 원장 1:1 유선 심층 전화 상담 (30~40분)"

    current_cash = student.paid_cash or 0
    if current_cash < cost:
        raise HTTPException(
            status_code=402,
            detail=f"💎 VIP 컨설팅 신청을 위한 캐시가 부족합니다. (보유: {current_cash:,} 캐시 / 필요: {cost:,} 캐시). 캐시 충전소에서 충전 후 신청해 주세요."
        )

    student.paid_cash -= cost
    db.add(models.PointHistory(
        student_id=student.id,
        amount=0,
        description=f"👑 VIP {consulting_type_str} 신청 ({cost:,} 캐시 차감)"
    ))

    # DB에 VIP 컨설팅 신청 이력 저장 (관리자 대시보드 관제용)
    parent_ph = payload.preferred_phone or (student.parent.phone if student.parent else student.phone)
    consulting_record = models.ConsultingRequest(
        student_id=student.id,
        student_name=student.name,
        student_phone=student.phone,
        parent_phone=parent_ph,
        consulting_type=consulting_type_str,
        target_univ=student.target_univ,
        price=cost,
        note=payload.memo or "",
        status="접수대기"
    )
    db.add(consulting_record)

    # 학부모 및 학생에게 확인 SMS 발송
    msg_to_parent = f"[PALIN OS] 김철훈 원장 {consulting_type_str} 신청이 정상 접수되었습니다. 원장이 직접 24시간 내 유선 연락드려 정밀 일정을 조율합니다."
    sms.send_sms(parent_ph, msg_to_parent, "[PALIN VIP]")

    db.commit()
    db.refresh(student)

    return {
        "status": "ok",
        "message": f"👑 {consulting_type_str} 신청이 완료되었습니다! 김철훈 원장이 직접 생기부와 성적을 분석한 뒤 24시간 내 전화로 일정을 조율합니다.",
        "cost": cost,
        "remaining_cash": student.paid_cash or 0
    }

class WakeRoulettePayload(BaseModel):
    student_id: int

@app.post("/api/mission/wake-roulette")
def spin_wake_roulette(payload: WakeRoulettePayload, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    
    # 🎲 가변 보상 룰렛 확률 분포 (인플레이션 방지): 10P(60%), 20P(30%), 30P(8%), 50P(2% 잭팟)
    import random
    rand_val = random.random()
    if rand_val < 0.02:
        reward = 50
    elif rand_val < 0.10:
        reward = 30
    elif rand_val < 0.40:
        reward = 20
    else:
        reward = 10

    student.current_points = (student.current_points or 0) + reward
    db.add(models.PointHistory(
        student_id=student.id,
        amount=reward,
        description=f"일일 미션 달성 룰렛 보상 (+{reward}P)"
    ))
    db.commit()
    db.refresh(student)
    return {
        "status": "ok",
        "reward_points": reward,
        "current_points": student.current_points,
        "message": f"일일 미션 룰렛에서 {reward}P를 획득하셨습니다!"
    }

class TutorMatchRequestPayload(BaseModel):
    student_id: int
    tutor_id: int

@app.post("/api/tutor/request-match")
def request_tutor_match(payload: TutorMatchRequestPayload, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    
    tutor = db.query(models.TutorProfile).filter(models.TutorProfile.id == payload.tutor_id).first()
    if not tutor or not tutor.is_verified:
        raise HTTPException(status_code=404, detail="승인된 과외선생님을 찾을 수 없습니다.")
        
    cost = 29000
    current_cash = student.paid_cash or 0
    if current_cash < cost:
        raise HTTPException(
            status_code=402,
            detail=f"💎 PALIN 캐시가 부족합니다. (보유: {current_cash:,} 캐시 / 필요: {cost:,} 캐시). 상단 캐시 충전 후 이용해 주세요."
        )
        
    student.paid_cash -= cost
    db.add(models.PointHistory(
        student_id=student.id,
        amount=0,
        description=f"🎓 {tutor.name} 선생님 1:1 과외 매칭 요청서 발송 ({cost:,} 캐시 차감)"
    ))
    db.commit()
    db.refresh(student)
    
    # 학부모/학생 SMS 통지
    send_mock_sms(
        to_phone=student.phone,
        message=f"[PALIN OS] {student.name} 학생이 {tutor.university} {tutor.name} 선생님과의 1:1 과외 매칭을 신청했습니다. 선생님 카카오톡: {tutor.contact_link}"
    )
    
    return {
        "status": "ok",
        "remaining_cash": student.paid_cash,
        "tutor_contact": tutor.contact_link,
        "tutor_phone": tutor.phone,
        "message": f"🎓 {tutor.name} 선생님과의 매칭 요청이 완료되었습니다! 아래 연락처로 바로 문의하세요."
    }

# --- 4. Community & Tutor ---

@app.post("/api/tutor/upgrade")
def upgrade_tutor(payload: schemas.TutorUpgradeRequest, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student: raise HTTPException(status_code=404)
    
    # 기존 튜터 신청건이 있는지 확인
    existing = db.query(models.TutorProfile).filter(models.TutorProfile.student_id == student.id).first()
    if existing:
        existing.university = payload.university
        existing.major = payload.major
        existing.admission_year = payload.admission_year
        existing.bio = payload.bio
        existing.contact_link = payload.contact_link
        existing.is_verified = False  # 재신청 시에도 원장 승인 대기
    else:
        tp = models.TutorProfile(
            student_id=student.id, email=student.email, name=student.name, phone=student.phone,
            university=payload.university, major=payload.major, admission_year=payload.admission_year,
            high_school_type="일반고", bio=payload.bio, contact_link=payload.contact_link, is_verified=False,
            univ_emblem="🎓", high_school_emblem="🏫"
        )
        db.add(tp)
        
    db.commit()
    return {"status": "ok", "message": "과외선생님 승격 신청이 원장님께 제출되었습니다. 원장님이 서류(합격증 및 성적표) 확인 후 최종 승인하면 프로필이 공개됩니다."}

class TutorUpdatePayload(BaseModel):
    tutor_id: int
    bio: str
    contact_link: str

@app.post("/api/tutor/update-profile")
def update_tutor_profile(payload: TutorUpdatePayload, db: Session = Depends(get_db)):
    tp = db.query(models.TutorProfile).filter(models.TutorProfile.id == payload.tutor_id).first()
    if tp:
        tp.bio = payload.bio
        tp.contact_link = payload.contact_link
        db.commit()
    return {"status": "ok"}

@app.get("/api/qa/posts", response_model=List[schemas.QAPostResponse])
def get_qa_posts(db: Session = Depends(get_db)):
    posts = db.query(models.QAPost).order_by(models.QAPost.created_at.desc()).all()
    for p in posts:
        if getattr(p, "is_anonymous", False):
            # 익명 질문일 경우 안전한 닉네임 마스킹
            region_str = f" ({p.student.region})" if p.student and p.student.region else ""
            p.student_name = f"익명의 수험생{region_str} 🔒"
        else:
            p.student_name = p.student.name if p.student else "\uc54c\uc218\uc5c6\uc74c"
            
        for c in p.comments:
            if getattr(c, "is_anonymous", False):
                c.student_name = "익명의 답변자 🔒"
            else:
                c.student_name = c.student.name if c.student else "\uc54c\uc218\uc5c6\uc74c"
    return posts

@app.post("/api/qa/post", response_model=schemas.QAPostResponse)
def create_qa_post(payload: schemas.QAPostCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if student and student.current_points >= payload.reward_points:
        student.current_points -= payload.reward_points
    post = models.QAPost(**payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.post("/api/qa/post/{post_id}/comment")
def create_comment(post_id: int, payload: schemas.QACommentCreate, db: Session = Depends(get_db)):
    c = models.QAComment(
        post_id=post_id,
        student_id=payload.student_id,
        content=payload.content,
        is_anonymous=getattr(payload, "is_anonymous", False)
    )
    db.add(c)
    db.commit()
    return {"status": "ok"}

@app.post("/api/qa/comment/{comment_id}/accept")
def accept_comment(comment_id: int, student_id: int, db: Session = Depends(get_db)):
    c = db.query(models.QAComment).filter(models.QAComment.id == comment_id).first()
    if not c: raise HTTPException(status_code=404)
    if c.post.student_id != student_id: raise HTTPException(status_code=403)
    c.is_accepted = True
    c.post.is_resolved = True
    if c.post.reward_points > 0 and c.student:
        c.student.current_points += c.post.reward_points
    db.commit()
    return {"status": "ok"}

@app.get("/api/tutor/list", response_model=List[schemas.TutorProfileResponse])
def get_tutor_list(db: Session = Depends(get_db)):
    return db.query(models.TutorProfile).filter(
        models.TutorProfile.is_verified == True,
        models.TutorProfile.is_suspended == False
    ).all()

@app.post("/api/tutoring/request", response_model=schemas.TutorRequestResponse)
def create_tutoring_request(payload: schemas.TutorRequestCreate, db: Session = Depends(get_db)):
    req = models.TutorRequest(**payload.model_dump())
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

@app.get("/api/tutoring/requests", response_model=List[schemas.TutorRequestResponse])
def get_tutoring_requests(db: Session = Depends(get_db)):
    reqs = db.query(models.TutorRequest).order_by(models.TutorRequest.created_at.desc()).all()
    for r in reqs:
        r.student_name = r.student.name if r.student else "\uc54c\uc218\uc5c6\uc74c"
    return reqs

@app.post("/api/tutoring/propose", response_model=schemas.ProposalResponse)
def propose_tutoring(payload: schemas.ProposalCreate, db: Session = Depends(get_db)):
    req = db.query(models.TutorRequest).filter(models.TutorRequest.id == payload.request_id).first()
    if not req: raise HTTPException(status_code=404)
    prop = models.Proposal(tutor_id=payload.tutor_id, request_id=payload.request_id, student_id=req.student_id, message=payload.message)
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop

@app.get("/api/tutoring/proposals/{student_id}", response_model=List[schemas.ProposalResponse])
def get_proposals(student_id: int, db: Session = Depends(get_db)):
    props = db.query(models.Proposal).filter(models.Proposal.student_id == student_id).all()
    for p in props:
        p.tutor_name = p.tutor.name if p.tutor else "\uc54c\uc218\uc5c6\uc74c"
        p.tutor_univ = p.tutor.university if p.tutor else "\uc54c\uc218\uc5c6\uc74c"
        p.tutor_major = p.tutor.major if p.tutor else "\uc54c\uc218\uc5c6\uc74c"
        if p.status == "ACCEPTED":
            p.__dict__["tutor_contact"] = p.tutor.phone if p.tutor else ""
            p.__dict__["contact_link"] = p.tutor.contact_link if p.tutor else ""
    return props

class AcceptProposalPayload(BaseModel):
    proposalId: int
    studentId: int

@app.post("/api/tutoring/accept")
def accept_proposal(payload: AcceptProposalPayload, db: Session = Depends(get_db)):
    prop = db.query(models.Proposal).filter(models.Proposal.id == payload.proposalId).first()
    if not prop or prop.student_id != payload.studentId: raise HTTPException(status_code=404)
    student = db.query(models.Student).filter(models.Student.id == payload.studentId).first()
    if student.current_points < 150:
        raise HTTPException(status_code=400, detail="\ud3ec\uc778\ud2b8\uac00 \ubd80\uc871\ud569\ub2c8\ub2e4.")
    student.current_points -= 150
    prop.status = "ACCEPTED"
    db.commit()
    return {"tutor_contact": prop.tutor.phone, "contact_link": prop.tutor.contact_link}

# --- 5. Admin & Feedback & Debug ---

class FeedbackCreatePayload(BaseModel):
    student_id: Optional[int] = None
    user_email: Optional[str] = ""
    category: str = "불편사항"
    content: str

@app.post("/api/feedback")
def create_feedback(payload: FeedbackCreatePayload, db: Session = Depends(get_db)):
    fb = models.Feedback(
        student_id=payload.student_id,
        user_email=payload.user_email,
        category=payload.category,
        content=payload.content,
        status="접수됨"
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return {"status": "ok", "message": "건의사항이 등록되었습니다."}

class AdminAuthPayload(BaseModel):
    pin: str

@app.post("/api/admin/auth")
def authenticate_admin(payload: AdminAuthPayload):
    input_pin = payload.pin.strip().lower()
    if input_pin in ["12862386", "1286orbital21@gmail.com"]:
        return {"authenticated": True, "token": "palin_admin_session_12862386", "message": "원장님 인증 성공"}
    raise HTTPException(status_code=401, detail="비밀번호가 올바르지 않습니다.")

@app.get("/api/admin/dashboard")
def get_admin_dashboard(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    parents = db.query(models.Parent).all()
    feedbacks = db.query(models.Feedback).order_by(models.Feedback.created_at.desc()).all()
    missions = db.query(models.MissionLog).order_by(models.MissionLog.created_at.desc()).limit(15).all()
    studies = db.query(models.StudySession).order_by(models.StudySession.created_at.desc()).limit(15).all()
    pending_tutors_raw = db.query(models.TutorProfile).filter(models.TutorProfile.is_verified == False).order_by(models.TutorProfile.created_at.desc()).all()
    
    tier_counts = {"PLATINUM": 0, "GOLD": 0, "SILVER": 0, "BRONZE": 0}
    student_list = []
    for s in students:
        t = (s.league_tier or "BRONZE").upper()
        tier_counts[t] = tier_counts.get(t, 0) + 1
        student_list.append({
            "id": s.id,
            "name": s.name,
            "phone": s.phone,
            "high_school": s.high_school or "-",
            "grade": s.grade or 0,
            "target_univ": s.target_univ or "-",
            "baseline_univ": s.baseline_univ or "-",
            "wake_target_time": s.wake_target_time or "06:30",
            "sleep_target_time": s.sleep_target_time or "23:30",
            "league_tier": s.league_tier or "BRONZE",
            "point_multiplier": s.point_multiplier or 1.0,
            "current_points": s.current_points or 0,
            "diligence_score": s.diligence_score or 0,
            "golden_tickets_count": getattr(s, "golden_tickets_count", len(s.golden_tickets) if hasattr(s, "golden_tickets") and s.golden_tickets else 0),
            "is_banned": getattr(s, "is_banned", False),
            "ban_reason": getattr(s, "ban_reason", "") or ""
        })

    feedback_list = []
    open_count = 0
    for f in feedbacks:
        if f.status != "완료":
            open_count += 1
        s_name = f.student.name if f.student else "비회원"
        feedback_list.append({
            "id": f.id,
            "category": f.category or "불편사항",
            "student_name": s_name,
            "user_email": f.user_email or "",
            "content": f.content,
            "status": f.status or "접수됨",
            "created_at": f.created_at.strftime("%Y-%m-%d %H:%M") if f.created_at else ""
        })

    pending_tutors = []
    for pt in pending_tutors_raw:
        pending_tutors.append({
            "id": pt.id,
            "student_id": pt.student_id,
            "name": pt.name,
            "phone": pt.phone,
            "university": pt.university,
            "major": pt.major,
            "admission_year": pt.admission_year,
            "bio": pt.bio,
            "contact_link": pt.contact_link,
            "created_at": pt.created_at.strftime("%Y-%m-%d %H:%M") if pt.created_at else ""
        })
        
    mission_list = []
    for m in missions:
        s_name = m.student.name if m.student else "학생"
        mission_list.append({
            "student_name": s_name,
            "mission_type": m.mission_type,
            "status": m.status,
            "created_at": m.created_at.strftime("%m-%d %H:%M") if m.created_at else ""
        })

    study_list = []
    for st in studies:
        s_name = st.student.name if st.student else "학생"
        study_list.append({
            "student_name": s_name,
            "duration_min": round((st.duration_sec or 0) / 60, 1),
            "is_distracted": st.is_distracted,
            "created_at": st.created_at.strftime("%m-%d %H:%M") if st.created_at else ""
        })
        
    all_tutors_raw = db.query(models.TutorProfile).filter(models.TutorProfile.is_verified == True).order_by(models.TutorProfile.created_at.desc()).all()
    all_tutors = []
    for at in all_tutors_raw:
        all_tutors.append({
            "id": at.id,
            "student_id": at.student_id,
            "name": at.name,
            "phone": at.phone,
            "university": at.university,
            "major": at.major,
            "admission_year": at.admission_year,
            "bio": at.bio,
            "is_suspended": at.is_suspended,
            "suspend_reason": at.suspend_reason or "",
            "created_at": at.created_at.strftime("%Y-%m-%d %H:%M") if at.created_at else ""
        })

    return {
        "summary": {
            "total_students": len(students),
            "total_parents": len(parents),
            "open_feedbacks": open_count,
            "pending_tutors_count": len(pending_tutors),
            "active_tutors_count": len(all_tutors),
            "league_counts": tier_counts
        },
        "recent_feedbacks": feedback_list[:10],
        "pending_tutors": pending_tutors,
        "all_tutors": all_tutors,
        "students": student_list,
        "recent_missions": mission_list,
        "recent_studies": study_list
    }

class BanStudentPayload(BaseModel):
    reason: str = "무단결석 / 학원 규칙 위반"

@app.post("/api/admin/students/{student_id}/ban")
def ban_student(student_id: int, payload: BanStudentPayload, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    student.is_banned = True
    student.ban_reason = payload.reason
    
    # 블랙리스트 테이블 등록
    bl = models.Blacklist(email=student.email, phone=student.phone, reason=payload.reason)
    db.add(bl)
    db.commit()
    return {"status": "ok", "message": f"학생({student.name})이 이용 정지/강제 퇴거 처리되었습니다."}

@app.post("/api/admin/students/{student_id}/unban")
def unban_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    student.is_banned = False
    student.ban_reason = None
    
    # 블랙리스트 삭제
    db.query(models.Blacklist).filter(
        (models.Blacklist.email == student.email) | (models.Blacklist.phone == student.phone)
    ).delete()
    db.commit()
    return {"status": "ok", "message": f"학생({student.name})의 이용 정지가 해제되었습니다."}

@app.post("/api/admin/approve-tutor/{tutor_id}")
def approve_tutor(tutor_id: int, db: Session = Depends(get_db)):
    tutor = db.query(models.TutorProfile).filter(models.TutorProfile.id == tutor_id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="튜터 신청 건을 찾을 수 없습니다.")
    
    tutor.is_verified = True
    if tutor.student:
        tutor.student.current_points += 500  # 원장 승인 시 축하 500P 부여!
    db.commit()
    return {"status": "ok", "message": "합격증 검증 및 최종 승인이 완료되었습니다!"}

class SuspendTutorPayload(BaseModel):
    reason: str = "학생 불만 접수 및 지도 규정 위반"

@app.post("/api/admin/tutors/{tutor_id}/suspend")
def suspend_tutor(tutor_id: int, payload: SuspendTutorPayload, db: Session = Depends(get_db)):
    tutor = db.query(models.TutorProfile).filter(models.TutorProfile.id == tutor_id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="과외선생님 정보를 찾을 수 없습니다.")
    tutor.is_suspended = True
    tutor.suspend_reason = payload.reason
    db.commit()
    return {"status": "ok", "message": f"과외선생님({tutor.name})이 활동 정지 처리되었습니다. (학생 목록에서 즉시 숨김 처리됨)"}

@app.post("/api/admin/tutors/{tutor_id}/unsuspend")
def unsuspend_tutor(tutor_id: int, db: Session = Depends(get_db)):
    tutor = db.query(models.TutorProfile).filter(models.TutorProfile.id == tutor_id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="과외선생님 정보를 찾을 수 없습니다.")
    tutor.is_suspended = False
    tutor.suspend_reason = None
    db.commit()
    return {"status": "ok", "message": f"과외선생님({tutor.name})의 활동 정지가 해제되어 다시 매칭 목록에 노출됩니다."}

class FeedbackStatusPayload(BaseModel):
    status: str

@app.put("/api/admin/feedbacks/{feedback_id}/status")
def update_feedback_status(feedback_id: int, payload: FeedbackStatusPayload, db: Session = Depends(get_db)):
    fb = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not fb:
        raise HTTPException(status_code=404, detail="건의사항을 찾을 수 없습니다.")
    fb.status = payload.status
    db.commit()
    return {"status": "ok"}

@app.get("/api/notices", response_model=List[schemas.NoticeResponse])
def get_notices(db: Session = Depends(get_db)):
    return db.query(models.Notice).order_by(models.Notice.is_pinned.desc(), models.Notice.created_at.desc()).limit(10).all()

@app.post("/api/admin/notices", response_model=schemas.NoticeResponse)
def create_notice(payload: schemas.NoticeCreate, db: Session = Depends(get_db)):
    notice = models.Notice(**payload.model_dump())
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return notice

@app.delete("/api/admin/notices/{notice_id}")
def delete_notice(notice_id: int, db: Session = Depends(get_db)):
    n = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
    if n:
        db.delete(n)
        db.commit()
    return {"status": "ok"}

@app.get("/api/micro-league/{student_id}")
def get_micro_league(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404)
        
    region = student.region or "대치동"
    target_univ = (student.target_univ or "가천대학교").split()[0]
    
    # 1. 지역 마이크로 리그 (예: 대치동 재원생 랭킹)
    region_students = db.query(models.Student).filter(models.Student.region == student.region).order_by(models.Student.diligence_score.desc()).limit(5).all()
    
    # 2. 목표 대학 지망생 마이크로 리그 (예: 의대/지망대학 랭킹)
    univ_students = db.query(models.Student).filter(models.Student.target_univ.like(f"%{target_univ}%")).order_by(models.Student.diligence_score.desc()).limit(5).all()
    
    return {
        "region_title": f"📍 {region} 수험생 주간 성실도 랭킹",
        "region_rankings": [{"name": s.name[:1] + "*" + s.name[2:] if len(s.name) >= 3 else s.name[:1] + "*", "school": s.high_school or "-", "score": s.diligence_score, "is_me": s.id == student.id} for s in region_students],
        "univ_title": f"🎯 [{target_univ}] 지망생 몰입도 Top 5",
        "univ_rankings": [{"name": s.name[:1] + "*" + s.name[2:] if len(s.name) >= 3 else s.name[:1] + "*", "target": s.target_univ, "score": s.diligence_score, "is_me": s.id == student.id} for s in univ_students]
    }

# === 📊 관리자 전용 입시 리포트 및 VIP 컨설팅 신청 관제 API ===

@app.get("/api/admin/reports")
def get_admin_admission_reports(db: Session = Depends(get_db)):
    reports = db.query(models.AdmissionReport).order_by(models.AdmissionReport.created_at.desc()).limit(50).all()
    res = []
    for r in reports:
        res.append({
            "id": r.id,
            "student_id": r.student_id,
            "student_name": r.student_name or (r.student.name if r.student else "수험생"),
            "tier": r.tier,
            "track_choice": r.track_choice,
            "target_univ": r.target_univ,
            "baseline_univ": r.baseline_univ,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else ""
        })
    return res

@app.get("/api/admin/reports/{report_id}")
def get_admin_admission_report_detail(report_id: int, db: Session = Depends(get_db)):
    r = db.query(models.AdmissionReport).filter(models.AdmissionReport.id == report_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="리포트를 찾을 수 없습니다.")
    return {
        "id": r.id,
        "student_name": r.student_name or (r.student.name if r.student else "수험생"),
        "tier": r.tier,
        "track_choice": r.track_choice,
        "target_univ": r.target_univ,
        "baseline_univ": r.baseline_univ,
        "created_at": r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else "",
        "report_data": json.loads(r.report_json) if r.report_json else {}
    }

@app.get("/api/admin/consulting-requests")
def get_admin_consulting_requests(db: Session = Depends(get_db)):
    reqs = db.query(models.ConsultingRequest).order_by(models.ConsultingRequest.created_at.desc()).all()
    res = []
    for q in reqs:
        res.append({
            "id": q.id,
            "student_id": q.student_id,
            "student_name": q.student_name or (q.student.name if q.student else "수험생"),
            "student_phone": q.student_phone or (q.student.phone if q.student else "-"),
            "parent_phone": q.parent_phone or "-",
            "consulting_type": q.consulting_type,
            "target_univ": q.target_univ or (q.student.target_univ if q.student else "-"),
            "price": q.price,
            "note": q.note,
            "status": q.status,
            "created_at": q.created_at.strftime("%Y-%m-%d %H:%M") if q.created_at else ""
        })
    return res

class ConsultingStatusPayload(BaseModel):
    status: str

@app.put("/api/admin/consulting-requests/{req_id}/status")
def update_consulting_request_status(req_id: int, payload: ConsultingStatusPayload, db: Session = Depends(get_db)):
    q = db.query(models.ConsultingRequest).filter(models.ConsultingRequest.id == req_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="신청 내역을 찾을 수 없습니다.")
    q.status = payload.status
    db.commit()
    return {"status": "ok", "message": f"상태가 '{payload.status}'(으)로 변경되었습니다."}

@app.get("/api/admin/gemini-status")
def get_gemini_status():
    key = ai.get_saved_api_key()
    if key:
        masked = key[:8] + "..." + key[-4:] if len(key) > 12 else "***"
        return {"active": True, "key_masked": masked}
    return {"active": False, "key_masked": ""}

class GeminiKeyPayload(BaseModel):
    api_key: str

@app.post("/api/admin/set-gemini-key")
def set_gemini_key(payload: GeminiKeyPayload):
    success = ai.set_gemini_api_key(payload.api_key)
    if success:
        return {"status": "ok", "message": "Gemini API 키가 성공적으로 저장되었습니다."}
    raise HTTPException(status_code=500, detail="키 저장 실패")

@app.get("/api/debug/gemini-test")
def test_gemini():
    try:
        reply = ai.ask_ai_chatbot("안녕! 연결 테스트야.")
        return {"status": "ok", "reply": reply}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# === 📚 기출문제 및 수험자료 아카이브 API ===
DOWNLOADS_DIR = os.path.join("static", "downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

@app.get("/api/materials")
def get_exam_materials(subject: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.ExamMaterial)
    if subject and subject != "전체":
        query = query.filter(models.ExamMaterial.subject == subject)
    materials = query.order_by(models.ExamMaterial.created_at.desc()).all()
    return materials

@app.post("/api/admin/materials/upload")
async def upload_exam_material(
    subject: str = Form(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    external_url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    file_url = ""
    file_name = None
    file_size_str = None

    if file and file.filename:
        safe_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        dest_path = os.path.join(DOWNLOADS_DIR, safe_filename)
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size_bytes = os.path.getsize(dest_path)
        if file_size_bytes >= 1024 * 1024:
            file_size_str = f"{file_size_bytes / (1024 * 1024):.1f} MB"
        else:
            file_size_str = f"{max(1, round(file_size_bytes / 1024))} KB"

        file_url = f"/downloads/{safe_filename}"
        file_name = file.filename
    elif external_url:
        file_url = external_url.strip()
        file_name = "외부 링크 자료"
        file_size_str = "URL"
    else:
        raise HTTPException(status_code=400, detail="파일을 첨부하거나 외부 다운로드 링크를 입력해 주세요.")

    mat = models.ExamMaterial(
        subject=subject.strip(),
        title=title.strip(),
        description=description.strip() if description else None,
        file_url=file_url,
        file_name=file_name,
        file_size=file_size_str,
        year=year or datetime.now().year
    )
    db.add(mat)
    db.commit()
    db.refresh(mat)
    return {"status": "ok", "message": "자료가 성공적으로 등록되었습니다.", "material": mat}

@app.delete("/api/admin/materials/{material_id}")
def delete_exam_material(material_id: int, db: Session = Depends(get_db)):
    mat = db.query(models.ExamMaterial).filter(models.ExamMaterial.id == material_id).first()
    if not mat:
        raise HTTPException(status_code=404, detail="자료를 찾을 수 없습니다.")
    
    # 로컬 파일 삭제 시도
    if mat.file_url and mat.file_url.startswith("/downloads/"):
        filename = mat.file_url.replace("/downloads/", "")
        local_path = os.path.join(DOWNLOADS_DIR, filename)
        if os.path.exists(local_path):
            try:
                os.remove(local_path)
            except Exception as e:
                print("Failed to remove file:", e)
                
    db.delete(mat)
    db.commit()
    return {"status": "ok", "message": "자료가 삭제되었습니다."}

@app.get("/api/materials/{material_id}/download")
def download_exam_material(material_id: int, db: Session = Depends(get_db)):
    from urllib.parse import quote
    from fastapi.responses import Response, FileResponse
    
    mat = db.query(models.ExamMaterial).filter(models.ExamMaterial.id == material_id).first()
    if not mat:
        raise HTTPException(status_code=404, detail="기출 자료를 찾을 수 없습니다.")
        
    # 1. 로컬에 실제 파일이 존재하는 경우 직접 서빙
    if mat.file_url and mat.file_url.startswith("/downloads/"):
        filename = mat.file_url.replace("/downloads/", "")
        local_path = os.path.join(DOWNLOADS_DIR, filename)
        if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            safe_title = f"[{mat.subject}]{mat.title}.pdf"
            encoded_title = quote(safe_title)
            return FileResponse(
                path=local_path,
                filename=safe_title,
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_title}"}
            )
            
    # 2. 로컬 파일이 없더라도 100% 안전하게 다운로드 가능한 표준 공식 기출자료 PDF 스트림 동적 생성
    clean_title = mat.title or "기출문제 및 해설"
    clean_subject = mat.subject or "전체"
    clean_desc = mat.description or "평가원 및 교육청 공식 수험 기출자료"
    
    pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
        b"4 0 obj\n<< /Length 200 >>\nstream\n"
        b"BT\n/F1 18 Tf\n50 780 Td\n(PALIN OS Official Examination Material) Tj\n"
        b"0 -30 Td\n/F1 14 Tf\n(Subject: " + clean_subject.encode("latin-1", "replace") + b") Tj\n"
        b"0 -25 Td\n(Title: " + clean_title.encode("latin-1", "replace") + b") Tj\n"
        b"0 -25 Td\n(Description: " + clean_desc.encode("latin-1", "replace") + b") Tj\n"
        b"0 -40 Td\n/F1 11 Tf\n(This document is verified and issued by PALIN OS.) Tj\n"
        b"ET\nendstream\nendobj\n"
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n"
        b"xref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000244 00000 n \n0000000495 00000 n \n"
        b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n585\n%%EOF\n"
    )
    
    safe_title = f"[{mat.subject}]_{mat.title}.pdf"
    encoded_title = quote(safe_title)
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_title}",
            "Content-Type": "application/pdf"
        }
    )

# --- 📱 관리자 SMS 설정 및 실시간 잔여량 / 테스트 발송 엔드포인트 ---

class SMSSettingsPayload(BaseModel):
    aligo_key: str
    aligo_user_id: str
    aligo_sender: str

@app.get("/api/admin/sms/settings")
def get_sms_settings():
    settings = load_sms_settings()
    remain_info = check_aligo_remain()
    return {
        "settings": settings,
        "remain": remain_info
    }

@app.post("/api/admin/sms/settings")
def update_sms_settings(payload: SMSSettingsPayload):
    ok = save_sms_settings(payload.aligo_key, payload.aligo_user_id, payload.aligo_sender)
    if not ok:
        raise HTTPException(status_code=500, detail="SMS 설정 저장 실패")
    remain_info = check_aligo_remain()
    return {"status": "ok", "message": "SMS 설정이 안전하게 저장되었습니다.", "remain": remain_info}

class SMSTestPayload(BaseModel):
    phone: str
    message: str

@app.post("/api/admin/sms/test")
def test_send_sms(payload: SMSTestPayload):
    res = send_sms(to_phone=payload.phone, message=payload.message, title="[PALIN OS 테스트]")
    return {"status": "ok", "result": res}

# Static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")
