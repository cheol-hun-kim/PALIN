# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "palin_data.db").replace(os.sep, "/")
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

# 1. postgres:// -> postgresql:// 변환 (Heroku / Render 호환)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 2. Supabase Pooler 포트 5432 -> 6543 자동 치환 (PgBouncer IPv4 안정성 보장)
if "pooler.supabase.com:5432" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("pooler.supabase.com:5432", "pooler.supabase.com:6543")

# 3. PostgreSQL 연결 시 SSL 모드 강제 보장
if not DATABASE_URL.startswith("sqlite"):
    if "sslmode=" not in DATABASE_URL:
        sep = "&" if "?" in DATABASE_URL else "?"
        DATABASE_URL = f"{DATABASE_URL}{sep}sslmode=require"

# 4. 환경별 엔진 생성
sqlite_engine = create_engine(
    f"sqlite:///{DEFAULT_DB_PATH}",
    connect_args={"check_same_thread": False}
)
SqliteSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)

if DATABASE_URL.startswith("sqlite"):
    engine = sqlite_engine
    SessionLocal = SqliteSessionLocal
else:
    try:
        engine = create_engine(
            DATABASE_URL,
            poolclass=NullPool,
            pool_pre_ping=True
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    except Exception as e:
        print(f"[DB] Primary PostgreSQL Engine Init Failed ({e}), falling back to SQLite.")
        engine = sqlite_engine
        SessionLocal = SqliteSessionLocal

Base = declarative_base()

def get_db():
    db = None
    try:
        db = SessionLocal()
    except Exception as e:
        print(f"[DB] Session connection error ({e}), switching to fallback SQLite.")
        db = SqliteSessionLocal()
    try:
        yield db
    finally:
        if db:
            db.close()
