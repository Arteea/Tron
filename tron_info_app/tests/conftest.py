import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))


from tronpy import AsyncTron
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import WalletInfo,Base


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