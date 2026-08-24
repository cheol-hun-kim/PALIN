from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./dev.db")

# Render.com provides postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Supabase Pooler 포트 5432(세션모드 타임아웃) -> 6543(트랜잭션모드 안정연결) 자동 최적화
if "pooler.supabase.com:5432" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("pooler.supabase.com:5432", "pooler.supabase.com:6543")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {
    "connect_timeout": 10,
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 10,
    "keepalives_count": 5
}

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
else:
    # Supabase / PostgreSQL Connection Pooler 최적화 (ECHECKOUTTIMEOUT 방지)
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30
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
