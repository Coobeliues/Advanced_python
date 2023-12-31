import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from your_module_path.userServices import edit_personal_info, check_company, get_info

# Replace 'your_module_path' with the actual path where your userServices.py module is located
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
async def test_edit_personal_info(db_session, mocker):
    # Mock the DB.execute function
    mocker.patch("your_module_path.userServices.DB.execute", return_value=None)

    # Mock the get_user_information function
    mocker.patch("your_module_path.userServices.get_user_information", return_value={"user_id": 1, "username": "testuser"})

    user_data = {"user_id": 1, "datas_from_users": {"firstname": "John", "lastname": "Doe"}, "is_done": False, "confirmed": False}
    
    response = await edit_personal_info(user_data)

    # Add assertions or checks based on the expected behavior of the edit_personal_info function
    assert response is None


@pytest.mark.asyncio
async def test_check_company():
    # You can write test cases for the check_company function based on your actual implementation
    pass


@pytest.mark.asyncio
async def test_get_info(db_session, mocker):
    # Mock the kafka.produce and kafka.consume functions
    mocker.patch("your_module_path.userServices._kafka.produce", return_value=None)
    mocker.patch("your_module_path.userServices._kafka.consume", side_effect=[{"bin": "12345"}])

    # Mock the get_data, generate_pdf, sent_to_email, and sent_to_telegram functions
    mocker.patch("your_module_path.userServices.get_data", return_value={"key": "value"})
    mocker.patch("your_module_path.userServices.generate_pdf", return_value=None)
    mocker.patch("your_module_path.userServices.sent_to_email", return_value=None)
    mocker.patch("your_module_path.userServices.sent_to_telegram", return_value=None)

    request_data = {"bin": "12345", "username": "testuser"}

    response = await get_info(request_data)

    # Add assertions or checks based on the expected behavior of the get_info function
    assert response is None
