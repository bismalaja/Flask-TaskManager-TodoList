import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "app.db")


def _get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    schema = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        due_date TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT NOT NULL,
        suggested_steps TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """
    with _get_connection() as connection:
        connection.executescript(schema)

        columns = connection.execute("PRAGMA table_info(tasks);").fetchall()
        column_names = {column[1] for column in columns}
        if "suggested_steps" not in column_names:
            connection.execute("ALTER TABLE tasks ADD COLUMN suggested_steps TEXT;")

        connection.commit()


class SQLiteConnection:
    def query_db(self, query, data=None):
        params = data or {}
        with _get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            statement = query.strip().lower()

            if statement.startswith("insert"):
                connection.commit()
                return cursor.lastrowid

            if statement.startswith("select"):
                rows = cursor.fetchall()
                return [dict(row) for row in rows]

            connection.commit()
            return cursor.rowcount


def connect_to_sqlite():
    return SQLiteConnection()
