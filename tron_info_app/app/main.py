from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Response
from app.config import settings
from . import models
from .database import engine




models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title='Tron Info API',
    description = 'API для получения информации кошелька сети Tron')


@app.get("/")
async def root():
    return {
        'message': "TronWalletInfo",
    }
