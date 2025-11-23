import sqlite3

AUTO_FILE = "parkolo_autok.db"

class AdatokSQL_FÁ:
    @staticmethod
    def init_db():
        conn = sqlite3.connect(AUTO_FILE)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS parkolo (
                id TEXT PRIMARY KEY,
                parknem TEXT,
                rendszam TEXT,
                kezdes TEXT          
            )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def load_all():
        conn = sqlite3.connect(AUTO_FILE)
        cur = conn.cursor()

        cur.execute("SELECT id, parknem, rendszam, kezdes FROM parkolo")
        rows = cur.fetchall()

        data = {}

        for rid, parknem_text, rendszam, kezdes in rows:
            if parknem_text is None:
                parknem_text = "szabad"

            data[rid] = {
                "foglalt": parknem_text,
                "rendszám": rendszam if rendszam else "",
                "kezdes": kezdes if kezdes else ""
            }

        expected = [f"A{i}" for i in range(1, 11)]
        for spot in expected:
            if spot not in data:
                data[spot] = {"foglalt": "szabad", "rendszám": "", "kezdes": ""}
                cur.execute("""
                    INSERT OR IGNORE INTO parkolo (id, parknem, rendszam, kezdes)
                    VALUES (?, 'szabad', '', '')
                """, (spot,))

        conn.commit()
        conn.close()
        return data

    @staticmethod
    def save_spot(spot_id, foglalt_text, rendszam, kezdes):
        conn = sqlite3.connect(AUTO_FILE)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO parkolo (id, parknem, rendszam, kezdes)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                parknem = excluded.parknem,
                rendszam = excluded.rendszam,
                kezdes = excluded.kezdes
        """, (spot_id, foglalt_text, rendszam, kezdes))

        conn.commit()
        conn.close()
