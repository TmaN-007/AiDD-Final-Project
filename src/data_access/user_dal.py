"""
Data Access Layer for User operations.
Encapsulates all database interactions for the users table.

# AI Contribution: Structure suggested by Copilot; implemented and validated by team.
"""

from src.data_access.database import Database
from datetime import datetime


class UserDAL:
    """Data Access Layer for User CRUD operations."""

    def __init__(self, db: Database):
        """Initialize UserDAL with database connection."""
        self.db = db

    def create_user(self, name, email, password_hash, role='student', department=None):
        """
        Create a new user.

        Args:
            name: User's full name
            email: User's email (must be unique)
            password_hash: Hashed password
            role: User role (student, staff, admin)
            department: Optional department

        Returns:
            user_id of created user or None if failed
        """
        query = """
            INSERT INTO users (name, email, password_hash, role, department)
            VALUES (?, ?, ?, ?, ?)
        """
        try:
            user_id = self.db.execute_query(
                query, (name, email, password_hash, role, department)
            )
            return user_id
        except Exception:
            return None

    def get_user_by_id(self, user_id):
        """Get user by ID."""
        query = "SELECT * FROM users WHERE user_id = ?"
        return self.db.execute_query(query, (user_id,), fetch_one=True)

    def get_user_by_email(self, email):
        """Get user by email."""
        query = "SELECT * FROM users WHERE email = ?"
        return self.db.execute_query(query, (email,), fetch_one=True)

    def update_user(self, user_id, **kwargs):
        """
        Update user information.

        Args:
            user_id: User ID to update
            **kwargs: Fields to update (name, email, department, profile_image)

        Returns:
            True if successful, False otherwise
        """
        allowed_fields = ['name', 'email', 'department', 'profile_image']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not updates:
            return False

        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        query = f"UPDATE users SET {set_clause} WHERE user_id = ?"
        values = list(updates.values()) + [user_id]

        try:
            self.db.execute_query(query, tuple(values))
            return True
        except Exception:
            return False

    def delete_user(self, user_id):
        """Delete a user."""
        query = "DELETE FROM users WHERE user_id = ?"
        try:
            self.db.execute_query(query, (user_id,))
            return True
        except Exception:
            return False

    def get_all_users(self, role=None):
        """
        Get all users, optionally filtered by role.

        Args:
            role: Optional role filter

        Returns:
            List of user records
        """
        if role:
            query = "SELECT * FROM users WHERE role = ? ORDER BY created_at DESC"
            return self.db.execute_query(query, (role,), fetch_all=True)
        else:
            query = "SELECT * FROM users ORDER BY created_at DESC"
            return self.db.execute_query(query, fetch_all=True)

    def user_exists(self, email):
        """Check if user with email exists."""
        user = self.get_user_by_email(email)
        return user is not None

    def update_password(self, user_id, new_password_hash):
        """Update user password."""
        query = "UPDATE users SET password_hash = ? WHERE user_id = ?"
        try:
            self.db.execute_query(query, (new_password_hash, user_id))
            return True
        except Exception:
            return False
