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

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS master_password (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password_hash BLOB NOT NULL
                )
                """
            )
            conn.commit()

    def get_key(self) -> bytes:
        """Retrieves the master password hash from the database.

        Returns:
            bytes: The master password hash.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM master_password WHERE id = 1")
            row = cursor.fetchone()
            if row:
                return row[0]

            else:
                raise ValueError(
                    "Master password not set in the database. Create a new master password."
                )

    def set_key(self, password_hash: bytes) -> None:
        """Sets the master password hash in the database.

        Args:
            password_hash (bytes): The master password hash to store.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO master_password (password_hash) VALUES (?)",
                (password_hash,),
            )
            conn.commit()
