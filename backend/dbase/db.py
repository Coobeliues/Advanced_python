import os

from databases import Database
# from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI


app = FastAPI()
# load_dotenv(find_dotenv())
DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL = "postgresql://postgres:601246@host.docker.internal:5432/egov"
# print(DATABASE_URL)
# if DATABASE_URL:
#     DB = Database(DATABASE_URL)
# else:
#     print("DATABASE_URL not found or is None. Database connection not initialized.")
DB = Database(DATABASE_URL)
