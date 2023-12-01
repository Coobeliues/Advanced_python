from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP,  ForeignKey, JSON, DateTime,UniqueConstraint, Boolean

metadata = MetaData()

users_info = Table(
    "users_info",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("username", String),
    Column("firstname", String),
    Column("lastname", String),
    Column("age", Integer),
    Column("nationality", String, default= "Kazakh"),
    Column("country", String, default= "Kazakhstan"),
    Column("city", String, default= "Almaty"),
    Column("education", String, default= "No education"),
    Column("phone_number", String),
    Column("gender", String),
    Column("birthdate", DateTime),
    Column("telegram_account", String, default= "@username"),
    Column("email", String),
    Column("role_id", Integer, ForeignKey("roles.id")),
)

roles = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("registered_at", TIMESTAMP),
    Column("role_id", Integer, ForeignKey("roles.id")),
)

requests = Table(
    "requests",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", String, nullable=False),
    Column("datas_from_users", JSON, nullable=False),
    Column("is_done", Boolean,default= False),
    UniqueConstraint('user_id', name='unique_user_id') 
)

class UserCreate(BaseModel):
    username: str
    password: str
    
class UserRead(BaseModel):
    id: int
    user_id: int
    username: str
    firstname: str
    lastname: str
    age: int
    nationality: str
    country: str
    city: str
    education: str
    phone_number: str
    gender: str
    birthdate: str
    telegram_account: str
    email: str
    role_id: int


class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None
