from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import select
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dbase import DB
import modules.model as _model



SECRET_KEY = "2e398ac8a4e549cc5928d00f6ff3484f38c0e2c6c214cd7998d3e5922c84b56f6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = _model.TokenData(username=username)
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    return token_data

async def get_user_information(tokendata: _model.TokenData = Depends(get_current_user)):
    username = tokendata.username
    print(username)
    query = _model.users_info.select().where(_model.users_info.c.username == username)  # Adjust this line
    try:
        user = await DB.fetch_one(query)
        print(user)
        return user
    except Exception as e:
        print(f"Error fetching user: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def check_is_done():
    def decorator(func):
        @wraps(func)
        async def wrapper(user: _model.UserRead, user1: _model.UserRead = Depends(get_user_information)):
            req = _model.requests.select().where(_model.requests.c.user_id == user1.user_id)
            exist = await DB.fetch_one(query=req)
            
            if exist is None:
                return await func(user, user1)
            else:
                query = select([_model.requests.c.is_done]).where(_model.requests.c.user_id == user1.user_id)
                query1 = select([_model.requests.c.confirmed]).where(_model.requests.c.user_id == user1.user_id)
                is_done = await DB.fetch_one(query)
                confirm = await DB.fetch_one(query1)
                if (is_done and confirm) or (not is_done and not confirm):
                    raise HTTPException(status_code=400, detail="already exists")
                else:
                    return await func(user, user1)

        return wrapper
    return decorator

