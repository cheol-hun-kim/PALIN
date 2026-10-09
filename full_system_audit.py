# -*- coding: utf-8 -*-
import sys, json, time, urllib.request
from sqlalchemy import text
from app.database import engine, SessionLocal
import app.models as models
from app.ai import ask_ai_chatbot

sys.stdout.reconfigure(encoding='utf-8')

print("=====================================================")
print("🚀 PALIN OS / PASS-MATE FULL SYSTEM DIAGNOSTIC SUITE")
print("=====================================================")

# 1. Database Connection & Data Integrity
print("\n[1. DATABASE LAYER (Supabase Pro)]")
try:
    with engine.connect() as conn:
        val = conn.execute(text("SELECT 1")).scalar()
        db_type = engine.dialect.name
        tables = [r[0] for r in conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")).fetchall()]
        print(f"✅ Engine Ping: {val} (Dialect: {db_type})")
        print(f"✅ Total PostgreSQL Tables: {len(tables)} tables")
        
    db = SessionLocal()
    st_count = db.query(models.Student).count()
    ilwon_count = db.query(models.Student).filter(models.Student.academy_code == "ILWON").count()
    parent_count = db.query(models.Parent).count()
    voc_count = db.query(models.Feedback).count()
    exam_count = db.query(models.ExamMaterial).count()
    tutor_count = db.query(models.TutorProfile).count()
    schedule_count = db.query(models.AdminSchedule).count()
    
    print(f"✅ Total Students: {st_count} (Ilwon Academy: {ilwon_count})")
    print(f"✅ Total Parents: {parent_count}")
    print(f"✅ VOC Feedbacks: {voc_count}")
    print(f"✅ Exam Materials: {exam_count}")
    print(f"✅ Tutors Registered: {tutor_count}")
    print(f"✅ Director Schedules: {schedule_count}")
    db.close()
except Exception as e:
    print(f"❌ DB Diagnostic Error: {e}")

# 2. AI Chatbot Matrix Test (All Tiers & Roles)
print("\n[2. AI MATRIX & TIER INTEGRATION (Gemini 3.8 Flash)]")
test_cases = [
    ("Tier 1 Free Student", {"message": "공부 계획 어떻게 짜요?", "tenant_tier": 1, "user_role": "STUDENT", "school_level": "HIGH"}),
    ("Tier 2 Compact Student", {"message": "9모 68점인데 어떡해요?", "tenant_tier": 2, "user_role": "STUDENT", "school_level": "HIGH"}),
    ("Tier 3 Enterprise Student", {"message": "수능 국어 1등급 비결 알려주세요.", "tenant_tier": 3, "user_role": "STUDENT", "school_level": "HIGH"}),
    ("Tier 4 Founder Student", {"message": "원장님 9모 68점 맞고 멘탈 나갔어요.", "tenant_tier": 4, "user_role": "STUDENT", "school_level": "HIGH"}),
    ("Elementary Pero", {"message": "오늘 구구단 다 외웠어!", "tenant_tier": 1, "user_role": "STUDENT", "school_level": "ELEMENTARY"}),
    ("Middle School Coach", {"message": "외대부고 가려면 내신 어떻게 챙겨야 해?", "tenant_tier": 1, "user_role": "STUDENT", "school_level": "MIDDLE"}),
    ("High Parent Anti-Marketing", {"message": "아이가 성적이 안 나와서 추가 과외를 시켜야 할까요?", "tenant_tier": 4, "user_role": "PARENT", "school_level": "HIGH"}),
    ("Director AI Cockpit", {"message": "원장 캘린더 등록 어떻게 하나요?", "tenant_tier": 4, "user_role": "DIRECTOR", "school_level": "HIGH"})
]

for label, params in test_cases:
    t0 = time.time()
    try:
        reply = ask_ai_chatbot(
            message=params["message"],
            history=[],
            tenant_tier=params.get("tenant_tier", 3),
            user_role=params.get("user_role", "STUDENT"),
            school_level=params.get("school_level", "HIGH")
        )
        elapsed = time.time() - t0
        print(f"  ✅ {label} ({elapsed:.2f}s, {len(reply)}자) -> {reply[:45].strip()}...")
    except Exception as e:
        print(f"  ❌ {label} Error: {e}")

# 3. Live Render.com Server Health
print("\n[3. LIVE RENDER PRODUCTION DEPLOYMENT]")
try:
    req = urllib.request.Request("https://palin-os.onrender.com/api/debug/db-status", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
        print(f"✅ Live Web Server Host: https://palin-os.onrender.com")
        print(f"✅ Live DB Engine Dialect: {data.get('engine_dialect')}")
        print(f"✅ Live DB Host Target: {data.get('db_host')}")
        print(f"✅ Live Queried Students: {data.get('student_count')} students")
        print(f"✅ Live Server Health Status: {data.get('status')}")
except Exception as e:
    print(f"❌ Live Server Health Error: {e}")
