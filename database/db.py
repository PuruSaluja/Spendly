import os
import sqlite3
from datetime import date

from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "expense_tracker.db",
)

CATEGORIES = [
    "Food",
    "Transport",
    "Bills",
    "Health",
    "Entertainment",
    "Shopping",
    "Other",
]


def get_db():
    """Return a SQLite connection with Row access and foreign keys enforced."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they do not already exist."""
    conn = get_db()
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TEXT DEFAULT (datetime('now'))
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT DEFAULT (datetime('now'))
                )
                """
            )
    finally:
        conn.close()


def seed_db():
    """Insert a demo user and sample expenses, once."""
    conn = get_db()
    try:
        if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
            return

        today = date.today()

        entries = [
            (42.50, "Food", "Weekly groceries"),
            (18.00, "Transport", "Metro card top-up"),
            (120.00, "Bills", "Electricity bill"),
            (35.75, "Health", "Pharmacy"),
            (24.99, "Entertainment", "Movie night"),
            (89.90, "Shopping", "New running shoes"),
            (15.00, "Other", "Gift card"),
            (27.40, "Food", "Dinner out"),
        ]

        # Spread evenly from the 1st of the month up to today, so dates stay
        # in the current month and are never in the future.
        last = len(entries) - 1
        samples = [
            (
                amount,
                category,
                date(
                    today.year,
                    today.month,
                    1 + round(i * (today.day - 1) / last),
                ).isoformat(),
                description,
            )
            for i, (amount, category, description) in enumerate(entries)
        ]

        with conn:
            cur = conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
            )
            user_id = cur.lastrowid
            conn.executemany(
                "INSERT INTO expenses (user_id, amount, category, date, description) "
                "VALUES (?, ?, ?, ?, ?)",
                [(user_id, amt, cat, d, desc) for amt, cat, d, desc in samples],
            )
    finally:
        conn.close()
