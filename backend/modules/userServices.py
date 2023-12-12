from fastapi import APIRouter, Depends
import modules.model as _model
from dbase import DB
from modules.services import check_is_done, get_user_information
import requests
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
from fpdf import FPDF
import asyncio

router = APIRouter()
KAFKA_BOOTSTRAP_SERVERS = 'broker:9094'
KAFKA_TOPIC_1 = 'topic1'
KAFKA_TOPIC_2 = 'topic2'
async def produce_to_kafka(data):
    producer_conf = {
        'bootstrap_servers': KAFKA_BOOTSTRAP_SERVERS
    }
    producer = AIOKafkaProducer(**producer_conf)
    
    await producer.start()
    await producer.send_and_wait(KAFKA_TOPIC_1, key=None, value=data)
    await producer.stop()

PDF_PATH = '/appp/output.pdf'

async def bin_info_consumer():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC_1, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id='bin_info_group')
    await consumer.start()
    
    async for message in consumer:
        bin_info_request = json.loads(message.value)
        parsed_data = process_bin_info(bin_info_request)
        
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()
        await producer.send_and_wait(KAFKA_TOPIC_2, value=json.dumps(parsed_data).encode('utf-8'))
        await producer.stop()

async def continuous_bin_info_consumer():
    while True:
        await bin_info_consumer()
        await asyncio.sleep(10)

async def pdf_generation_consumer(bin_iin):
    consumer = AIOKafkaConsumer(KAFKA_TOPIC_2, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id='pdf_generation_group')
    await consumer.start()
    
    async for message in consumer:
        parsed_data = json.loads(message.value)
        if parsed_data.get("bin") == bin_iin:
            generate_pdf(parsed_data)
            return parsed_data
 

def process_bin_info(bin_info_request):
    bin_data = get_datas(bin_info_request["bin"])
    return bin_data 

def get_datas(bin_iin, lang='en'):
    api_url = f'https://old.stat.gov.kz/api/juridical/counter/api/?bin={bin_iin}&lang={lang}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return {}
    
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    if 'bin' in data:
        for key, value in data.items():
            pdf.cell(0, 10, f"{key}: {value}", ln=True)
        pdf.output(PDF_PATH)
    else:
        print("Key 'bin' not found in data")



# @router.post("/editInfo")
# @check_is_done()
# async def edit_personal_info(user: _model.UserRead, user1: _model.UserRead = Depends(get_user_information)):
#     user_data = user.dict()
#     query = _model.requests.insert().values(user_id=user1.user_id, is_done=False, confirmed = False, type = "Editing personal info", datas_from_users=user_data)
#     result = await DB.execute(query)
  
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

@router.post("/editInfo")
@check_is_done()
async def edit_personal_info(user: _model.UserRead, user1: _model.UserRead = Depends(get_user_information)):
    user_data = user.dict()
    query = _model.requests.insert().values(user_id=user1.user_id, is_done=False, confirmed=False, type="Editing personal info", datas_from_users=user_data)
    result = await DB.execute(query)

@router.get("/check-company/{bin}/{lang}")
async def check_company(bin: str, lang: str):
    result = check_company_by_bin(bin, lang)
    return result

@router.post("/getInfo")
async def check_company(request: _model.Request2Read): 
    query = _model.request2.insert().values(username=request.username, bin=request.bin, result=request.result)
    await DB.execute(query)
    data = json.dumps({"bin": request.bin}).encode('utf-8')
    
    await produce_to_kafka(data)
    
    asyncio.create_task(continuous_bin_info_consumer())