import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from your_module_path.users import get_all_users, get_user, get_user_info

# Replace 'your_module_path' with the actual path where your users.py module is located
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
async def test_get_all_users(db_session, mocker):
    # Mock the DB.fetch_all function
    mocker.patch("your_module_path.users.DB.fetch_all", return_value=[{"id": 1, "username": "user1"}, {"id": 2, "username": "user2"}])

    response = await get_all_users()

    # Add assertions or checks based on the expected behavior of the get_all_users function
    assert response == [{"id": 1, "username": "user1"}, {"id": 2, "username": "user2"}]


@pytest.mark.asyncio
async def test_get_user(db_session, mocker):
    # Mock the get_current_user function
    mocker.patch("your_module_path.users.get_current_user", return_value={"id": 1, "username": "testuser"})

    response = await get_user()

    # Add assertions or checks based on the expected behavior of the get_user function
    assert response == {"id": 1, "username": "testuser"}


@pytest.mark.asyncio
async def test_get_user_info(db_session, mocker):
    # Mock the get_user_information function
    mocker.patch("your_module_path.users.get_user_information", return_value={"user_id": 1, "username": "testuser", "firstname": "John"})

    response = await get_user_info()

    # Add assertions or checks based on the expected behavior of the get_user_info function
    assert response == {"user_id": 1, "username": "testuser", "firstname": "John"}
