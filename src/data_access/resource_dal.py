"""
Data Access Layer for Resource operations.
Encapsulates all database interactions for the resources table.
"""

from src.data_access.database import Database
import json


class ResourceDAL:
    """Data Access Layer for Resource CRUD operations."""

    def __init__(self, db: Database):
        """Initialize ResourceDAL with database connection."""
        self.db = db

    def create_resource(self, owner_id, title, description, category, location,
                        capacity, images=None, availability_rules=None, status='draft'):
        """
        Create a new resource.

        Args:
            owner_id: ID of the resource owner
            title: Resource title
            description: Resource description
            category: Resource category
            location: Physical location
            capacity: Maximum capacity
            images: JSON string of image paths
            availability_rules: JSON string of availability rules
            status: Resource status (draft, published, archived)

        Returns:
            resource_id of created resource
        """
        query = """
            INSERT INTO resources (owner_id, title, description, category, location,
                                 capacity, images, availability_rules, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self.db.execute_query(
            query, (owner_id, title, description, category, location,
                   capacity, images, availability_rules, status)
        )

    def get_resource_by_id(self, resource_id):
        """Get resource by ID."""
        query = "SELECT * FROM resources WHERE resource_id = ?"
        return self.db.execute_query(query, (resource_id,), fetch_one=True)

    def update_resource(self, resource_id, **kwargs):
        """
        Update resource information.

        Args:
            resource_id: Resource ID to update
            **kwargs: Fields to update

        Returns:
            True if successful, False otherwise
        """
        allowed_fields = ['title', 'description', 'category', 'location',
                         'capacity', 'images', 'availability_rules', 'status']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not updates:
            return False

        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        query = f"UPDATE resources SET {set_clause} WHERE resource_id = ?"
        values = list(updates.values()) + [resource_id]

        try:
            self.db.execute_query(query, tuple(values))
            return True
        except Exception:
            return False

    def delete_resource(self, resource_id):
        """Delete a resource."""
        query = "DELETE FROM resources WHERE resource_id = ?"
        try:
            self.db.execute_query(query, (resource_id,))
            return True
        except Exception:
            return False

    def get_resources_by_owner(self, owner_id):
        """Get all resources owned by a user."""
        query = "SELECT * FROM resources WHERE owner_id = ? ORDER BY created_at DESC"
        return self.db.execute_query(query, (owner_id,), fetch_all=True)

    def search_resources(self, keyword=None, category=None, location=None, status='published'):
        """
        Search resources with filters.

        Args:
            keyword: Search in title and description
            category: Filter by category
            location: Filter by location
            status: Filter by status (default: published)

        Returns:
            List of matching resources
        """
        query = "SELECT * FROM resources WHERE status = ?"
        params = [status]

        if keyword:
            query += " AND (title LIKE ? OR description LIKE ?)"
            search_term = f"%{keyword}%"
            params.extend([search_term, search_term])

        if category:
            query += " AND category = ?"
            params.append(category)

        if location:
            query += " AND location LIKE ?"
            params.append(f"%{location}%")

        query += " ORDER BY created_at DESC"

        return self.db.execute_query(query, tuple(params), fetch_all=True)

    def get_all_resources(self, status=None):
        """
        Get all resources, optionally filtered by status.

        Args:
            status: Optional status filter

        Returns:
            List of resource records
        """
        if status:
            query = "SELECT * FROM resources WHERE status = ? ORDER BY created_at DESC"
            return self.db.execute_query(query, (status,), fetch_all=True)
        else:
            query = "SELECT * FROM resources ORDER BY created_at DESC"
            return self.db.execute_query(query, fetch_all=True)

    def get_categories(self):
        """Get distinct categories."""
        query = "SELECT DISTINCT category FROM resources WHERE status = 'published' AND category IS NOT NULL"
        results = self.db.execute_query(query, fetch_all=True)
        return [row['category'] for row in results] if results else []

    def get_resource_with_owner(self, resource_id):
        """Get resource with owner information joined."""
        query = """
            SELECT r.*, u.name as owner_name, u.email as owner_email
            FROM resources r
            JOIN users u ON r.owner_id = u.user_id
            WHERE r.resource_id = ?
        """
        return self.db.execute_query(query, (resource_id,), fetch_one=True)

    def get_top_rated_resources(self, limit=10):
        """Get top-rated resources based on average review ratings."""
        query = """
            SELECT r.*, AVG(rv.rating) as avg_rating, COUNT(rv.review_id) as review_count
            FROM resources r
            LEFT JOIN reviews rv ON r.resource_id = rv.resource_id
            WHERE r.status = 'published'
            GROUP BY r.resource_id
            HAVING COUNT(rv.review_id) > 0
            ORDER BY avg_rating DESC, review_count DESC
            LIMIT ?
        """
        return self.db.execute_query(query, (limit,), fetch_all=True)
