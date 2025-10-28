"""Main controller - homepage and dashboard."""

from flask import Blueprint, render_template, session
from src.data_access.database import Database
from src.data_access.resource_dal import ResourceDAL
from src.data_access.booking_dal import BookingDAL
from src.controllers.auth_controller import login_required

main_bp = Blueprint('main', __name__)

db = Database()
resource_dal = ResourceDAL(db)
booking_dal = BookingDAL(db)


@main_bp.route('/')
def index():
    """Homepage."""
    featured_resources = resource_dal.get_top_rated_resources(limit=6)
    categories = resource_dal.get_categories()
    return render_template('index.html',
                         featured_resources=featured_resources,
                         categories=categories)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard."""
    user_id = session['user_id']

    # Get user's resources
    my_resources = resource_dal.get_resources_by_owner(user_id)

    # Get user's bookings
    my_bookings = booking_dal.get_bookings_by_requester(user_id)

    # Get bookings for user's resources
    bookings_for_my_resources = booking_dal.get_bookings_by_owner(user_id)

    # Get upcoming bookings
    upcoming_bookings = booking_dal.get_upcoming_bookings(user_id)

    return render_template('dashboard.html',
                         my_resources=my_resources,
                         my_bookings=my_bookings,
                         bookings_for_my_resources=bookings_for_my_resources,
                         upcoming_bookings=upcoming_bookings)
