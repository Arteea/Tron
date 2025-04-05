from fastapi import HTTPException
import pytest
from app.schemas import WalletBase
from app.services import log_to_database
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import WalletInfo
from sqlalchemy.exc import SQLAlchemyError


@pytest.mark.unit
@pytest.mark.parametrize("address,is_valid,expected_error", [
    # Валидные адреса
    ("TLSgRcoeokT8mSB8Fsm9FYw3bAHmCijLkZ", True, None),
    # Невалидные адреса
    ("TLSgRcoeokT8mSB8Fsm9FYw3bAHmCijLk", False, "Длина адреса должна быть 34 символа"),  # 33 символа
    ("TLSgRcoeokT8mSB8Fsm9FYw3bAHmCijLkZZ", False, "Длина адреса должна быть 34 символа"), # 35 символов
    ("1LSgRcoeokT8mSB8Fsm9FYw3bAHmCijLkZ", False, "Адрес должен начинаться с 'T'"),              # Неправильный префикс
    ("T!@#gRcoeokT8mSB8Fsm9FYw3bAHmCijLk", False, "Адрес содержит недопустимые символы"),        # Спецсимволы
    ("TLSgRcoeokT8mSB8Fsm9FYw3bAHmCijLk ", False, "Адрес содержит недопустимые символы"),        # Пробел в конце
])
def test_wallet_address_validation(address, is_valid, expected_error):
    if is_valid:
        wallet = WalletBase(address=address)
        assert wallet.address == address
    else:
        with pytest.raises(ValueError) as exc_info:
            WalletBase(address=address)
        assert expected_error in str(exc_info.value)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_log_to_database_success(get_db_session: AsyncSession):
    address='TLSgRcoeokT8mSB8Fsm9FYw3bAHmCijLkZ'
    wallet = WalletBase(address=address)
    result = await log_to_database(wallet=wallet,database=get_db_session)
    
    assert result is True

    record = await get_db_session.get(WalletInfo,1)

    assert record.address == address



@pytest.mark.unit
@pytest.mark.asyncio
async def test_log_to_database_sql_error(get_db_session: AsyncSession, mocker):
    address='TLSgRcoeokT8mSB8Fsm9FYw3bAHmCijLkZ'
    wallet = WalletBase(address=address)
    
    mocker.patch.object(get_db_session, "add", side_effect=SQLAlchemyError("DB error"))

    with pytest.raises(HTTPException) as exc_info:
        await log_to_database(wallet,get_db_session)

    assert exc_info.value.status_code == 500
    assert 'Произошла ошибка базы данных' in str(exc_info.value.detail)

@pytest.mark.unit
@pytest.mark.asyncio
async def test_log_to_database_common_error(get_db_session: AsyncSession, mocker):
    address='TLSgRcoeokT8mSB8Fsm9FYw3bAHmCijLkZ'
    wallet = WalletBase(address=address)
    
    mocker.patch.object(get_db_session, "commit", side_effect=Exception('Server Error'))

    with pytest.raises(HTTPException) as exc_info:
        await log_to_database(wallet,get_db_session)
        
    assert exc_info.value.status_code ==500
    assert 'Произошла ошибка на сервере' in str(exc_info.value.detail)