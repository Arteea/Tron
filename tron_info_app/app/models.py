from sqlalchemy import Column,Integer,String,DateTime,Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class WalletInfo(Base):

    __tablename__ = "tron_wallet_info"

    id = Column(Integer,primary_key=True, index=True)
    address = Column(String(34), index=True)
    time_stamp = Column(DateTime,server_default=func.now(), onupdate=func.now())
    # balance = Column(Numeric(32,6))
    # bandwidth = Column(Integer, default=0)
    # energy = Column(Integer,default=0)
