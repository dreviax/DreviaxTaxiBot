import aiosqlite
import asyncio

DB_PATH = "orders.db"

# Инициализация БД
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            num_order INTEGER DEFAULT 0
        )
        """)
        await db.commit()

# Добавить пользователя, если ещё нет
async def add_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        INSERT OR IGNORE INTO users (user_id, num_order)
        VALUES (?, 0)
        """, (user_id,))
        await db.commit()

# Увеличить количество заказов
async def add_order(user_id: int, count: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        UPDATE users
        SET num_order = num_order + ?
        WHERE user_id = ?
        """, (count, user_id))
        await db.commit()

# Уменьшить количество заказов
async def de_order(user_id: int, count: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        UPDATE users
        SET num_order = MAX(num_order - ?, 0)
        WHERE user_id = ?
        """, (count, user_id))
        await db.commit()

# Получить количество заказов
async def get_orders(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT num_order FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

