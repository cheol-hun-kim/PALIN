from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./dev.db")

# Render.com provides postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Supabase Pooler 포트 5432(세션모드 타임아웃) -> 6543(트랜잭션모드 안정연결) 자동 최적화
if "pooler.supabase.com:5432" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("pooler.supabase.com:5432", "pooler.supabase.com:6543")

# Supabase 연결에 필수적인 sslmode=require 보장
if not DATABASE_URL.startswith("sqlite"):
    if "sslmode=" not in DATABASE_URL:
        sep = "&" if "?" in DATABASE_URL else "?"
        DATABASE_URL = f"{DATABASE_URL}{sep}sslmode=require"

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
else:
    # Supabase PgBouncer Pooler 공식 권장 설정 (server didn't return client encoding 해결)
    connect_args = {
        "sslmode": "require",
        "connect_timeout": 15,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5
    }
    
    # Supabase 트랜잭션 풀러(6543)와 SQLAlchemy 이중 풀링 충돌 방지 -> NullPool 사용 (공식 권장)
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        poolclass=NullPool,
        pool_pre_ping=True
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DB 세션 의존성 주입용 헬퍼
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
