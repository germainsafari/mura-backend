# backend/routes.py
from flask import Blueprint, request, jsonify
from models import User, Conversation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from openai_handler import get_gpt_response
import datetime

auth_blueprint = Blueprint('auth', __name__)
chat_blueprint = Blueprint('chat', __name__)

# Register route
@auth_blueprint.route('/register', methods=['POST'])
def register():
    from app import db  # Import db within the function to avoid circular import
    data = request.json
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201

# Login route
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(days=1))
        return jsonify(access_token=access_token)
    return jsonify(message="Invalid credentials"), 401

# Chat route
@chat_blueprint.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    from app import db  # Import db within the function
    data = request.json
    user_id = get_jwt_identity()
    user_input = data['message']

    # Fetch user's previous conversation (optional)
    conversation_history = Conversation.query.filter_by(user_id=user_id).order_by(Conversation.timestamp).all()
    formatted_history = [{"role": "assistant", "content": conv.response} for conv in conversation_history]

    # Get GPT-4 response
    gpt_response = get_gpt_response(user_input, formatted_history)

    # Save conversation in database
    new_conversation = Conversation(user_id=user_id, message=user_input, response=gpt_response)
    db.session.add(new_conversation)
    db.session.commit()

    return jsonify(response=gpt_response)
