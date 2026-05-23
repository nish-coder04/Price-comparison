import sqlite3
from datetime import datetime

DB_NAME = "prices.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            platform TEXT NOT NULL,
            price REAL NOT NULL,
            unit TEXT,
            available INTEGER DEFAULT 1,
            delivery_time TEXT,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_price(product_name, platform, price, unit="", available=True, delivery_time=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO price_history (product_name, platform, price, unit, available, delivery_time, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (product_name.lower(), platform, price, unit, 1 if available else 0, delivery_time,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_price_history(product_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT platform, price, unit, timestamp FROM price_history
        WHERE LOWER(product_name) LIKE ?
        ORDER BY timestamp DESC LIMIT 30
    ''', (f"%{product_name.lower()}%",))
    rows = cursor.fetchall()
    conn.close()
    return [{"platform": r[0], "price": r[1], "unit": r[2], "timestamp": r[3]} for r in rows]
