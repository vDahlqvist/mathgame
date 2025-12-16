import sqlite3

class DatabaseManager:
    """Manages database operations for storing and retrieving game scores.
    
    This class handles all interactions with the SQLite database, including
    creating tables, saving scores, and retrieving score history.
    """
    
    def __init__(self):
        """Initialize the database manager."""
        pass

    def init_db(self):
        """Initialize the database by creating the scores table if it doesn't exist.
        
        This should be called at application startup to ensure the database
        is properly set up before any operations.
        
        Returns:
            bool: True if initialization successful, False if database error occurred.
        """
        try:
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
            conn.commit()
            conn.close()
            return True
        
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
            return False
        finally:
            conn.commit()
            conn.close()

    def save_score(self, name, score, difficulty, subject):
        """Save a player's score to the database.
        
        Creates the scores table if it doesn't exist, then inserts a new score record
        with the player's name, score, difficulty level, subject, and timestamp.
        
        Args:
            name (str): The player's name.
            score (int): The player's final score.
            difficulty (str): The difficulty level ("easy" or "hard").
            subject (str): The subject(s) played (e.g., "algebra", "equations").
            
        Returns:
            bool: True if save successful, False if database error occurred.
        """
        try:
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
            return True

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.commit()
            conn.close()
        
    def get_scores(self):
        """Retrieve all scores from the database sorted by score descending.
        
        Returns:
            list: List of tuples containing score data. Each tuple contains:
                  (name, score, difficulty, subject, date).
                  Returns empty list if database error occurs.
        """
        try:
            conn = sqlite3.connect('scores.db')
            c = conn.cursor()
            c.execute('''
                SELECT name, score, difficulty, subject, date
                FROM scores ORDER BY score DESC
            ''')
            scores = c.fetchall()
            conn.close()
            return scores
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()

