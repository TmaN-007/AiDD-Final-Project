"""
Authentication controller.
Handles user registration, login, and logout.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.data_access.database import Database
from src.data_access.user_dal import UserDAL
from src.utils.auth import hash_password, verify_password, validate_password_strength
from src.utils.validators import validate_email, validate_name, validate_role
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Initialize database and DAL
db = Database()
user_dal = UserDAL(db)


def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """Decorator to require specific roles for routes."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))

            user = user_dal.get_user_by_id(session['user_id'])
            if not user or user['role'] not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('main.index'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'student')
        department = request.form.get('department', '').strip()

        # Server-side validation
        is_valid, error = validate_name(name)
        if not is_valid:
            flash(error, 'danger')
            return render_template('auth/register.html')

        is_valid, error = validate_email(email)
        if not is_valid:
            flash(error, 'danger')
            return render_template('auth/register.html')

        is_valid, error = validate_role(role)
        if not is_valid:
            flash(error, 'danger')
            return render_template('auth/register.html')

        is_valid, error = validate_password_strength(password)
        if not is_valid:
            flash(error, 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        # Check if user exists
        if user_dal.user_exists(email):
            flash('Email already registered.', 'danger')
            return render_template('auth/register.html')

        # Create user
        password_hash = hash_password(password)
        user_id = user_dal.create_user(name, email, password_hash, role, department)

        if user_id:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Please try again.', 'danger')

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Server-side validation
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return render_template('auth/login.html')

        # Get user
        user = user_dal.get_user_by_email(email)

        if user and verify_password(password, user['password_hash']):
            # Set session
            session['user_id'] = user['user_id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']

            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    """User logout."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    user = user_dal.get_user_by_id(session['user_id'])
    return render_template('auth/profile.html', user=user)


@auth_bp.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    """Edit user profile."""
    name = request.form.get('name', '').strip()
    department = request.form.get('department', '').strip()

    # Validate
    is_valid, error = validate_name(name)
    if not is_valid:
        flash(error, 'danger')
        return redirect(url_for('auth.profile'))

    # Update user
    success = user_dal.update_user(session['user_id'], name=name, department=department)

    if success:
        session['user_name'] = name
        flash('Profile updated successfully.', 'success')
    else:
        flash('Failed to update profile.', 'danger')

    return redirect(url_for('auth.profile'))
