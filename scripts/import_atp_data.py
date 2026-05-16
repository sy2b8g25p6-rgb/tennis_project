import pandas as pd
import sqlite3
import glob

DB_FILE = "atp_tennis.db"

# Connessione database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Tabella matches
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    tourney_name TEXT,
    surface TEXT,
    tourney_date INTEGER,
    round TEXT,
    winner_name TEXT,
    loser_name TEXT,
    score TEXT,
    best_of INTEGER,
    minutes INTEGER,
    winner_rank INTEGER,
    loser_rank INTEGER
)
""")

# Tutti i file ATP singles
csv_files = glob.glob("tennis_atp/atp_matches_*.csv")

inserted = 0
skipped = 0

for file in csv_files:

    # ignora altri tipi di match
    if "doubles" in file or "futures" in file or "qual" in file:
        continue

    print("Importando:", file)

    df = pd.read_csv(file, low_memory=False)

    for _, row in df.iterrows():

        try:
            tourney_date = int(row["tourney_date"])
        except:
            skipped += 1
            continue

        # chiave unica match
        match_id = f"{tourney_date}_{row['winner_name']}_{row['loser_name']}_{row['tourney_name']}"

        try:
            cursor.execute("""
            INSERT INTO matches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                match_id,
                row["tourney_name"],
                row["surface"],
                tourney_date,
                row["round"],
                row["winner_name"],
                row["loser_name"],
                row["score"],
                row["best_of"],
                row["minutes"],
                row["winner_rank"],
                row["loser_rank"]
            ))

            inserted += 1

        except sqlite3.IntegrityError:
            skipped += 1

conn.commit()
conn.close()

print("\nIMPORT COMPLETATO")
print("Inseriti:", inserted)
print("Saltati (duplicati):", skipped)
