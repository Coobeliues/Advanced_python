import json

import modules.kafka as _kafka
import modules.model as _model
from dbase import DB
from fastapi import APIRouter, Depends
from modules.services import (check_company_by_bin, check_is_done,
                              generate_pdf, get_data, get_user_information,
                              sent_to_email, sent_to_telegram)

TOPIC_1 = "topic1"
TOPIC_2 = "topic2"

router = APIRouter()
 
@router.post("/editInfo")
@check_is_done()
async def edit_personal_info(user: _model.UserRead, user_info: _model.UserRead = Depends(get_user_information)):
    """
    Edits personal information for the user.

    Parameters:
    - user: UserRead - The user data to be edited.
    - user_info: UserRead - The current user information obtained from the database.

    """
    user_data = user.dict()
    query = _model.requests.insert().values(user_id=user_info.user_id, is_done=False, confirmed = False, type = "Editing personal info", datas_from_users=user_data)
    await DB.execute(query)
  

@router.get("/check-company/{bin}/{lang}")
async def check_company(bin: str, lang: str):
    # Call the function to check company details by bin 
    result = check_company_by_bin(bin, lang)
    return result


@router.post("/getInfo")
async def get_info(request: _model.Request2Read):
    # Produce a message to TOPIC_1 in Kafka with the given bin from the request 
    await _kafka.produce(TOPIC_1, {"bin":request.bin})

    # Consume messages from TOPIC_1 in Kafka
    async for bin_data in _kafka.consume(TOPIC_1):
        # Extract the bin value from the Kafka message data
        bin_value = json.loads(bin_data).get("bin").strip('"')
        # Get detailed data
        detailed_data =  await get_data(bin_value)
        await _kafka.produce(TOPIC_2, json.dumps(detailed_data))
        async for topic2_data in _kafka.consume(TOPIC_2):
            data_from_topic2 = json.loads(topic2_data)
            generate_pdf(data_from_topic2)
            await sent_to_email(request.username)
            await sent_to_telegram(request.username)
   