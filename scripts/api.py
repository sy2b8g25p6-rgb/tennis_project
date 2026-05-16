from fastapi import FastAPI
import sqlite3
import os

app = FastAPI()

DB_FILE = "atp_tennis.db"


# -------------------------
# DATABASE CONNECTION
# -------------------------
def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# DATABASE INIT (CRUCIAL FOR RENDER)
# -------------------------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tourney_name TEXT,
        tourney_date TEXT,
        player_1 TEXT,
        player_2 TEXT,
        winner TEXT,
        score TEXT
    )
    """)

    conn.commit()
    conn.close()


# inizializza DB all’avvio server
init_db()


# -------------------------
# API ROUTES
# -------------------------
@app.get("/")
def home():
    return {"status": "ok", "message": "ATP Tennis API running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/matches/latest")
def latest_matches(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM matches
        ORDER BY tourney_date DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/player/{name}")
def player_matches(name: str, limit: int = 20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM matches
        WHERE player_1 = ? OR player_2 = ?
        ORDER BY tourney_date DESC
        LIMIT ?
    """, (name, name, limit))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/match/{match_id}")
def get_match(match_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM matches
        WHERE id = ?
    """, (match_id,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {"error": "match not found"}

    return dict(row)
