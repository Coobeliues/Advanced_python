from fastapi import APIRouter, Depends
import json
import modules.model as _model
from dbase import DB
from modules.services import check_is_done, get_user_information

router = APIRouter()

@router.post("/editInfo")
@check_is_done()
async def edit_personal_info(user: _model.UserRead, user1: _model.UserRead = Depends(get_user_information)):
    user_data = user.dict()
    query = _model.requests.insert().values(user_id=user1.user_id, is_done=False, confirmed = False, type = "Editing personal info", datas_from_users=user_data)
    result = await DB.execute(query)

    