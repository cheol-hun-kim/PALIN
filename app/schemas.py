from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

# --- 과외선생님 프로필 응답 (상위 선언 필요) ---
class TutorProfileResponse(BaseModel):
    id: int
    student_id: Optional[int] = None
    email: str
    name: str
    phone: str
    university: str
    major: str
    admission_year: int
    high_school_type: str
    bio: str
    contact_link: str
    is_verified: bool
    is_suspended: bool = False
    suspend_reason: Optional[str] = None
    univ_emblem: Optional[str] = None
    high_school_emblem: Optional[str] = None

    class Config:
        from_attributes = True

# --- 학생/부모 관련 스키마 ---
class StudentCreate(BaseModel):
    email: EmailStr
    name: str
    phone: str
    grade: int
    region: str
    high_school: str
    target_univ: str
    baseline_univ: str
    parent_name: str
    parent_phone: str

class StudentResponse(BaseModel):
    id: int
    email: str
    name: str
    phone: str
    grade: int
    region: str
    high_school: str
    target_univ: str
    baseline_univ: str
    wake_target_time: str = "06:30"
    sleep_target_time: str = "23:30"
    current_points: int
    parent_id: int
    
    # PALIN OS 필드
    league_tier: str = "BRONZE"
    point_multiplier: float = 1.0
    golden_tickets_count: int = 3
    diligence_score: int = 0
    referrer_id: Optional[int] = None
    is_banned: bool = False
    ban_reason: Optional[str] = None
    
    # 심리통제 & D-Day 확장
    dday_date: str = "2026-11-19"
    dday_title: str = "2027 수능"
    streak_days: int = 0
    max_streak_days: int = 0
    medical_symbol: str = "GENERAL"

    tutor_profile: Optional[TutorProfileResponse] = None # 연계 튜터 정보 연동 추가
    
    class Config:
        from_attributes = True

class StudentProfileUpdate(BaseModel):
    student_id: int
    name: Optional[str] = None
    phone: Optional[str] = None
    grade: Optional[int] = None
    region: Optional[str] = None
    high_school: Optional[str] = None
    target_univ: Optional[str] = None
    baseline_univ: Optional[str] = None
    wake_target_time: Optional[str] = None
    sleep_target_time: Optional[str] = None
    dday_date: Optional[str] = None
    dday_title: Optional[str] = None
    medical_symbol: Optional[str] = None

class NoticeCreate(BaseModel):
    title: str
    content: str
    category: str = "일반공지"
    is_pinned: bool = False

class NoticeResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    is_pinned: bool
    created_at: datetime

    class Config:
        from_attributes = True

class FeedbackCreate(BaseModel):
    student_id: Optional[int] = None
    user_email: Optional[str] = None
    category: str = "불편사항" # 불편사항 | 기능제안 | 기타
    content: str

class FeedbackResponse(BaseModel):
    id: int
    student_id: Optional[int] = None
    student_name: Optional[str] = None
    user_email: Optional[str] = None
    category: str
    content: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class FeedbackStatusUpdate(BaseModel):
    status: str # 접수됨 | 처리중 | 완료


class GoldenTicketClaim(BaseModel):
    student_id: int
    ticket_code: str

class GoldenTicketResponse(BaseModel):
    id: int
    code: str
    referrer_id: int
    claimed_by_id: Optional[int] = None
    is_claimed: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ParentResponse(BaseModel):
    id: int
    name: str
    phone: str
    is_premium_subscribed: bool
    
    class Config:
        from_attributes = True


# --- 신규: 대학 합격생 과외 선생님 승격 요청 스키마 ---
class TutorUpgradeRequest(BaseModel):
    student_id: int
    university: str
    major: str
    admission_year: int
    high_school: str
    bio: str
    contact_link: str


# --- 시간표 플래너 스키마 ---
class PlannerBlockCreate(BaseModel):
    student_id: int
    day_of_week: int  # 0=월, 1=화, ... 6=일
    start_time: str    # "HH:MM"
    end_time: str      # "HH:MM"
    title: str

class PlannerBlockResponse(BaseModel):
    id: int
    student_id: int
    day_of_week: int
    start_time: str
    end_time: str
    title: str
    is_completed: bool

    class Config:
        from_attributes = True


# --- 미션 및 집중 타이머 스키마 ---
class MissionVerify(BaseModel):
    student_id: int
    mission_type: str  # "WAKEUP" | "SLEEP"
    img_data: Optional[str] = None  # Base64 이미지 데이터 (Mock 업로드용)

class MissionLogResponse(BaseModel):
    id: int
    student_id: int
    mission_type: str
    scheduled_time: datetime
    completed_time: Optional[datetime] = None
    proof_img_url: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class StudySessionRequest(BaseModel):
    student_id: int
    action: str  # "START" | "STOP"
    session_id: Optional[int] = None
    is_distracted: Optional[bool] = False

class StudySessionResponse(BaseModel):
    id: int
    student_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_sec: int
    is_distracted: bool

    class Config:
        from_attributes = True


# --- AI 관련 스키마 ---
class ChatHistoryItem(BaseModel):
    role: str  # "user" or "bot"
    content: str

class AIChatRequest(BaseModel):
    student_id: Optional[int] = None
    message: str
    history: Optional[List[Any]] = None

class AIChatResponse(BaseModel):
    reply: str
    remaining_chats: int

class PredictRequestSchema(BaseModel):
    student_id: int
    gpa: float = Field(..., ge=1.0, le=9.0)
    kor_percentile: int = Field(..., ge=0, le=100)
    math_percentile: int = Field(..., ge=0, le=100)
    eng_score: int = Field(..., ge=0, le=100)
    tam1_percentile: int = Field(..., ge=0, le=100)
    tam2_percentile: int = Field(..., ge=0, le=100)
    history_score: int = Field(..., ge=0, le=50)
    target_univ: str
    baseline_univ: str

class UnivPredictResult(BaseModel):
    university: str
    result_tier: str
    tip: str

class PredictResponseSchema(BaseModel):
    success: bool
    target_susi: UnivPredictResult
    target_jeongsi: UnivPredictResult
    baseline_susi: UnivPredictResult
    baseline_jeongsi: UnivPredictResult
    cost_points: int
    remaining_points: int


# --- 커뮤니티 및 Q&A 스키마 ---
class QAPostCreate(BaseModel):
    student_id: int
    subject: str
    title: str
    content: str
    reward_points: int

class QACommentCreate(BaseModel):
    student_id: int
    content: str

class QACommentResponse(BaseModel):
    id: int
    post_id: int
    student_id: int
    student_name: Optional[str] = None
    content: str
    is_accepted: bool
    created_at: datetime

    class Config:
        from_attributes = True

class QAPostResponse(BaseModel):
    id: int
    student_id: int
    student_name: Optional[str] = None
    subject: str
    title: str
    content: str
    reward_points: int
    is_resolved: bool
    created_at: datetime
    comments: List[QACommentResponse] = []

    class Config:
        from_attributes = True


# --- 과외 매칭 스키마 ---
class TutorRequestCreate(BaseModel):
    student_id: int
    subject: str
    budget: str
    details: str

class TutorRequestResponse(BaseModel):
    id: int
    student_id: int
    student_name: Optional[str] = None
    subject: str
    budget: str
    details: str
    created_at: datetime

    class Config:
        from_attributes = True

class ProposalCreate(BaseModel):
    tutor_id: int
    request_id: int
    message: str

class ProposalResponse(BaseModel):
    id: int
    tutor_id: int
    tutor_name: Optional[str] = None
    tutor_univ: Optional[str] = None
    tutor_major: Optional[str] = None
    message: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
