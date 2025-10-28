"""
Input validation utilities for server-side validation.
Ensures data integrity and prevents malicious input.
"""

import re
from datetime import datetime


def validate_email(email):
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"

    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"

    if len(email) > 255:
        return False, "Email is too long"

    return True, None


def validate_name(name):
    """
    Validate user name.

    Args:
        name: Name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "Name is required"

    if len(name) < 2:
        return False, "Name must be at least 2 characters"

    if len(name) > 100:
        return False, "Name is too long"

    return True, None


def validate_role(role):
    """
    Validate user role.

    Args:
        role: Role to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_roles = ['student', 'staff', 'admin']
    if role not in valid_roles:
        return False, f"Role must be one of: {', '.join(valid_roles)}"

    return True, None


def validate_resource_title(title):
    """
    Validate resource title.

    Args:
        title: Title to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "Title is required"

    if len(title) < 3:
        return False, "Title must be at least 3 characters"

    if len(title) > 200:
        return False, "Title is too long"

    return True, None


def validate_rating(rating):
    """
    Validate review rating.

    Args:
        rating: Rating to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        rating_int = int(rating)
        if rating_int < 1 or rating_int > 5:
            return False, "Rating must be between 1 and 5"
        return True, None
    except (ValueError, TypeError):
        return False, "Rating must be a valid number"


def validate_datetime(datetime_str):
    """
    Validate and parse datetime string.

    Args:
        datetime_str: Datetime string in ISO format

    Returns:
        Tuple of (is_valid, datetime_object or error_message)
    """
    if not datetime_str:
        return False, "Datetime is required"

    try:
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return True, dt
    except (ValueError, AttributeError):
        return False, "Invalid datetime format"


def validate_booking_times(start_datetime, end_datetime):
    """
    Validate booking start and end times.

    Args:
        start_datetime: Start datetime
        end_datetime: End datetime

    Returns:
        Tuple of (is_valid, error_message)
    """
    if start_datetime >= end_datetime:
        return False, "End time must be after start time"

    if start_datetime < datetime.now():
        return False, "Cannot book in the past"

    # Check if booking is reasonable (not more than 1 year in advance)
    max_advance_days = 365
    if (end_datetime - datetime.now()).days > max_advance_days:
        return False, f"Cannot book more than {max_advance_days} days in advance"

    # Check if duration is reasonable (not more than 7 days)
    max_duration_hours = 168  # 7 days
    duration_hours = (end_datetime - start_datetime).total_seconds() / 3600
    if duration_hours > max_duration_hours:
        return False, f"Booking duration cannot exceed {max_duration_hours // 24} days"

    return True, None


def sanitize_string(text, max_length=None):
    """
    Sanitize string input by removing potentially dangerous characters.

    Args:
        text: Text to sanitize
        max_length: Optional maximum length

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Strip whitespace
    text = text.strip()

    # Truncate if necessary
    if max_length and len(text) > max_length:
        text = text[:max_length]

    return text


def validate_file_upload(filename):
    """
    Validate uploaded file.

    Args:
        filename: Name of uploaded file

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not filename:
        return False, "No file selected"

    # Check for path traversal attempts
    if '..' in filename or '/' in filename or '\\' in filename:
        return False, "Invalid filename"

    # Check file extension
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' not in filename:
        return False, "File must have an extension"

    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        return False, f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"

    return True, None
