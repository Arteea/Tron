from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI, Depends, Query
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import add_pagination,Page,Params
from app.config import settings
from . import models,schemas
from .database import engine,get_database
from sqlalchemy.orm import Session

from tronpy import Tron


client = Tron(network=settings.TRON_NETWORK)

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title='Tron Info API',
    description = 'API для получения информации кошелька сети Tron')


@app.post("/get_wallet_info/", response_model = schemas.WalletInfoResponse)
def get_wallet_info(request: schemas.WalletBase,
                    db: Session = Depends(get_database)):
    account = client.get_account(request.address)
    account_energy = account.get("account_resource", {}).get("energy_usage", 0)
    balance = client.get_account_balance(request.address)
    bandwidth = client.get_bandwidth(request.address)

    try:
        db_request = models.WalletInfo(address = request.address)
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
    except Exception as e:
        return {'Exception': e}


    return schemas.WalletInfoResponse(
        address= request.address,
        balance = balance,
        bandwidth = bandwidth,
        energy = account_energy)



@app.get("/get_list_of_wallets/",response_model = Page[schemas.WalletLogInfo])
def get_list_of_wallets(db: Session = Depends(get_database),
                        page: int = Query(1,ge=0),
                        size: int = Query(2)) -> list:
    query = db.query(models.WalletInfo).order_by(models.WalletInfo.time_stamp.desc())
    return paginate(query, params=Params(page=page, size=size))

add_pagination(app)