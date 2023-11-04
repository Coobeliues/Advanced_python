
from fastapi import FastAPI
from modules import auth,users
from dbase import DB

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await DB.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await DB.disconnect()

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])
