"""
Database connection and initialization module.
Provides database connection management and schema setup.
"""

import sqlite3
import os
from contextlib import contextmanager
from src.models.schema import SCHEMA


class Database:
    """Database connection manager."""

    def __init__(self, db_path='campus_hub.db'):
        """Initialize database connection manager."""
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_db(self):
        """Initialize the database with schema."""
        with self.get_connection() as conn:
            conn.executescript(SCHEMA)

    def execute_query(self, query, params=(), fetch_one=False, fetch_all=False):
        """
        Execute a SQL query with parameterized values.

        Args:
            query: SQL query string
            params: Tuple of parameters for the query
            fetch_one: Return single row
            fetch_all: Return all rows

        Returns:
            Query result or None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                return cursor.lastrowid
