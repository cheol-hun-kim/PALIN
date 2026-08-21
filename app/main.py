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
                conn.execute(text("ALTER TABLE tutor_profiles ADD COLUMN IF NOT EXISTS is_suspended BOOLEAN DEFAULT FALSE"))
                conn.execute(text("ALTER TABLE tutor_profiles ADD COLUMN IF NOT EXISTS suspend_reason VARCHAR"))
                conn.execute(text("ALTER TABLE qa_posts ADD COLUMN IF NOT EXISTS is_anonymous BOOLEAN DEFAULT FALSE"))
                conn.execute(text("ALTER TABLE qa_comments ADD COLUMN IF NOT EXISTS is_anonymous BOOLEAN DEFAULT FALSE"))
                conn.commit()
                print("PostgreSQL Schema Migration Complete!")
        except Exception as e:
            print("DB Schema Migration Warning:", e)

init_db_schema()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SMS_LOG_FILE = "sms_log.txt"
def send_mock_sms(to_phone: str, message: str):
    log_msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] TO: {to_phone} | MSG: {message}\n"
    print(log_msg.strip())
    try:
        with open(SMS_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_msg)
    except:
        pass

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

@app.post("/api/register", response_model=schemas.StudentResponse)
def register_student(payload: schemas.StudentCreate, db: Session = Depends(get_db)):
    # 블랙리스트 검사
    banned = db.query(models.Blacklist).filter(
        (models.Blacklist.email == payload.email) | (models.Blacklist.phone == payload.phone)
    ).first()
    if banned:
        raise HTTPException(status_code=403, detail=f"원장님에 의해 이용이 정지/퇴거된 계정입니다. (사유: {banned.reason or '학원 규칙 위반'})")

    parent = db.query(models.Parent).filter(models.Parent.phone == payload.parent_phone).first()
    if not parent:
        parent = models.Parent(name=payload.parent_name, phone=payload.parent_phone, is_premium_subscribed=False)
        db.add(parent)
        db.commit()
        db.refresh(parent)
        
    student = models.Student(
        email=payload.email, name=payload.name, phone=payload.phone,
        grade=payload.grade, region=payload.region, high_school=payload.high_school,
        target_univ=payload.target_univ, baseline_univ=payload.baseline_univ,
        current_points=100, parent_id=parent.id
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    
    db.add(models.PointHistory(student_id=student.id, amount=100, description="가입 축하 포인트"))
    db.commit()
    return student

class LoginPayload(BaseModel):
    email: str

@app.post("/api/login", response_model=schemas.StudentResponse)
def login_student(payload: LoginPayload, db: Session = Depends(get_db)):
    clean_email = payload.email.strip().lower()
    from sqlalchemy import func
    # 대소문자 무시 검색 + 공백 제거 매칭
    student = db.query(models.Student).filter(
        (func.lower(models.Student.email) == clean_email) |
        (models.Student.email == payload.email.strip())
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생 정보를 찾을 수 없습니다. (가입된 이메일을 확인하시거나 회원가입을 진행해 주세요.)")
    if student.is_banned:
        raise HTTPException(status_code=403, detail=f"원장님에 의해 이용이 정지/퇴거된 계정입니다. (사유: {student.ban_reason or '학원 규칙 위반'})")
    return student

@app.get("/api/student/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    if student.is_banned:
        raise HTTPException(status_code=403, detail=f"원장님에 의해 이용이 정지/퇴거된 계정입니다. (사유: {student.ban_reason or '학원 규칙 위반'})")
    return student

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
        raise HTTPException(status_code=404)
        
    status_val = "SUCCESS" if payload.img_data == "success" else "FAIL"
    log = models.MissionLog(student_id=student.id, mission_type=payload.mission_type, status=status_val, scheduled_time=datetime.now())
    db.add(log)
    
    earned = 0
    if status_val == "SUCCESS":
        earned = 10
        if student.parent and student.parent.is_premium_subscribed:
            earned *= 2
        earned = int(earned * student.point_multiplier)
        student.current_points += earned
        
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

# Static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")
