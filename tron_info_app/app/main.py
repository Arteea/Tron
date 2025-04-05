from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI, Depends, Query
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import add_pagination,Page,Params
from app.config import settings
from . import models,schemas
from .database import engine,get_database,lifespan
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession,AsyncEngine
from sqlalchemy.future import select
from sqlalchemy import desc
from .services import get_account_details,log_to_database

from tronpy import AsyncTron


client = AsyncTron(network=settings.TRON_NETWORK)




app = FastAPI(lifespan=lifespan,
    title='Tron Info API',
    description = 'API для получения информации кошелька сети Tron')

@app.post("/get_wallet_info/", response_model = schemas.WalletInfoResponse)
async def get_wallet_info(wallet: schemas.WalletBase,
                    db: AsyncSession = Depends(get_database)):
    

    wallet_info =await get_account_details(wallet=wallet,client=client)

    await log_to_database(wallet=wallet,database=db)    
    return wallet_info



@app.get("/get_list_of_wallets/",response_model = Page[schemas.WalletLogInfo])
async def get_list_of_wallets(db: AsyncSession = Depends(get_database),
                        page: int = Query(1,ge=0),
                        size: int = Query(2)):

    # query = db.query(models.WalletInfo).order_by(models.WalletInfo.time_stamp.desc())

    query = select(models.WalletInfo).order_by(desc(models.WalletInfo.time_stamp))
    return await paginate(db,query, params=Params(page=page, size=size))

add_pagination(app)