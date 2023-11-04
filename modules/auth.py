from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from databases import Database
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
# from databases import Database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from dbase import DB
import jwt
from jwt import decode
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates

# Configuration
SECRET_KEY = "2e398ac8a4e549cc5928d00f6ff3484f38c0e2c6c214cd7998d3e5922c84b56f6"
ALGORITHM = "HS256"
# app = FastAPI()
router = APIRouter()
templates = Jinja2Templates(directory=r"C:\Users\amina\KBTU\Adv-Python\project_egov\frontend\frontend")

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

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)  # Default expiration time
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Create a user
@router.post("/register/", response_model=User)
# async def register(user: UserCreate):
async def register(username: str, password: str):
    # query = users.insert().values(username=user.username, password=pwd_context.hash(user.password))
    query = users.insert().values(username=username, password=pwd_context.hash(password))
    user_id = await DB.execute(query)
    return {"username": username}
    # return templates.TemplateResponse("profile.html", {"request": username})

# Login and get a JWT token
@router.post("/login/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    query = users.select().where(users.c.username == form_data.username)
    user = await DB.fetch_one(query)
    if user is None or not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    
    return {"access_token": create_access_token(data={"sub": form_data.username}), "token_type": "bearer", "greting" : user["username"]}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data

# Logout
@router.post("/logout/")
async def logout(current_user: User = Depends(get_current_user)):
    # You can implement logout logic here, like blacklisting the token.
    return {"message": "Logged out successfully", "user": current_user}
