"""
Unit tests for User Data Access Layer.
Tests CRUD operations independently from Flask routes.
"""

import pytest
import os
import sys
from src.data_access.database import Database
from src.data_access.user_dal import UserDAL
from src.utils.auth import hash_password


@pytest.fixture
def test_db():
    """Create a test database."""
    db = Database('test_users.db')
    yield db
    # Cleanup
    if os.path.exists('test_users.db'):
        os.remove('test_users.db')


@pytest.fixture
def user_dal(test_db):
    """Create UserDAL instance with test database."""
    return UserDAL(test_db)


def test_create_user(user_dal):
    """Test creating a new user."""
    password_hash = hash_password('TestPass123')
    user_id = user_dal.create_user(
        name='Test User',
        email='test@example.com',
        password_hash=password_hash,
        role='student',
        department='Computer Science'
    )

    assert user_id is not None
    assert isinstance(user_id, int)


def test_get_user_by_id(user_dal):
    """Test retrieving user by ID."""
    password_hash = hash_password('TestPass123')
    user_id = user_dal.create_user(
        name='Test User',
        email='test@example.com',
        password_hash=password_hash,
        role='student'
    )

    user = user_dal.get_user_by_id(user_id)

    assert user is not None
    assert user['name'] == 'Test User'
    assert user['email'] == 'test@example.com'
    assert user['role'] == 'student'


def test_get_user_by_email(user_dal):
    """Test retrieving user by email."""
    password_hash = hash_password('TestPass123')
    user_dal.create_user(
        name='Test User',
        email='test@example.com',
        password_hash=password_hash,
        role='student'
    )

    user = user_dal.get_user_by_email('test@example.com')

    assert user is not None
    assert user['name'] == 'Test User'
    assert user['email'] == 'test@example.com'


def test_user_exists(user_dal):
    """Test checking if user exists."""
    password_hash = hash_password('TestPass123')
    user_dal.create_user(
        name='Test User',
        email='test@example.com',
        password_hash=password_hash,
        role='student'
    )

    assert user_dal.user_exists('test@example.com') is True
    assert user_dal.user_exists('nonexistent@example.com') is False


def test_update_user(user_dal):
    """Test updating user information."""
    password_hash = hash_password('TestPass123')
    user_id = user_dal.create_user(
        name='Test User',
        email='test@example.com',
        password_hash=password_hash,
        role='student'
    )

    success = user_dal.update_user(
        user_id,
        name='Updated Name',
        department='Engineering'
    )

    assert success is True

    user = user_dal.get_user_by_id(user_id)
    assert user['name'] == 'Updated Name'
    assert user['department'] == 'Engineering'


def test_delete_user(user_dal):
    """Test deleting a user."""
    password_hash = hash_password('TestPass123')
    user_id = user_dal.create_user(
        name='Test User',
        email='test@example.com',
        password_hash=password_hash,
        role='student'
    )

    success = user_dal.delete_user(user_id)
    assert success is True

    user = user_dal.get_user_by_id(user_id)
    assert user is None


def test_duplicate_email(user_dal):
    """Test that duplicate emails are not allowed."""
    password_hash = hash_password('TestPass123')

    user_dal.create_user(
        name='First User',
        email='test@example.com',
        password_hash=password_hash,
        role='student'
    )

    # Try to create another user with same email
    user_id = user_dal.create_user(
        name='Second User',
        email='test@example.com',
        password_hash=password_hash,
        role='student'
    )

    assert user_id is None  # Should fail due to unique constraint
