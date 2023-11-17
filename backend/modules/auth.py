

# import jwt
from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy import Column, Integer, MetaData, String, Table

import modules.model as _model
from dbase import DB
from modules.services import create_access_token, get_current_user

router = APIRouter()

# Database setup
metadata = MetaData()
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String, unique=True, index=True),
    Column("password", String),
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Create a user
@router.post("/register/", response_model=_model.Token)
async def register(user: _model.UserCreate):
    # Check if the username is already taken
    query = users.select().where(users.c.username == user.username)
    existing_user = await DB.fetch_one(query)

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password
    hashed_password = pwd_context.hash(user.password)

    # Insert the user into the database
    query = users.insert().values(username=user.username, password=hashed_password)
    user_id = await DB.execute(query)

    # Generate and return an access token after successful registration
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "greeting": user.username}
# @router.post("/register/", response_model= _model.User)
# # async def register(user: UserCreate):
# async def register(username: str, password: str):
#     # query = users.insert().values(username=user.username, password=pwd_context.hash(user.password))
#     query = users.insert().values(username=username, password=pwd_context.hash(password))
#     user_id = await DB.execute(query)
#     return {"username": username}
#     # return templates.TemplateResponse("profile.html", {"request": username})

# Login and get a JWT token
@router.post("/login/", response_model= _model.Token)
async def login_for_access_token(user1: _model.UserCreate):
    query = users.select().where(users.c.username == user1.username)
    user = await DB.fetch_one(query)
    if user is None or not pwd_context.verify(user1.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    
    return {"access_token": create_access_token(data={"sub": user1.username}), "token_type": "bearer", "greting" : user["username"]}


# Logout
@router.post("/logout/")
async def logout(current_user: _model.User = Depends(get_current_user)):
    # You can implement logout logic here, like blacklisting the token.
    return {"message": "Logged out successfully", "user": current_user}
