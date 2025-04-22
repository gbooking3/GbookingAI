# server/app/services/chat_service.py
import difflib
from app.ai.init_ai import ask_gemini
from app.utils.gbooking_helpers import get_services, get_doctors,get_available_slots
from app.models.chat import Chat

def contains_fuzzy_keyword(message, target="services", threshold=0.8):
    words = message.lower().split()
    matches = difflib.get_close_matches(target, words, n=1, cutoff=threshold)
    return bool(matches)

def enrich_user_message(user_message):
    try:
        if contains_fuzzy_keyword(user_message, target="services"):
            services_list = get_services()
            print(f'{ services_list= }')
            services_str = ", ".join(services_list)
            return f"We offer the following services: {services_str}. {user_message}"

        elif contains_fuzzy_keyword(user_message, target="doctors"):
            doctors = get_doctors()
            print(f'{ doctors= }')
            doctor_str = ", ".join([f"Dr. {doc['name']} ({doc['profession']})" for doc in doctors])
            return f"These are our available doctors: {doctor_str}. {user_message}"
        

        elif contains_fuzzy_keyword(user_message, target="dates") or contains_fuzzy_keyword(user_message, target="hours"):
            dates = get_available_slots(
            business_id="4000000008542",
            resources_items=[
                {"id": "66e6b856b57b88c54a2ab1b9", "duration": 30},
                {"id": "66e6b669bbe2b5c4faf5bdd7", "duration": 30}
            ],
            taxonomy_ids=["9175163"],
            from_date="2025-05-13T00:00:00.000Z",
            to_date="2025-05-16T00:00:00.000Z"
            )
            print(f'{ dates= }')
            return f"These are our available dates: {dates}. {user_message}"
        

    except Exception as e:
        print("Error enriching message:", e)

    return user_message

def process_user_message(user_id, user_name, user_message, conversation_id):
    enriched_message = enrich_user_message(user_message)
    response = ask_gemini(enriched_message)
   
    saved_convo_id = Chat.start_or_update_conversation(
        ownid=user_id,
        user_name=user_name,
        user_msg=enriched_message,
        bot_msg=response,
        conversation_id=conversation_id
    )

    return {
        "message": response,
        "conversation_id": saved_convo_id,
    }
