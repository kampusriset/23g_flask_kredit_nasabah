from flask import request
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from . import socketio, db
from .models.chat import ChatMessage
from .models.user import User

@socketio.on('connect')
def handle_connect():
    if not current_user.is_authenticated:
        return False
    
    if current_user.role == 'admin':
        join_room('admin_global')
    else:
        # Nasabah joins their own room
        join_room(f"user_{current_user.id}")

@socketio.on('join_chat')
def join_chat(data):
    # Used by admins to join a specific user's chat room
    if current_user.is_authenticated and current_user.role == 'admin':
        target_user_id = data.get('user_id')
        if target_user_id:
            join_room(f"user_{target_user_id}")

@socketio.on('send_message')
def handle_message(data):
    if not current_user.is_authenticated:
        return

    message = data.get('message')
    recipient_id = data.get('recipient_id') # If admin sending to user
    
    if not message:
        return

    if current_user.role == 'admin':
        if not recipient_id:
            return
        
        # Save to DB
        new_msg = ChatMessage(
            sender_id=current_user.id,
            receiver_id=recipient_id,
            message=message
        )
        db.session.add(new_msg)
        db.session.commit()

        # Emit to the user's room
        # include timestamp string for UI
        emit('receive_message', {
            'sender_id': current_user.id,
            'message': message,
            'timestamp': new_msg.timestamp.strftime('%H:%M'),
            'role': 'admin'
        }, room=f"user_{recipient_id}")
        
    else:
        # Nasabah sending to admin (conceptually)
        # Receiver ID is conceptually 'an admin', but we can leave it null or pick one.
        # For this simple app, let's leave receiver_id null or set it if we had a specific agent.
        # Let's say receiver_id = None means "to support".
        
        new_msg = ChatMessage(
            sender_id=current_user.id,
            receiver_id=None, # System/Support
            message=message
        )
        db.session.add(new_msg)
        db.session.commit()

        # Emit to user's room (so admins in there see it)
        emit('receive_message', {
            'sender_id': current_user.id,
            'message': message,
            'timestamp': new_msg.timestamp.strftime('%H:%M'),
            'role': 'nasabah',
            'sender_name': current_user.username
        }, room=f"user_{current_user.id}")

        # Notification to all admins
        emit('new_chat_notification', {
            'sender_id': current_user.id,
            'sender_name': current_user.username,
            'message': message[:30] + '...' if len(message) > 30 else message
        }, room='admin_global')
