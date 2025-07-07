import telebot
from telebot import types
import sqlite3

TOKEN = "7891694680:AAGGrGmRidKrCUFJ3vsIpSNyUbYEQUxdxjM"
bot = telebot.TeleBot(TOKEN)

# --- Инициализация SQLite ---
conn = sqlite3.connect("stars_bot.sqlite3", check_same_thread=False)
cur = conn.cursor()
cur.execute("""
  CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0
  )
""")
cur.execute("""
  CREATE TABLE IF NOT EXISTS payments (
    tx_id TEXT PRIMARY KEY,
    user_id INTEGER,
    amount INTEGER
  )
""")
conn.commit()

def get_balance(user_id: int) -> int:
    row = cur.execute("SELECT balance FROM users WHERE telegram_id = ?", (user_id,)).fetchone()
    if not row:
        cur.execute("INSERT INTO users (telegram_id, balance) VALUES (?, 0)", (user_id,))
        conn.commit()
        return 0
    return row[0]

def add_balance(user_id: int, amount: int):
    bal = get_balance(user_id) + amount
    cur.execute("UPDATE users SET balance = ? WHERE telegram_id = ?", (bal, user_id))
    conn.commit()
    return bal

def save_payment(tx_id: str, user_id: int, amount: int) -> bool:
    try:
        cur.execute("INSERT INTO payments (tx_id, user_id, amount) VALUES (?, ?, ?)",
                    (tx_id, user_id, amount))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# --- Клавиатуры ---
def main_kb(balance: int):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(f"⭐ Баланс: {balance}", callback_data="ignore"))
    kb.add(
        types.InlineKeyboardButton("💰 Пополнить", callback_data="refill"),
        types.InlineKeyboardButton("📤 Вывод", callback_data="withdraw")
    )
    return kb

def payment_kb(amount: int):
    kb = types.InlineKeyboardMarkup()
    # кнопка оплаты звездочками
    kb.add(types.InlineKeyboardButton(text=f"Пополнить на {amount} ⭐", pay=True))
    return kb

# --- Команда /start ---
@bot.message_handler(commands=["start"])
def cmd_start(msg: types.Message):
    balance = get_balance(msg.from_user.id)
    bot.send_message(
        msg.chat.id,
        "Привет! Это твой кошелёк:\n",
        reply_markup=main_kb(balance)
    )

# --- Обработка inline-кнопок ---
@bot.callback_query_handler(lambda c: True)
def callback_handler(c: types.CallbackQuery):
    uid = c.from_user.id
    if c.data == "ignore":
        bot.answer_callback_query(c.id)
    elif c.data == "refill":
        bot.send_message(c.message.chat.id, "Сколько ⭐ хочешь пополнить? Введи целое число.")
        bot.register_next_step_handler(c.message, ask_refill_amount)
    elif c.data == "withdraw":
        bal = get_balance(uid)
        if bal > 0:
            add_balance(uid, -bal)
            bot.send_message(c.message.chat.id,
                             f"📤 Выведено ⭐{bal}. Баланс обнулён.",
                             reply_markup=main_kb(0))
        else:
            bot.send_message(c.message.chat.id, "У тебя нет звёзд для вывода.")
    bot.answer_callback_query(c.id)

# --- Запрос суммы пополнения ---
def ask_refill_amount(msg: types.Message):
    try:
        amount = int(msg.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        return bot.send_message(msg.chat.id, "Пожалуйста, введи число больше 0.")
    # отправляем инвойс на оплату звездами
    prices = [types.LabeledPrice(label="Пополнение", amount=amount)]
    bot.send_invoice(
        msg.chat.id,
        title="Пополнение баланса",
        description=f"Пополнить на {amount} ⭐",
        invoice_payload="refill",
        provider_token=None,  # для XTR token не нужен  [oai_citation:0‡pytba.readthedocs.io](https://pytba.readthedocs.io/en/4.27.0/sync_version/index.html?utm_source=chatgpt.com) [oai_citation:1‡blogfork.telegram.org](https://blogfork.telegram.org/bots/payments-stars?utm_source=chatgpt.com) [oai_citation:2‡github.com](https://github.com/xep1x/telegram-bot-payments?utm_source=chatgpt.com) [oai_citation:3‡habr.com](https://habr.com/ru/articles/821415/?utm_source=chatgpt.com) [oai_citation:4‡dev.to](https://dev.to/king_triton/integrating-telegram-stars-payment-in-a-python-bot-3667?utm_source=chatgpt.com) [oai_citation:5‡habr.com](https://habr.com/ru/sandbox/244248/?utm_source=chatgpt.com) [oai_citation:6‡habr.com](https://habr.com/ru/articles/907158/?utm_source=chatgpt.com)
        currency="XTR",
        prices=prices,
        reply_markup=payment_kb(amount)
    )

# --- pre_checkout (подтверждение) ---
@bot.pre_checkout_query_handler(func=lambda q: True)
def precheckout(q):
    bot.answer_pre_checkout_query(q.id, ok=True)

# --- Успешный платёж ---
@bot.message_handler(content_types=['successful_payment'])
def successful_payment(msg: types.Message):
    uid = msg.from_user.id
    pay = msg.successful_payment
    tx = pay.provider_payment_charge_id or pay.telegram_payment_charge_id
    amount = pay.total_amount
    if save_payment(tx, uid, amount):
        newbal = add_balance(uid, amount)
        bot.send_message(msg.chat.id, f"✅ Спасибо! Твой баланс: ⭐{newbal}",
                         reply_markup=main_kb(newbal))
    else:
        bot.send_message(msg.chat.id, "ℹ Эта транзакция уже учтена.")

if __name__ == "__main__":
    bot.infinity_polling()
