"""Verify database schema and contents."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "products.db"


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
    if not cur.fetchone():
        print("ERROR: table 'products' not found")
        sys.exit(1)
    cur.execute("PRAGMA table_info(products)")
    columns = {row[1]: row for row in cur.fetchall()}
    print("Columns:", list(columns.keys()))
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    print(f"Row count: {len(rows)}")
    for row in rows:
        print(row)
    conn.close()


if __name__ == "__main__":
    import sys

    main()
