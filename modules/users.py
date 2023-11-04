
from dbase import DB
from fastapi import APIRouter

router = APIRouter()

@router.get("/all/")
async def get_all_users():
    query = "SELECT * FROM users"
    results = await DB.fetch_all(query=query)
    return results