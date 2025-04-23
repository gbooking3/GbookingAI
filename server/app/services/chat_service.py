# server/app/services/chat_service.py
import difflib
from app.ai.init_ai import ask_gemini
from app.utils.gbooking_helpers import get_services, get_doctors, get_available_slots, reserve_appointment, get_business_names, business_ids_from_network, get_business_doctors
from app.models.chat import Chat
networkID = 456
english_to_hebrew = {
    "Cardiology": "קרדיולוגיה",
    "Gastroenterology": "גסטרואנטרולוגיה",
    "Neurology": "נוירולוגיה",
    "CT": "CT",  # if it's written the same
}

businesses_id = business_ids_from_network(networkID)
businesses_names, businesses_names_ids = get_business_names(businesses_id)

def contains_fuzzy_keyword(message, target="services", threshold=0.8):
    words = message.lower().split()
    matches = difflib.get_close_matches(target, words, n=1, cutoff=threshold)
    return bool(matches)

def enrich_user_message(user_message):
    try:
        if contains_fuzzy_keyword(user_message, target="departments") or contains_fuzzy_keyword(user_message, target="business"):
            #businesses_id = business_ids_from_network(networkID)
            #businesses_names,_ = get_business_names(businesses_id)
            print(f'{ businesses_names= }')
            businesses_names_str = ", ".join(businesses_names)
            return f"These are our departments in the hosptial: {businesses_names_str}. {user_message}"
        
        elif contains_fuzzy_keyword(user_message, target="Cardiology") or contains_fuzzy_keyword(user_message, target="30040"):
            hebrew_department = english_to_hebrew.get("Cardiology")
            matching_id = None
            business_name = ""
            for dept_id, label in businesses_names_ids:
                if hebrew_department in label:
                    matching_id = dept_id
                    business_name = label
                    break
            
            doctorsOfBusiness = get_business_doctors(matching_id)
            print("The doctors of the  ",business_name," with the id ", matching_id, " are:")
            print(f'{ doctorsOfBusiness= }')
            doctorsOfBusiness_str = ", ".join([f"Doctor. {doc['name']}" for doc in doctorsOfBusiness])
            return f"These are our available doctors: {doctorsOfBusiness_str}. {user_message}"

        elif contains_fuzzy_keyword(user_message, target="Gastroenterology") or contains_fuzzy_keyword(user_message, target="31200"):
            hebrew_department = english_to_hebrew.get("Gastroenterology")
            matching_id = None
            business_name = ""
            for dept_id, label in businesses_names_ids:
                if hebrew_department in label:
                    matching_id = dept_id
                    business_name = label
                    break
            
            doctorsOfBusiness = get_business_doctors(matching_id)
            print("The doctors of the  ",business_name," with the id ", matching_id, " are:")
            print(f'{ doctorsOfBusiness= }')
            doctorsOfBusiness_str = ", ".join([f"Doctor. {doc['name']}" for doc in doctorsOfBusiness])
            return f"These are our available doctors: {doctorsOfBusiness_str}. {user_message}"
        
        elif contains_fuzzy_keyword(user_message, target="Neurology") or contains_fuzzy_keyword(user_message, target="30300"):
            hebrew_department = english_to_hebrew.get("Neurology")
            matching_id = None
            business_name = ""
            for dept_id, label in businesses_names_ids:
                if hebrew_department in label:
                    matching_id = dept_id
                    business_name = label
                    break
            
            doctorsOfBusiness = get_business_doctors(matching_id)
            print("The doctors of the  ",business_name," with the id ", matching_id, " are:")
            print(f'{ doctorsOfBusiness= }')
            doctorsOfBusiness_str = ", ".join([f"Doctor. {doc['name']}" for doc in doctorsOfBusiness])
            return f"These are our available doctors: {doctorsOfBusiness_str}. {user_message}"
        
        elif contains_fuzzy_keyword(user_message, target="CT") or contains_fuzzy_keyword(user_message, target="46350"):
            print("ana hoooon")
            hebrew_department = english_to_hebrew.get("CT")
            matching_id = None
            business_name = ""
            for dept_id, label in businesses_names_ids:
                if hebrew_department in label:
                    matching_id = dept_id
                    business_name = label
                    break
            
            doctorsOfBusiness = get_business_doctors(matching_id)
            print("The doctors of the  ",business_name," with the id ", matching_id, " are:")
            print(f'{ doctorsOfBusiness= }')
            doctorsOfBusiness_str = ", ".join([f"Doctor. {doc['name']}" for doc in doctorsOfBusiness])
            return f"These are our available doctors: {doctorsOfBusiness_str}. {user_message}"
        

        elif contains_fuzzy_keyword(user_message, target="Doctor."):
            print("10"*10)
            print(user_message)

        
        elif contains_fuzzy_keyword(user_message, target="services"):
            services_list = get_services()
            print(f'{ services_list= }')
            services_str = ", ".join(services_list)
            return f"We offer the following services: {services_str}. {user_message}"

       
       # elif contains_fuzzy_keyword(user_message, target="doctors"):
       #    doctors = get_doctors()
        #    print(f'{ doctors= }')
         #   doctor_str = ", ".join([f"Dr. {doc['name']} ({doc['taxonomies']})" for doc in doctors])
          #  return f"These are our available doctors: {doctor_str}. {user_message}"
        

        elif contains_fuzzy_keyword(user_message, target="dates") or contains_fuzzy_keyword(user_message, target="hours"):
            dates = get_available_slots(
            business_id="4000000008542",
            resources_items=[
                {"id": "67e16c86c43bdd3739a7b415", "duration": 30},
                {"id": "66e6b669bbe2b5c4faf5bdd7", "duration": 30}
            ],
            taxonomy_ids=["9268431"],
            from_date="2025-05-13T00:00:00.000Z",
            to_date="2025-05-16T00:00:00.000Z"
            )
            print(f'{ dates= }')
            return f"These are our available dates: {dates}. {user_message}"
        
        elif contains_fuzzy_keyword(user_message, target="book"):
            book  = reserve_appointment(
                token="02ccadf0487e1e7ae27fea5048c3f53e7330fa45",
                user="67e16c86c43bdd3739a7b415",
                business_id="4000000008542",
                taxonomy_id="9346291",
                resource_id="66e6b669bbe2b5c4faf5bdd7",
                start_time="2025-05-15T08:20:00"
)
            print(f'{ book= }')
            return f" {book}. {user_message}" 
        

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
