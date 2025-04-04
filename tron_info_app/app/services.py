from sqlalchemy.orm import Session
from .schemas import WalletBase,WalletInfoResponse
from typing import Annotated
from fastapi import Depends,HTTPException
from tronpy import Tron
from .database import get_database
from .models import WalletInfo
from sqlalchemy.exc import SQLAlchemyError



def verify_tron_client(client:Tron):
    if not isinstance(client,Tron):
        raise TypeError("Переданный аргумент не является объектом клиента Tron")
    return client



def get_account_details(wallet: WalletBase,
                        client: Annotated[Tron, Depends(verify_tron_client)]
                        ) -> WalletInfoResponse:
    
    account = client.get_account(wallet.address)
    energy = account.get("account_resource", {}).get("energy_usage", 0)
    balance = client.get_account_balance(wallet.address)
    bandwidth = client.get_bandwidth(wallet.address)

    return WalletInfoResponse(address=wallet.address,
                              balance=balance,
                              bandwidth=bandwidth,
                              energy=energy)


def log_to_database(wallet: WalletBase,database: Session = Depends(get_database)) ->bool:
    try:
        db_request = WalletInfo(address = wallet.address)
        database.add(db_request)
        database.commit()
        database.refresh(db_request)
    except SQLAlchemyError as e:
        database.rollback()
        raise HTTPException(status_code=500,detail={"message": f"Произошла ошибка базы данных: {e}"})
    except Exception as e:
        database.rollback()
        raise HTTPException(status_code=500,detail={"message": f"Произошла ошибка на сервере: {e}"})
    
