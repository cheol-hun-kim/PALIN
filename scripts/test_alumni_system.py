# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app import models
from app.main import graduate_student_with_alumni_badges, toggle_student_alumni_badge, get_student_alumni_badges, StudentGraduatePayload, BadgeTogglePayload

db = SessionLocal()

print("=== TESTING ALUMNI GRADUATION & BADGES ===")

# Test on student ID 304
s = db.query(models.Student).get(304)
if s:
    print(f"Found student {s.id}: {s.name} ({s.high_school})")
    
    # 1. Graduate student
    payload = StudentGraduatePayload(
        passed_univ="연세대학교",
        passed_major="의예과",
        admission_track="JEONGSI",
        verify_academy=True,
        verify_school=True,
        verify_univ=True
    )
    res = graduate_student_with_alumni_badges(304, payload, db)
    print("1. Graduation Result:")
    print(f"   Message: {res['message']}")
    print(f"   Badges: {res['badges']}")

    # 2. Verify TutorProfile created
    tutor = db.query(models.TutorProfile).filter(models.TutorProfile.student_id == 304).first()
    if tutor:
        print(f"2. TutorProfile: ID={tutor.id}, Univ={tutor.university}, Major={tutor.major}, Track={tutor.admission_track}, Verified={tutor.is_verified}")

    # 3. Toggle off school badge
    t_res = toggle_student_alumni_badge(304, BadgeTogglePayload(badge_type="SCHOOL", is_equipped=False), db)
    print("3. Toggle SCHOOL badge to False:")
    print(f"   Badges: {t_res['badges']}")

    # 4. Toggle back on
    t_res2 = toggle_student_alumni_badge(304, BadgeTogglePayload(badge_type="SCHOOL", is_equipped=True), db)
    print("4. Toggle SCHOOL badge back to True:")
    print(f"   Badges: {t_res2['badges']}")

    # 5. Fetch badges endpoint
    b_res = get_student_alumni_badges(304, db)
    print(f"5. Final Badges API response: is_alumni={b_res['is_alumni']}, badges={b_res['badges']}")

db.close()
print("=== TEST COMPLETED SUCCESSFULLY ===")
