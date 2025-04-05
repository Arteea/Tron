from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,AsyncEngine
from sqlalchemy.orm import sessionmaker
from .config import settings
from .models import Base
from fastapi import FastAPI
from contextlib import asynccontextmanager

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Логирование SQL-запросов
    future=True,
    connect_args={
        "check_same_thread": False  # Только для SQLite
    } if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

AsyncSessionLocal = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

async def init_database(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database(engine)
    app.state.engine = engine
    yield
    await engine.dispose()


async def get_database():
    async with AsyncSessionLocal() as database:
        try:
            yield database
        finally:
            database.close()
