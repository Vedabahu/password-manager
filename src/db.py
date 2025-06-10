from config import DB_NAME, DB_PATH
from pathlib import Path

import sqlite3


class DataBaseHandler:
    def __init__(self):
        """Initializes the database handler."""
        self.db_path = Path(DB_PATH) / DB_NAME

    def db_init(self) -> None:
        """Initializes the database if it does not exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS vault (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    website TEXT NOT NULL,
                    password TEXT NOT NULL
                )
                """
            )
            conn.commit()
