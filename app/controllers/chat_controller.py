from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from .. import db
from ..models.chat import ChatMessage
from ..models.user import User
from sqlalchemy import or_

bp = Blueprint('chat', __name__)

@bp.route('/admin/live-chat')
@login_required
def admin_index():
    if current_user.role != 'admin':
        return render_template('errors/403.html'), 403
    
    # Get distinct users who have sent messages
    # We join User and ChatMessage
    users_with_chats = db.session.query(User).join(ChatMessage, ChatMessage.sender_id == User.id).filter(User.role == 'nasabah').distinct().all()
    
    return render_template('chat/admin_index.html', chat_users=users_with_chats)

@bp.route('/api/chat/history')
@bp.route('/api/chat/history/<int:user_id>')
@login_required
def get_history(user_id=None):
    if current_user.role == 'nasabah':
        target_id = current_user.id
    else:
        # Admin requesting
        target_id = user_id
        if not target_id:
            return jsonify([])

    # Messages where:
    # 1. Sender is the target_id (User -> Admin)
    # 2. Receiver is the target_id (Admin -> User)
    messages = ChatMessage.query.filter(
        or_(
            ChatMessage.sender_id == target_id,
            ChatMessage.receiver_id == target_id
        )
    ).order_by(ChatMessage.timestamp.asc()).all()
    
    return jsonify([msg.to_dict() for msg in messages])
