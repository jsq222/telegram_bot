import sqlite3

def init_db():
    db = sqlite3.connect("bot.db")
    cursor = db.cursor()

    # Создаём таблицу пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER UNIQUE,
        username TEXT,
        subscription_end DATETIME,
        payment_status BOOLEAN DEFAULT FALSE
    )
    """)
    db.commit()
    return db

db = init_db()
