from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import WalletBase,WalletInfoResponse
from typing import Annotated
from fastapi import Depends,HTTPException
from tronpy import AsyncTron
from .database import get_database
from .models import WalletInfo
from sqlalchemy.exc import SQLAlchemyError



async def verify_tron_client(client:AsyncTron):
    if not isinstance(client,AsyncTron):
        raise TypeError("Переданный аргумент не является объектом клиента Tron")
    return client



async def get_account_details(wallet: WalletBase,
                        client: Annotated[AsyncTron, Depends(verify_tron_client)]
                        ) -> WalletInfoResponse:
    
    account = await client.get_account(wallet.address)
    energy = account.get("account_resource", {}).get("energy_usage", 0)
    balance = await client.get_account_balance(wallet.address)
    bandwidth = await client.get_bandwidth(wallet.address)

    return WalletInfoResponse(address=wallet.address,
                              balance=balance,
                              bandwidth=bandwidth,
                              energy=energy)


async def log_to_database(wallet: WalletBase,database: AsyncSession = Depends(get_database)) ->bool:
    try:
        db_request = WalletInfo(address = wallet.address)
        database.add(db_request)
        await database.commit()
        await database.refresh(db_request)
        return True
    except SQLAlchemyError as e:
        await database.rollback()
        raise HTTPException(status_code=500,detail={"message": f"Произошла ошибка базы данных: {e}"})
    except Exception as e:
        await database.rollback()
        raise HTTPException(status_code=500,detail={"message": f"Произошла ошибка на сервере: {e}"})
    
