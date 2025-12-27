import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# ==============================
# 🔑 ВСТАВЬ ТОКЕН ЗДЕСЬ
# ==============================
TOKEN = "8204791388:AAF-YV_nNPYSlDQAQ8ksZHkrFHUCB8g4LKE"
# ==============================

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Хранилища ---
users = {}              # user_id -> username
selecting = {}          # user_id -> [user_id, user_id]
waiting_text = set()    # кто сейчас вводит текст

# --- Главное меню ---
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📢 Рассылка")]
    ],
    resize_keyboard=True
)

# --- /start ---
@dp.message(CommandStart())
async def start(message: types.Message):
    uid = message.from_user.id
    uname = message.from_user.username or f"user_{uid}"
    users[uid] = uname

    await message.answer(
        "👋 Привет! Как дела?\n"
        "Чем могу помочь? ✅\n",
        reply_markup=menu
    )

# --- Меню ---
@dp.message()
async def menu_handler(message: types.Message):
    uid = message.from_user.id
    uname = message.from_user.username or f"user_{uid}"
    users[uid] = uname

    # Если ждём текст для рассылки
    if uid in waiting_text:
        text = message.text
        targets = selecting.get(uid, [])

        sent = 0
        for t in targets:
            try:
                await bot.send_message(t, text)
                sent += 1
            except Exception as e:
                print(f"Ошибка отправки {t}: {e}")

        waiting_text.remove(uid)
        selecting[uid] = []

        await message.answer(
            f"✅ Сообщение отправлено {sent} пользователям",
            reply_markup=menu
        )
        return

    # Кнопка рассылки
    if message.text == "📢 Рассылка":
        if len(users) <= 1:
            await message.answer("❌ Пока нет других пользователей")
            return

        kb = InlineKeyboardMarkup()
        selecting[uid] = []

        for user_id, name in users.items():
            if user_id != uid:
                kb.add(
                    InlineKeyboardButton(
                        text=f"@{name}",
                        callback_data=f"pick_{user_id}"
                    )
                )

        await message.answer(
            "Выбери пользователей для рассылки 👇",
            reply_markup=kb
        )

# --- Выбор пользователей ---
@dp.callback_query()
async def pick_user(call: types.CallbackQuery):
    uid = call.from_user.id
    target_id = int(call.data.split("_")[1])

    if target_id not in selecting[uid]:
        selecting[uid].append(target_id)

    await call.answer("✅ Добавлен")

    if uid not in waiting_text:
        waiting_text.add(uid)
        await bot.send_message(
            uid,
            "✏️ Теперь напиши текст сообщения для рассылки"
        )

# --- Запуск ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
