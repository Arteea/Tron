import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.models import WalletInfo


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_list_of_wallets(test_client, get_db_session: AsyncSession):
    wallets = [
        WalletInfo(address='TWFQMtqXCKFgKeNuoPqJ8Hez8jELULmHi9'),
        WalletInfo(address='TLSgRcoeokT8mSB8Fsm9FYw3bAHmCijLkZ'),
        WalletInfo(address='TFBcc8k2xdGJ9YojJyCryT6o6oe8wHBuqB')
    ]
    get_db_session.add_all(wallets)
    await get_db_session.commit()
    
    response=test_client.get("/get_list_of_wallets/")
    assert response.status_code == 200

    data = response.json()
    assert len(data["items"]) == 2 #Дефолтное значение 2
    assert data["total"] == 3
    assert data["items"][0]["address"] == 'TWFQMtqXCKFgKeNuoPqJ8Hez8jELULmHi9'

    response = test_client.get("/get_list_of_wallets/?page=2&size=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["address"] == "TLSgRcoeokT8mSB8Fsm9FYw3bAHmCijLkZ"

    response = test_client.get("/get_list_of_wallets/?page=-1")
    assert response.status_code == 422

    #Удаляем таблицу и проверяем
    await get_db_session.execute(delete(WalletInfo.__table__))
    await get_db_session.commit()
    response = test_client.get("/get_list_of_wallets/")
    assert response.status_code == 200
    assert response.json()["total"] == 0


