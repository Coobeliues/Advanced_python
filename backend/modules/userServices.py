from fastapi import APIRouter, Depends
import json
import modules.model as _model
from dbase import DB
from modules.services import check_is_done, get_user_information

router = APIRouter()

@router.post("/editInfo")
@check_is_done()
async def edit_personal_info(user: _model.UserRead,user1: _model.UserRead = Depends(get_user_information)):
    user_data = user.dict()
    user_data_json = json.dumps(user_data)
    print(user_data_json )
    query = _model.requests.insert().values(user_id = user1.user_id,is_done = False,datas_from_users=user_data_json)
    result = await DB.execute(query)

    