import os

from databases import Database
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

load_dotenv(find_dotenv())
app = FastAPI()
DATABASE_URL = os.getenv("DATABASE_URL")
DB = Database(DATABASE_URL)
