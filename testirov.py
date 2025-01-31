import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import requests
from flask import Flask, request, jsonify

API = '7760162438:AAFhnCr0jantPwzZaf-__XW0XeIUTXvKj2s'
USERS = {357158811114185, 353742337513196}

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
disp = Dispatcher(bot, storage=MemoryStorage())


def authorized(token):
    return token == API


@disp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Отправьте IMEI для проверки.")


@disp.message_handler(lambda message: message.from_user.id in USERS)
async def check(message: types.Message):
    imei = message.text
    response = check_imei(imei)
    await message.reply(response)


@disp.message_handler(lambda message: message.from_user.id not in USERS)
async def not_access(message: types.Message):
    await message.reply("У вас нет доступа.")


def check_imei(imei):
    url = "https://imeicheck.net/api/check-imei"
    response = requests.post(url, json={"imei": imei, "token": "e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b"})

    if response.status_code != 200:
        return {"error": "Ошибка проверки IMEI"}

    return response.json()


if __name__== '__main__':
    executor.start_polling(disp, skip_updates=True)

app = Flask(__name__)


@app.route('/api/check-imei', methods=['POST'])
def api_check_imei():
    token = request.json.get('token')
    imei = request.json.get('imei')

    if not authorized(token):
        return jsonify({"error": "Unauthorized"}), 403

    response = check_imei(imei)
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=5000)










