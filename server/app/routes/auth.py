from flask import Blueprint, request, jsonify
from app.ai.init_ai import ask_gemini
from app.services.auth_service import (
    register_user, login_user_by_ownid, refresh_user_token,
    send_otp_via_yandex, generate_otp
)
from app.models.user import User
from app.models.chat import Chat
import difflib
import requests

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
generated_otp   =None


@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400
    required_fields = ["email", "phone", "ownid"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400
    return register_user(data)


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    ownid = data.get("ownid")
    method = data.get("method")
    contact_value = User.find_by_ownid(ownid)
    email = contact_value["email"]
    print("The email is : ",email)
    global generated_otp
    user = User.find_by_ownid(ownid)
    if not user:
        return jsonify({ "error": "Invalid credentials" }), 404

 
    if method == "email":
       
        otp = send_otp_via_yandex(
            sender_email='mohamedabohamad@yandex.com',
            sender_password='qoebhhdmafgowgjn',
            recipient_email=email
        )
    elif method == "phone":
        otp = generate_otp()
        print(f"Simulated SMS to {contact_value}: OTP = {otp}")
    else:
        return jsonify({"error": "Invalid contact method"}), 400

    generated_otp = otp
    return login_user_by_ownid(ownid)


@bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    ownid = data.get("ownid")
    otp = data.get("otp")
    stored_otp = generated_otp 
    print("                ",stored_otp)
    print(type(otp))
    print(type(stored_otp))

    if stored_otp != otp:
        return jsonify({"error": "OTP is wrong"}), 400

    return jsonify({"message": "OTP verified successfully"}), 200



@bp.route('/refresh-token', methods=['POST'])
def refresh():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    data = request.get_json()
    return refresh_user_token(data)


@bp.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    print(data)
    return jsonify({"message": "Data received successfully", "received_data": data}), 200

def contains_fuzzy_keyword(message, target="services", threshold=0.8):
    words = message.lower().split()
    matches = difflib.get_close_matches(target, words, n=1, cutoff=threshold)
    return bool(matches)


@bp.route('/history', methods=['POST'])
def get_chat_history():
    data = request.get_json()
    user_id = data.get("id")
    if not user_id:
        return jsonify({"error": "Missing user ID"}), 400

    conversations = Chat.get_user_chats(user_id)
    return jsonify({"history": conversations})

@bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing data"}), 400

    user_id = data.get("id")
    user_name = data.get("name")
    user_message = data.get("message")
    conversation_id = data.get("conversation_id")

    print(f"[Request] User: {user_name}, ID: {user_id}, Msg: {user_message}, Conversation ID: {conversation_id}")

    try:
        if contains_fuzzy_keyword(user_message, target="services"):
            services_list = get_services()
            services_str = ", ".join(services_list)
            user_message = f"We offer the following services: {services_str}. {user_message}"

        elif contains_fuzzy_keyword(user_message, target="doctor"):
            doctors = get_doctors()
            doctor_str = ", ".join([f"Dr. {doc['name']} ({doc['profession']})" for doc in doctors])
            user_message = f"These are our available doctors: {doctor_str}. {user_message}"

    except Exception as e:
        print("Error enriching user message:", e)

    response = ask_gemini(user_message)

    saved_convo_id = Chat.start_or_update_conversation(
        ownid=user_id,
        user_name=user_name,
        user_msg=user_message,
        bot_msg=response,
        conversation_id=conversation_id
    )

    return jsonify({
        "message": response,
        "conversation_id": saved_convo_id,
    })


# server/app/utils/gbooking_helpers.py

def get_services():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": "8e7d61be4f200e39ea29b1231006a248de108d9a",
            "user": "5b1035dcaff15607133b523f"
        },
        "method": "business.get_profile_by_id",
        "params": {
            "business": {"id": "4000000006304"},
            "with_networks": True
        }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post("https://apiv2.gbooking.ru/rpc", headers=headers, json=payload)
    services = response.json().get("result", {}).get("business", {}).get("taxonomies", [])
    return [s.get("alias", {}).get("ru-ru", "Unnamed") for s in services]

def get_doctors():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": "8e7d61be4f200e39ea29b1231006a248de108d9a",
            "user": "5b1035dcaff15607133b523f"
        },
        "method": "business.get_profile_by_id",
        "params": {
            "business": {"id": "4000000006304"},
            "with_networks": True
        }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post("https://apiv2.gbooking.ru/rpc", headers=headers, json=payload)
    data = response.json()

    resources = data.get("result", {}).get("business", {}).get("resources", [])
    doctors = []

    for person in resources:
        profession = (person.get("profession") or "").lower()
        description = (person.get("description") or "").lower()
        name = f"{person.get('name', '')} {person.get('surname', '')}".strip()
        print(description+"\n")
        # if any(keyword in profession or keyword in description for keyword in ["doctor", "dr", "physician"]):
        #     doctors.append({
        #         "id": person.get("id"),
        #         "name": name,
        #         "profession": person.get("profession"),
        #         "description": person.get("description"),
        #         "email": person.get("email"),
        #         "status": person.get("status"),
        #         "icon_url": person.get("icon_url")
        #     })

    return doctors
