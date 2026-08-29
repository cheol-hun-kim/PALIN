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
    region = Column(String)  # 지역 (예: 경기도 성남시 분당구)
    sido = Column(String, default="경기도") # 시도
    sigungu = Column(String, default="성남시 분당구") # 시군구
    high_school = Column(String)  # 고등학교 (예: 낙생고등학교)
    high_school_type = Column(String, default="일반고") # 일반고 | 전국자사고 | 광역자사고 | 과학고 | 외국어고 | 영재학교 | 특성화고
    target_univ = Column(String)  # 목표 대학/학과
    baseline_univ = Column(String)  # 마지노선 대학/학과
    wake_target_time = Column(String, default="06:30")  # 기상 목표 시간 (HH:MM)
    sleep_target_time = Column(String, default="23:30")  # 취침 목표 시간 (HH:MM)
    current_points = Column(Integer, default=100)
    
    # PALIN OS 전용 성장/리그전/바이럴/VIP 시스템 필드
    league_tier = Column(String, default="BRONZE")  # BRONZE | SILVER | GOLD | PLATINUM
    point_multiplier = Column(Float, default=1.0)   # 1.0x | 1.2x | 1.5x | 2.0x
    referrer_id = Column(Integer, ForeignKey("students.id"), nullable=True) # 나를 초대한 유저 ID
    diligence_score = Column(Integer, default=0) # 누적 성실도 점수 (훗날 과외 튜터 신뢰도 자산)
    is_vip = Column(Boolean, default=False)      # 주간 자습 상위 1% VIP 블랙 등급 여부
    is_banned = Column(Boolean, default=False)   # 강제 퇴거/차단 여부
    ban_reason = Column(String, nullable=True)   # 강제 퇴거/차단 사유
    
    # 💰 금융 인질 성실 보증금 에스크로 (Beeminder 모델)
    escrow_deposit = Column(Integer, default=50000) # 성실 보증금 잔액 (기본 50,000원)
    escrow_deductions = Column(Integer, default=0)  # 누적 차감 벌금액 (미션 실패/딴짓 시 1,000원씩)
    
    # 듀오링고/포레스트/D-Day 고도화 필드
    dday_date = Column(String, default="2026-11-19") # 사용자 지정 목표 D-Day 날짜
    dday_title = Column(String, default="2027 수능")  # 사용자 지정 목표 D-Day 시험명
    streak_days = Column(Integer, default=0)         # 연속 기상/자습 성공 불꽃 일수
    max_streak_days = Column(Integer, default=0)     # 최고 연속 기록
    medical_symbol = Column(String, default="GENERAL") # 메디컬/전공 엠블럼 심볼
 
    # 💎 B2C 유료 캐시 & 친구 초대 바이럴 루프 필드
    paid_cash = Column(Integer, default=0)                # 유료 결제 PALIN 캐시 (1캐시=1원)
    free_report_tickets = Column(Integer, default=0)      # 19,000원 상당 AI 심층 리포트 무료 열람권
    referral_code = Column(String, unique=True, index=True, nullable=True) # 내 고유 친구 초대 코드
    referred_by = Column(String, nullable=True)           # 나를 초대한 친구 코드
    has_unlimited_chat = Column(Boolean, default=False)   # AI 멘토 무제한 패스 보유 여부
 
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

    @property
    def golden_tickets_count(self):
        try:
            return len(self.golden_tickets) if self.golden_tickets else 3
        except Exception:
            return 3


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
    is_anonymous = Column(Boolean, default=False)
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
    is_anonymous = Column(Boolean, default=False)
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
    is_suspended = Column(Boolean, default=False) # 원장 강제 활동정지 여부
    suspend_reason = Column(String, nullable=True) # 활동정지 사유
    
    # 🌟 고급형 튜터 티어 (Gacha 모델: SSR=SKY/의치한약수, SR=서성한/특수대, R=일반)
    tier = Column(String, default="SR") # SSR | SR | R
    diligence_verified_badge = Column(Boolean, default=True) # PALIN 공인 성실도 인증 뱃지
    
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


class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    category = Column(String, default="일반공지")  # 긴급공지 | 일반공지 | 이벤트
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ExamMaterial(Base):
    __tablename__ = "exam_materials"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)  # 국어 | 수학 | 영어 | 탐구 | 기타
    title = Column(String)
    description = Column(String, nullable=True)
    file_url = Column(String)  # 문제지 다운로드 링크 (/downloads/...)
    file_name = Column(String, nullable=True)
    file_size = Column(String, nullable=True)
    answer_file_url = Column(String, nullable=True) # 정답/해설지 다운로드 링크 (PDF 또는 이미지)
    answer_file_name = Column(String, nullable=True)
    year = Column(Integer, default=2027)  # 2027학년도 | 2026학년도 | 2025학년도 등
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AdmissionReport(Base):
    __tablename__ = "admission_reports"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    student_name = Column(String, nullable=True)
    tier = Column(Integer, default=3)
    track_choice = Column(String, default="정시")
    target_univ = Column(String, nullable=True)
    baseline_univ = Column(String, nullable=True)
    report_json = Column(Text)  # JSON 전문 저장
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student")


class ConsultingRequest(Base):
    __tablename__ = "consulting_requests"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    student_name = Column(String)
    student_phone = Column(String, nullable=True)
    parent_phone = Column(String, nullable=True)
    consulting_type = Column(String, default="유선 전화 상담 (30~40분)")  # 유선 전화 상담 (30~40분) | 원장 집무실 1:1 대면 상담 (50분)
    target_univ = Column(String, nullable=True)
    status = Column(String, default="접수대기")  # 접수대기 | 상담일정확정 | 상담완료 | 취소
    price = Column(Integer, default=300000)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student")


class AdminKnowledge(Base):
    """원장님 전용 실시간 AI 지식 증강 & 칼럼 학습 DB"""
    __tablename__ = "admin_knowledge"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String) # 지식/칼럼 제목
    category = Column(String, default="입시철학") # 입시철학 | 국어공부법 | 멘탈통제 | 수시정시전략
    content = Column(Text) # 칼럼/지침 본문
    is_active = Column(Boolean, default=True) # 활성화 여부
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BlackLoungePost(Base):
    """주간 자습 상위 1% VIP 전용 폐쇄형 블랙 라운지 Q&A"""
    __tablename__ = "black_lounge_posts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    student_name = Column(String)
    target_univ = Column(String, nullable=True)
    title = Column(String)
    content = Column(Text)
    reply_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student")


class PlatformScholarshipPool(Base):
    """학생들의 딴짓/미션실패 벌금 차감액이 적립되어 상위 1%에게 지급되는 장학금 풀"""
    __tablename__ = "platform_scholarship_pool"

    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Integer, default=0)
    distributed_amount = Column(Integer, default=0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


