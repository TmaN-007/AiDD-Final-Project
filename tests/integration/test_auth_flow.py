"""
Integration test for authentication flow.
Tests register → login → access protected route workflow.
"""

import pytest
import os
from app import create_app
from src.data_access.database import Database


@pytest.fixture
def app():
    """Create and configure test app."""
    os.environ['DATABASE_PATH'] = 'test_auth.db'
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    yield app

    # Cleanup
    if os.path.exists('test_auth.db'):
        os.remove('test_auth.db')


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def test_register_login_protected_route(client):
    """Test complete authentication flow."""
    # Step 1: Register a new user
    response = client.post('/auth/register', data={
        'name': 'Test User',
        'email': 'testuser@example.com',
        'password': 'TestPass123',
        'confirm_password': 'TestPass123',
        'role': 'student',
        'department': 'Computer Science'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Registration successful' in response.data or b'Login' in response.data

    # Step 2: Login with registered credentials
    response = client.post('/auth/login', data={
        'email': 'testuser@example.com',
        'password': 'TestPass123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Welcome back' in response.data or b'Dashboard' in response.data

    # Step 3: Access protected route (dashboard)
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Dashboard' in response.data or b'My Resources' in response.data


def test_login_with_invalid_credentials(client):
    """Test login fails with wrong credentials."""
    response = client.post('/auth/login', data={
        'email': 'wrong@example.com',
        'password': 'WrongPass123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid email or password' in response.data


def test_protected_route_without_login(client):
    """Test accessing protected route without login redirects."""
    response = client.get('/dashboard', follow_redirects=False)
    assert response.status_code == 302  # Redirect
    assert '/auth/login' in response.location


def test_logout(client):
    """Test logout functionality."""
    # First login
    client.post('/auth/register', data={
        'name': 'Test User',
        'email': 'testuser@example.com',
        'password': 'TestPass123',
        'confirm_password': 'TestPass123',
        'role': 'student'
    })

    client.post('/auth/login', data={
        'email': 'testuser@example.com',
        'password': 'TestPass123'
    })

    # Then logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'logged out' in response.data

    # Try accessing protected route after logout
    response = client.get('/dashboard', follow_redirects=False)
    assert response.status_code == 302  # Should redirect to login
