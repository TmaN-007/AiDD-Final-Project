"""Admin controller - admin dashboard and management functions."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.data_access.database import Database
from src.data_access.admin_dal import AdminDAL
from src.data_access.user_dal import UserDAL
from src.data_access.resource_dal import ResourceDAL
from src.data_access.booking_dal import BookingDAL
from src.data_access.review_dal import ReviewDAL
from src.controllers.auth_controller import login_required, role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

db = Database()
admin_dal = AdminDAL(db)
user_dal = UserDAL(db)
resource_dal = ResourceDAL(db)
booking_dal = BookingDAL(db)
review_dal = ReviewDAL(db)


@admin_bp.route('/')
@role_required('admin', 'staff')
def dashboard():
    """Admin dashboard with system statistics."""
    stats = admin_dal.get_system_stats()
    pending_bookings = booking_dal.get_pending_bookings()
    recent_logs = admin_dal.get_admin_logs(limit=20)

    return render_template('admin/dashboard.html',
                         stats=stats,
                         pending_bookings=pending_bookings,
                         recent_logs=recent_logs)


@admin_bp.route('/users')
@role_required('admin')
def manage_users():
    """User management page."""
    users = user_dal.get_all_users()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@role_required('admin')
def delete_user(user_id):
    """Delete a user."""
    if user_id == session['user_id']:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.manage_users'))

    user = user_dal.get_user_by_id(user_id)
    if user:
        success = user_dal.delete_user(user_id)
        if success:
            admin_dal.log_action(session['user_id'], f'Deleted user: {user["email"]}', 'users')
            flash('User deleted successfully.', 'success')
        else:
            flash('Failed to delete user.', 'danger')

    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/resources')
@role_required('admin', 'staff')
def manage_resources():
    """Resource management page."""
    resources = resource_dal.get_all_resources()
    return render_template('admin/resources.html', resources=resources)


@admin_bp.route('/bookings')
@role_required('admin', 'staff')
def manage_bookings():
    """Booking management page."""
    pending_bookings = booking_dal.get_pending_bookings()
    return render_template('admin/bookings.html', bookings=pending_bookings)


@admin_bp.route('/reviews')
@role_required('admin')
def manage_reviews():
    """Review moderation page."""
    reviews = review_dal.get_all_reviews(limit=50)
    return render_template('admin/reviews.html', reviews=reviews)


@admin_bp.route('/analytics')
@role_required('admin', 'staff')
def analytics():
    """Analytics and reports."""
    stats = admin_dal.get_system_stats()
    usage_by_category = admin_dal.get_usage_by_category()
    usage_by_department = admin_dal.get_usage_by_department()

    return render_template('admin/analytics.html',
                         stats=stats,
                         usage_by_category=usage_by_category,
                         usage_by_department=usage_by_department)
