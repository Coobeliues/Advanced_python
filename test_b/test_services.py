import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from your_module_path.services import (
    sent_to_email,
    sent_to_telegram,
    get_data,
    check_company_by_bin,
    get_datas,
    create_access_token,
    get_current_user,
    get_user_information,
    check_is_done,
    generate_pdf,
)
from your_module_path.model import UserRead, TokenData

# Replace 'your_module_path' with the actual path where your services.py module is located
# Replace 'your_database_url' with the actual database URL for testing
DATABASE_URL = "your_database_url"


@pytest.fixture
def engine():
    return create_async_engine(DATABASE_URL)


@pytest.fixture
async def db_session(engine):
    async with engine.begin() as conn:
        # Add code to initialize your database schema (if necessary)
        pass
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


@pytest.mark.asyncio
async def test_sent_to_email(db_session, mocker):
    # Mock the send_email function
    mocker.patch("your_module_path.services.send_email", return_value=None)

    username = "testuser"
    await sent_to_email(username)

    # Add assertions or checks based on the behavior of the send_email function


@pytest.mark.asyncio
async def test_sent_to_telegram(db_session, mocker):
    # Mock the send_pdf_bot function
    mocker.patch("your_module_path.services.send_pdf_bot", return_value=None)

    username = "testuser"
    await sent_to_telegram(username)

    # Add assertions or checks based on the behavior of the send_pdf_bot function


@pytest.mark.asyncio
async def test_get_data(db_session, mocker):
    # Mock the DB.fetch_one function
    mocker.patch("your_module_path.services.DB.fetch_one", return_value=(None,))

    bin_value = "123456789"
    result = await get_data(bin_value)

    # Add assertions or checks based on the expected behavior of the get_data function


@pytest.mark.asyncio
async def test_check_company_by_bin(mocker):
    # Mock the requests.get function
    mocker.patch("your_module_path.services.requests.get", return_value=mocker.Mock(status_code=200, json=lambda: {"success": True, "obj": {"name": "Company Name"}}))

    bin_value = "123456789"
    lang = "en"
    result = check_company_by_bin(bin_value, lang)

    # Add assertions or checks based on the expected behavior of the check_company_by_bin function


@pytest.mark.asyncio
async def test_get_datas(mocker):
    # Mock the requests.get function
    mocker.patch("your_module_path.services.requests.get", return_value=mocker.Mock(status_code=200, json=lambda: {"obj": {"key": "value"}}))

    bin_iin = "123456789"
    result = get_datas(bin_iin)

    # Add assertions or checks based on the expected behavior of the get_datas function


@pytest.mark.asyncio
async def test_create_access_token():
    data = {"username": "testuser"}
    expires_delta = timedelta(minutes=30)
    token = create_access_token(data, expires_delta)

    # Add assertions or checks based on the expected behavior of the create_access_token function


@pytest.mark.asyncio
async def test_get_current_user():
    # Implement test for get_current_user function using a mocked token

    # Example using mocker:
    # mocker.patch("your_module_path.services.jwt.decode", return_value={"username": "testuser"})
    # token_data = await get_current_user(token="mocked_token")

    # Add assertions or checks based on the expected behavior of the get_current_user function


@pytest.mark.asyncio
async def test_get_user_information(db_session, mocker):
    # Mock the DB.fetch_one function
    mocker.patch("your_module_path.services.DB.fetch_one", return_value=(None,))

    token_data = TokenData(username="testuser")
    user_info = await get_user_information(tokendata=token_data)

    # Add assertions or checks based on the expected behavior of the get_user_information function


@pytest.mark.asyncio
async def test_check_is_done(db_session, mocker):
    # Implement test for check_is_done function

    # Example using mocker:
    # mocker.patch("your_module_path.services.DB.fetch_one", return_value=(None,))
    # mocker.patch("your_module_path.services.DB.fetch_one", return_value=(True,))
    # mocker.patch("your_module_path.services.DB.fetch_one", return_value=(False,))

    # Add assertions or checks based on the expected behavior of the check_is_done function


@pytest.mark.asyncio
async def test_generate_pdf():
    # Implement test for generate_pdf function

    # Add assertions or checks based on the expected behavior of the generate_pdf function
