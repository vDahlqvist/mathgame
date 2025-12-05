import sqlite3

class DatabaseManager:
    """Manages database operations for storing and retrieving game scores.
    
    This class handles all interactions with the SQLite database, including
    creating tables, saving scores, and retrieving score history.
    """
    
    def __init__(self):
        """Initialize the database manager."""
        pass

    def save_score(self, name, score, difficulty, subject):
        """Save a player's score to the database.
        
        Creates the scores table if it doesn't exist, then inserts a new score record
        with the player's name, score, difficulty level, subject, and timestamp.
        
        Args:
            name (str): The player's name.
            score (int): The player's final score.
            difficulty (str): The difficulty level ("easy" or "hard").
            subject (str): The subject(s) played (e.g., "algebra", "equations").
        """
        conn = sqlite3.connect('scores.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                score INTEGER,
                difficulty TEXT,
                subject TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        c.execute('''
            INSERT INTO scores (name, score, difficulty, subject)
            VALUES (?, ?, ?, ?)
        ''', (name, score, difficulty, subject))
        conn.commit()
        conn.close()
        
    def get_scores(self):
        """Retrieve all scores from the database.
        
        Returns:
            list: List of tuples containing score data. Each tuple contains:
                  (id, name, score, difficulty, subject, date).
        """
        conn = sqlite3.connect('scores.db')
        c = conn.cursor()
        c.execute('''
            SELECT * FROM scores
        ''')
        scores = c.fetchall()
        conn.close()
        return scores

