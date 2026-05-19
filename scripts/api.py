import os
import psycopg2
from fastapi import FastAPI

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL not set")


# -------------------------
# CONNECTION
# -------------------------
def get_connection():
    return psycopg2.connect(
        DATABASE_URL,
        sslmode="require"
    )
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
    return {
        "status": "healthy",
        "db_check": DATABASE_URL is not None
    }
# -------------------------
# LATEST MATCHES (SAFE VERSION)
# -------------------------
@app.get("/matches/latest")
def latest_matches(limit: int = 10):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM matches
            ORDER BY tourney_date DESC
            LIMIT %s
        """, (limit,))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        # ritorna raw per evitare mismatch colonne
        return [
            list(r)
            for r in rows
        ]

    except Exception as e:
        return {
            "error": str(e)
        }


# -------------------------
# PLAYER MATCHES (SAFE VERSION)
# -------------------------
@app.get("/player/{name}")
def player_matches(name: str, limit: int = 20):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM matches
            WHERE player_1 = %s OR player_2 = %s
            ORDER BY tourney_date DESC
            LIMIT %s
        """, (name, name, limit))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            list(r)
            for r in rows
        ]

    except Exception as e:
        return {
            "error": str(e)
        }


# -------------------------
# SINGLE MATCH
# -------------------------
@app.get("/match/{match_id}")
def get_match(match_id: int):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM matches
            WHERE id = %s
        """, (match_id,))

        row = cur.fetchone()

        cur.close()
        conn.close()

        if not row:
            return {"error": "match not found"}

        return list(row)

    except Exception as e:
        return {
            "error": str(e)
        }