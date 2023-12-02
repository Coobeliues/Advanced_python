from fastapi import APIRouter, Depends
import json
import modules.model as _model
from dbase import DB
from modules.services import check_is_done, get_user_information
import modules.model as _model
from sqlalchemy import update

router = APIRouter()

@router.get("/allRequests")
async def get_all_requests():
    query = "SELECT * FROM requests"
    results = await DB.fetch_all(query=query)
    return results


@router.put("/confirm")
async def confirm_status(request: _model.RequestRead):
    update_query = (
        update(_model.requests)
        .where(_model.requests.c.user_id == request.user_id)  
        .values(is_done=True)
    )
    await DB.execute(update_query)

    user_info_query = (
        update(_model.users_info)
        .where(_model.users_info.c.user_id == request.user_id) 
        .values(
            firstname=request.data_from_users.firstname,
            lastname=request.data_from_users.lastname,
            age=request.data_from_users.age,
            nationality=request.data_from_users.nationality,
            country=request.data_from_users.country,
            city=request.data_from_users.city,
            education=request.data_from_users.education,
            phone_number=request.data_from_users.phone_number,
            gender=request.data_from_users.gender,
            birthdate=request.data_from_users.birthdate,
            telegram_account=request.data_from_users.telegram_account,
            email=request.data_from_users.email
        )
    )
    await DB.execute(user_info_query)

    return {"message": "Status confirmed and user_info updated"}

    