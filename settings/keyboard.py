from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🛒 Купить ордер", callback_data="buy"), 
        InlineKeyboardButton(text="📦 Заказать", callback_data="order")
    ],
    [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")]
])

back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
])

buy_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1 ордер (1 звезда)", callback_data="buy1")],
    [InlineKeyboardButton(text="5 ордеров (4 звезды)", callback_data="buy5")],
    [InlineKeyboardButton(text="10 ордеров (7 звезд)", callback_data="buy10")],
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
])

pay_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Оплатить", pay=True)],
    [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
])