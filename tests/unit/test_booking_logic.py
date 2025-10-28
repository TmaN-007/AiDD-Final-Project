"""
Unit tests for booking conflict detection logic.
Tests the critical booking conflict detection feature.
"""

import pytest
import os
from datetime import datetime, timedelta
from src.data_access.database import Database
from src.data_access.resource_dal import ResourceDAL
from src.data_access.booking_dal import BookingDAL
from src.data_access.user_dal import UserDAL
from src.utils.auth import hash_password


@pytest.fixture
def test_db():
    """Create a test database."""
    db = Database('test_bookings.db')
    yield db
    if os.path.exists('test_bookings.db'):
        os.remove('test_bookings.db')


@pytest.fixture
def setup_data(test_db):
    """Set up test data."""
    user_dal = UserDAL(test_db)
    resource_dal = ResourceDAL(test_db)
    booking_dal = BookingDAL(test_db)

    # Create test user
    password_hash = hash_password('TestPass123')
    user_id = user_dal.create_user(
        name='Test User',
        email='test@example.com',
        password_hash=password_hash,
        role='student'
    )

    # Create test resource
    resource_id = resource_dal.create_resource(
        owner_id=user_id,
        title='Test Room',
        description='A test room',
        category='Study Room',
        location='Building A',
        capacity=10,
        status='published'
    )

    return {
        'user_id': user_id,
        'resource_id': resource_id,
        'user_dal': user_dal,
        'resource_dal': resource_dal,
        'booking_dal': booking_dal
    }


def test_create_booking(setup_data):
    """Test creating a booking."""
    booking_dal = setup_data['booking_dal']
    resource_id = setup_data['resource_id']
    user_id = setup_data['user_id']

    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)

    booking_id = booking_dal.create_booking(
        resource_id=resource_id,
        requester_id=user_id,
        start_datetime=start_time.isoformat(),
        end_datetime=end_time.isoformat(),
        notes='Test booking'
    )

    assert booking_id is not None


def test_conflict_detection_overlap(setup_data):
    """Test conflict detection for overlapping bookings."""
    booking_dal = setup_data['booking_dal']
    resource_id = setup_data['resource_id']
    user_id = setup_data['user_id']

    # Create first booking: 2pm - 4pm tomorrow
    base_time = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0) + timedelta(days=1)
    start1 = base_time
    end1 = start1 + timedelta(hours=2)

    booking_dal.create_booking(
        resource_id=resource_id,
        requester_id=user_id,
        start_datetime=start1.isoformat(),
        end_datetime=end1.isoformat()
    )

    # Update to approved status
    booking_dal.update_booking_status(1, 'approved')

    # Test overlapping booking: 3pm - 5pm (overlaps with 2pm-4pm)
    start2 = base_time + timedelta(hours=1)
    end2 = start2 + timedelta(hours=2)

    has_conflict = booking_dal.check_booking_conflict(
        resource_id,
        start2.isoformat(),
        end2.isoformat()
    )

    assert has_conflict is True


def test_no_conflict_sequential(setup_data):
    """Test no conflict for sequential bookings."""
    booking_dal = setup_data['booking_dal']
    resource_id = setup_data['resource_id']
    user_id = setup_data['user_id']

    # Create first booking: 2pm - 4pm tomorrow
    base_time = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0) + timedelta(days=1)
    start1 = base_time
    end1 = start1 + timedelta(hours=2)

    booking_dal.create_booking(
        resource_id=resource_id,
        requester_id=user_id,
        start_datetime=start1.isoformat(),
        end_datetime=end1.isoformat()
    )

    booking_dal.update_booking_status(1, 'approved')

    # Test sequential booking: 4pm - 6pm (no overlap)
    start2 = end1
    end2 = start2 + timedelta(hours=2)

    has_conflict = booking_dal.check_booking_conflict(
        resource_id,
        start2.isoformat(),
        end2.isoformat()
    )

    assert has_conflict is False


def test_booking_status_transitions(setup_data):
    """Test booking status transitions."""
    booking_dal = setup_data['booking_dal']
    resource_id = setup_data['resource_id']
    user_id = setup_data['user_id']

    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)

    booking_id = booking_dal.create_booking(
        resource_id=resource_id,
        requester_id=user_id,
        start_datetime=start_time.isoformat(),
        end_datetime=end_time.isoformat()
    )

    # Check initial status
    booking = booking_dal.get_booking_by_id(booking_id)
    assert booking['status'] == 'pending'

    # Approve booking
    success = booking_dal.update_booking_status(booking_id, 'approved')
    assert success is True

    booking = booking_dal.get_booking_by_id(booking_id)
    assert booking['status'] == 'approved'

    # Cancel booking
    success = booking_dal.update_booking_status(booking_id, 'cancelled')
    assert success is True

    booking = booking_dal.get_booking_by_id(booking_id)
    assert booking['status'] == 'cancelled'
