"""
Campus Resource Hub - Main Flask Application
A full-stack web application for managing and booking campus resources.
"""

import os
from flask import Flask, session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import controllers
from src.controllers.main_controller import main_bp
from src.controllers.auth_controller import auth_bp
from src.controllers.resource_controller import resource_bp
from src.controllers.booking_controller import booking_bp
from src.controllers.review_controller import review_bp
from src.controllers.message_controller import message_bp
from src.controllers.admin_controller import admin_bp
from src.controllers.concierge_controller import concierge_bp

# Initialize database
from src.data_access.database import Database
db = Database()


def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__,
                template_folder='src/views',
                static_folder='src/static')

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_UPLOAD_SIZE', 5242880))
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'src/static/uploads')

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(resource_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(concierge_bp)

    # Context processor for templates
    @app.context_processor
    def inject_user():
        """Inject user info into all templates."""
        return dict(
            current_user_id=session.get('user_id'),
            current_user_name=session.get('user_name'),
            current_user_role=session.get('user_role')
        )

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
