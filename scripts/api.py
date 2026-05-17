import os
import psycopg2
from fastapi import FastAPI

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


@app.get("/")
def home():
    return {"status": "ok", "message": "ATP Tennis API running (PostgreSQL)"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/matches/latest")
def latest_matches(limit: int = 10):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, tourney_date, winner_name, loser_name, score
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
            "winner_name": r[2],
            "loser_name": r[3],
            "score": r[4]
        }
        for r in rows
    ]


@app.get("/player/{name}")
def player_matches(name: str, limit: int = 20):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, tourney_date, winner_name, loser_name, score
        FROM matches
        WHERE winner_name = %s OR loser_name = %s
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
            "winner_name": r[2],
            "loser_name": r[3],
            "score": r[4]
        }
        for r in rows
    ]