from databases import Database
import os  
from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
app = FastAPI()
DATABASE_URL = os.getenv("DATABASE_URL")
DB = Database(DATABASE_URL)
