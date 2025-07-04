import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("krishi.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT,
            advice TEXT,
            temperature REAL,
            humidity REAL,
            pH REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_prediction(disease, advice, temperature, humidity, ph):
    conn = sqlite3.connect("krishi.db")
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO predictions (disease, advice, temperature, humidity, pH, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (disease, advice, temperature, humidity, ph, timestamp))
    conn.commit()
    conn.close()

def get_all_predictions():
    conn = sqlite3.connect("krishi.db")
    c = conn.cursor()
    c.execute("SELECT * FROM predictions")
    rows = c.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "disease": row[1],
            "advice": row[2],
            "temperature": row[3],
            "humidity": row[4],
            "pH": row[5],
            "timestamp": row[6]
        })

    return results
