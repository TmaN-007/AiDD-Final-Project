"""
Data Access Layer for Admin operations.
Encapsulates database interactions for admin logs and analytics.
"""

from src.data_access.database import Database


class AdminDAL:
    """Data Access Layer for Admin operations."""

    def __init__(self, db: Database):
        """Initialize AdminDAL with database connection."""
        self.db = db

    def log_action(self, admin_id, action, target_table, details=None):
        """
        Log an admin action.

        Args:
            admin_id: ID of admin performing action
            action: Description of action
            target_table: Table affected
            details: Optional additional details

        Returns:
            log_id of created log entry
        """
        query = """
            INSERT INTO admin_logs (admin_id, action, target_table, details)
            VALUES (?, ?, ?, ?)
        """
        return self.db.execute_query(query, (admin_id, action, target_table, details))

    def get_admin_logs(self, limit=100):
        """Get recent admin logs."""
        query = """
            SELECT al.*, u.name as admin_name
            FROM admin_logs al
            JOIN users u ON al.admin_id = u.user_id
            ORDER BY al.timestamp DESC
            LIMIT ?
        """
        return self.db.execute_query(query, (limit,), fetch_all=True)

    def get_system_stats(self):
        """Get system-wide statistics."""
        stats = {}

        # Total users by role
        query = "SELECT role, COUNT(*) as count FROM users GROUP BY role"
        role_counts = self.db.execute_query(query, fetch_all=True)
        stats['users_by_role'] = {row['role']: row['count'] for row in role_counts} if role_counts else {}

        # Total resources by status
        query = "SELECT status, COUNT(*) as count FROM resources GROUP BY status"
        resource_counts = self.db.execute_query(query, fetch_all=True)
        stats['resources_by_status'] = {row['status']: row['count'] for row in resource_counts} if resource_counts else {}

        # Total bookings by status
        query = "SELECT status, COUNT(*) as count FROM bookings GROUP BY status"
        booking_counts = self.db.execute_query(query, fetch_all=True)
        stats['bookings_by_status'] = {row['status']: row['count'] for row in booking_counts} if booking_counts else {}

        # Total reviews
        query = "SELECT COUNT(*) as count FROM reviews"
        review_count = self.db.execute_query(query, fetch_one=True)
        stats['total_reviews'] = review_count['count'] if review_count else 0

        # Most booked resources
        query = """
            SELECT r.resource_id, r.title, COUNT(b.booking_id) as booking_count
            FROM resources r
            LEFT JOIN bookings b ON r.resource_id = b.resource_id
            WHERE b.status IN ('approved', 'completed')
            GROUP BY r.resource_id
            ORDER BY booking_count DESC
            LIMIT 5
        """
        most_booked = self.db.execute_query(query, fetch_all=True)
        stats['most_booked_resources'] = [dict(row) for row in most_booked] if most_booked else []

        return stats

    def get_usage_by_category(self):
        """Get booking statistics by resource category."""
        query = """
            SELECT r.category, COUNT(b.booking_id) as booking_count
            FROM resources r
            LEFT JOIN bookings b ON r.resource_id = b.resource_id
            WHERE r.category IS NOT NULL AND b.status IN ('approved', 'completed')
            GROUP BY r.category
            ORDER BY booking_count DESC
        """
        return self.db.execute_query(query, fetch_all=True)

    def get_usage_by_department(self):
        """Get booking statistics by user department."""
        query = """
            SELECT u.department, COUNT(b.booking_id) as booking_count
            FROM users u
            JOIN bookings b ON u.user_id = b.requester_id
            WHERE u.department IS NOT NULL AND b.status IN ('approved', 'completed')
            GROUP BY u.department
            ORDER BY booking_count DESC
        """
        return self.db.execute_query(query, fetch_all=True)
