import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Клавиатура с языками
lang_kb = ReplyKeyboardMarkup(resize_keyboard=True)
lang_kb.add(KeyboardButton("🇷🇺 Русский"), KeyboardButton("🇬🇧 English"), KeyboardButton("🇨🇳 中文"))

# Переводы
messages = {
    "start": {
        "ru": "Привет! Я помогу вам с экскурсиями. Выберите язык:",
        "en": "Hello! I will help you with tours. Choose a language:",
        "zh": "你好！我会帮助你了解旅行团。请选择语言："
    },
    "buy_ticket": {
        "ru": "Билеты можно купить на сайте: https://paritetplus.com",
        "en": "You can buy tickets at: https://paritetplus.com",
        "zh": "您可以在此网站购买门票：https://paritetplus.com"
    },
    "meeting_point": {
        "ru": "Сбор туристов: ул. Думская, д. 2 (метро Невский проспект, у Гостиного двора)",
        "en": "Meeting point: Dumskaia St. 2 (Nevsky Prospect metro, near Gostiny Dvor)",
        "zh": "集合地点：Dumskaia 街 2 号（涅夫斯基地铁站，Gostiny Dvor 附近）"
    }
}

user_lang = {}

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer(messages["start"]["ru"], reply_markup=lang_kb)

@dp.message_handler(lambda m: m.text in ["🇷🇺 Русский", "🇬🇧 English", "🇨🇳 中文"])
async def set_language(message: types.Message):
    lang = {"🇷🇺 Русский": "ru", "🇬🇧 English": "en", "🇨🇳 中文": "zh"}[message.text]
    user_lang[message.from_user.id] = lang
    await message.answer("Язык установлен. Задайте вопрос, например: Где купить билет?")

@dp.message_handler()
async def handle_questions(message: types.Message):
    lang = user_lang.get(message.from_user.id, "ru")
    text = message.text.lower()
    if "билет" in text or "ticket" in text or "门票" in text:
        await message.answer(messages["buy_ticket"][lang])
    elif "сбор" in text or "meeting" in text or "集合" in text:
        await message.answer(messages["meeting_point"][lang])
    else:
        await message.answer("Попробуйте задать вопрос иначе.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)