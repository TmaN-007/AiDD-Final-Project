"""
Data Access Layer for Message operations.
Encapsulates all database interactions for the messages table.
"""

from src.data_access.database import Database


class MessageDAL:
    """Data Access Layer for Message CRUD operations."""

    def __init__(self, db: Database):
        """Initialize MessageDAL with database connection."""
        self.db = db

    def create_message(self, thread_id, sender_id, receiver_id, content):
        """
        Create a new message.

        Args:
            thread_id: Message thread ID
            sender_id: ID of sender
            receiver_id: ID of receiver
            content: Message content

        Returns:
            message_id of created message
        """
        query = """
            INSERT INTO messages (thread_id, sender_id, receiver_id, content)
            VALUES (?, ?, ?, ?)
        """
        return self.db.execute_query(query, (thread_id, sender_id, receiver_id, content))

    def get_message_by_id(self, message_id):
        """Get message by ID."""
        query = "SELECT * FROM messages WHERE message_id = ?"
        return self.db.execute_query(query, (message_id,), fetch_one=True)

    def get_thread_messages(self, thread_id):
        """Get all messages in a thread."""
        query = """
            SELECT m.*,
                   sender.name as sender_name,
                   receiver.name as receiver_name
            FROM messages m
            JOIN users sender ON m.sender_id = sender.user_id
            JOIN users receiver ON m.receiver_id = receiver.user_id
            WHERE m.thread_id = ?
            ORDER BY m.timestamp ASC
        """
        return self.db.execute_query(query, (thread_id,), fetch_all=True)

    def get_user_threads(self, user_id):
        """
        Get all message threads for a user.

        Returns list of threads with latest message info.
        """
        query = """
            SELECT DISTINCT
                m.thread_id,
                CASE
                    WHEN m.sender_id = ? THEN m.receiver_id
                    ELSE m.sender_id
                END as other_user_id,
                CASE
                    WHEN m.sender_id = ? THEN receiver.name
                    ELSE sender.name
                END as other_user_name,
                (SELECT content FROM messages m2
                 WHERE m2.thread_id = m.thread_id
                 ORDER BY timestamp DESC LIMIT 1) as last_message,
                (SELECT timestamp FROM messages m2
                 WHERE m2.thread_id = m.thread_id
                 ORDER BY timestamp DESC LIMIT 1) as last_timestamp
            FROM messages m
            JOIN users sender ON m.sender_id = sender.user_id
            JOIN users receiver ON m.receiver_id = receiver.user_id
            WHERE m.sender_id = ? OR m.receiver_id = ?
            GROUP BY m.thread_id
            ORDER BY last_timestamp DESC
        """
        return self.db.execute_query(query, (user_id, user_id, user_id, user_id), fetch_all=True)

    def get_or_create_thread_id(self, user1_id, user2_id):
        """
        Get existing thread ID between two users or create a new one.

        Args:
            user1_id: First user ID
            user2_id: Second user ID

        Returns:
            thread_id
        """
        # Check for existing thread
        query = """
            SELECT DISTINCT thread_id
            FROM messages
            WHERE (sender_id = ? AND receiver_id = ?)
               OR (sender_id = ? AND receiver_id = ?)
            LIMIT 1
        """
        result = self.db.execute_query(
            query, (user1_id, user2_id, user2_id, user1_id), fetch_one=True
        )

        if result:
            return result['thread_id']

        # Create new thread - use combination of user IDs as thread_id
        # For simplicity, thread_id = smaller_id * 100000 + larger_id
        return min(user1_id, user2_id) * 100000 + max(user1_id, user2_id)

    def delete_message(self, message_id):
        """Delete a message."""
        query = "DELETE FROM messages WHERE message_id = ?"
        try:
            self.db.execute_query(query, (message_id,))
            return True
        except Exception:
            return False
