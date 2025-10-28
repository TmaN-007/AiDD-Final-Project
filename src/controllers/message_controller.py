"""Message controller - handles messaging between users."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.data_access.database import Database
from src.data_access.message_dal import MessageDAL
from src.data_access.user_dal import UserDAL
from src.controllers.auth_controller import login_required
from src.utils.validators import sanitize_string

message_bp = Blueprint('message', __name__, url_prefix='/messages')

db = Database()
message_dal = MessageDAL(db)
user_dal = UserDAL(db)


@message_bp.route('/')
@login_required
def inbox():
    """View message inbox."""
    threads = message_dal.get_user_threads(session['user_id'])
    return render_template('messages/inbox.html', threads=threads)


@message_bp.route('/thread/<int:thread_id>')
@login_required
def view_thread(thread_id):
    """View a message thread."""
    messages = message_dal.get_thread_messages(thread_id)

    # Verify user is part of this thread
    if messages:
        user_id = session['user_id']
        is_participant = any(m['sender_id'] == user_id or m['receiver_id'] == user_id for m in messages)
        if not is_participant:
            flash('You do not have access to this conversation.', 'danger')
            return redirect(url_for('message.inbox'))
    else:
        flash('No messages found.', 'info')
        return redirect(url_for('message.inbox'))

    return render_template('messages/thread.html', messages=messages, thread_id=thread_id)


@message_bp.route('/send/<int:receiver_id>', methods=['GET', 'POST'])
@login_required
def send_message(receiver_id):
    """Send a message to a user."""
    receiver = user_dal.get_user_by_id(receiver_id)

    if not receiver:
        flash('User not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        content = request.form.get('content', '').strip()

        if not content:
            flash('Message cannot be empty.', 'danger')
            return render_template('messages/compose.html', receiver=receiver)

        content = sanitize_string(content, 2000)

        thread_id = message_dal.get_or_create_thread_id(session['user_id'], receiver_id)
        message_id = message_dal.create_message(thread_id, session['user_id'], receiver_id, content)

        if message_id:
            flash('Message sent successfully!', 'success')
            return redirect(url_for('message.view_thread', thread_id=thread_id))
        else:
            flash('Failed to send message.', 'danger')

    return render_template('messages/compose.html', receiver=receiver)


@message_bp.route('/reply/<int:thread_id>', methods=['POST'])
@login_required
def reply_to_thread(thread_id):
    """Reply to a message thread."""
    content = request.form.get('content', '').strip()

    if not content:
        flash('Message cannot be empty.', 'danger')
        return redirect(url_for('message.view_thread', thread_id=thread_id))

    # Get thread messages to find the other user
    messages = message_dal.get_thread_messages(thread_id)
    if not messages:
        flash('Thread not found.', 'danger')
        return redirect(url_for('message.inbox'))

    # Find receiver (the other person in the conversation)
    user_id = session['user_id']
    first_message = messages[0]
    receiver_id = first_message['sender_id'] if first_message['receiver_id'] == user_id else first_message['receiver_id']

    content = sanitize_string(content, 2000)
    message_id = message_dal.create_message(thread_id, user_id, receiver_id, content)

    if message_id:
        flash('Reply sent successfully!', 'success')
    else:
        flash('Failed to send reply.', 'danger')

    return redirect(url_for('message.view_thread', thread_id=thread_id))
