from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
# from databases import Database
from fastapi.security import OAuth2PasswordBearer
from dbase import DB
import modules.model as _model

# Configuration
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
    except:
        raise credentials_exception

    return token_data

async def get_user_information(tokendata: _model.TokenData = Depends(get_current_user)):
    username = tokendata.username
    query = _model.users.select().where(_model.users.c.username == username)
    user = await DB.fetch_one(query)

    return user