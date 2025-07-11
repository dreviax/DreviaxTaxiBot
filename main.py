import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from settings.database import init_db, add_user, add_order, de_order, get_orders
from settings.config import BOT_TOKEN, menu_text
from settings.keyboard import *

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

### ОСНОВНОЕ МЕНЮ ###

@dp.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    await add_user(user_id)
    await message.answer(menu_text, reply_markup=start_keyboard, parse_mode="MarkdownV2")

@dp.callback_query()
async def handle_buttons(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data

    if data == "buy":
        text = "🛒 *Выберите форму покупки в Telegram Stars:*"
        markup = buy_keyboard
    
    elif data == "buy1":
        await bot.send_invoice(
            chat_id=callback.message.chat.id,
            title="Покупка 1 ордера",
            description="Покупка 1 ордера за 1 Telegram Star",
            payload="buy1_order",
            currency="XTR",
            prices=[LabeledPrice(label="1 ордер", amount=1)],
            provider_token="",
            reply_markup=pay_keyboard
        )

    elif data == "buy5":
        await bot.send_invoice(
            chat_id=callback.message.chat.id,
            title="Покупка 5 ордеров",
            description="Покупка 5 ордеров за 4 Telegram Stars",
            payload="buy5_orders",
            currency="XTR",
            prices=[LabeledPrice(label="5 ордеров", amount=4)],
            provider_token="",
            reply_markup=pay_keyboard
        )

    elif data == "buy10":
        await bot.send_invoice(
            chat_id=callback.message.chat.id,
            title="Покупка 10 ордеров",
            description="Покупка 10 ордеров за 7 Telegram Stars",
            payload="buy10_orders",
            currency="XTR",
            prices=[LabeledPrice(label="10 ордеров", amount=7)],
            provider_token="",
            reply_markup=pay_keyboard
        )

    elif data == "order":
        orders = await get_orders(user_id)
        if orders > 0:
            text = "📦 *Пришлите ссылку на сообщение для заказа:*"
            markup = back_keyboard
        else:
            text = "📦 *У вас нет ордеров\\.*"
            markup = back_keyboard
            
    elif data == "profile":
        orders = await get_orders(user_id)
        text = f"👤 *Ваш профиль:*\n🆔 *ID:* `{user_id}`\n📦 *Ордеров:* `{orders}`"
        markup = back_keyboard

    elif data == "cancel":
        await callback.message.delete()

    elif data == "back":
        text = menu_text
        markup = start_keyboard

    else:
        text = menu_text
        markup = start_keyboard

    if data in ["buy", "order", "profile", "back"]:
        await callback.message.edit_text(text, reply_markup=markup, parse_mode="MarkdownV2")
    await callback.answer()

### ОСНОВНОЕ МЕНЮ ###

### ОПЛАТА TELEGRAM STARS ###

@dp.pre_checkout_query()
async def pre_checkout_query(pre_checkout: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    user_id = message.from_user.id
    payload = message.successful_payment.invoice_payload
    
    if payload == "buy1_order":
        await add_order(user_id, 1)
        await message.answer("✅ *Успешно приобретен 1 ордер\\!*", reply_markup=back_keyboard, parse_mode="MarkdownV2")
    elif payload == "buy5_orders":
        await add_order(user_id, 5)
        await message.answer("✅ *Успешно приобретено 5 ордеров\\!*", reply_markup=back_keyboard, parse_mode="MarkdownV2")
    elif payload == "buy10_orders":
        await add_order(user_id, 10)
        await message.answer("✅ *Успешно приобретено 10 ордеров\\!*", reply_markup=back_keyboard, parse_mode="MarkdownV2")

### ОПЛАТА TELEGRAM STARS ###

### MAIN ФУНКЦИЯ ###

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

### MAIN ФУНКЦИЯ ###