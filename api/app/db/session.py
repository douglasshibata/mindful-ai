import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

DB_URL = settings.DATABASE_URL
if DB_URL.startswith("postgresql://"):
    ASYNC_DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://")
    SYNC_DB_URL = DB_URL
elif DB_URL.startswith("postgresql+asyncpg://"):
    ASYNC_DB_URL = DB_URL
    SYNC_DB_URL = DB_URL.replace("postgresql+asyncpg://", "postgresql://")
elif DB_URL.startswith("sqlite+aiosqlite://"):
    ASYNC_DB_URL = DB_URL
    SYNC_DB_URL = DB_URL.replace("sqlite+aiosqlite://", "sqlite://")
elif DB_URL.startswith("sqlite:///"):
    SYNC_DB_URL = DB_URL
    ASYNC_DB_URL = DB_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
else:
    ASYNC_DB_URL = DB_URL
    SYNC_DB_URL = DB_URL

sync_engine = create_engine(
    SYNC_DB_URL,
    connect_args={"check_same_thread": False} if SYNC_DB_URL.startswith("sqlite") else {},
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

async_engine = create_async_engine(
    ASYNC_DB_URL,
    connect_args={"check_same_thread": False} if ASYNC_DB_URL.startswith("sqlite") else {},
    pool_pre_ping=True
)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
