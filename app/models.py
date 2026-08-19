from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    phone = Column(String)
    grade = Column(Integer)  # 고1=1, 고2=2, 고3=3
    region = Column(String)  # 지역 (예: 서울 강남구)
    high_school = Column(String)  # 고등학교 (예: 대치고)
    target_univ = Column(String)  # 목표 대학/학과
    baseline_univ = Column(String)  # 마지노선 대학/학과
    wake_target_time = Column(String, default="06:30")  # 기상 목표 시간 (HH:MM)
    sleep_target_time = Column(String, default="23:30")  # 취침 목표 시간 (HH:MM)
    current_points = Column(Integer, default=100)
    
    # PALIN OS 전용 성장/리그전/바이럴 시스템 필드
    league_tier = Column(String, default="BRONZE")  # BRONZE | SILVER | GOLD | PLATINUM
    point_multiplier = Column(Float, default=1.0)   # 1.0x | 1.2x | 1.5x | 2.0x
    referrer_id = Column(Integer, ForeignKey("students.id"), nullable=True) # 나를 초대한 유저 ID (5% 복리 보상용)
    diligence_score = Column(Integer, default=0) # 누적 성실도 점수 (훗날 과외 튜터 신뢰도 자산)
    is_banned = Column(Boolean, default=False)   # 강제 퇴거/차단 여부
    ban_reason = Column(String, nullable=True)   # 강제 퇴거/차단 사유

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    parent_id = Column(Integer, ForeignKey("parents.id"))
    parent = relationship("Parent", back_populates="students")

    mission_logs = relationship("MissionLog", back_populates="student")
    study_sessions = relationship("StudySession", back_populates="student")
    predict_requests = relationship("PredictRequest", back_populates="student")
    qa_posts = relationship("QAPost", back_populates="student")
    qa_comments = relationship("QAComment", back_populates="student")
    tutor_requests = relationship("TutorRequest", back_populates="student")
    point_histories = relationship("PointHistory", back_populates="student")
    tutor_proposals = relationship("Proposal", back_populates="student")
    planner_blocks = relationship("PlannerBlock", back_populates="student", cascade="all, delete-orphan")
    golden_tickets = relationship("GoldenTicket", foreign_keys="[GoldenTicket.referrer_id]", back_populates="referrer")
    feedbacks = relationship("Feedback", back_populates="student")
    
    # 1:1 관계 추가 (학생이 대학 합격 시 과외 프로필 연동)
    tutor_profile = relationship("TutorProfile", back_populates="student", uselist=False)


class GoldenTicket(Base):
    __tablename__ = "golden_tickets"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    referrer_id = Column(Integer, ForeignKey("students.id"))
    claimed_by_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    is_claimed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    referrer = relationship("Student", foreign_keys=[referrer_id], back_populates="golden_tickets")


class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String, unique=True, index=True)
    is_premium_subscribed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    students = relationship("Student", back_populates="parent")


class PlannerBlock(Base):
    __tablename__ = "planner_blocks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    day_of_week = Column(Integer)  # 0=월, 1=화, ... 6=일
    start_time = Column(String)    # "HH:MM"
    end_time = Column(String)      # "HH:MM"
    title = Column(String)         # 과목 및 계획 이름
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="planner_blocks")


class MissionLog(Base):
    __tablename__ = "mission_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    mission_type = Column(String)  # "WAKEUP" | "SLEEP"
    scheduled_time = Column(DateTime)
    completed_time = Column(DateTime, nullable=True)
    proof_img_url = Column(String, nullable=True)
    status = Column(String)  # "SUCCESS" | "FAIL" | "PENDING"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="mission_logs")


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)
    duration_sec = Column(Integer, default=0)
    is_distracted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="study_sessions")


class PredictRequest(Base):
    __tablename__ = "predict_requests"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    gpa = Column(Float)
    mock_score_json = Column(Text)
    target_univ = Column(String)
    baseline_univ = Column(String)
    target_result_tier = Column(String)
    baseline_result_tier = Column(String)
    cost_points = Column(Integer, default=50)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="predict_requests")


class QAPost(Base):
    __tablename__ = "qa_posts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String)
    title = Column(String)
    content = Column(Text)
    reward_points = Column(Integer, default=0)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="qa_posts")
    comments = relationship("QAComment", back_populates="post")


class QAComment(Base):
    __tablename__ = "qa_comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("qa_posts.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    content = Column(Text)
    is_accepted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    post = relationship("QAPost", back_populates="comments")
    student = relationship("Student", back_populates="qa_comments")


# 튜터 테이블: student_id FK 연동 추가
class TutorProfile(Base):
    __tablename__ = "tutor_profiles"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True) # 학생 연계용 FK 추가
    
    email = Column(String, unique=True, index=True)
    name = Column(String)
    phone = Column(String)
    university = Column(String)
    major = Column(String)
    admission_year = Column(Integer)
    high_school_type = Column(String)
    bio = Column(Text)
    contact_link = Column(String)
    is_verified = Column(Boolean, default=False)
    
    univ_emblem = Column(String, nullable=True)
    high_school_emblem = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="tutor_profile")
    proposals = relationship("Proposal", back_populates="tutor")


class TutorRequest(Base):
    __tablename__ = "tutor_requests"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String)
    budget = Column(String)
    details = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="tutor_requests")
    proposals = relationship("Proposal", back_populates="request")


class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    tutor_id = Column(Integer, ForeignKey("tutor_profiles.id"))
    request_id = Column(Integer, ForeignKey("tutor_requests.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    message = Column(Text)
    cost_points = Column(Integer, default=100)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tutor = relationship("TutorProfile", back_populates="proposals")
    request = relationship("TutorRequest", back_populates="proposals")
    student = relationship("Student", back_populates="tutor_proposals")


class PointHistory(Base):
    __tablename__ = "point_histories"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    amount = Column(Integer)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="point_histories")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    user_email = Column(String, nullable=True)
    category = Column(String, default="불편사항")  # 불편사항 | 기능제안 | 기타
    content = Column(Text)
    status = Column(String, default="접수됨")  # 접수됨 | 처리중 | 완료
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="feedbacks")


class Blacklist(Base):
    __tablename__ = "blacklists"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=True)
    phone = Column(String, index=True, nullable=True)
    reason = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

