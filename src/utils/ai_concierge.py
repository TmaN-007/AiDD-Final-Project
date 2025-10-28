"""
AI Resource Concierge - Context-aware assistant for Campus Resource Hub.

This module provides an AI-powered assistant that helps users find resources,
understand booking policies, and get system insights. It uses context from the
database and project documentation to provide accurate, grounded responses.

# AI Contribution: Core architecture designed with Claude Code assistance.
# This feature demonstrates AI integration requirement for the project.
"""

from src.data_access.database import Database
from src.data_access.resource_dal import ResourceDAL
from src.data_access.booking_dal import BookingDAL
from src.data_access.review_dal import ReviewDAL
from src.data_access.admin_dal import AdminDAL
import json
from datetime import datetime


class ResourceConcierge:
    """
    AI-powered assistant for resource queries.

    This class provides intelligent responses to user queries about campus resources,
    availability, booking policies, and system statistics. All responses are grounded
    in actual database data - NO fabricated information.
    """

    def __init__(self):
        """Initialize the concierge with database access."""
        self.db = Database()
        self.resource_dal = ResourceDAL(self.db)
        self.booking_dal = BookingDAL(self.db)
        self.review_dal = ReviewDAL(self.db)
        self.admin_dal = AdminDAL(self.db)

    def get_context_summary(self):
        """
        Get a summary of current system state for context.

        Returns:
            dict: System context including resource counts, categories, etc.
        """
        stats = self.admin_dal.get_system_stats()
        categories = self.resource_dal.get_categories()
        top_resources = self.resource_dal.get_top_rated_resources(limit=5)

        return {
            'total_resources': sum(stats.get('resources_by_status', {}).values()),
            'published_resources': stats.get('resources_by_status', {}).get('published', 0),
            'categories': categories,
            'total_users': sum(stats.get('users_by_role', {}).values()),
            'top_resources': [
                {
                    'title': r['title'],
                    'category': r['category'],
                    'location': r['location'],
                    'avg_rating': round(r['avg_rating'], 1) if r['avg_rating'] else 0
                }
                for r in top_resources
            ]
        }

    def answer_query(self, query_type, **params):
        """
        Answer a structured query based on query type.

        Args:
            query_type: Type of query (e.g., 'search', 'recommendations', 'stats')
            **params: Additional parameters for the query

        Returns:
            dict: Response with data and explanation
        """
        if query_type == 'search_resources':
            return self._search_resources(**params)
        elif query_type == 'resource_recommendations':
            return self._get_recommendations(**params)
        elif query_type == 'availability_check':
            return self._check_availability(**params)
        elif query_type == 'system_stats':
            return self._get_system_stats()
        elif query_type == 'popular_resources':
            return self._get_popular_resources(**params)
        elif query_type == 'category_info':
            return self._get_category_info(**params)
        else:
            return {
                'success': False,
                'message': 'Unknown query type. Available types: search_resources, resource_recommendations, availability_check, system_stats, popular_resources, category_info'
            }

    def _search_resources(self, keyword=None, category=None, location=None):
        """Search for resources based on criteria."""
        resources = self.resource_dal.search_resources(
            keyword=keyword,
            category=category,
            location=location
        )

        results = []
        for resource in resources:
            rating_info = self.review_dal.get_average_rating(resource['resource_id'])
            results.append({
                'resource_id': resource['resource_id'],
                'title': resource['title'],
                'description': resource['description'],
                'category': resource['category'],
                'location': resource['location'],
                'capacity': resource['capacity'],
                'avg_rating': rating_info['avg_rating'],
                'review_count': rating_info['review_count']
            })

        return {
            'success': True,
            'count': len(results),
            'results': results,
            'message': f"Found {len(results)} resources matching your criteria."
        }

    def _get_recommendations(self, category=None, min_rating=4.0):
        """Get resource recommendations based on ratings."""
        top_resources = self.resource_dal.get_top_rated_resources(limit=10)

        filtered = []
        for resource in top_resources:
            if category and resource['category'] != category:
                continue
            if resource['avg_rating'] >= min_rating:
                filtered.append({
                    'resource_id': resource['resource_id'],
                    'title': resource['title'],
                    'category': resource['category'],
                    'location': resource['location'],
                    'avg_rating': round(resource['avg_rating'], 1),
                    'review_count': resource['review_count']
                })

        return {
            'success': True,
            'count': len(filtered),
            'recommendations': filtered,
            'message': f"Here are {len(filtered)} highly-rated resources"
                      f"{' in ' + category if category else ''}."
        }

    def _check_availability(self, resource_id, start_datetime=None, end_datetime=None):
        """Check if a resource is available for booking."""
        resource = self.resource_dal.get_resource_by_id(resource_id)

        if not resource:
            return {
                'success': False,
                'message': f"Resource {resource_id} not found."
            }

        if resource['status'] != 'published':
            return {
                'success': False,
                'available': False,
                'resource': resource['title'],
                'message': f"Resource '{resource['title']}' is not currently available for booking."
            }

        if start_datetime and end_datetime:
            has_conflict = self.booking_dal.check_booking_conflict(
                resource_id, start_datetime, end_datetime
            )

            return {
                'success': True,
                'available': not has_conflict,
                'resource': resource['title'],
                'message': f"Resource '{resource['title']}' is "
                          f"{'NOT available' if has_conflict else 'available'} "
                          f"for the requested time."
            }
        else:
            # Just check general availability
            return {
                'success': True,
                'available': True,
                'resource': resource['title'],
                'message': f"Resource '{resource['title']}' is published and accepting bookings."
            }

    def _get_system_stats(self):
        """Get system-wide statistics."""
        stats = self.admin_dal.get_system_stats()
        context = self.get_context_summary()

        return {
            'success': True,
            'stats': {
                'total_users': context['total_users'],
                'total_resources': context['total_resources'],
                'published_resources': context['published_resources'],
                'categories': context['categories'],
                'bookings_by_status': stats.get('bookings_by_status', {}),
                'most_booked_resources': stats.get('most_booked_resources', [])
            },
            'message': "System statistics retrieved successfully."
        }

    def _get_popular_resources(self, limit=5):
        """Get most popular resources by booking count."""
        stats = self.admin_dal.get_system_stats()
        most_booked = stats.get('most_booked_resources', [])[:limit]

        return {
            'success': True,
            'count': len(most_booked),
            'popular_resources': most_booked,
            'message': f"Top {len(most_booked)} most booked resources."
        }

    def _get_category_info(self, category=None):
        """Get information about resource categories."""
        if category:
            resources = self.resource_dal.search_resources(category=category)
            return {
                'success': True,
                'category': category,
                'count': len(resources),
                'message': f"Found {len(resources)} resources in category '{category}'."
            }
        else:
            categories = self.resource_dal.get_categories()
            usage = self.admin_dal.get_usage_by_category()

            category_info = []
            for cat in categories:
                usage_data = next((u for u in usage if u['category'] == cat), None)
                category_info.append({
                    'category': cat,
                    'booking_count': usage_data['booking_count'] if usage_data else 0
                })

            return {
                'success': True,
                'categories': category_info,
                'message': f"Found {len(categories)} resource categories."
            }

    def generate_natural_language_response(self, query_text):
        """
        Generate a natural language response to a user query.

        This is a simplified version that maps common questions to query types.
        In a production system, this would use an LLM to parse intent.

        Args:
            query_text: Natural language query from user

        Returns:
            str: Natural language response
        """
        query_lower = query_text.lower()

        # Simple keyword-based routing
        if 'top rated' in query_lower or 'best' in query_lower or 'recommend' in query_lower:
            result = self.answer_query('resource_recommendations')
            if result['success'] and result['recommendations']:
                response = f"Here are the top-rated resources:\n\n"
                for r in result['recommendations'][:5]:
                    response += f"- {r['title']} ({r['category']}) - Rating: {r['avg_rating']}/5 at {r['location']}\n"
                return response
            return "I couldn't find any highly-rated resources at the moment."

        elif 'popular' in query_lower or 'most booked' in query_lower:
            result = self.answer_query('popular_resources')
            if result['success'] and result['popular_resources']:
                response = f"Most popular resources by bookings:\n\n"
                for r in result['popular_resources']:
                    response += f"- {r['title']}: {r['booking_count']} bookings\n"
                return response
            return "No booking data available yet."

        elif 'category' in query_lower or 'categories' in query_lower or 'types' in query_lower:
            result = self.answer_query('category_info')
            if result['success']:
                response = f"Available resource categories:\n\n"
                for c in result['categories']:
                    response += f"- {c['category']}: {c['booking_count']} bookings\n"
                return response
            return "No categories found."

        elif 'stats' in query_lower or 'statistics' in query_lower or 'overview' in query_lower:
            result = self.answer_query('system_stats')
            if result['success']:
                stats = result['stats']
                response = f"Campus Resource Hub Statistics:\n\n"
                response += f"- Total Users: {stats['total_users']}\n"
                response += f"- Published Resources: {stats['published_resources']}\n"
                response += f"- Categories: {', '.join(stats['categories'])}\n"
                return response
            return "Statistics unavailable."

        else:
            # Default help message
            return """I'm the Campus Resource Hub AI Concierge! I can help you with:

- Finding top-rated resources ("Show me the best resources")
- Viewing popular resources ("What are the most booked resources?")
- Exploring categories ("What categories are available?")
- System statistics ("Show me system stats")

What would you like to know?"""


# Initialize global concierge instance
concierge = ResourceConcierge()
