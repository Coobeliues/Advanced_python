from fastapi import APIRouter, Depends
import modules.model as _model
from dbase import DB
from modules.services import check_is_done, get_user_information
import requests
router = APIRouter()

@router.post("/editInfo")
@check_is_done()
async def edit_personal_info(user: _model.UserRead, user1: _model.UserRead = Depends(get_user_information)):
    user_data = user.dict()
    query = _model.requests.insert().values(user_id=user1.user_id, is_done=False, confirmed = False, type = "Editing personal info", datas_from_users=user_data)
    result = await DB.execute(query)
  
def check_company_by_bin(bin: str, lang: str):
    url = f"https://old.stat.gov.kz/api/juridical/counter/api/?bin={bin}&lang={lang}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            company_exists = data.get("success", False)
            obj = data.get("obj", {})
            name = data.get("obj", {}).get("name", "")  
            return {"exists": company_exists, "Name": name, "Object":obj}
        return {"exists": False, "Name": ""}
    except Exception as e:
        print(e)
        return {"exists": False, "Name": ""}

@router.get("/check-company/{bin}/{lang}")
async def check_company(bin: str, lang: str):
    result = check_company_by_bin(bin, lang)
    return result

@router.post("/getInfo")
async def check_company(request: _model.Request2Read): 
    query = _model.request2.insert().values(username=request.username, bin=request.bin, result=request.result)
    await DB.execute(query)

