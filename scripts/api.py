import os
import psycopg2
from fastapi import FastAPI

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL not set")


# -------------------------
# DB CONNECTION
# -------------------------
def get_connection():
    return psycopg2.connect(DATABASE_URL)


# -------------------------
# ROOT
# -------------------------
@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "ATP Tennis API running (PostgreSQL)"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


# -------------------------
# LATEST MATCHES
# -------------------------
@app.get("/matches/latest")
def latest_matches(limit: int = 10):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, tourney_date, player_1, player_2, winner, score
        FROM matches
        ORDER BY tourney_date DESC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "tourney_date": r[1],
            "player_1": r[2],
            "player_2": r[3],
            "winner": r[4],
            "score": r[5]
        }
        for r in rows
    ]


# -------------------------
# PLAYER SEARCH
# -------------------------
@app.get("/player/{name}")
def player_matches(name: str, limit: int = 20):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, tourney_date, player_1, player_2, winner, score
        FROM matches
        WHERE player_1 = %s OR player_2 = %s
        ORDER BY tourney_date DESC
        LIMIT %s
    """, (name, name, limit))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "tourney_date": r[1],
            "player_1": r[2],
            "player_2": r[3],
            "winner": r[4],
            "score": r[5]
        }
        for r in rows
    ]


# -------------------------
# SINGLE MATCH
# -------------------------
@app.get("/match/{match_id}")
def get_match(match_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, tourney_date, player_1, player_2, winner, score
        FROM matches
        WHERE id = %s
    """, (match_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return {"error": "match not found"}

    return {
        "id": row[0],
        "tourney_date": row[1],
        "player_1": row[2],
        "player_3": row[3],
        "winner": row[4],
        "score": row[5]
    }