import pandas as pd
import sqlite3

# =========================
# FILE CONFIG
# =========================
CSV_FILE = "data/tennis_data.csv"
DB_FILE = "tennis.db"

# =========================
# CONNESSIONE DATABASE
# =========================
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# =========================
# CREAZIONE TABELLA
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    date TEXT,
    tournament TEXT,
    round TEXT,
    player_1 TEXT,
    player_2 TEXT,
    winner TEXT,
    score TEXT,
    surface TEXT,
    court TEXT,
    best_of INTEGER
)
""")

conn.commit()

# =========================
# LETTURA CSV
# =========================
df = pd.read_csv(CSV_FILE)

# =========================
# CREAZIONE MATCH_ID UNICO
# =========================
def create_match_id(row):
    return f"{row['Date']}_{row['Player_1']}_{row['Player_2']}_{row['Tournament']}"

df["match_id"] = df.apply(create_match_id, axis=1)

# =========================
# IMPORT DATI
# =========================
inserted = 0
skipped = 0

for _, row in df.iterrows():

    cursor.execute(
        "SELECT 1 FROM matches WHERE match_id = ?",
        (row["match_id"],)
    )

    exists = cursor.fetchone()

    if exists:
        skipped += 1
        continue

    cursor.execute("""
        INSERT INTO matches (
            match_id,
            date,
            tournament,
            round,
            player_1,
            player_2,
            winner,
            score,
            surface,
            court,
            best_of
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["match_id"],
        row.get("date"),
        row.get("tournament"),
        row.get("round"),
        row.get("player_1"),
        row.get("player_2"),
        row.get("winner"),
        row.get("score"),
        row.get("surface"),
        row.get("court"),
        row.get("best_of")
    ))

    inserted += 1

# =========================
# SALVATAGGIO E CHIUSURA
# =========================
conn.commit()
conn.close()

# =========================
# OUTPUT FINALE
# =========================
print("IMPORT COMPLETATO")
print(f"Inseriti: {inserted}")
print(f"Saltati (duplicati): {skipped}")
