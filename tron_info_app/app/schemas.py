from pydantic import BaseModel,Field,field_validator
from datetime import datetime

class WalletBase(BaseModel):

    address: str = Field(description="Aдрес кошелька,длина 34 символа,начинается с 'T'")

    @field_validator("address")
    def check_address(cls,address):
        if len(address)!=34:
            raise ValueError('Длина адреса должна быть 34 символа')
        if not address.startswith('T'):
            raise ValueError("Адрес должен начинаться с 'T'")
        if not address[1:].isalnum():
            raise ValueError("Адрес содержит недопустимые символы")
        return address
        


class WalletInfoResponse(WalletBase):
    balance: float = Field(description="Баланс кошелька")
    bandwidth: int = Field(description="Пропусканая способность Tron")
    energy: int = Field(description="Энергия доступная на кошельке")



class WalletLogInfo(WalletBase):
    id: int = Field(description="Id запроса кошелька")
    time_stamp: datetime = Field(description="Дата запроса")
