"""Review controller - handles review creation and management."""

from flask import Blueprint, request, redirect, url_for, flash, session
from src.data_access.database import Database
from src.data_access.review_dal import ReviewDAL
from src.data_access.resource_dal import ResourceDAL
from src.controllers.auth_controller import login_required
from src.utils.validators import validate_rating, sanitize_string

review_bp = Blueprint('review', __name__, url_prefix='/reviews')

db = Database()
review_dal = ReviewDAL(db)
resource_dal = ResourceDAL(db)


@review_bp.route('/create/<int:resource_id>', methods=['POST'])
@login_required
def create_review(resource_id):
    """Create a review for a resource."""
    rating = request.form.get('rating')
    comment = request.form.get('comment', '').strip()

    # Validate
    is_valid, error = validate_rating(rating)
    if not is_valid:
        flash(error, 'danger')
        return redirect(url_for('resource.view_resource', resource_id=resource_id))

    # Check if user has already reviewed
    if review_dal.user_has_reviewed(resource_id, session['user_id']):
        flash('You have already reviewed this resource.', 'warning')
        return redirect(url_for('resource.view_resource', resource_id=resource_id))

    comment = sanitize_string(comment, 1000)

    review_id = review_dal.create_review(resource_id, session['user_id'], int(rating), comment)

    if review_id:
        flash('Review submitted successfully!', 'success')
    else:
        flash('Failed to submit review.', 'danger')

    return redirect(url_for('resource.view_resource', resource_id=resource_id))


@review_bp.route('/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    """Delete a review."""
    review = review_dal.get_review_by_id(review_id)

    if not review:
        flash('Review not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    # Check permission
    if review['reviewer_id'] != session['user_id'] and session.get('user_role') != 'admin':
        flash('You do not have permission to delete this review.', 'danger')
        return redirect(url_for('main.dashboard'))

    success = review_dal.delete_review(review_id)

    if success:
        flash('Review deleted successfully.', 'info')
    else:
        flash('Failed to delete review.', 'danger')

    return redirect(url_for('resource.view_resource', resource_id=review['resource_id']))
