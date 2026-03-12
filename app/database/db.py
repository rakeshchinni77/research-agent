import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./research_agent.db")


def get_db_connection():
    """
    Creates and returns a SQLite database connection.
    """
    
    # Extract database file path
    if DATABASE_URL.startswith("sqlite:///"):
        db_path = DATABASE_URL.replace("sqlite:///", "")
    else:
        raise ValueError("Only SQLite database is supported.")

    connection = sqlite3.connect(db_path)

    # Enables dictionary-like row access
    connection.row_factory = sqlite3.Row

    return connection