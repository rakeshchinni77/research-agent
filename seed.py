import sqlite3

DATABASE_FILE = "research_agent.db"


def seed_database():
    """
    Creates the users table and inserts sample users.
    """

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        signup_date TEXT NOT NULL
    )
    """)

    # Sample users
    users_to_add = [
        (1, "Alice", "2023-01-15"),
        (2, "Bob", "2023-02-20"),
        (3, "Charlie", "2023-03-10")
    ]

    # Insert users (ignore duplicates)
    for user in users_to_add:
        cursor.execute(
            "INSERT OR IGNORE INTO users (id, name, signup_date) VALUES (?, ?, ?)",
            user
        )

    connection.commit()
    connection.close()

    print("Database seeded successfully.")


if __name__ == "__main__":
    seed_database()