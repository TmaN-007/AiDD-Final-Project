"""
AI Concierge controller.
Provides API endpoints for the AI Resource Concierge feature.
"""

from flask import Blueprint, render_template, request, jsonify, session
from src.utils.ai_concierge import concierge
from src.controllers.auth_controller import login_required

concierge_bp = Blueprint('concierge', __name__, url_prefix='/concierge')


@concierge_bp.route('/')
@login_required
def index():
    """AI Concierge interface page."""
    context = concierge.get_context_summary()
    return render_template('concierge/index.html', context=context)


@concierge_bp.route('/ask', methods=['POST'])
@login_required
def ask():
    """
    Handle AI Concierge queries.

    Accepts JSON with 'query' field containing natural language question.
    Returns JSON response with answer.
    """
    data = request.get_json()
    query_text = data.get('query', '').strip()

    if not query_text:
        return jsonify({
            'success': False,
            'message': 'Query cannot be empty.'
        }), 400

    # Generate response
    response = concierge.generate_natural_language_response(query_text)

    return jsonify({
        'success': True,
        'response': response,
        'query': query_text
    })


@concierge_bp.route('/api/query', methods=['POST'])
@login_required
def structured_query():
    """
    Handle structured API queries to the concierge.

    Accepts JSON with 'query_type' and additional parameters.
    """
    data = request.get_json()
    query_type = data.get('query_type')

    if not query_type:
        return jsonify({
            'success': False,
            'message': 'query_type is required.'
        }), 400

    # Remove query_type from params
    params = {k: v for k, v in data.items() if k != 'query_type'}

    # Execute query
    result = concierge.answer_query(query_type, **params)

    return jsonify(result)
