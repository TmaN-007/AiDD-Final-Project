"""
Data Access Layer for Review operations.
Encapsulates all database interactions for the reviews table.
"""

from src.data_access.database import Database


class ReviewDAL:
    """Data Access Layer for Review CRUD operations."""

    def __init__(self, db: Database):
        """Initialize ReviewDAL with database connection."""
        self.db = db

    def create_review(self, resource_id, reviewer_id, rating, comment=None):
        """
        Create a new review.

        Args:
            resource_id: ID of the resource being reviewed
            reviewer_id: ID of the reviewer
            rating: Rating (1-5)
            comment: Optional comment

        Returns:
            review_id of created review or None if user already reviewed
        """
        query = """
            INSERT INTO reviews (resource_id, reviewer_id, rating, comment)
            VALUES (?, ?, ?, ?)
        """
        try:
            return self.db.execute_query(query, (resource_id, reviewer_id, rating, comment))
        except Exception:
            # Likely duplicate review (unique constraint)
            return None

    def get_review_by_id(self, review_id):
        """Get review by ID."""
        query = "SELECT * FROM reviews WHERE review_id = ?"
        return self.db.execute_query(query, (review_id,), fetch_one=True)

    def get_reviews_by_resource(self, resource_id):
        """Get all reviews for a resource."""
        query = """
            SELECT r.*, u.name as reviewer_name
            FROM reviews r
            JOIN users u ON r.reviewer_id = u.user_id
            WHERE r.resource_id = ?
            ORDER BY r.timestamp DESC
        """
        return self.db.execute_query(query, (resource_id,), fetch_all=True)

    def get_reviews_by_user(self, reviewer_id):
        """Get all reviews written by a user."""
        query = """
            SELECT r.*, res.title as resource_title
            FROM reviews r
            JOIN resources res ON r.resource_id = res.resource_id
            WHERE r.reviewer_id = ?
            ORDER BY r.timestamp DESC
        """
        return self.db.execute_query(query, (reviewer_id,), fetch_all=True)

    def get_average_rating(self, resource_id):
        """Get average rating for a resource."""
        query = """
            SELECT AVG(rating) as avg_rating, COUNT(*) as review_count
            FROM reviews
            WHERE resource_id = ?
        """
        result = self.db.execute_query(query, (resource_id,), fetch_one=True)
        if result and result['review_count'] > 0:
            return {
                'avg_rating': round(result['avg_rating'], 1),
                'review_count': result['review_count']
            }
        return {'avg_rating': 0, 'review_count': 0}

    def user_has_reviewed(self, resource_id, reviewer_id):
        """Check if user has already reviewed a resource."""
        query = """
            SELECT COUNT(*) as count
            FROM reviews
            WHERE resource_id = ? AND reviewer_id = ?
        """
        result = self.db.execute_query(query, (resource_id, reviewer_id), fetch_one=True)
        return result['count'] > 0 if result else False

    def update_review(self, review_id, rating, comment):
        """Update an existing review."""
        query = """
            UPDATE reviews
            SET rating = ?, comment = ?, timestamp = CURRENT_TIMESTAMP
            WHERE review_id = ?
        """
        try:
            self.db.execute_query(query, (rating, comment, review_id))
            return True
        except Exception:
            return False

    def delete_review(self, review_id):
        """Delete a review."""
        query = "DELETE FROM reviews WHERE review_id = ?"
        try:
            self.db.execute_query(query, (review_id,))
            return True
        except Exception:
            return False

    def get_all_reviews(self, limit=None):
        """Get all reviews (for admin)."""
        query = """
            SELECT r.*, u.name as reviewer_name, res.title as resource_title
            FROM reviews r
            JOIN users u ON r.reviewer_id = u.user_id
            JOIN resources res ON r.resource_id = res.resource_id
            ORDER BY r.timestamp DESC
        """
        if limit:
            query += f" LIMIT {limit}"

        return self.db.execute_query(query, fetch_all=True)
