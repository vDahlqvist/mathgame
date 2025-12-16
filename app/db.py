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
        is properly set up before any operations. Uses try-except-finally pattern
        to ensure database connection is properly closed even if errors occur.
        
        Returns:
            bool: True if initialization successful, False if database error occurred.
        """
        conn = None
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
            return True
        
        except sqlite3.Error:
            return False
        finally:
            if conn:
                conn.close()

    def save_score(self, name, score, difficulty, subject):
        """Save a player's score to the database.
        
        Inserts a new score record with the player's name, score, difficulty level,
        subject, and timestamp. Uses try-except-finally pattern to ensure database
        connection is properly closed even if errors occur.
        
        Args:
            name (str): The player's name.
            score (int): The player's final score.
            difficulty (str): The difficulty level ("easy" or "hard").
            subject (str): The subject(s) played (e.g., "algebra", "equations").
            
        Returns:
            bool: True if save successful, False if database error occurred.
        """
        conn = None
        try:
            conn = sqlite3.connect('scores.db')
            c = conn.cursor()

            c.execute('''
                INSERT INTO scores (name, score, difficulty, subject)
                VALUES (?, ?, ?, ?)
            ''', (name, score, difficulty, subject))
            conn.commit()
            return True

        except sqlite3.Error:
            return False
        finally:
            if conn:
                conn.close()
        
    def get_scores(self):
        """Retrieve all scores from the database sorted by score descending.
        
        Queries all saved scores and returns them ordered by highest score first.
        Uses try-except-finally pattern to ensure database connection is properly
        closed even if errors occur. Prints error message to console on failure.
        
        Returns:
            list: List of tuples containing score data. Each tuple contains:
                (name, score, difficulty, subject, date).
                Returns empty list if database error occurs.
        """
        conn = None
        try:
            conn = sqlite3.connect('scores.db')
            c = conn.cursor()
            c.execute('''
                SELECT name, score, difficulty, subject, date
                FROM scores ORDER BY score DESC
            ''')
            scores = c.fetchall()
            return scores
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            if conn:
                conn.close()

