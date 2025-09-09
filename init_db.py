import sqlite3, json, pandas as pd
from pathlib import Path

ART = Path("artifacts")
DB = "telecom.db"

def create_tables(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS plans (
      plan_id INTEGER PRIMARY KEY,
      name TEXT,
      price REAL,
      centroid TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      phone TEXT UNIQUE,
      current_plan_id INTEGER,
      day_mins REAL,
      eve_mins REAL,
      night_mins REAL,
      intl_mins REAL,
      custserv_calls REAL
    )""")
    conn.commit()

def load_plans(conn, csv_path):
    df = pd.read_csv(csv_path)
    for _, r in df.iterrows():
        cur = conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO plans (plan_id, name, price, centroid)
        VALUES (?, ?, ?, ?)
        """, (int(r["plan_id"]), r["name"], float(r.get("price", 0)), str(r["centroid"])))
    conn.commit()

def insert_sample_customers(conn):
    cur = conn.cursor()
    samples = [
      ("382-4657", 0, 120, 100, 80, 5, 1),
      ("358-1921", 2, 600, 400, 300, 50, 2),
      ("350-8884", 1, 300, 200, 150, 10, 1)
    ]
    for phone, plan_id, d,e,n,i,c in samples:
        cur.execute("""
          INSERT OR IGNORE INTO customers (phone, current_plan_id, day_mins, eve_mins, night_mins, intl_mins, custserv_calls)
          VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (phone, plan_id, d, e, n, i, c))
    conn.commit()

if __name__ == "__main__":
    conn = sqlite3.connect(DB)
    create_tables(conn)
    load_plans(conn, ART / "plan_catalog.csv")
    insert_sample_customers(conn)
    conn.close()
    print("DB initialized:", DB)

