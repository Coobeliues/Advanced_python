
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dbase import DB
from modules import auth, users, userServices, managerServices

app = FastAPI()
# origins = [
#     "http://localhost:3000",
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
    
# ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return {"message": "Egov system"}
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(userServices.router, prefix="/services", tags=["services"])
app.include_router(managerServices.router, prefix="/manager", tags=["manager"])