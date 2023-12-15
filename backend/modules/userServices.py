import json
import confluent_kafka as _a
import modules.model as _model
import requests
from dbase import DB
from sqlalchemy import select
from modules.mail import send_email
from fastapi import APIRouter, Depends
from modules.teleg import send_to_bot
from modules.services import (check_is_done, generate_pdf, get_datas,
                              get_user_information)

router = APIRouter()
producer_conf = {'bootstrap.servers': 'broker:9094', 'client.id': 'my-app'}
consumer_conf = {'bootstrap.servers': 'broker:9094', 'group.id': 'my-group', 'auto.offset.reset': 'latest'}
consumer_conf1 = {'bootstrap.servers': 'broker:9094', 'group.id': 'my-group1', 'auto.offset.reset': 'earliest'}
producer = _a.Producer(producer_conf)
consumer = _a.Consumer(consumer_conf)
consumer1 = _a.Consumer(consumer_conf1)

async def consume(topic):
    if topic == "topic1":
        consumer.subscribe([topic])
        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == _a.KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f"Consumer error: {msg.error()}")
                        break
                print("_______________")
                msg_value = msg.value().decode('utf-8')
                print(msg_value)
                print("_______________")
                if msg_value:
                    print(f"Received message from topic1: {msg_value}")
                    yield msg_value
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()
    elif topic == "topic2":
        consumer1.subscribe([topic])
        try:
            while True:
                msg = consumer1.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == _a.KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f"Consumer error: {msg.error()}")
                        break
                msg_value = msg.value().decode('utf-8')
                if msg_value:
                    try:
                        data = json.loads(msg_value)
                        yield data
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
        except KeyboardInterrupt:
            pass
        finally:
            consumer1.close()

async def produce(topic, data: dict):
    try:
        data = json.dumps(data).encode('utf-8')
        producer.produce(topic, value=data)
        producer.flush()
    except Exception as e:
        print(f"Failed to publish message to Kafka: {e}")
    
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
            name = data.get("obj", {}).get("name", "")  
            return {"exists": company_exists, "Name": name}
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
    query = _model.request2.insert().values(username=request.username, bin=request.bin, status=False)
    await DB.execute(query)
    await produce("topic1", {"bin":request.bin})
    
    async for bin_data in consume("topic1"):
        bin_value = json.loads(bin_data).get("bin").strip('"')
        detailed_data = get_datas(bin_value)
        await produce("topic2", json.dumps(detailed_data))
        async for topic2_data in consume("topic2"):
            try:
                data_from_topic2 = json.loads(topic2_data)
                generate_pdf(data_from_topic2)
                print("jjjjjjj")
            except Exception as e:
                print(f"Error processing data from topic2: {e}")
    query1 = select([_model.telegram_users.c.chat_id]).where((_model.telegram_users.c.username == request.username))
    result = await DB.fetch_one(query1)
    chat_id = result[0]
    send_to_bot(chat_id)
    query2 = select([_model.users_info.c.email]).where((_model.users_info.c.username == request.username))
    result2 = await DB.fetch_one(query2)
    email = result2[0]
    send_email(email)

