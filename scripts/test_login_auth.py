# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app import models, schemas
from app.main import handle_role_login, login_student, LoginPayload

db = SessionLocal()
s = db.query(models.Student).first()
print("Test student:", s.id, s.name, s.email)

print("\n--- Testing login_student ---")
try:
    res = login_student(LoginPayload(email=s.email), db)
    print("login_student OK:", res.get("id"), res.get("name"))
except Exception as e:
    import traceback
    print("login_student FAIL:", traceback.format_exc())

print("\n--- Testing handle_role_login ---")
try:
    role_res = handle_role_login(schemas.RoleLoginRequest(email=s.email, login_type="STUDENT", password=""), db)
    print("handle_role_login OK:", role_res)
except Exception as e:
    import traceback
    print("handle_role_login FAIL:", traceback.format_exc())

db.close()
