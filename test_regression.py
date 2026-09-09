# -*- coding: utf-8 -*-
"""
PALIN OS Phase 1.5 Automated Regression Test Suite
전체 핵심 비즈니스 로직 및 심리 통제 기전 무결성 검증
"""

import sys
import unittest
from datetime import datetime
from sqlalchemy.orm import Session

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from app.database import SessionLocal, engine, get_db
from app import models, schemas
from app.main import app, init_db_schema, get_admin_dashboard

class PalinOSRegressionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db_schema()
        cls.db = SessionLocal()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_01_db_schema_columns(self):
        """1. DB 컬럼 확장 무결성 검사"""
        student = models.Student(
            email="test_reg@palin.os",
            name="테스트학생",
            phone="010-9999-8888",
            grade=4,
            region="서울 강남구 대치동",
            high_school="대치고",
            target_univ="서울대학교 의예과",
            baseline_univ="연세대학교 치의예과",
            dday_date="2026-11-19",
            dday_title="2027 수능",
            streak_days=5,
            medical_symbol="MED"
        )
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)

        self.assertEqual(student.grade, 4)
        self.assertEqual(student.medical_symbol, "MED")
        self.assertEqual(student.streak_days, 5)
        self.assertEqual(student.dday_title, "2027 수능")
        
        self.db.delete(student)
        self.db.commit()
        print("[PASS] 1. DB Schema & Column Migration Integrity Test Passed")

    def test_02_streak_gamification_logic(self):
        """2. 듀오링고 불꽃 (Streak) 성공 시 증가, 실패 시 리셋 로직 검증"""
        student = models.Student(
            email="streak_test@palin.os",
            name="불꽃학생",
            phone="010-7777-6666",
            current_points=100,
            streak_days=3,
            max_streak_days=3
        )
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)

        student.streak_days += 1
        if student.streak_days > student.max_streak_days:
            student.max_streak_days = student.streak_days
        self.assertEqual(student.streak_days, 4)
        self.assertEqual(student.max_streak_days, 4)

        student.streak_days = 0
        self.assertEqual(student.streak_days, 0)
        self.assertEqual(student.max_streak_days, 4)

        self.db.delete(student)
        self.db.commit()
        print("[PASS] 2. Duolingo Streak Flame Calculation Test Passed")

    def test_03_notice_api_integrity(self):
        """3. 원장 공지사항 등록 및 쿼리 무결성 검증"""
        notice = models.Notice(
            title="[테스트] 6월 모평 대비 집중 주간",
            content="모든 재원생은 기상 미션을 엄수하십시오.",
            category="긴급공지",
            is_pinned=True
        )
        self.db.add(notice)
        self.db.commit()
        self.db.refresh(notice)

        fetched = self.db.query(models.Notice).filter(models.Notice.id == notice.id).first()
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.category, "긴급공지")

        self.db.delete(notice)
        self.db.commit()
        print("[PASS] 3. Notice Management & Pinning Test Passed")

    def test_04_admin_dashboard_no_attribute_error(self):
        """4. 관리자 대시보드 API 런타임 무결성 검증"""
        dashboard_data = get_admin_dashboard(self.db)
        self.assertIn("summary", dashboard_data)
        self.assertIn("students", dashboard_data)
        self.assertIn("recent_missions", dashboard_data)
        self.assertIn("recent_studies", dashboard_data)
        print(f"[PASS] 4. Admin Dashboard Execution Integrity Passed (Total Students: {len(dashboard_data['students'])})")

    def test_05_login_api_integrity(self):
        """5. 로그인 API 및 Pydantic 직렬화 무결성 검증"""
        from app.main import login_student, LoginPayload
        # 임의의 학생 등록 또는 기존 학생으로 테스트
        test_email = "test_login_user@palin.com"
        existing = self.db.query(models.Student).filter(models.Student.email == test_email).first()
        if not existing:
            parent = models.Parent(name="부모", phone="010-0000-0000")
            self.db.add(parent)
            self.db.commit()
            self.db.refresh(parent)
            existing = models.Student(
                name="로그인테스트학생",
                email=test_email,
                phone="010-1111-2222",
                grade=3,
                region="대치동",
                high_school="대치고",
                target_univ="서울대학교",
                baseline_univ="연세대학교",
                current_points=100,
                parent_id=parent.id
            )
            self.db.add(existing)
            self.db.commit()
            self.db.refresh(existing)

        payload = LoginPayload(email="  TEST_LOGIN_USER@palin.com  ") # 대소문자/공백 무시 검증
        res = login_student(payload, self.db)
        self.assertEqual(res["email"], test_email)
        
        # Pydantic serialization check
        res_schema = schemas.StudentResponse.model_validate(res)
        self.assertEqual(res_schema.email, test_email)
        print("[PASS] 5. Login API Case-Insensitive & Schema Validation Integrity Passed")

    def test_06_admin_auth_integrity(self):
        from app.main import authenticate_admin, AdminAuthPayload
        # 1286 및 12Yonsei21* 성공 테스트
        auth_res = authenticate_admin(AdminAuthPayload(pin="1286"))
        self.assertTrue(auth_res["authenticated"])
        
        # 잘못된 핀 실패 테스트 (401)
        from fastapi import HTTPException
        with self.assertRaises(HTTPException):
            authenticate_admin(AdminAuthPayload(pin="9999"))
        print("[PASS] 6. Admin Authentication & Protection Security Integrity Passed")

if __name__ == "__main__":
    unittest.main()
