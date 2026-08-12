import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Student, Parent, TutorProfile, QAPost, PointHistory, PlannerBlock

# 기존 SQLite 파일 삭제하여 마이그레이션 효과 (테이블 스키마 리셋)
DB_FILE = "dev.db"
if os.path.exists(DB_FILE):
    try:
        # 데이터베이스 커넥션 닫힌 상태에서 안전하게 삭제하기 위해 커넥션 풀을 리셋
        engine.dispose()
        os.remove(DB_FILE)
        print("Successfully deleted old database file.")
    except Exception as e:
        print(f"Warning: Could not remove old database: {e}")

print("Recreating database tables for seed...")
Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

try:
    print("Clearing existing data...")
    db.query(PointHistory).delete()
    db.query(QAPost).delete()
    db.query(PlannerBlock).delete()
    db.query(TutorProfile).delete()
    db.query(Student).delete()
    db.query(Parent).delete()
    db.commit()

    print("Inserting seed data...")

    # 1. Create Parent
    parent = Parent(
        id=1,
        name="김철수(부모)",
        phone="010-1234-5678",
        is_premium_subscribed=False
    )
    db.add(parent)
    db.flush()

    # 2. Create Student
    student = Student(
        id=1,
        email="student@test.com",
        name="홍길동",
        phone="010-9876-5432",
        grade=3,
        region="서울 강남구",
        high_school="대치고",
        target_univ="연세대학교 신소재공학과",
        baseline_univ="국민대학교 신소재공학과",
        current_points=100,
        parent_id=parent.id
    )
    db.add(student)
    db.flush()

    # 3. Create Point History
    point_history = PointHistory(
        student_id=1,
        amount=100,
        description="가입 환영 포인트 지급"
    )
    db.add(point_history)

    # 4. Create Tutor Profiles with emblems (Windows 콘솔 인코딩을 위해 이모지 대신 명확한 텍스트 배지 정보 입력)
    tutor1 = TutorProfile(
        id=1,
        email="tutor1@test.com",
        name="김선배",
        phone="010-1111-2222",
        university="서울대학교",
        major="의예과",
        admission_year=25,
        high_school_type="일반고",
        bio="의대생 선배의 확실한 수학/과학 밀착 케어 약속드립니다.",
        contact_link="https://open.kakao.com/o/sSNU1_SN",
        is_verified=True,
        univ_emblem="[서울대 의예 의학배지]",
        high_school_emblem="[대치고]"
    )
    tutor2 = TutorProfile(
        id=2,
        email="tutor2@test.com",
        name="이선배",
        phone="010-3333-4444",
        university="연세대학교",
        major="신소재공학과",
        admission_year=24,
        high_school_type="자사고",
        bio="목표 대학 합격을 위한 내신 다지기 및 자소서 상담 환영!",
        contact_link="https://open.kakao.com/o/sSNU2_SN",
        is_verified=True,
        univ_emblem="[연세대 신소재 🦅]",
        high_school_emblem="[경기고]"
    )
    db.add(tutor1)
    db.add(tutor2)

    # 5. Create Q&A Posts
    post1 = QAPost(
        student_id=1,
        subject="수학",
        title="수학2 극대 극소 개념이 헷갈려요.",
        content="3차함수 극대 극소를 판정할 때 도함수 부호 변화 외에 기하적으로 쉽게 보는 방법이 있나요? 팁 부탁드립니다.",
        reward_points=50,
        is_resolved=False
    )
    db.add(post1)

    # 6. Create initial Planner Blocks (Everytime-style timetable testing)
    # day_of_week: 0=월, 1=화, 2=수, 3=목, 4=금, 5=토, 6=일
    pb1 = PlannerBlock(
        student_id=1,
        day_of_week=0,  # 월요일
        start_time="09:00",
        end_time="11:30",
        title="수학 모의고사 실전 연습",
        is_completed=False
    )
    pb2 = PlannerBlock(
        student_id=1,
        day_of_week=2,  # 수요일
        start_time="14:00",
        end_time="15:30",
        title="영어 연계교재 지문 분석",
        is_completed=False
    )
    pb3 = PlannerBlock(
        student_id=1,
        day_of_week=4,  # 금요일
        start_time="19:00",
        end_time="21:00",
        title="국어 비문학 과학/기술 오답",
        is_completed=False
    )
    db.add(pb1)
    db.add(pb2)
    db.add(pb3)

    db.commit()
    print("Seed data loaded successfully (including planner blocks & tutor emblems)!")

except Exception as e:
    db.rollback()
    # 인코딩 안전 출력
    try:
        print(f"Error during seeding: {str(e)}")
    except Exception:
        print("Error during seeding (failed to print detail due to encoding).")
finally:
    db.close()
