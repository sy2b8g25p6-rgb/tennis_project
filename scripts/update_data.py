import pandas as pd
import sqlite3
from datetime import datetime

CSV_FILE = "data/tennis_data.csv"
DB_FILE = "tennis.db"

def update_db():
    print("Aggiornamento database...")

    df = pd.read_csv(CSV_FILE)

    # pulizia base
    df.columns = df.columns.str.strip()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # qui puoi riusare la tua logica di import
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO matches (
                    date, tournament, round, player_1, player_2,
                    winner, score, surface, court, best_of
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["Date"],
                row["Tournament"],
                row["Round"],
                row["Player_1"],
                row["Player_2"],
                row["Winner"],
                row["Score"],
                row["Surface"],
                row["Court"],
                row["Best of"]
            ))
        except Exception as e:
            print("Errore riga:", e)

    conn.commit()
    conn.close()

    print("Update completato:", datetime.now())

if __name__ == "__main__":
    update_db()
