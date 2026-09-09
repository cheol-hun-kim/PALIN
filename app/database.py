# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool, NullPool
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

# 4. SQLite 로컬 엔진 (Thread-safe & 30s timeout)
sqlite_engine = create_engine(
    f"sqlite:///{DEFAULT_DB_PATH}",
    connect_args={"check_same_thread": False, "timeout": 30}
)
SqliteSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)

engine = sqlite_engine
SessionLocal = SqliteSessionLocal

# 5. PostgreSQL Strict Mode & Connection Pooling
if not DATABASE_URL.startswith("sqlite"):
    try:
        # High-concurrency QueuePool for Supabase/PostgreSQL
        pg_engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_size=20,
            max_overflow=10,
            pool_recycle=1800,
            pool_pre_ping=True,
            pool_timeout=15,
            connect_args={"connect_timeout": 15}
        )
        with pg_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine = pg_engine
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pg_engine)
        print("[DB] PostgreSQL Live Supabase Connection Succeeded 100% (Strict Mode & QueuePool Active)!")
    except Exception as e:
        print(f"[DB CRITICAL ERROR] PostgreSQL Connection Failed: {e}. Strict mode active (NO SILENT FALLBACK).")
        engine = pg_engine
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pg_engine)

Base = declarative_base()

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()
