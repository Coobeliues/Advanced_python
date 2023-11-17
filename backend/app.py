
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dbase import DB
from modules import auth, users

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    await DB.connect()


@app.on_event("shutdown")
async def shutdown_db_client():
    await DB.disconnect()


@app.get("/")
async def root():
    return {"message": "Awesome Leads Manager"}
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])
