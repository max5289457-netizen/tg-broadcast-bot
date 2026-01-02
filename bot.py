import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

# 🔴 ВСТАВЬ СЮДА СВОЙ ТОКЕН
TOKEN = "8204791388:AAF-YV_nNPYSlDQAQ8ksZHkrFHUCB8g4LKE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Меню ---
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="ℹ️ О боте")],
        [KeyboardButton(text="📞 Контакты")]
    ],
    resize_keyboard=True
)

# --- /start ---
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Привет!\nВыбери пункт меню 👇",
        reply_markup=menu
    )

# --- Кнопка О боте ---
@dp.message(lambda m: m.text == "ℹ️ О боте")
async def about(message: Message):
    await message.answer("🤖 Это простой Telegram-бот с меню.")

# --- Кнопка Контакты ---
@dp.message(lambda m: m.text == "📞 Контакты")
async def contacts(message: Message):
    await message.answer("📧 Контакты: example@mail.com")

# --- Запуск ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
