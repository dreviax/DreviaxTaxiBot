import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import LabeledPrice, PreCheckoutQuery, SuccessfulPayment
from aiogram.filters import Command

TOKEN = "7891694680:AAGGrGmRidKrCUFJ3vsIpSNyUbYEQUxdxjM"  # зарегистрируйтесь у BotFather
bot = Bot(TOKEN)
dp = Dispatcher()

# База
conn = sqlite3.connect("stars.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, balance INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS payments(tx_id TEXT PRIMARY KEY, user_id INTEGER, amount INTEGER)")
conn.commit()

def get_balance(u): ...
def add_balance(u, a): ...
def save_payment(tx, u, a): ...

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    bal = get_balance(m.from_user.id)
    await m.answer(f"Привет! У тебя {bal} ⭐\nНапиши /buy, чтобы пополниться")

@dp.message(Command("buy"))
async def cmd_buy(m: types.Message):
    prices = [LabeledPrice(label="Тестовая звёзда", amount=1)]
    await bot.send_invoice(
        chat_id=m.chat.id,
        title="Пополнение",
        description="Купи звезду",
        payload="stars_refill",
        currency="XTR",
        prices=prices,
        provider_token="",  # Важно: пустой
    )

@dp.pre_checkout_query()
async def pq(q: PreCheckoutQuery):
    await q.answer(ok=True)

@dp.message(F.successful_payment)
async def paid(m: types.Message):
    tx = m.successful_payment.telegram_payment_charge_id
    amt = m.successful_payment.total_amount
    u = m.from_user.id
    if save_payment(tx,u,amt):
        add_balance(u, amt)
        await m.answer(f"Спасибо! Твой баланс пополнен на {amt} ⭐")
    else:
        await m.answer("Ошибка: этот платеж уже обработан")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
