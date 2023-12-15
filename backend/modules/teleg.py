
# import requests

# # Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
# TELEGRAM_BOT_TOKEN = '6897226082:AAHIKd83Se06Bp-8dd0NKaM-Dw_qffjam2c'
# # Replace 'USER_CHAT_ID' with the actual chat ID of the user you want to send the file to
# USER_CHAT_ID = '406085612'

# # URL for the Telegram Bot API sendDocument endpoint
# api_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument'

# # Open the file you want to send
# with open('D:/e_tg_egov_pdf/output.pdf', 'rb') as file:
#     files = {'document': ('output.pdf', file)}

#     # Set the chat_id and other optional parameters
#     params = {'chat_id': USER_CHAT_ID, 'caption': 'Optional caption for the document'}

#     # Make the request to send the document
#     response = requests.post(api_url, params=params, files=files)

#     # Check the response
#     if response.status_code == 200:
#         print('Document sent successfully!')
#     else:
#         print(f'Failed to send document. Status code: {response.status_code}, Response: {response.text}')

import asyncio

import confluent_kafka as _a
import dbase as _dbase
import modules.model as _model
import modules.services as _services
from aiogram import Bot, Dispatcher, types
from fpdf import FPDF
from sqlalchemy import select, update


async def connect_to_db():
    await _dbase.DB.connect()

async def disconnect_from_db():
    await _dbase.DB.disconnect()

TELEGRAM_BOT_TOKEN = '6897226082:AAHIKd83Se06Bp-8dd0NKaM-Dw_qffjam2c'

api_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument'

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

async def on_startup(dp):
    await connect_to_db()

async def on_shutdown(dp):
    await disconnect_from_db()
    
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Welcome to egov bot!Send your username from egov')


@dp.message_handler(lambda message: not message.text.startswith('/'))
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.text
    res = await save_username(username, user_id)
    if res:
        await message.answer(f'Thank you, {username}! Your username has been saved.')
    else:
        await message.answer(f'Your username already exist')
        # with open(_services.PDF_PATH, 'rb') as pdf_file:
        #     await bot.send_document(message.chat.id, pdf_file)
        # await message.answer('Here is your PDF')
        # update_query = (
        #     update(_model.request2)
        #     .where((_model.request2.c.username == username) & (_model.request2.c.bin == bin_iin))
        #     .values(status=True)
        # )
        # await _dbase.DB.execute(update_query)

async def save_username(username, user_id):
    query = _model.telegram_users.select().where(_model.telegram_users.c.username == username)
    existing_user = await _dbase.DB.fetch_one(query)

    if existing_user:
        return False 
    else:
        query1 = _model.telegram_users.insert().values(username=username, chat_id=str(user_id))
        await _dbase.DB.execute(query1)
        return True

# with open('D:/e_tg_egov_pdf/output.pdf', 'rb') as file:
#     files = {'document': ('output.pdf', file)}

#     # Set the chat_id and other optional parameters
#     params = {'chat_id': USER_CHAT_ID, 'caption': 'Optional caption for the document'}

#     # Make the request to send the document
#     response = requests.post(api_url, params=params, files=files)

#     # Check the response
#     if response.status_code == 200:
#         print('Document sent successfully!')
#     else:
#         print(f'Failed to send document. Status code: {response.status_code}, Response: {response.text}')


async def main():
    await connect_to_db()
    await dp.start_polling()
    await disconnect_from_db()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
