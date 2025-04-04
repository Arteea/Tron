from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI, Depends, Query
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import add_pagination,Page,Params
from app.config import settings
from . import models,schemas
from .database import engine,get_database
from sqlalchemy.orm import Session

from .services import get_account_details,log_to_database

from tronpy import Tron


client = Tron(network=settings.TRON_NETWORK)

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title='Tron Info API',
    description = 'API для получения информации кошелька сети Tron')


@app.post("/get_wallet_info/", response_model = schemas.WalletInfoResponse)
def get_wallet_info(wallet: schemas.WalletBase,
                    db: Session = Depends(get_database)):
    
    #Получаем данные кошелька
    wallet_info = get_account_details(wallet=wallet,client=client)
    #Записываем запрос в базу данных
    log_to_database(wallet=wallet,database=db)
    
    return wallet_info



@app.get("/get_list_of_wallets/",response_model = Page[schemas.WalletLogInfo])
def get_list_of_wallets(db: Session = Depends(get_database),
                        page: int = Query(1,ge=0),
                        size: int = Query(2)):

    query = db.query(models.WalletInfo).order_by(models.WalletInfo.time_stamp.desc())

    return paginate(query, params=Params(page=page, size=size))

add_pagination(app)