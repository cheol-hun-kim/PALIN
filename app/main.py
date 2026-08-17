from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel
import json
import os

from app.database import get_db, engine
from app import models, schemas, ai

# FastAPI 인스턴스 생성
app = FastAPI(title="PASS-MATE API", description="PASS-MATE MVP용 Backend API 서비스")

# 데이터베이스 테이블 자동 생성
models.Base.metadata.create_all(bind=engine)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock SMS 발송 로그 기록 함수
SMS_LOG_FILE = "sms_log.txt"

def send_mock_sms(to_phone: str, message: str):
    log_msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] TO: {to_phone} | MSG: {message}\n"
    print(f"[MOCK SMS SENDER]: {log_msg.strip()}")
    try:
        with open(SMS_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_msg)
    except Exception as e:
        print(f"Failed to write SMS log: {e}")


# --- 1. 회원가입 및 사용자 정보 API ---

@app.post("/api/register", response_model=schemas.StudentResponse)
def register_student(payload: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing_student = db.query(models.Student).filter(models.Student.email == payload.email).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
        
    parent = db.query(models.Parent).filter(models.Parent.phone == payload.parent_phone).first()
    if not parent:
        parent = models.Parent(
            name=payload.parent_name,
            phone=payload.parent_phone,
            is_premium_subscribed=False
        )
        db.add(parent)
        db.commit()
        db.refresh(parent)
        
    student = models.Student(
        email=payload.email,
        name=payload.name,
        phone=payload.phone,
        grade=payload.grade,
        region=payload.region,
        high_school=payload.high_school,
        target_univ=payload.target_univ,
        baseline_univ=payload.baseline_univ,
        current_points=100,
        parent_id=parent.id
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    
    history = models.PointHistory(
        student_id=student.id,
        amount=100,
        description="가입 축하 포인트 지급"
    )
    db.add(history)
    db.commit()
    
    return student

class LoginPayload(BaseModel):
    email: str

@app.post("/api/login")
def login_student(payload: LoginPayload, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.email == payload.email).first()
    if not student:
        raise HTTPException(status_code=404, detail="등록되지 않은 이메일입니다. 회원가입을 진행해 주세요.")
    return student

@app.get("/api/student/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    return student

@app.put("/api/student/profile", response_model=schemas.StudentResponse)
def update_student_profile(payload: schemas.StudentProfileUpdate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    if payload.target_univ is not None:
        student.target_univ = payload.target_univ
    if payload.baseline_univ is not None:
        student.baseline_univ = payload.baseline_univ
    if payload.wake_target_time is not None:
        student.wake_target_time = payload.wake_target_time
    if payload.sleep_target_time is not None:
        student.sleep_target_time = payload.sleep_target_time
    db.commit()
    db.refresh(student)
    return student

@app.post("/api/feedback", response_model=schemas.FeedbackResponse)
def create_feedback(payload: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    st_name = None
    if payload.student_id:
        st = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
        if st:
            st_name = st.name
            if not payload.user_email:
                payload.user_email = st.email

    feedback = models.Feedback(
        student_id=payload.student_id,
        user_email=payload.user_email,
        category=payload.category,
        content=payload.content,
        status="접수됨"
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    res = schemas.FeedbackResponse.from_orm(feedback)
    res.student_name = st_name
    return res

@app.get("/api/admin/feedbacks", response_model=List[schemas.FeedbackResponse])
def get_admin_feedbacks(db: Session = Depends(get_db)):
    feedbacks = db.query(models.Feedback).order_by(models.Feedback.created_at.desc()).all()
    result = []
    for fb in feedbacks:
        st_name = None
        if fb.student_id:
            st = db.query(models.Student).filter(models.Student.id == fb.student_id).first()
            if st:
                st_name = st.name
        item = schemas.FeedbackResponse.from_orm(fb)
        item.student_name = st_name
        result.append(item)
    return result

@app.put("/api/admin/feedbacks/{feedback_id}/status", response_model=schemas.FeedbackResponse)
def update_feedback_status(feedback_id: int, payload: schemas.FeedbackStatusUpdate, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="건의사항을 찾을 수 없습니다.")
    feedback.status = payload.status
    db.commit()
    db.refresh(feedback)
    st_name = None
    if feedback.student_id:
        st = db.query(models.Student).filter(models.Student.id == feedback.student_id).first()
        if st:
            st_name = st.name
    item = schemas.FeedbackResponse.from_orm(feedback)
    item.student_name = st_name
    return item


@app.get("/api/student/{student_id}/parent", response_model=schemas.ParentResponse)
def get_student_parent(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student or not student.parent:
        raise HTTPException(status_code=404, detail="학부모 정보를 찾을 수 없습니다.")
    return student.parent

@app.post("/api/student/{student_id}/toggle-premium", response_model=schemas.ParentResponse)
def toggle_parent_premium(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student or not student.parent:
        raise HTTPException(status_code=404, detail="학부모 정보를 찾을 수 없습니다.")
    
    parent = student.parent
    parent.is_premium_subscribed = not parent.is_premium_subscribed
    db.commit()
    db.refresh(parent)
    return parent


# --- 2. 1페이지: 생활관리 API (미션 및 집중 타이머) ---

@app.post("/api/mission/verify")
def verify_mission(payload: schemas.MissionVerify, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")

    now = datetime.now()
    scheduled_time = now
    status = "SUCCESS"
    earned_points = 50 if (student.parent and student.parent.is_premium_subscribed) else 25

    if payload.img_data == "fail":
        status = "FAIL"
        earned_points = 0
    else:
        # 1일 1회 미션 보상 중복 지급 방지
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        existing_today = db.query(models.MissionLog).filter(
            models.MissionLog.student_id == payload.student_id,
            models.MissionLog.mission_type == payload.mission_type,
            models.MissionLog.status == "SUCCESS",
            models.MissionLog.created_at >= today_start
        ).first()

        if existing_today:
            m_label = "기상" if payload.mission_type == "WAKEUP" else "취침"
            raise HTTPException(
                status_code=400,
                detail=f"오늘의 {m_label} 미션은 이미 성공 인증을 완료하셨습니다. (1일 1회 적립 가능)"
            )
        
    log = models.MissionLog(
        student_id=payload.student_id,
        mission_type=payload.mission_type,
        scheduled_time=scheduled_time,
        completed_time=now if status == "SUCCESS" else None,
        proof_img_url="proof_photo.png" if status == "SUCCESS" else None,
        status=status
    )
    db.add(log)
    
    if status == "SUCCESS":
        multiplier = student.point_multiplier or 1.0
        final_earned = int(earned_points * multiplier)
        
        student.current_points += final_earned
        student.diligence_score += 10 # 누적 성실도 자산 10점 추가
        
        history = models.PointHistory(
            student_id=student.id,
            amount=final_earned,
            description=f"{payload.mission_type} 미션 성공 보상 ({multiplier}x 배수 적용)"
        )
        db.add(history)
        
        if student.referrer_id:
            referrer = db.query(models.Student).filter(models.Student.id == student.referrer_id).first()
            if referrer:
                bonus = max(1, int(final_earned * 0.05))
                referrer.current_points += bonus
                ref_history = models.PointHistory(
                    student_id=referrer.id,
                    amount=bonus,
                    description=f"초대한 유저({student.name}) 미션 성공 5% 영구 복리 보상"
                )
                db.add(ref_history)
    else:
        msg = f"[PALIN OS] {student.name} 학생이 기설정된 {payload.mission_type} 미션 수행에 실패하였습니다. 수험 궤적 통제가 필요합니다."
        send_mock_sms(student.parent.phone if student.parent else "010-0000-0000", msg)
        
    db.commit()
    db.refresh(student)
    
    return {
        "success": True, 
        "status": status, 
        "earned_points": earned_points, 
        "current_points": student.current_points,
        "diligence_score": student.diligence_score,
        "league_tier": student.league_tier,
        "multiplier": student.point_multiplier
    }

@app.get("/api/mission/status/{student_id}")
def get_mission_daily_status(student_id: int, db: Session = Depends(get_db)):
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    wakeup_done = db.query(models.MissionLog).filter(
        models.MissionLog.student_id == student_id,
        models.MissionLog.mission_type == "WAKEUP",
        models.MissionLog.status == "SUCCESS",
        models.MissionLog.created_at >= today_start
    ).first() is not None

    sleep_done = db.query(models.MissionLog).filter(
        models.MissionLog.student_id == student_id,
        models.MissionLog.mission_type == "SLEEP",
        models.MissionLog.status == "SUCCESS",
        models.MissionLog.created_at >= today_start
    ).first() is not None

    return {"wakeup_done": wakeup_done, "sleep_done": sleep_done}

@app.get("/api/mission/logs/{student_id}")
def get_mission_logs(student_id: int, db: Session = Depends(get_db)):
    logs = db.query(models.MissionLog).filter(models.MissionLog.student_id == student_id).order_by(models.MissionLog.created_at.desc()).limit(10).all()
    return logs

@app.post("/api/study/session", response_model=schemas.StudySessionResponse)
def handle_study_session(payload: schemas.StudySessionRequest, db: Session = Depends(get_db)):
    if payload.action == "START":
        session = models.StudySession(
            student_id=payload.student_id,
            start_time=datetime.now()
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
        
    elif payload.action == "STOP":
        if not payload.session_id:
            raise HTTPException(status_code=400, detail="종료 시 session_id가 필요합니다.")
            
        session = db.query(models.StudySession).filter(models.StudySession.id == payload.session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
            
        session.end_time = datetime.now()
        session.duration_sec = int((session.end_time - session.start_time).total_seconds())
        session.is_distracted = payload.is_distracted
        
        student = db.query(models.Student).filter(models.Student.id == session.student_id).first()
        if student:
            if payload.is_distracted:
                history = models.PointHistory(
                    student_id=student.id,
                    amount=0,
                    description=f"공부 중 딴짓 감지 (공부시간: {session.duration_sec//60}분, 포인트 미지급)"
                )
                db.add(history)
                msg = f"[PASS-MATE] {student.name} 학생이 공부 측정 중 다른 어플리케이션을 사용하여 집중을 유지하지 못했습니다."
                send_mock_sms(student.parent.phone, msg)
            else:
                earned = max(1, session.duration_sec // 60)
                student.current_points += earned
                history = models.PointHistory(
                    student_id=student.id,
                    amount=earned,
                    description=f"집중 학습 타이머 달성 ({earned}분)"
                )
                db.add(history)
            
        db.commit()
        db.refresh(session)
        return session
        
    raise HTTPException(status_code=400, detail="유효하지 않은 액션입니다.")

@app.get("/api/study/report/{student_id}")
def get_study_report(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
        
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    sessions = db.query(models.StudySession).filter(
        models.StudySession.student_id == student_id,
        models.StudySession.created_at >= seven_days_ago,
        models.StudySession.is_distracted == False
    ).all()
    
    total_study_sec = sum(s.duration_sec for s in sessions)
    
    missions = db.query(models.MissionLog).filter(
        models.MissionLog.student_id == student_id,
        models.MissionLog.created_at >= seven_days_ago
    ).all()
    
    success_count = sum(1 for m in missions if m.status == "SUCCESS")
    fail_count = sum(1 for m in missions if m.status == "FAIL")
    
    return {
        "total_study_hours": round(total_study_sec / 3600, 1),
        "mission_success_rate": round(success_count / max(1, success_count + fail_count) * 100, 0),
        "total_sessions": len(sessions)
    }


# --- 2.0 PALIN OS 전용 리그전 & 골든 티켓 추천 시스템 API ---

import uuid

@app.get("/api/league/{student_id}")
def get_league_status(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
        
    seven_days_ago = datetime.now() - timedelta(days=7)
    missions = db.query(models.MissionLog).filter(
        models.MissionLog.student_id == student_id,
        models.MissionLog.created_at >= seven_days_ago
    ).all()
    
    success_count = sum(1 for m in missions if m.status == "SUCCESS")
    total_count = len(missions)
    rate = (success_count / total_count * 100) if total_count > 0 else 0
    
    # 성실도 미션 달성률에 따른 리그 티어 및 배수 업데이트
    if rate >= 90:
        student.league_tier = "PLATINUM"
        student.point_multiplier = 2.0
    elif rate >= 75:
        student.league_tier = "GOLD"
        student.point_multiplier = 1.5
    elif rate >= 50:
        student.league_tier = "SILVER"
        student.point_multiplier = 1.2
    else:
        student.league_tier = "BRONZE"
        student.point_multiplier = 1.0
        
    db.commit()
    db.refresh(student)
    
    return {
        "student_id": student.id,
        "league_tier": student.league_tier,
        "point_multiplier": student.point_multiplier,
        "weekly_success_rate": round(rate, 1),
        "diligence_score": student.diligence_score,
        "golden_tickets_count": student.golden_tickets_count
    }

@app.post("/api/referral/generate-ticket/{student_id}")
def generate_golden_ticket(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
        
    if student.golden_tickets_count <= 0:
        raise HTTPException(status_code=400, detail="남은 골든 티켓이 없습니다. 미션 성실도를 높여 리그 승급 시 추가 지급됩니다.")
        
    code = f"PALIN-{uuid.uuid4().hex[:6].upper()}"
    ticket = models.GoldenTicket(
        code=code,
        referrer_id=student.id
    )
    student.golden_tickets_count -= 1
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    return ticket

@app.post("/api/referral/claim-ticket")
def claim_golden_ticket(payload: schemas.GoldenTicketClaim, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
        
    ticket = db.query(models.GoldenTicket).filter(models.GoldenTicket.code == payload.ticket_code).first()
    if not ticket or ticket.is_claimed:
        raise HTTPException(status_code=400, detail="유효하지 않거나 이미 사용된 골든 티켓입니다.")
        
    if ticket.referrer_id == student.id:
        raise HTTPException(status_code=400, detail="자신이 생성한 티켓은 사용할 수 없습니다.")
        
    ticket.is_claimed = True
    ticket.claimed_by_id = student.id
    student.referrer_id = ticket.referrer_id
    
    # 가입 축하 보너스 (+50P) 양측 지급
    student.current_points += 50
    db.add(models.PointHistory(student_id=student.id, amount=50, description="골든 티켓 등록 가입 축하 보너스"))
    
    referrer = db.query(models.Student).filter(models.Student.id == ticket.referrer_id).first()
    if referrer:
        referrer.current_points += 50
        db.add(models.PointHistory(student_id=referrer.id, amount=50, description="골든 티켓 추천 피초대자 가입 보너스"))
        
    db.commit()
    return {"success": True, "message": "골든 티켓 등록 성공! 50P가 지급되었으며, 향후 미션 5% 복리 보상 네트워크에 연결되었습니다."}


# --- 2.1 에브리타임 스타일 주간 시간표 API ---

@app.post("/api/planner/block", response_model=schemas.PlannerBlockResponse)
def create_planner_block(payload: schemas.PlannerBlockCreate, db: Session = Depends(get_db)):
    block = models.PlannerBlock(
        student_id=payload.student_id,
        day_of_week=payload.day_of_week,
        start_time=payload.start_time,
        end_time=payload.end_time,
        title=payload.title,
        is_completed=False
    )
    db.add(block)
    db.commit()
    db.refresh(block)
    return block

@app.get("/api/planner/blocks/{student_id}", response_model=List[schemas.PlannerBlockResponse])
def get_planner_blocks(student_id: int, db: Session = Depends(get_db)):
    blocks = db.query(models.PlannerBlock).filter(models.PlannerBlock.student_id == student_id).all()
    return blocks

@app.delete("/api/planner/block/{block_id}")
def delete_planner_block(block_id: int, db: Session = Depends(get_db)):
    block = db.query(models.PlannerBlock).filter(models.PlannerBlock.id == block_id).first()
    if not block:
        raise HTTPException(status_code=404, detail="시간표 항목을 찾을 수 없습니다.")
    db.delete(block)
    db.commit()
    return {"success": True}


# --- 3. 2페이지: 학습공간 API (AI 챗봇, 합격예측) ---

@app.post("/api/ai/chat", response_model=schemas.AIChatResponse)
def handle_ai_chat(payload: schemas.AIChatRequest, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
        
    remaining = 5
    if not student.parent.is_premium_subscribed:
        remaining = 3
        
    history_dicts = None
    if payload.history:
        history_dicts = [{"role": h.role, "content": h.content} for h in payload.history]
    
    reply = ai.ask_ai_chatbot(payload.message, history=history_dicts)
    return schemas.AIChatResponse(reply=reply, remaining_chats=remaining)

from app.predict import predict_admission, raw_to_eng_grade, raw_to_hist_grade, load_entries

class PredictPayload(BaseModel):
    kor_pct: float          # 국어 백분위
    math_pct: float         # 수학 백분위
    eng_raw: int            # 영어 원점수
    tam1_pct: float         # 탐구1 백분위
    tam2_pct: float         # 탐구2 백분위
    hist_raw: int           # 한국사 원점수
    math_type: str = '미적'  # 미적/기하/확통
    gyeyeol: str = '이과'    # 이과/문과
    target_univ: str = ''   # 목표 대학
    target_dept: str = ''   # 목표 학과

@app.post('/api/ai/predict')
def predict_endpoint(payload: PredictPayload):
    result = predict_admission(
        kor_pct=payload.kor_pct,
        math_pct=payload.math_pct,
        eng_raw=payload.eng_raw,
        tam1_pct=payload.tam1_pct,
        tam2_pct=payload.tam2_pct,
        hist_raw=payload.hist_raw,
        math_type=payload.math_type,
        gyeyeol=payload.gyeyeol,
        target_univ=payload.target_univ,
        target_dept=payload.target_dept
    )
    return result

@app.get('/api/predict/universities')
def get_universities():
    entries = load_entries()
    univs = sorted(set(e['대학교'] for e in entries if e.get('대학교')))
    return univs

@app.get('/api/predict/departments/{univ_name}')
def get_departments(univ_name: str):
    entries = load_entries()
    depts = sorted(set(e['전공'] for e in entries if e.get('대학교') == univ_name and e.get('전공')))
    return depts

class UpdateUnivPayload(BaseModel):
    target_univ: str = ''
    baseline_univ: str = ''

@app.post('/api/student/{student_id}/update-univ')
def update_student_univ(student_id: int, payload: UpdateUnivPayload, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    if payload.target_univ:
        student.target_univ = payload.target_univ
    if payload.baseline_univ:
        student.baseline_univ = payload.baseline_univ
    db.commit()
    db.refresh(student)
    return {"target_univ": student.target_univ, "baseline_univ": student.baseline_univ}


# --- 4. 3페이지: 커뮤니티 API (공부 Q&A 및 과외매칭) ---

@app.post("/api/qa/post", response_model=schemas.QAPostResponse)
def create_qa_post(payload: schemas.QAPostCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
        
    if payload.reward_points > 0:
        if student.current_points < payload.reward_points:
            raise HTTPException(status_code=400, detail="게시물 보상 포인트가 보유 포인트보다 큽니다.")
        student.current_points -= payload.reward_points
        history = models.PointHistory(
            student_id=student.id,
            amount=-payload.reward_points,
            description=f"공부 Q&A 에스크로 설정 (보상: {payload.reward_points}P)"
        )
        db.add(history)
        
    post = models.QAPost(
        student_id=payload.student_id,
        subject=payload.subject,
        title=payload.title,
        content=payload.content,
        reward_points=payload.reward_points,
        is_resolved=False
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    
    post.student_name = student.name
    return post

@app.get("/api/qa/posts")
def list_qa_posts(db: Session = Depends(get_db)):
    posts = db.query(models.QAPost).order_by(models.QAPost.created_at.desc()).all()
    for p in posts:
        p.student_name = p.student.name
        for c in p.comments:
            c.student_name = c.student.name
    return posts

@app.post("/api/qa/post/{post_id}/comment", response_model=schemas.QACommentResponse)
def add_qa_comment(post_id: int, payload: schemas.QACommentCreate, db: Session = Depends(get_db)):
    post = db.query(models.QAPost).filter(models.QAPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")
        
    comment = models.QAComment(
        post_id=post_id,
        student_id=payload.student_id,
        content=payload.content
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    comment.student_name = comment.student.name
    return comment

@app.post("/api/qa/comment/{comment_id}/accept")
def accept_qa_comment(comment_id: int, student_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.QAComment).filter(models.QAComment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="답변을 찾을 수 없습니다.")
        
    post = comment.post
    if post.student_id != student_id:
        raise HTTPException(status_code=403, detail="자신의 게시글 답변만 채택할 수 있습니다.")
        
    if post.is_resolved:
        raise HTTPException(status_code=400, detail="이미 채택이 완료된 질문입니다.")
        
    comment.is_accepted = True
    post.is_resolved = True
    
    if post.reward_points > 0:
        answerer = comment.student
        answerer.current_points += post.reward_points
        history = models.PointHistory(
            student_id=answerer.id,
            amount=post.reward_points,
            description=f"공부 Q&A 채택 보상 수령 (글번호: {post.id})"
        )
        db.add(history)
        
    db.commit()
    return {"success": True, "reward_transferred": post.reward_points}


# --- 4.1 대학 합격 인증 및 과외 선생님 승격 API ---

@app.post("/api/tutor/upgrade", response_model=schemas.TutorProfileResponse)
def upgrade_to_tutor(payload: schemas.TutorUpgradeRequest, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생 계정을 찾을 수 없습니다.")
        
    # 기존 프로필이 있는 지 체크
    tutor = db.query(models.TutorProfile).filter(models.TutorProfile.student_id == payload.student_id).first()
    if tutor:
        raise HTTPException(status_code=400, detail="이미 과외 선생님으로 등록되어 있습니다.")

    # 대학교명에 매칭되는 시각 엠블럼 뱃지 부여
    univ = payload.university
    dept = payload.major
    univ_tag = f"🎓 {univ} {dept}"
    if "서울대" in univ:
        univ_tag = f"🦁 서울대 {dept} [합격배지]"
    elif "연세대" in univ:
        univ_tag = f"🦅 연세대 {dept} [합격배지]"
    elif "고려대" in univ:
        univ_tag = f"🐯 고려대 {dept} [합격배지]"
        
    # 의대/의학 계열 엠블럼 추가 보정
    if "의예" in dept or "의대" in dept or "치의" in dept or "한의" in dept or "약학" in dept:
        univ_tag += " ⚕️"

    tutor = models.TutorProfile(
        student_id=payload.student_id,
        email=student.email,
        name=student.name,
        phone=student.phone,
        university=univ,
        major=dept,
        admission_year=payload.admission_year,
        high_school_type="자사고" if "자사" in payload.high_school else "일반고",
        bio=payload.bio,
        contact_link=payload.contact_link,
        is_verified=True, # 목업이므로 즉시 자동 인증
        univ_emblem=univ_tag,
        high_school_emblem=f"🏫 {payload.high_school}"
    )
    db.add(tutor)
    
    # 대학 합격 축하 및 선생님 프로필 개설 축하 대규모 보너스 포인트 지급
    student.current_points += 500
    history = models.PointHistory(
        student_id=student.id,
        amount=500,
        description="🎉 대학 합격 및 과외 선생님 승격 축하 포인트 지급!"
    )
    db.add(history)
    db.commit()
    db.refresh(tutor)
    return tutor

@app.post("/api/tutor/update-profile", response_model=schemas.TutorProfileResponse)
def update_tutor_profile(payload: dict, db: Session = Depends(get_db)):
    tutor_id = payload.get("tutor_id")
    bio = payload.get("bio")
    contact_link = payload.get("contact_link")
    
    tutor = db.query(models.TutorProfile).filter(models.TutorProfile.id == tutor_id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="과외 선생님 프로필을 찾을 수 없습니다.")
        
    tutor.bio = bio
    tutor.contact_link = contact_link
    db.commit()
    db.refresh(tutor)
    return tutor


class GeminiKeyPayload(BaseModel):
    api_key: str

@app.post("/api/admin/set-gemini-key")
def set_gemini_key(payload: GeminiKeyPayload):
    if not payload.api_key or len(payload.api_key.strip()) < 10:
        raise HTTPException(status_code=400, detail="유효한 Gemini API 키를 입력해주세요.")
    success = ai.set_gemini_api_key(payload.api_key.strip())
    if success:
        return {"message": "🎉 Gemini 2.5 AI API 키가 성공적으로 저장 및 탑재되었습니다!"}
    raise HTTPException(status_code=500, detail="API 키 저장 실패")

@app.get("/api/admin/gemini-status")
def get_gemini_status():
    key = ai.get_saved_api_key()
    active = bool(key and len(key) > 10)
    masked = f"{key[:6]}...{key[-4:]}" if active else "미설정"
    return {"active": active, "key_masked": masked}

# --- 과외 매칭 API ---

@app.get("/api/tutor/list", response_model=List[schemas.TutorProfileResponse])
def list_tutors(db: Session = Depends(get_db)):
    tutors = db.query(models.TutorProfile).filter(models.TutorProfile.is_verified == True).all()
    return tutors

@app.post("/api/tutoring/request", response_model=schemas.TutorRequestResponse)
def create_tutor_request(payload: schemas.TutorRequestCreate, db: Session = Depends(get_db)):
    req = models.TutorRequest(
        student_id=payload.student_id,
        subject=payload.subject,
        budget=payload.budget,
        details=payload.details
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    req.student_name = req.student.name
    return req

@app.get("/api/tutoring/requests")
def list_tutor_requests(db: Session = Depends(get_db)):
    reqs = db.query(models.TutorRequest).order_by(models.TutorRequest.created_at.desc()).all()
    for r in reqs:
        r.student_name = r.student.name
    return reqs

@app.post("/api/tutoring/propose", response_model=schemas.ProposalResponse)
def tutor_propose_tutoring(payload: schemas.ProposalCreate, db: Session = Depends(get_db)):
    tutor = db.query(models.TutorProfile).filter(models.TutorProfile.id == payload.tutor_id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="튜터 프로필을 찾을 수 없습니다.")
        
    req = db.query(models.TutorRequest).filter(models.TutorRequest.id == payload.request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="학생 과외 요청을 찾을 수 없습니다.")
        
    proposal = models.Proposal(
        tutor_id=payload.tutor_id,
        request_id=payload.request_id,
        student_id=req.student_id,
        message=payload.message,
        cost_points=100,
        status="PENDING"
    )
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    
    proposal.tutor_name = tutor.name
    proposal.tutor_univ = tutor.university
    proposal.tutor_major = tutor.major
    return proposal

@app.get("/api/tutoring/proposals/{student_id}")
def get_received_proposals(student_id: int, db: Session = Depends(get_db)):
    proposals = db.query(models.Proposal).filter(models.Proposal.student_id == student_id).order_by(models.Proposal.created_at.desc()).all()
    for p in proposals:
        p.tutor_name = p.tutor.name
        p.tutor_univ = p.tutor.university
        p.tutor_major = p.tutor.major
    return proposals

@app.post("/api/tutoring/accept")
def accept_tutor_proposal(payload: dict, db: Session = Depends(get_db)):
    proposal_id = payload.get("proposalId")
    student_id = payload.get("studentId")
    
    proposal = db.query(models.Proposal).filter(models.Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="제안서를 찾을 수 없습니다.")
        
    if proposal.student_id != student_id:
        raise HTTPException(status_code=403, detail="본인에게 온 제안서만 수락할 수 있습니다.")
        
    proposal.status = "ACCEPTED"
    
    msg = f"[PASS-MATE] {proposal.student.name} 학생과의 과외 매칭이 성사되었습니다. 연락처: {proposal.student.phone}"
    send_mock_sms(proposal.tutor.phone, msg)
    
    db.commit()
    
    return {
        "success": True,
        "tutor_contact": proposal.tutor.phone,
        "contact_link": proposal.tutor.contact_link
    }


# --- 4.2 대학교 및 학과 정보 조회 API ---

UNIV_DEPS_PATH = os.path.join(os.path.dirname(__file__), "univ_departments.json")

@app.get("/api/univ-data")
def get_university_data():
    if not os.path.exists(UNIV_DEPS_PATH):
        try:
            from parse_univ_data import run_parsing
            run_parsing()
        except Exception as e:
            print(f"Error running parser on demand: {e}")
            
    if os.path.exists(UNIV_DEPS_PATH):
        try:
            with open(UNIV_DEPS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"대학 데이터를 읽는 중 오류가 발생했습니다: {e}")
            
    return {}


# --- 4.3 원장님 전용 통합 관제 대시보드 API ---

@app.get("/api/admin/dashboard")
def get_admin_dashboard(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    parents = db.query(models.Parent).all()
    tutors = db.query(models.TutorProfile).all()
    
    # 리그별 수험생 분포 집계
    league_counts = {"BRONZE": 0, "SILVER": 0, "GOLD": 0, "PLATINUM": 0}
    for s in students:
        tier = s.league_tier or "BRONZE"
        league_counts[tier] = league_counts.get(tier, 0) + 1
        
    # 최근 20개 미션 로그
    mission_logs = db.query(models.MissionLog).order_by(models.MissionLog.created_at.desc()).limit(20).all()
    recent_missions = []
    for m in mission_logs:
        st = db.query(models.Student).filter(models.Student.id == m.student_id).first()
        recent_missions.append({
            "id": m.id,
            "student_name": st.name if st else "알수없음",
            "mission_type": m.mission_type,
            "status": m.status,
            "created_at": m.created_at.strftime("%Y-%m-%d %H:%M") if m.created_at else ""
        })
        
    # 최근 10개 공부 타이머 세션
    study_sessions = db.query(models.StudySession).order_by(models.StudySession.created_at.desc()).limit(10).all()
    recent_studies = []
    for ss in study_sessions:
        st = db.query(models.Student).filter(models.Student.id == ss.student_id).first()
        recent_studies.append({
            "id": ss.id,
            "student_name": st.name if st else "알수없음",
            "duration_min": round(ss.duration_sec / 60, 1),
            "is_distracted": ss.is_distracted,
            "created_at": ss.created_at.strftime("%Y-%m-%d %H:%M") if ss.created_at else ""
        })

    # 학생 종합 브리핑 리스트
    student_list = []
    for s in students:
        student_list.append({
            "id": s.id,
            "name": s.name,
            "phone": s.phone,
            "high_school": s.high_school,
            "grade": s.grade,
            "target_univ": s.target_univ or "",
            "baseline_univ": s.baseline_univ or "",
            "wake_target_time": s.wake_target_time or "06:30",
            "sleep_target_time": s.sleep_target_time or "23:30",
            "league_tier": s.league_tier or "BRONZE",
            "point_multiplier": s.point_multiplier or 1.0,
            "current_points": s.current_points,
            "diligence_score": s.diligence_score,
            "golden_tickets_count": s.golden_tickets_count
        })

    # 최근 10개 건의사항 / 불편사항 로그
    feedbacks = db.query(models.Feedback).order_by(models.Feedback.created_at.desc()).limit(10).all()
    recent_feedbacks = []
    open_feedback_count = 0
    for fb in feedbacks:
        if fb.status != "완료":
            open_feedback_count += 1
        st = db.query(models.Student).filter(models.Student.id == fb.student_id).first() if fb.student_id else None
        recent_feedbacks.append({
            "id": fb.id,
            "student_name": st.name if st else "비회원/익명",
            "user_email": fb.user_email or (st.email if st else ""),
            "category": fb.category,
            "content": fb.content,
            "status": fb.status,
            "created_at": fb.created_at.strftime("%Y-%m-%d %H:%M") if fb.created_at else ""
        })

    return {
        "summary": {
            "total_students": len(students),
            "total_parents": len(parents),
            "total_tutors": len(tutors),
            "open_feedbacks": open_feedback_count,
            "league_counts": league_counts
        },
        "students": student_list,
        "recent_missions": recent_missions,
        "recent_studies": recent_studies,
        "recent_feedbacks": recent_feedbacks
    }


# --- 5. 프론트엔드 정적 파일 서빙 ---
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
else:
    print(f"Warning: Static directory '{static_dir}' not found. Ensure to create frontend files.")
