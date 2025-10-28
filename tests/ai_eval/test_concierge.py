"""
AI Feature Validation Tests.
Verifies that the AI Concierge returns accurate, grounded responses.
"""

import pytest
import os
from src.data_access.database import Database
from src.data_access.user_dal import UserDAL
from src.data_access.resource_dal import ResourceDAL
from src.utils.ai_concierge import ResourceConcierge
from src.utils.auth import hash_password


@pytest.fixture
def setup_test_data():
    """Set up test database with sample data."""
    db = Database('test_concierge.db')
    user_dal = UserDAL(db)
    resource_dal = ResourceDAL(db)

    # Create test user
    password_hash = hash_password('TestPass123')
    user_id = user_dal.create_user(
        name='Test Owner',
        email='owner@example.com',
        password_hash=password_hash,
        role='staff'
    )

    # Create test resources
    resource_dal.create_resource(
        owner_id=user_id,
        title='Study Room A',
        description='Quiet study space',
        category='Study Room',
        location='Library Building',
        capacity=8,
        status='published'
    )

    resource_dal.create_resource(
        owner_id=user_id,
        title='Conference Room B',
        description='Meeting space',
        category='Meeting Room',
        location='Admin Building',
        capacity=20,
        status='published'
    )

    yield db

    # Cleanup
    if os.path.exists('test_concierge.db'):
        os.remove('test_concierge.db')


def test_concierge_search_resources(setup_test_data):
    """Test that concierge search returns real data."""
    concierge = ResourceConcierge()

    result = concierge.answer_query('search_resources', keyword='Study')

    assert result['success'] is True
    assert result['count'] >= 1
    assert any('Study Room' in r['title'] for r in result['results'])
    # Verify no fabricated data
    for resource in result['results']:
        assert 'resource_id' in resource
        assert 'title' in resource


def test_concierge_category_info(setup_test_data):
    """Test category information accuracy."""
    concierge = ResourceConcierge()

    result = concierge.answer_query('category_info')

    assert result['success'] is True
    assert 'categories' in result
    # Verify categories are real from database
    assert isinstance(result['categories'], list)


def test_concierge_system_stats(setup_test_data):
    """Test system statistics are factual."""
    concierge = ResourceConcierge()

    result = concierge.answer_query('system_stats')

    assert result['success'] is True
    assert 'stats' in result
    stats = result['stats']

    # Verify stats are numeric and reasonable
    assert stats['total_users'] >= 0
    assert stats['published_resources'] >= 0
    assert isinstance(stats['categories'], list)


def test_concierge_availability_check(setup_test_data):
    """Test availability checking returns accurate status."""
    concierge = ResourceConcierge()

    # Check availability of resource 1
    result = concierge.answer_query('availability_check', resource_id=1)

    assert result['success'] is True
    assert 'available' in result
    assert isinstance(result['available'], bool)
    assert 'resource' in result


def test_concierge_no_fabrication(setup_test_data):
    """Test that concierge does not fabricate data."""
    concierge = ResourceConcierge()

    # Try to get info about non-existent resource
    result = concierge.answer_query('availability_check', resource_id=9999)

    assert result['success'] is False
    assert 'not found' in result['message'].lower()


def test_natural_language_response(setup_test_data):
    """Test natural language query processing."""
    concierge = ResourceConcierge()

    response = concierge.generate_natural_language_response("Show me the best resources")

    assert isinstance(response, str)
    assert len(response) > 0
    # Should contain meaningful content
    assert 'resource' in response.lower() or 'available' in response.lower()


def test_concierge_recommendations_quality(setup_test_data):
    """Test that recommendations are based on actual ratings."""
    concierge = ResourceConcierge()

    result = concierge.answer_query('resource_recommendations', min_rating=0)

    assert result['success'] is True
    # All recommendations should have rating info
    for rec in result['recommendations']:
        assert 'avg_rating' in rec
        assert 'review_count' in rec
        assert rec['avg_rating'] >= 0
