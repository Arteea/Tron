import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))


from tronpy import AsyncTron
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import WalletInfo,Base
from app.database import get_database
from fastapi.testclient import TestClient
from app.main import app


@pytest_asyncio.fixture
async def tron_client():
    with AsyncTron(network="shasta") as tron_client:
        yield tron_client



@pytest_asyncio.fixture
async def get_db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:",future=True,connect_args={"check_same_thread": False})
    async with engine.begin() as conn:
        await conn.run_sync(WalletInfo.metadata.create_all)
    
    AsyncSessionTest = sessionmaker(bind=engine,expire_on_commit=False,class_=AsyncSession)
    
    async with AsyncSessionTest() as test_session:
        yield test_session
        await test_session.close()

@pytest_asyncio.fixture
async def test_client(get_db_session):

    async def override_get_database():
        return get_db_session
    
    app.dependency_overrides[get_database] = override_get_database

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()