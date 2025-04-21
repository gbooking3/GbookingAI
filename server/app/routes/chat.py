from flask import Blueprint, request, jsonify
from app.services.chat_service import process_user_message
from app.models.chat import Chat

bp = Blueprint('chat', __name__, url_prefix='/api/v1/chat')

@bp.route('/history', methods=['POST'])
def get_chat_history():
    data = request.get_json()
    user_id = data.get("id")
    if not user_id:
        return jsonify({"error": "Missing user ID"}), 400

    conversations = Chat.get_user_chats(user_id)
    return jsonify({"history": conversations})

@bp.route("/message", methods=["POST"])
def process_chat_request():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing data"}), 400

    user_id = data.get("id")
    user_name = data.get("name")
    user_message = data.get("message")
    conversation_id = data.get("conversation_id")

    print(f"[Request] User: {user_name}, ID: {user_id}, Msg: {user_message}, Conversation ID: {conversation_id}")

    response_data = process_user_message(
        user_id=user_id,
        user_name=user_name,
        user_message=user_message,
        conversation_id=conversation_id
    )

    return jsonify(response_data)
