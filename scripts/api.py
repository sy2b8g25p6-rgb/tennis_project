from fastapi import FastAPI
import sqlite3

app = FastAPI()

DB_FILE = "atp_tennis.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


# 🔹 HOME
@app.get("/")
def home():
    return {"status": "ok", "message": "ATP Tennis API running"}


# 🔹 ULTIMI MATCH
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


# 🔹 MATCH PER GIOCATORE
@app.get("/player/{name}")
def player_matches(name: str, limit: int = 20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM matches
        WHERE winner_name = ? OR loser_name = ?
        ORDER BY tourney_date DESC
        LIMIT ?
    """, (name, name, limit))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# 🔹 MATCH BY ID
@app.get("/match/{match_id}")
def get_match(match_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM matches WHERE match_id = ?
    """, (match_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return {"error": "Match not found"}
