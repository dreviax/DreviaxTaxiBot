import os
from dotenv import load_dotenv

menu_text = '''*Главное меню:*
🛒 Покупайте ордеры за Telegram Stars
📦 Заказывайте такси'''

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")