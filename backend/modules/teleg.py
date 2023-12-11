import requests
from fpdf import FPDF
import dbase as _dbase
import modules.model as _model
import asyncio
from aiogram import Bot, Dispatcher, types
from sqlalchemy import select

async def connect_to_db():
    await _dbase.DB.connect()

async def disconnect_from_db():
    await _dbase.DB.disconnect()

TELEGRAM_BOT_TOKEN = '6897226082:AAHIKd83Se06Bp-8dd0NKaM-Dw_qffjam2c'
PDF_PATH = '/appp/output.pdf'

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

async def on_startup(dp):
    await connect_to_db()

async def on_shutdown(dp):
    await disconnect_from_db()
    
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Welcome to egov bot!')

@dp.message_handler(commands=['get_data'])
async def get_data_command(message: types.Message):
    await message.answer('Send your username from egov')

@dp.message_handler(lambda message: not message.text.startswith('/'))
async def get_data(message: types.Message):
    user_id = message.from_user.id
    username = message.text
    await save_username(username, user_id)
    await message.answer(f'Thank you, {username}! Your username has been saved.')

    query = select([_model.request2.c.bin]).where(_model.request2.c.username == username)
    result = await _dbase.DB.fetch_one(query)
    
    if result is not None:
        bin_iin = result[0] 
        lang = 'en'
        data = get_datas(bin_iin, lang)

        print(f"API Response: {data}")

        if 'success' in data and data['success']:
            generate_pdf(data)
            with open(PDF_PATH, 'rb') as pdf_file:
                await bot.send_document(message.chat.id, pdf_file)
            await message.answer('Here is your PDF')
        else:
            await message.answer('Failed to fetch data. Please try again.')
    else:
        await message.answer('Username not found. Please try again.')

async def save_username(username, user_id):
    query = _model.telegram_users.select().where(_model.telegram_users.c.username == username)
    existing_user = await _dbase.DB.fetch_one(query)

    if existing_user:
        await bot.send_message(user_id, "Username already exists. Please try another one.")
        return

    query1 = _model.telegram_users.insert().values(username=username, chat_id=str(user_id))
    await _dbase.DB.execute(query1)

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
    pdf.add_font('DejaVuSans', '', '/appp/DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVuSans", size=12)

    bin_iin_text = f"BIN/IIN: {data['obj']['bin']}"
    name_text = f"Name: {data['obj']['name']}"
    register_date_text = f"Registration Date: {data['obj']['registerDate']}"
    oked_code_text = f"Main code of the GCoEA: {data['obj']['okedCode']}"
    oked_name_text = f"Type of Economic Activity: {data['obj']['okedName']}"
    secondOkeds_text = f"Secondary code of the GCoEA: {data['obj']['secondOkeds']}"
    krpCode_text = f"Code of CoDE: {data['obj']['secondOkeds']}"
    krpName_text = f"Name of CoDE: {data['obj']['krpName']}"
    krpBfCode_text = f"Code of CoDE (excluding branches): {data['obj']['krpBfCode']}"
    krpBfName_text = f"Name of CoDE: {data['obj']['krpBfName']}"
    kseCode_text = f"CoATO: {data['obj']['kseCode']}"
    kseName_text = f"Name of the economic sector: {data['obj']['kseName']}"
    kfsCode_text = f"KFP code: {data['obj']['kfsCode']}"
    kfsName_text = f"KFP name: {data['obj']['katoId']}"
    katoCode_text = f"CoATO: {data['obj']['katoCode']}"
    katoId_text = f"CoATO Id: {data['obj']['katoId']}"
    katoAddress_text = f"Legal address: {data['obj']['katoAddress']}"
    fio_text = f"Surname, name, patronymic of the head: {data['obj']['fio']}"


   
    pdf.multi_cell(0, 10, txt=bin_iin_text)
    pdf.multi_cell(0, 10, txt=name_text)
    pdf.multi_cell(0, 10, txt=register_date_text)
    pdf.multi_cell(0, 10, txt=oked_code_text)
    pdf.multi_cell(0, 10, txt=oked_name_text)
    pdf.multi_cell(0, 10, txt=secondOkeds_text)
    pdf.multi_cell(0, 10, txt=krpCode_text)
    pdf.multi_cell(0, 10, txt=krpName_text)
    pdf.multi_cell(0, 10, txt=krpBfCode_text)
    pdf.multi_cell(0, 10, txt=krpBfName_text)
    pdf.multi_cell(0, 10, txt=kseCode_text)
    pdf.multi_cell(0, 10, txt=kseName_text)
    pdf.multi_cell(0, 10, txt=kfsCode_text)
    pdf.multi_cell(0, 10, txt=kfsName_text)
    pdf.multi_cell(0, 10, txt=katoCode_text)
    pdf.multi_cell(0, 10, txt=katoId_text)
    pdf.multi_cell(0, 10, txt=katoAddress_text)
    pdf.multi_cell(0, 10, txt=fio_text)

    pdf.output(PDF_PATH)
    print(data)

async def main():
    await connect_to_db()
    await dp.start_polling()
    await disconnect_from_db()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
