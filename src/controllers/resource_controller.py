"""
Resource controller.
Handles resource CRUD operations and search functionality.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.data_access.database import Database
from src.data_access.resource_dal import ResourceDAL
from src.data_access.review_dal import ReviewDAL
from src.controllers.auth_controller import login_required
from src.utils.validators import validate_resource_title, sanitize_string
import json

resource_bp = Blueprint('resource', __name__, url_prefix='/resources')

# Initialize database and DAL
db = Database()
resource_dal = ResourceDAL(db)
review_dal = ReviewDAL(db)


@resource_bp.route('/')
def list_resources():
    """List and search resources."""
    keyword = request.args.get('keyword', '').strip()
    category = request.args.get('category', '').strip()
    location = request.args.get('location', '').strip()

    # Search resources
    resources = resource_dal.search_resources(
        keyword=keyword if keyword else None,
        category=category if category else None,
        location=location if location else None
    )

    # Get categories for filter dropdown
    categories = resource_dal.get_categories()

    # Add rating info to each resource
    resources_with_ratings = []
    for resource in resources:
        resource_dict = dict(resource)
        rating_info = review_dal.get_average_rating(resource['resource_id'])
        resource_dict['avg_rating'] = rating_info['avg_rating']
        resource_dict['review_count'] = rating_info['review_count']
        resources_with_ratings.append(resource_dict)

    return render_template(
        'resources/list.html',
        resources=resources_with_ratings,
        categories=categories,
        keyword=keyword,
        category=category,
        location=location
    )


@resource_bp.route('/<int:resource_id>')
def view_resource(resource_id):
    """View resource details."""
    resource = resource_dal.get_resource_with_owner(resource_id)

    if not resource:
        flash('Resource not found.', 'danger')
        return redirect(url_for('resource.list_resources'))

    # Get reviews
    reviews = review_dal.get_reviews_by_resource(resource_id)
    rating_info = review_dal.get_average_rating(resource_id)

    # Check if current user has reviewed
    user_has_reviewed = False
    if 'user_id' in session:
        user_has_reviewed = review_dal.user_has_reviewed(resource_id, session['user_id'])

    return render_template(
        'resources/view.html',
        resource=resource,
        reviews=reviews,
        rating_info=rating_info,
        user_has_reviewed=user_has_reviewed
    )


@resource_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_resource():
    """Create a new resource."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        location = request.form.get('location', '').strip()
        capacity = request.form.get('capacity', type=int)
        status = request.form.get('status', 'draft')

        # Server-side validation
        is_valid, error = validate_resource_title(title)
        if not is_valid:
            flash(error, 'danger')
            return render_template('resources/create.html')

        if not category:
            flash('Category is required.', 'danger')
            return render_template('resources/create.html')

        if not location:
            flash('Location is required.', 'danger')
            return render_template('resources/create.html')

        if not capacity or capacity < 1:
            flash('Capacity must be at least 1.', 'danger')
            return render_template('resources/create.html')

        if status not in ['draft', 'published']:
            status = 'draft'

        # Sanitize inputs
        title = sanitize_string(title, 200)
        description = sanitize_string(description, 2000)
        category = sanitize_string(category, 50)
        location = sanitize_string(location, 200)

        # Create resource
        resource_id = resource_dal.create_resource(
            owner_id=session['user_id'],
            title=title,
            description=description,
            category=category,
            location=location,
            capacity=capacity,
            status=status
        )

        if resource_id:
            flash('Resource created successfully!', 'success')
            return redirect(url_for('resource.view_resource', resource_id=resource_id))
        else:
            flash('Failed to create resource.', 'danger')

    return render_template('resources/create.html')


@resource_bp.route('/<int:resource_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_resource(resource_id):
    """Edit a resource."""
    resource = resource_dal.get_resource_by_id(resource_id)

    if not resource:
        flash('Resource not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    # Check ownership
    if resource['owner_id'] != session['user_id'] and session.get('user_role') != 'admin':
        flash('You do not have permission to edit this resource.', 'danger')
        return redirect(url_for('resource.view_resource', resource_id=resource_id))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        location = request.form.get('location', '').strip()
        capacity = request.form.get('capacity', type=int)
        status = request.form.get('status', 'draft')

        # Server-side validation
        is_valid, error = validate_resource_title(title)
        if not is_valid:
            flash(error, 'danger')
            return render_template('resources/edit.html', resource=resource)

        if not category or not location:
            flash('Category and location are required.', 'danger')
            return render_template('resources/edit.html', resource=resource)

        if not capacity or capacity < 1:
            flash('Capacity must be at least 1.', 'danger')
            return render_template('resources/edit.html', resource=resource)

        # Sanitize inputs
        title = sanitize_string(title, 200)
        description = sanitize_string(description, 2000)
        category = sanitize_string(category, 50)
        location = sanitize_string(location, 200)

        # Update resource
        success = resource_dal.update_resource(
            resource_id=resource_id,
            title=title,
            description=description,
            category=category,
            location=location,
            capacity=capacity,
            status=status
        )

        if success:
            flash('Resource updated successfully!', 'success')
            return redirect(url_for('resource.view_resource', resource_id=resource_id))
        else:
            flash('Failed to update resource.', 'danger')

    return render_template('resources/edit.html', resource=resource)


@resource_bp.route('/<int:resource_id>/delete', methods=['POST'])
@login_required
def delete_resource(resource_id):
    """Delete a resource."""
    resource = resource_dal.get_resource_by_id(resource_id)

    if not resource:
        flash('Resource not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    # Check ownership
    if resource['owner_id'] != session['user_id'] and session.get('user_role') != 'admin':
        flash('You do not have permission to delete this resource.', 'danger')
        return redirect(url_for('resource.view_resource', resource_id=resource_id))

    success = resource_dal.delete_resource(resource_id)

    if success:
        flash('Resource deleted successfully.', 'success')
    else:
        flash('Failed to delete resource.', 'danger')

    return redirect(url_for('main.dashboard'))
