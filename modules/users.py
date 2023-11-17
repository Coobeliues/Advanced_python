from fastapi import APIRouter, Depends

import modules.model as _model
from dbase import DB
from modules.services import get_current_user

router = APIRouter()

@router.get("/all/")
async def get_all_users():
    query = "SELECT * FROM users"
    results = await DB.fetch_all(query=query)
    return results

@router.get("/me/")
async def get_user(user: _model.User = Depends(get_current_user)):
    return user