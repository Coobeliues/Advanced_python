
import os
import requests
import telebot
from fpdf import FPDF
import dbase as _dbase
import modules.model as _model
from fastapi import HTTPException

TELEGRAM_BOT_TOKEN = '6897226082:AAHIKd83Se06Bp-8dd0NKaM-Dw_qffjam2c'
PDF_PATH = '/app/output.pdf'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Welcome to egov bot!')


@bot.message_handler(commands=['add_username'])
def add_username(message):
    bot.send_message(message.chat.id, 'Send your username from egov')


@bot.message_handler(commands=['get_data'])
def get_datasss(message):
    bot.send_message(message.chat.id, 'Enter BIN or IIN to get information about company')


@bot.message_handler(func=lambda message: True and not message.text.startswith('/'))
def get_data(message):
    user_id = message.from_user.id
    username = ''
    if message.text.isalpha():
        username = message.text
        save_username(username, user_id)
        bot.send_message(message.chat.id, f'Thank you, {username}! Your username has been saved.')
        
    else:

        bin_iin = message.text
        lang = 'en' 
        data = get_datas(bin_iin, lang)

        print(f"API Response: {data}")

        if 'success' in data and data['success']:
            generate_pdf(data)
            with open(PDF_PATH, 'rb') as pdf_file:
                bot.send_document(message.chat.id, pdf_file)
            bot.send_message(message.chat.id, 'Here is your PDF')
        else:
            bot.send_message(message.chat.id, 'Failed to fetch data. Please try again.')


def get_datas(bin_iin, lang='en'):
    api_url = f'https://old.stat.gov.kz/api/juridical/counter/api/?bin={bin_iin}&lang={lang}'
    response = requests.get(api_url)
    return response.json()


def generate_pdf(data):
    pdf = FPDF()
    
    pdf.add_page()


    pdf.add_font('DejaVuSans', '', '/app/modules/DejaVuSans.ttf', uni=True)
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


async def save_username(username, user_id):
    query = _model.telegram_users.select().where(_model.telegram_users.c.username == username)
    existing_user = await _dbase.DB.fetch_one(query)

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exist")
    
    query1 = _model.telegram_users.insert().values(username=username,chat_id = user_id)
    await _dbase.DB.execute(query1)



if __name__ == '__main__':
    bot.polling(none_stop=True)
