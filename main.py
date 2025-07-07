import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

TOKEN = "7891694680:AAGGrGmRidKrCUFJ3vsIpSNyUbYEQUxdxjM"
bot = Bot(TOKEN)
dp = Dispatcher(bot)

# База
conn = sqlite3.connect("stars_db.sqlite3")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0
)""")
conn.commit()

# FSM
class Form(StatesGroup):
    refill = State()

# Главное меню (inline buttons)
def main_kb(balance: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Баланс: ⭐ {balance}", callback_data="ignore")],
        [InlineKeyboardButton(text="💰 Пополнить", callback_data="refill"),
         InlineKeyboardButton(text="📤 Вывод", callback_data="withdraw")],
    ])
    return kb

async def get_balance(user_id: int) -> int:
    cur.execute("SELECT balance FROM users WHERE telegram_id = ?", (user_id,))
    row = cur.fetchone()
    return row[0] if row else 0

async def set_balance(user_id: int, new_balance: int):
    cur.execute("INSERT INTO users(telegram_id, balance) VALUES(?, ?) ON CONFLICT(telegram_id) DO UPDATE SET balance = ?",
                (user_id, new_balance, new_balance))
    conn.commit()

@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    bal = await get_balance(user_id)
    await set_balance(user_id, bal)  # если новый — создаём
    await message.answer(
        text="Привет! Это твой баланс ⭐",
        reply_markup=main_kb(bal)
    )

@dp.callback_query(lambda c: c.data == "ignore")
async def on_ignore(cq: types.CallbackQuery):
    await cq.answer()  # no popup

@dp.callback_query(lambda c: c.data == "refill")
async def on_refill(cq: types.CallbackQuery, state: FSMContext):
    await cq.message.answer("Сколько звёзд пополнить? Введи число:")
    await state.set_state(Form.refill)

@dp.message(Form.refill)
async def process_refill(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        amount = int(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        return await message.answer("Пожалуйста, введи положительное целое число.")
    bal = await get_balance(user_id)
    new_bal = bal + amount
    await set_balance(user_id, new_bal)
    await message.answer(f"✅ Пополнено на ⭐{amount}. Текущий баланс: ⭐{new_bal}",
                         reply_markup=main_kb(new_bal))
    await state.clear()

@dp.callback_query(lambda c: c.data == "withdraw")
async def on_withdraw(cq: types.CallbackQuery):
    user_id = cq.from_user.id
    bal = await get_balance(user_id)
    if bal <= 0:
        await cq.answer("У тебя нет звезд для вывода.", show_alert=True)
    else:
        # просто "отправляем" баланс обратно: сбрасываем у пользователя
        await set_balance(user_id, 0)
        # можно здесь добавить логику "отправки куда-то" если нужно
        await cq.message.answer(f"📤 Выведено ⭐{bal}. Твой новый баланс: ⭐0",
                                 reply_markup=main_kb(0))
    await cq.answer()

# Запуск
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling())
