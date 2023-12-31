import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from your_module_path.teleg import on_startup, on_shutdown, send_pdf_bot, save_username

# Replace 'your_module_path' with the actual path where your teleg.py module is located
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
async def test_on_startup(db_session):
    await on_startup(None)  # Assuming on_startup does not require any parameters


@pytest.mark.asyncio
async def test_on_shutdown(db_session):
    await on_shutdown(None)  # Assuming on_shutdown does not require any parameters


@pytest.mark.asyncio
async def test_send_pdf_bot(mocker):
    # Mock the requests.post function
    mocker.patch("your_module_path.teleg.requests.post", return_value=mocker.Mock(status_code=200, text="Success"))

    chat_id = "123456789"
    await send_pdf_bot(chat_id)

    # Add assertions or checks based on the expected behavior of the send_pdf_bot function


@pytest.mark.asyncio
async def test_save_username(db_session, mocker):
    # Mock the DB.fetch_one and DB.execute functions
    mocker.patch("your_module_path.teleg.DB.fetch_one", return_value=None)
    mocker.patch("your_module_path.teleg.DB.execute", return_value=None)

    username = "testuser"
    user_id = "123456789"
    result = await save_username(username, user_id)

    # Add assertions or checks based on the expected behavior of the save_username function
