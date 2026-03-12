import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./research_agent.db")


def sql_query_tool(query: str) -> str:
    """
    Executes a SQL query on the SQLite database and returns the result.
    """

    try:
        # Extract SQLite database file path
        if DATABASE_URL.startswith("sqlite:///"):
            db_path = DATABASE_URL.replace("sqlite:///", "")
        else:
            return "Only SQLite databases are supported."

        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)

        # Enable dictionary-style row access
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch results
        rows = cursor.fetchall()

        conn.close()

        # If query returns no results
        if not rows:
            return "Query executed successfully."

        # Convert rows to readable output
        results = []
        for row in rows:
            results.append(dict(row))

        return str(results)

    except Exception as e:
        return f"SQL Error: {str(e)}"