import sqlite3

class DatabaseManager:
    def __init__(self):
        pass

    def save_score(self, name, score, difficulty, subject):
        conn = sqlite3.connect('scores.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                score INTEGER,
                difficulty TEXT,
                subject TEXT
            )
        ''')
        c.execute('''
            INSERT INTO scores (name, score, difficulty, subject)
            VALUES (?, ?, ?, ?)
        ''', (name, score, difficulty, subject))
        conn.commit()
        conn.close()
