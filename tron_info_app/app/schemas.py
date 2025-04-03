from pydantic import BaseModel,Field,field_validator
from datetime import datetime

class WalletBase(BaseModel):

    address: str = Field(min_length=34,max_length=34,description="Aдрес кошелька")

    @field_validator("address")
    def check_address(cls,address):
        if not address.startswith('T'):
            raise ValueError("Адрес кошелька Tron должен начинаться с 'T' ")
        return address
        


class WalletInfoResponse(WalletBase):
    balance: float = Field(description="Баланс кошелька")
    bandwidth: int = Field(description="Пропусканая способность Tron")
    energy: int = Field(description="Энергия доступная на кошельке")



class WalletLogInfo(WalletBase):
    id: int = Field(description="Id запроса кошелька")
    time_stamp: datetime = Field(description="Дата запроса")
