"""
Booking controller.
Handles booking creation, approval, and management.

# AI Contribution: Conflict detection logic enhanced by Claude Code.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.data_access.database import Database
from src.data_access.booking_dal import BookingDAL
from src.data_access.resource_dal import ResourceDAL
from src.controllers.auth_controller import login_required
from src.utils.validators import validate_datetime, validate_booking_times, sanitize_string
from datetime import datetime

booking_bp = Blueprint('booking', __name__, url_prefix='/bookings')

# Initialize database and DAL
db = Database()
booking_dal = BookingDAL(db)
resource_dal = ResourceDAL(db)


@booking_bp.route('/create/<int:resource_id>', methods=['GET', 'POST'])
@login_required
def create_booking(resource_id):
    """Create a booking for a resource."""
    resource = resource_dal.get_resource_by_id(resource_id)

    if not resource:
        flash('Resource not found.', 'danger')
        return redirect(url_for('resource.list_resources'))

    if resource['status'] != 'published':
        flash('This resource is not available for booking.', 'danger')
        return redirect(url_for('resource.view_resource', resource_id=resource_id))

    if request.method == 'POST':
        start_datetime_str = request.form.get('start_datetime', '')
        end_datetime_str = request.form.get('end_datetime', '')
        notes = request.form.get('notes', '').strip()

        # Validate datetimes
        is_valid, start_dt = validate_datetime(start_datetime_str)
        if not is_valid:
            flash(f'Invalid start time: {start_dt}', 'danger')
            return render_template('bookings/create.html', resource=resource)

        is_valid, end_dt = validate_datetime(end_datetime_str)
        if not is_valid:
            flash(f'Invalid end time: {end_dt}', 'danger')
            return render_template('bookings/create.html', resource=resource)

        # Validate booking times
        is_valid, error = validate_booking_times(start_dt, end_dt)
        if not is_valid:
            flash(error, 'danger')
            return render_template('bookings/create.html', resource=resource)

        # Check for conflicts
        has_conflict = booking_dal.check_booking_conflict(
            resource_id, start_dt.isoformat(), end_dt.isoformat()
        )

        if has_conflict:
            flash('This time slot conflicts with an existing booking.', 'danger')
            return render_template('bookings/create.html', resource=resource)

        # Sanitize notes
        notes = sanitize_string(notes, 500)

        # Create booking
        booking_id = booking_dal.create_booking(
            resource_id=resource_id,
            requester_id=session['user_id'],
            start_datetime=start_dt.isoformat(),
            end_datetime=end_dt.isoformat(),
            notes=notes
        )

        if booking_id:
            flash('Booking request created successfully! Awaiting approval.', 'success')
            return redirect(url_for('booking.view_booking', booking_id=booking_id))
        else:
            flash('Failed to create booking.', 'danger')

    return render_template('bookings/create.html', resource=resource)


@booking_bp.route('/<int:booking_id>')
@login_required
def view_booking(booking_id):
    """View booking details."""
    booking = booking_dal.get_booking_with_details(booking_id)

    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    # Check permission
    user_id = session['user_id']
    user_role = session.get('user_role')
    is_requester = booking['requester_id'] == user_id
    is_owner = booking['owner_name']  # Will check in template with owner_id

    # Get resource to check ownership
    resource = resource_dal.get_resource_by_id(booking['resource_id'])
    is_owner = resource['owner_id'] == user_id if resource else False

    if not (is_requester or is_owner or user_role in ['staff', 'admin']):
        flash('You do not have permission to view this booking.', 'danger')
        return redirect(url_for('main.dashboard'))

    return render_template('booking/view.html', booking=booking, is_owner=is_owner)


@booking_bp.route('/<int:booking_id>/approve', methods=['POST'])
@login_required
def approve_booking(booking_id):
    """Approve a booking (for resource owner, staff, or admin)."""
    booking = booking_dal.get_booking_by_id(booking_id)

    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    # Check permission
    resource = resource_dal.get_resource_by_id(booking['resource_id'])
    user_role = session.get('user_role')

    if not resource:
        flash('Resource not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    is_owner = resource['owner_id'] == session['user_id']
    can_approve = is_owner or user_role in ['staff', 'admin']

    if not can_approve:
        flash('You do not have permission to approve this booking.', 'danger')
        return redirect(url_for('booking.view_booking', booking_id=booking_id))

    if booking['status'] != 'pending':
        flash('This booking cannot be approved.', 'danger')
        return redirect(url_for('booking.view_booking', booking_id=booking_id))

    # Approve booking
    success = booking_dal.update_booking_status(booking_id, 'approved')

    if success:
        flash('Booking approved successfully!', 'success')
    else:
        flash('Failed to approve booking.', 'danger')

    return redirect(url_for('booking.view_booking', booking_id=booking_id))


@booking_bp.route('/<int:booking_id>/reject', methods=['POST'])
@login_required
def reject_booking(booking_id):
    """Reject a booking."""
    booking = booking_dal.get_booking_by_id(booking_id)

    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    # Check permission
    resource = resource_dal.get_resource_by_id(booking['resource_id'])
    user_role = session.get('user_role')

    if not resource:
        flash('Resource not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    is_owner = resource['owner_id'] == session['user_id']
    can_reject = is_owner or user_role in ['staff', 'admin']

    if not can_reject:
        flash('You do not have permission to reject this booking.', 'danger')
        return redirect(url_for('booking.view_booking', booking_id=booking_id))

    if booking['status'] != 'pending':
        flash('This booking cannot be rejected.', 'danger')
        return redirect(url_for('booking.view_booking', booking_id=booking_id))

    success = booking_dal.update_booking_status(booking_id, 'rejected')

    if success:
        flash('Booking rejected.', 'info')
    else:
        flash('Failed to reject booking.', 'danger')

    return redirect(url_for('booking.view_booking', booking_id=booking_id))


@booking_bp.route('/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    """Cancel a booking (by requester)."""
    booking = booking_dal.get_booking_by_id(booking_id)

    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    # Check permission - must be requester
    if booking['requester_id'] != session['user_id']:
        flash('You do not have permission to cancel this booking.', 'danger')
        return redirect(url_for('booking.view_booking', booking_id=booking_id))

    if booking['status'] not in ['pending', 'approved']:
        flash('This booking cannot be cancelled.', 'danger')
        return redirect(url_for('booking.view_booking', booking_id=booking_id))

    success = booking_dal.update_booking_status(booking_id, 'cancelled')

    if success:
        flash('Booking cancelled successfully.', 'info')
    else:
        flash('Failed to cancel booking.', 'danger')

    return redirect(url_for('main.dashboard'))
