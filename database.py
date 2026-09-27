import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "review_classifier"),
}


def get_connection():
    """Return a new MySQL connection using credentials from environment variables."""
    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    """Create the users and predictions tables if they don't already exist.

    Safe to call every time the app starts — it only creates tables that
    are missing, it never drops or overwrites existing data.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            review_text TEXT NOT NULL,
            prediction TINYINT NOT NULL,
            sentiment_pos FLOAT,
            sentiment_neu FLOAT,
            sentiment_neg FLOAT,
            sentiment_compound FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
