"""
Data Access Layer for Booking operations.
Encapsulates all database interactions for the bookings table.
"""

from src.data_access.database import Database
from datetime import datetime


class BookingDAL:
    """Data Access Layer for Booking CRUD operations."""

    def __init__(self, db: Database):
        """Initialize BookingDAL with database connection."""
        self.db = db

    def create_booking(self, resource_id, requester_id, start_datetime, end_datetime, notes=None):
        """
        Create a new booking.

        Args:
            resource_id: ID of the resource to book
            requester_id: ID of the user requesting booking
            start_datetime: Booking start time
            end_datetime: Booking end time
            notes: Optional notes

        Returns:
            booking_id of created booking
        """
        query = """
            INSERT INTO bookings (resource_id, requester_id, start_datetime, end_datetime, notes, status)
            VALUES (?, ?, ?, ?, ?, 'pending')
        """
        return self.db.execute_query(
            query, (resource_id, requester_id, start_datetime, end_datetime, notes)
        )

    def get_booking_by_id(self, booking_id):
        """Get booking by ID."""
        query = "SELECT * FROM bookings WHERE booking_id = ?"
        return self.db.execute_query(query, (booking_id,), fetch_one=True)

    def update_booking_status(self, booking_id, status):
        """
        Update booking status.

        Args:
            booking_id: Booking ID to update
            status: New status (pending, approved, rejected, cancelled, completed)

        Returns:
            True if successful, False otherwise
        """
        query = """
            UPDATE bookings
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE booking_id = ?
        """
        try:
            self.db.execute_query(query, (status, booking_id))
            return True
        except Exception:
            return False

    def get_bookings_by_requester(self, requester_id):
        """Get all bookings made by a user."""
        query = """
            SELECT b.*, r.title as resource_title, r.location as resource_location
            FROM bookings b
            JOIN resources r ON b.resource_id = r.resource_id
            WHERE b.requester_id = ?
            ORDER BY b.start_datetime DESC
        """
        return self.db.execute_query(query, (requester_id,), fetch_all=True)

    def get_bookings_by_resource(self, resource_id):
        """Get all bookings for a resource."""
        query = """
            SELECT b.*, u.name as requester_name, u.email as requester_email
            FROM bookings b
            JOIN users u ON b.requester_id = u.user_id
            WHERE b.resource_id = ?
            ORDER BY b.start_datetime DESC
        """
        return self.db.execute_query(query, (resource_id,), fetch_all=True)

    def check_booking_conflict(self, resource_id, start_datetime, end_datetime, exclude_booking_id=None):
        """
        Check if a booking conflicts with existing bookings.

        Args:
            resource_id: Resource to check
            start_datetime: Proposed start time
            end_datetime: Proposed end time
            exclude_booking_id: Optional booking ID to exclude from conflict check

        Returns:
            True if conflict exists, False otherwise
        """
        query = """
            SELECT COUNT(*) as conflict_count
            FROM bookings
            WHERE resource_id = ?
            AND status IN ('approved', 'pending')
            AND (
                (start_datetime < ? AND end_datetime > ?)
                OR (start_datetime < ? AND end_datetime > ?)
                OR (start_datetime >= ? AND end_datetime <= ?)
            )
        """
        params = [resource_id, end_datetime, start_datetime, end_datetime, start_datetime, start_datetime, end_datetime]

        if exclude_booking_id:
            query += " AND booking_id != ?"
            params.append(exclude_booking_id)

        result = self.db.execute_query(query, tuple(params), fetch_one=True)
        return result['conflict_count'] > 0 if result else False

    def get_pending_bookings(self):
        """Get all pending bookings (for admin/staff approval)."""
        query = """
            SELECT b.*, r.title as resource_title, u.name as requester_name
            FROM bookings b
            JOIN resources r ON b.resource_id = r.resource_id
            JOIN users u ON b.requester_id = u.user_id
            WHERE b.status = 'pending'
            ORDER BY b.created_at ASC
        """
        return self.db.execute_query(query, fetch_all=True)

    def get_bookings_by_owner(self, owner_id):
        """Get all bookings for resources owned by a user."""
        query = """
            SELECT b.*, r.title as resource_title, u.name as requester_name, u.email as requester_email
            FROM bookings b
            JOIN resources r ON b.resource_id = r.resource_id
            JOIN users u ON b.requester_id = u.user_id
            WHERE r.owner_id = ?
            ORDER BY b.start_datetime DESC
        """
        return self.db.execute_query(query, (owner_id,), fetch_all=True)

    def get_upcoming_bookings(self, user_id):
        """Get upcoming approved bookings for a user."""
        query = """
            SELECT b.*, r.title as resource_title, r.location as resource_location
            FROM bookings b
            JOIN resources r ON b.resource_id = r.resource_id
            WHERE b.requester_id = ?
            AND b.status = 'approved'
            AND b.start_datetime > datetime('now')
            ORDER BY b.start_datetime ASC
        """
        return self.db.execute_query(query, (user_id,), fetch_all=True)

    def get_booking_with_details(self, booking_id):
        """Get booking with resource and user details."""
        query = """
            SELECT b.*, r.title as resource_title, r.location as resource_location,
                   u.name as requester_name, u.email as requester_email,
                   owner.name as owner_name, owner.email as owner_email
            FROM bookings b
            JOIN resources r ON b.resource_id = r.resource_id
            JOIN users u ON b.requester_id = u.user_id
            JOIN users owner ON r.owner_id = owner.user_id
            WHERE b.booking_id = ?
        """
        return self.db.execute_query(query, (booking_id,), fetch_one=True)

    def delete_booking(self, booking_id):
        """Delete a booking."""
        query = "DELETE FROM bookings WHERE booking_id = ?"
        try:
            self.db.execute_query(query, (booking_id,))
            return True
        except Exception:
            return False
