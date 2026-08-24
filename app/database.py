from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
import traceback

RAW_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./palin_data.db")

def build_engine(url_str: str):
    if url_str.startswith("postgres://"):
        url_str = url_str.replace("postgres://", "postgresql://", 1)
        
    if url_str.startswith("sqlite"):
        return create_engine(url_str, connect_args={"check_same_thread": False})
    else:
        # PostgreSQL / Supabase
        connect_args = {
            "connect_timeout": 10,
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5
        }
        if "sslmode=" not in url_str:
            sep = "&" if "?" in url_str else "?"
            url_str = f"{url_str}{sep}sslmode=require"
            
        return create_engine(
            url_str,
            connect_args=connect_args,
            poolclass=NullPool,
            pool_pre_ping=True
        )

# 1차 시도: 환경변수 DATABASE_URL
engine = None
is_postgres_active = False

if not RAW_DATABASE_URL.startswith("sqlite"):
    try:
        candidate_engine = build_engine(RAW_DATABASE_URL)
        with candidate_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine = candidate_engine
        is_postgres_active = True
        print("✅ [DATABASE] PostgreSQL (Supabase) Database Connected Successfully!")
    except Exception as pg_err:
        print(f"⚠️ [DATABASE WARNING] PostgreSQL connection failed ({pg_err}). Falling back to robust SQLite engine...")
        engine = build_engine("sqlite:///./palin_data.db")
else:
    engine = build_engine(RAW_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DB 세션 의존성 주입용 헬퍼 (무중단 세션 보장)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
