import sqlite3
from models import Transaction

DB_NAME = "despesas.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_transaction(transaction: Transaction):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO transacoes (valor, categoria, data, tipo)
        VALUES (?, ?, ?, ?)
    """, (transaction.valor, transaction.categoria, transaction.data, transaction.tipo))
    conn.commit()
    conn.close()

def get_transactions():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, valor, categoria, data, tipo FROM transacoes")
    rows = c.fetchall()
    conn.close()
    return [Transaction(*row) for row in rows]
    descricao: str | None