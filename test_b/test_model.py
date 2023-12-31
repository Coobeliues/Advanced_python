import pytest
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from your_module_path.model import UserCreate, RequestRead, UserRead, User, UserInDB, Token, TokenData
from your_module_path.model import metadata, users_info, roles, telegram_users, users, requests, types, request2


# Replace 'your_module_path' with the actual path where your model.py module is located
# Replace 'your_database_url' with the actual database URL for testing

DATABASE_URL = "your_database_url"


@pytest.fixture
def engine():
    return create_async_engine(DATABASE_URL)


@pytest.fixture
async def db_session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


@pytest.mark.asyncio
async def test_user_create(db_session):
    user_create_data = {"username": "testuser", "password": "testpassword"}
    user_create = UserCreate(**user_create_data)

    assert user_create.username == user_create_data["username"]
    assert user_create.password == user_create_data["password"]


@pytest.mark.asyncio
async def test_user_read(db_session):
    user_read_data = {
        "user_id": 1,
        "username": "testuser",
        "firstname": "John",
        "lastname": "Doe",
        "age": 25,
        "nationality": "Kazakh",
        "country": "Kazakhstan",
        "city": "Almaty",
        "education": "No education",
        "phone_number": "123456789",
        "gender": "Male",
        "birthdate": "1998-01-01",
        "telegram_account": "@testuser",
        "email": "testuser@example.com",
    }
    user_read = UserRead(**user_read_data)

    assert user_read.user_id == user_read_data["user_id"]
    assert user_read.username == user_read_data["username"]
    assert user_read.firstname == user_read_data["firstname"]
    # Add assertions for other attributes

# Add more test cases for other classes and tables as needed
