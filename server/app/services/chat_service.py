# server/app/services/chat_service.py

import difflib
import re
import string
from datetime import datetime, timedelta
import os

from app.ai.init_ai import ask_gemini
from app.models.chat import Chat
from app.utils.gbooking_helpers import (
    get_services, get_doctors, get_available_slots, reserve_appointment,
    get_business_names, business_ids_from_network, get_business_doctors, get_doctor_services
)

from app.services.predict import predict_intent

networkID = 456

english_to_hebrew = {
    "Cardiology": "קרדיולוגיה",
    "Gastroenterology": "גסטרואנטרולוגיה",
    "Neurology": "נוירולוגיה",
    "CT": "CT",
}

department_keywords = {
    "Cardiology": ["Cardiology", "30040"],
    "Gastroenterology": ["Gastroenterology", "31200"],
    "Neurology": ["Neurology", "30300"],
    "CT": ["CT", "46350"]
}

doctor_keywords = ["dr", "dr.", "doctor", "Dr", "Doctor", "דר"]

service_lists = [
    get_services(4000000008541),
    get_services(4000000008542),
    get_services(4000000008543),
    get_services(4000000008544),
]

import difflib
import string


def contains_fuzzy_keyword(message, keyword, threshold=0.8):
    translator = str.maketrans('', '', string.punctuation)
    message = message.translate(translator).lower()
    keyword = keyword.lower()

    # Direct substring match
    if keyword in message:
        return True

    # Token-based matching: compare keyword against every word or phrase in message
    message_tokens = message.split()
    for i in range(len(message_tokens)):
        for j in range(i + 1, min(i + 4, len(message_tokens) + 1)):
            window = " ".join(message_tokens[i:j])
            ratio = difflib.SequenceMatcher(None, window, keyword).ratio()
            if ratio >= threshold:
                return True

    return False


def fetch_patient_info(conversation_id):
    return (
        Chat.get_patient_business_id(conversation_id),
        Chat.get_patient_resource_id(conversation_id),
        Chat.get_patient_toxonomy_id(conversation_id),
        Chat.get_patient_date(conversation_id)
    )


def find_department_business(english_name):
    hebrew_department = english_to_hebrew.get(english_name)
    for dept_id, label in businesses_ids_names:
        if hebrew_department in label:
            return dept_id, label
    return None, None


def clean_name(name):
    return name.replace("דר ", "").replace("Dr. ", "").strip()


def extract_date_from_message(message):
    iso_pattern = r'\d{4}-\d{2}-\d{2}'
    if match := re.search(iso_pattern, message):
        return match.group()

    natural_pattern = r'([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})'
    if match := re.search(natural_pattern, message):
        month_str, day, year = match.groups()
        try:
            date_obj = datetime.strptime(f"{month_str} {day} {year}", "%B %d %Y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return None
    return None


def extract_time_from_message(message):
    pattern = r'\b([01]?[0-9]|2[0-3]):([0-5][0-9])\b'
    if match := re.search(pattern, message):
        return match.group()
    return None


def add_one_day(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return (date_obj + timedelta(days=1)).strftime("%Y-%m-%d")


def add_one_day(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return (date_obj + timedelta(days=1)).strftime("%Y-%m-%d")


def process_user_message(user_id, user_name, user_message, conversation_id):
    enriched_message, client_business_id, client_resource_id, client_toxonomy_id, client_date = enrich_user_message(
        user_message, conversation_id)
    print("enriched_message ", enriched_message)

    response = ask_gemini(enriched_message)

    print("response ", response)

    # Re-fetch latest IDs because they might have changed during enrich_user_message
    client_business_id = Chat.get_patient_business_id(conversation_id)
    client_resource_id = Chat.get_patient_resource_id(conversation_id)
    client_toxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
    client_date = Chat.get_patient_date(conversation_id)

    saved_convo_id = Chat.start_or_update_conversation(
        ownid=user_id,
        user_name=user_name,
        user_msg=enriched_message,
        bot_msg=response,
        conversation_id=conversation_id,
        business_id=client_business_id,
        resource_id=client_resource_id,
        taxonomy_id=client_toxonomy_id,
        date=client_date
    )

    return {
        "message": response,
        "conversation_id": saved_convo_id,
    }


businesses_ids = business_ids_from_network(networkID)
businesses_names, businesses_ids_names = get_business_names(businesses_ids)
print("businesses_names ", businesses_names)
print("businesses_names_ids ", businesses_ids_names)
name_to_id = {name: bus_id for bus_id, name in businesses_ids_names}

print("HHHH")
bussiness_and_its_doctors = {}
for bus_id, bus_name in businesses_ids_names:
    bussiness_and_its_doctors[bus_name] = get_business_doctors(bus_id)

print("hello")
print(list(bussiness_and_its_doctors.keys()))
print("hello")
print(bussiness_and_its_doctors["31200 - גסטרואנטרולוגיה"])
print("hello")
doctors_and_its_services_departments = {}

for department_name, doctors in bussiness_and_its_doctors.items():
    for doctor in doctors:
        name = doctor.get('name', 'Unnamed')
        if name:  # Only include entries with a name
            doctors_and_its_services_departments[name] = {
                'taxonomies': doctor.get('taxonomies', []),
                'id': doctor.get('id', ''),
                'department_name': department_name
            }
for name, data in doctors_and_its_services_departments.items():
    print(f"{name}: {data}")
doctor_and_services = {}
for name, data in doctors_and_its_services_departments.items():
    resource_id = data.get("id")
    business_name = data.get("department_name")

    # Find the corresponding business_id
    business_id = next((id_ for id_, name_ in businesses_ids_names if name_ == business_name), None)

    # Get doctor's services
    doctor_services = get_doctor_services(business_id, resource_id)

    # Add all info into one dictionary per doctor
    doctor_and_services[name] = {
        "business_id": business_id,
        "resource_id": resource_id,
        "services": [
            {
                "service_id": service.get("id"),
                "name": service.get("name")
            }
            for service in doctor_services
        ]
    }

# print("come on bitch")
# for name, data in doctor_and_services.items():
# print(f"{name}: {data}")
# print("come on bitch")


# get_doctor_services(busid,docid)

user_message = "i want to set an appointment"
intent = predict_intent(user_message)
print("Predicted Intent:", intent)

department_aliases = {
    "cardiology": "30040 - קרדיולוגיה",
    "קרדיולוגיה": "30040 - קרדיולוגיה",
    "gastroenterology": "31200 - גסטרואנטרולוגיה",
    "גסטרואנטרולוגיה": "31200 - גסטרואנטרולוגיה",
    "neurology": "30300 - נוירולוגיה",
    "נוירולוגיה": "30300 - נוירולוגיה",
    "ct": "46350 - CT",
    "ct scan": "46350 - CT"
}


def normalize_department_input(user_input):
    user_input = user_input.strip().lower()
    return department_aliases.get(user_input)


# lazim tef7as show bser bel change date,doctor,service,department aza mn2ash el2eshe y3ni lzim ykon fe else
def enrich_user_message(user_message, conversation_id):
    intent = predict_intent(user_message)
    patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date = fetch_patient_info(conversation_id)
    if conversation_id:
        context_stage = Chat.get_context_stage(conversation_id)
    else:
        context_stage = "start"
    print("conversation_id ", conversation_id)
    print("intent ", intent)
    print("context_stage ", context_stage)
    response = ""
    if intent == "chitchat" and context_stage == "start":
        return user_message, patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date

    if contains_fuzzy_keyword(user_message, "change department"):
        print("change department")
        Chat.set_patient_business_id(conversation_id, None)
        Chat.set_business_name(conversation_id, None)
        Chat.set_patient_resource_id(conversation_id, None)
        Chat.set_resource_name(conversation_id, None)
        Chat.set_patient_taxonomy_id(conversation_id, None)
        Chat.set_taxonomy_name(conversation_id, None)
        Chat.set_patient_date(conversation_id, None)
        Chat.set_patient_time(conversation_id, None)
        Chat.set_context_stage(conversation_id, "choose_department")
        response = "show the user those departments:\n" + "\n".join(
            businesses_names) + "\n and tell him to write the department that he needs"
        return response, None, None, None, None
    elif contains_fuzzy_keyword(user_message, "change doctor"):
        print("change doctor")
        Chat.set_patient_resource_id(conversation_id, None)
        Chat.set_resource_name(conversation_id, None)
        Chat.set_patient_taxonomy_id(conversation_id, None)
        Chat.set_taxonomy_name(conversation_id, None)
        Chat.set_patient_date(conversation_id, None)
        Chat.set_patient_time(conversation_id, None)
        Chat.set_context_stage(conversation_id, "choose_doctor")
        doctors = bussiness_and_its_doctors.get((Chat.get_business_name(conversation_id)), [])
        print("doctors ", doctors)
        if not doctors:
            return f"Sorry, no doctors found in {Chat.get_business_name(conversation_id)}", str(
                patient_business_id), None, None, None
        doctor_names = "\n".join([doc["name"] for doc in doctors])

        response = "show the user those doctors:\n" + doctor_names + "\n and tell him to write the doctor that he needs"
        return response, patient_business_id, None, None, None
    elif contains_fuzzy_keyword(user_message, "change service"):
        print("change service")
        Chat.set_patient_taxonomy_id(conversation_id, None)
        Chat.set_taxonomy_name(conversation_id, None)
        Chat.set_patient_date(conversation_id, None)
        Chat.set_patient_time(conversation_id, None)
        Chat.set_context_stage(conversation_id, "choose_service")
        doctor_info = doctor_and_services[Chat.get_resource_name(conversation_id)]
        services = doctor_info["services"]
        service_list = "\n".join([f"- {s['name']}" for s in services])

        response = (
            f"You selected Dr. {Chat.get_resource_name(conversation_id)}.\n"
            f"Here are the services available:\n{service_list}\n"
            f"➡️ Please select a service by name.\n"
            f"➡️ {add_Edit_choices('choose_doctor')}"
        )
        return response, patient_business_id, patient_resource_id, None, None
    elif contains_fuzzy_keyword(user_message, "change date"):
        print("change date")
        Chat.set_patient_date(conversation_id, None)
        Chat.set_patient_time(conversation_id, None)
        Chat.set_context_stage(conversation_id, "choose_date")
        fromDate = "2025-04-30T00:00:00.000Z"
        toDate = "2025-05-20T00:00:00.000Z"
        slots_data = get_available_slots(
            business_id=patient_business_id,
            resources_items=[{"id": patient_resource_id, "duration": 30}],
            taxonomy_ids=[patient_taxonomy_id],
            from_date=fromDate,
            to_date=toDate,
        )
        if not slots_data:
            return f"Sorry, there are no available slots for '{Chat.get_taxonomy_name(conversation_id)}' in the next 10 days.\n please select the service again {services}", business_id, resource_id, None, None
        slot_lines = []
        for entry in slots_data:
            date = entry["date"]
            times = ", ".join(entry["slots"].get(Chat.get_patient_resource_id(conversation_id), []))
            if times:
                slot_lines.append(f"{date}")
        response = f"\nHere are the available slots:\n" + "\n".join(
            slot_lines) + "\nplease select a date" + add_Edit_choices("choose_date")
        return response, patient_business_id, patient_resource_id, patient_taxonomy_id, None
    elif contains_fuzzy_keyword(user_message, "change hour"):
        Chat.set_patient_time(conversation_id, None)
        Chat.set_context_stage(conversation_id, "choose_time")
        fromDate = "2025-04-30T00:00:00.000Z"
        toDate = "2025-05-20T00:00:00.000Z"
        slots_data = get_available_slots(
            business_id=patient_business_id,
            resources_items=[{"id": patient_resource_id, "duration": 30}],
            taxonomy_ids=[patient_taxonomy_id],
            from_date=fromDate,
            to_date=toDate,
        )
        if not slots_data:
            return f"Sorry, there are no available slots for '{Chat.get_taxonomy_name(conversation_id)}' in the next 10 days.\n please select the service again {services}", business_id, resource_id, None, None
        slot_lines = []
        for entry in slots_data:
            date = entry["date"]
            times = ", ".join(entry["slots"].get(Chat.get_patient_resource_id(conversation_id), []))
            if times:
                slot_lines.append(f"{date} {times}")
                available_dates = {}
        for line in slot_lines:
            if ": " in line:
                date_part, times_part = line.split(": ", 1)  # Split only on ': ' (colon followed by space)
                available_dates[date_part.strip()] = times_part.strip()
        print("available_dates ", available_dates)
        if (patient_date + "T00:00:00Z") in available_dates.keys():
            print("✅ Valid date selected by user.")
            available_times = available_dates[(patient_date + "T00:00:00Z")]
        response = (
            f"➡️ Please choose one of the available time slots.\n"
            f"🗓️ Available times on {Chat.get_patient_date(conversation_id)}:\n{available_times}\n"
            f"{edit_choices}"
        )
        return response, patient_business_id, patient_resource_id, patient_taxonomy_id, Chat.get_patient_date(
            conversation_id)

    if intent == "start_booking":
        if context_stage == "start":
            response = (
                "Great! Here's how scheduling works:\n"
                "1️⃣ Choose a department\n"
                "2️⃣ Pick a doctor\n"
                "3️⃣ Select a service\n"
                "4️⃣ Choose a date\n"
                "5️⃣ Pick an available time\n"
                "➡️ Do you want to start with choosing the department?"
            )
            return (
                               "Show the user this entire response: " + response), patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date
    elif intent == "confirmation":
        if context_stage == "start":
            Chat.set_context_stage(conversation_id, "choose_department")
            response = "show the user those departments:\n" + "\n".join(
                businesses_names) + "\n and tell him to write the department that he needs"
            print("context stage : ", Chat.get_context_stage(conversation_id))
            return response, patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date
    if context_stage == "choose_department":
        selected_department = normalize_department_input(user_message)
        if not selected_department:
            # Try fuzzy match if not found directly
            for dept_name in bussiness_and_its_doctors.keys():
                if contains_fuzzy_keyword(user_message, dept_name):
                    selected_department = dept_name
                    break
        print("selected_department ", selected_department)

        if selected_department:
            # Chat.set_context_stage(conversation_id, "choose_doctor")
            patient_business_id = name_to_id.get(selected_department)
            Chat.set_patient_business_id(conversation_id, str(patient_business_id))
            Chat.set_business_name(conversation_id, selected_department)
            Chat.set_context_stage(conversation_id, "choose_doctor")
            print("patient_business_id ", patient_business_id)
            doctors = bussiness_and_its_doctors.get(selected_department, [])
            if not doctors:
                return f"Sorry, no doctors found in {selected_department}", str(patient_business_id), None, None, None
            doctor_names = "\n".join([doc["name"] for doc in doctors])
            print("doctor_names ", doctor_names)
            response = f"Here are the available doctors in {selected_department}:\n{doctor_names}\n➡️ Please choose a doctor by name. \n➡️ {add_Edit_choices('choose_department')}"
            return response, str(patient_business_id), None, None, None
        else:
            return "Sorry, I didn't recognize that department. Please choose from the list shown again." + "\n".join(
                businesses_names), None, None, None, None
    doctors = bussiness_and_its_doctors.get((Chat.get_business_name(conversation_id)), [])
    if not doctors:
        return f"Sorry, no doctors found in {selected_department}", str(patient_business_id), None, None, None
    doctor_names = "\n".join([doc["name"] for doc in doctors])
    doctor_names_only = [doc["name"] for doc in doctors if doc["name"]]

    if context_stage == "choose_doctor":
        selected_doctor = None
        normalized_message = user_message.strip().lower()

        for doc in doctor_names_only:
            doc_lower = doc.lower()
            if doc_lower in normalized_message:
                print("doc ", doc)
                print("doc_lower ", doc_lower)
                print("normalized_message ", normalized_message)
                print("ana hom")
                selected_doctor = doc
                break
            elif contains_fuzzy_keyword(normalized_message, doc_lower):
                print("ana hon 2")
                selected_doctor = doc
                break

        print("selected_doctor ", selected_doctor)
        if selected_doctor:
            doctor_info = doctor_and_services[selected_doctor]
            resource_id = doctor_info["resource_id"]
            services = doctor_info["services"]

            # Update patient state
            Chat.set_context_stage(conversation_id, "choose_service")
            Chat.set_patient_resource_id(conversation_id, str(resource_id))
            Chat.set_resource_name(conversation_id, selected_doctor)

            if not services:
                return f"Sorry, {selected_doctor} has no services available at the moment.", patient_business_id, str(
                    resource_id), None, None
            print("services ", services)
            service_list = "\n".join([f"- {s['name']}" for s in services])
            print("service_list ", service_list)
            response = (
                f"You selected Dr. {selected_doctor}.\n"
                f"Here are the services available:\n{service_list}\n"
                f"➡️ Please select a service by name.\n"
                f"➡️ {add_Edit_choices('choose_doctor')}"
            )
            return response, patient_business_id, resource_id, None, None

        else:
            print("wooooooo")
            print(add_Edit_choices('choose_doctor'))
            print("wooooooo")
            edit_choices = add_Edit_choices('choose_doctor')
            return (
                f"Sorry, I couldn't match that doctor. Please choose a doctor from the list again.\n{doctor_names}\n{edit_choices}",
                patient_business_id, None, None, None
            )

    doctor_info = doctor_and_services[Chat.get_resource_name(conversation_id)]
    services = doctor_info["services"]
    if not services:
        return f"Sorry, the doctor you selected has no services available at the moment.", patient_business_id, patient_resource_id, None, None
    print("service_list ", services)
    if context_stage == "choose_service":
        selected_service = None
        selected_service_id = None
        normalized_message = user_message.strip().lower()

        for service in services:
            service_name = service["name"].lower()

            if service_name in normalized_message:
                selected_service = service["name"]
                selected_service_id = service["service_id"]
                break
            elif contains_fuzzy_keyword(normalized_message, service_name):
                selected_service = service["name"]
                selected_service_id = service["service_id"]
                break
        if selected_service:
            Chat.set_context_stage(conversation_id, "choose_date")
            Chat.set_patient_taxonomy_id(conversation_id, selected_service_id)
            Chat.set_taxonomy_name(conversation_id, selected_service)
            resource_id = Chat.get_patient_resource_id(conversation_id)
            taxonomy_id = selected_service_id
            fromDate = "2025-04-30T00:00:00.000Z"
            toDate = "2025-05-20T00:00:00.000Z"
            slots_data = get_available_slots(
                business_id=patient_business_id,
                resources_items=[{"id": patient_resource_id, "duration": 30}],
                taxonomy_ids=[taxonomy_id],
                from_date=fromDate,
                to_date=toDate,
            )
            if not slots_data:
                return f"Sorry, there are no available slots for '{selected_service}' in the next 10 days.\n please select the service again {services}", business_id, resource_id, None, None
            slot_lines = []
            for entry in slots_data:
                date = entry["date"]
                times = ", ".join(entry["slots"].get(resource_id, []))
                if times:
                    slot_lines.append(f"{date}")
            response = f"You chose '{selected_service}'.\nHere are the available dates:\n" + "\n".join(
                slot_lines) + "\nplease select a date" + add_Edit_choices("choose_service")
            return response, business_id, resource_id, taxonomy_id, None

    fromDate = "2025-04-30T00:00:00.000Z"
    toDate = "2025-05-20T00:00:00.000Z"
    slots_data = get_available_slots(
        business_id=patient_business_id,
        resources_items=[{"id": patient_resource_id, "duration": 30}],
        taxonomy_ids=[patient_taxonomy_id],
        from_date=fromDate,
        to_date=toDate,
    )
    if not slots_data:
        return f"Sorry, there are no available slots for '{selected_service}' in the next 10 days.\n please select the service again {services}", business_id, resource_id, None, None
    slot_dates = []
    slot_lines = []
    for entry in slots_data:
        date = entry["date"]
        times = ", ".join(entry["slots"].get(patient_resource_id, []))
        if times:
            slot_dates.append(f"{date}")
            slot_lines.append(f"{date}: {times}")
    print("slot_lines ", slot_lines)
    if context_stage == "choose_date":
        extracted_date = extract_date_from_message(user_message)
        if extracted_date:
            print("User entered date:", extracted_date)
            available_dates = {}
            for line in slot_lines:
                if ": " in line:
                    date_part, times_part = line.split(": ", 1)  # Split only on ': ' (colon followed by space)
                    available_dates[date_part.strip()] = times_part.strip()
            print("available_dates ", available_dates)
            # Check if the user's date is among the available dates
            if (extracted_date + "T00:00:00Z") in available_dates.keys():
                print("✅ Valid date selected by user.")
                print("extracted_date ", extracted_date)
                patient_date = extracted_date
                Chat.set_patient_date(conversation_id, patient_date)
                available_times = available_dates[(extracted_date + "T00:00:00Z")]
                Chat.set_context_stage(conversation_id, "choose_time")
                edit_choices = add_Edit_choices('choose_date')
                print("edit_choices ", edit_choices)
                response = (
                    f"➡️ Please choose one of the available time slots.\n"
                    f"🗓️ Available times on {extracted_date}:\n{available_times}\n"
                    f"{edit_choices}"
                )
                return response, patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date
        else:
            return (
                f"❌ Couldn't recognize a valid available date in your message.\n"
                f"📅 Please choose one of the following dates:\n{slot_dates}",
                patient_business_id, patient_resource_id, patient_taxonomy_id, None
            )

    print("patient date ", patient_date)
    available_dates = {}
    for line in slot_lines:
        if ": " in line:
            date_part, times_part = line.split(": ", 1)  # Split only on ': ' (colon followed by space)
            available_dates[date_part.strip()] = times_part.strip()
    print("available_dates ", available_dates)
    if (patient_date + "T00:00:00Z") in available_dates.keys():
        print("✅ Valid date selected by user.")
        available_times = available_dates[(patient_date + "T00:00:00Z")]
        available_times_list = [time.strip() for time in available_times.split(",")]

    print("available_times ", available_times_list)
    if context_stage == "choose_time":
        selected_time = extract_time_from_message(user_message)
        if selected_time:
            print("User selected time:", selected_time)
            if selected_time and selected_time in available_times_list:
                print("✅ Valid time selected by user: ", selected_time)
                print("patient date: ", patient_date)
                Chat.set_patient_time(conversation_id, selected_time)
                edit_choices = add_Edit_choices('choose_time')
                response = (f"To summurize your choices:\n1.Department name: {Chat.get_business_name(conversation_id)}"
                            f"\n2.Doctor name: {Chat.get_resource_name(conversation_id)}"
                            f"\n3.Service name: {Chat.get_taxonomy_name(conversation_id)}"
                            f"\n4.Date : {Chat.get_patient_date(conversation_id)}"
                            f"\n5. Hour : {Chat.get_patient_time(conversation_id)}"
                            f"\n{edit_choices}"
                            )
                return response, patient_business_id, patient_resource_id, patient_taxonomy_id, Chat.get_patient_date(
                    conversation_id)



        else:
            return (
                f"❌ Couldn't recognize a valid available time in your message.\n"
                f"📅 Please choose one of the following dates:\n{available_times}",
                patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date
            )

    return user_message, patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date


def add_Edit_choices(edit):
    displays = []
    if edit in ["choose_department", "choose_doctor", "choose_service", "choose_date", "choose_time"]:
        displays.append("If you want to select a different department, please just type => change department")
    if edit in ["choose_doctor", "choose_service", "choose_date", "choose_time"]:
        displays.append("If you want to select a different doctor, please just type => change doctor")
    if edit in ["choose_service", "choose_date", "choose_time"]:
        displays.append("If you want to select a different service, please just type => change service")
    if edit in ["choose_date", "choose_time"]:
        displays.append("If you want to select a different date, please just type => change date")
    if edit in ["choose_time"]:
        displays.append("If you want to select a different hour, please just type => change hour")
    return "\n".join(displays)# server/app/services/chat_service.py

import difflib
import re
import string
from datetime import datetime, timedelta
import os

from app.ai.init_ai import ask_gemini
from app.models.chat import Chat
from app.utils.gbooking_helpers import (
    get_services, get_doctors, get_available_slots, reserve_appointment,
    get_business_names, business_ids_from_network, get_business_doctors, get_doctor_services
)

from app.services.predict import predict_intent


networkID = 456



english_to_hebrew = {
    "Cardiology": "קרדיולוגיה",
    "Gastroenterology": "גסטרואנטרולוגיה",
    "Neurology": "נוירולוגיה",
    "CT": "CT",
}

department_keywords = {
    "Cardiology": ["Cardiology", "30040"],
    "Gastroenterology": ["Gastroenterology", "31200"],
    "Neurology": ["Neurology", "30300"],
    "CT": ["CT", "46350"]
}

doctor_keywords = ["dr", "dr.", "doctor", "Dr", "Doctor", "דר"]

service_lists = [
    get_services(4000000008541),
    get_services(4000000008542),
    get_services(4000000008543),
    get_services(4000000008544),
]


import difflib
import string

def contains_fuzzy_keyword(message, keyword, threshold=0.8):
    translator = str.maketrans('', '', string.punctuation)
    message = message.translate(translator).lower()
    keyword = keyword.lower()

    # Direct substring match
    if keyword in message:
        return True

    # Token-based matching: compare keyword against every word or phrase in message
    message_tokens = message.split()
    for i in range(len(message_tokens)):
        for j in range(i+1, min(i+4, len(message_tokens)+1)):
            window = " ".join(message_tokens[i:j])
            ratio = difflib.SequenceMatcher(None, window, keyword).ratio()
            if ratio >= threshold:
                return True

    return False


def fetch_patient_info(conversation_id):
    return (
        Chat.get_patient_business_id(conversation_id),
        Chat.get_patient_resource_id(conversation_id),
        Chat.get_patient_toxonomy_id(conversation_id),
        Chat.get_patient_date(conversation_id)
    )


def find_department_business(english_name):
    hebrew_department = english_to_hebrew.get(english_name)
    for dept_id, label in businesses_ids_names:
        if hebrew_department in label:
            return dept_id, label
    return None, None


def clean_name(name):
    return name.replace("דר ", "").replace("Dr. ", "").strip()


def extract_date_from_message(message):
    iso_pattern = r'\d{4}-\d{2}-\d{2}'
    if match := re.search(iso_pattern, message):
        return match.group()

    natural_pattern = r'([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})'
    if match := re.search(natural_pattern, message):
        month_str, day, year = match.groups()
        try:
            date_obj = datetime.strptime(f"{month_str} {day} {year}", "%B %d %Y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return None
    return None


def extract_time_from_message(message):
    pattern = r'\b([01]?[0-9]|2[0-3]):([0-5][0-9])\b'
    if match := re.search(pattern, message):
        return match.group()
    return None

def add_one_day(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return (date_obj + timedelta(days=1)).strftime("%Y-%m-%d")


def add_one_day(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return (date_obj + timedelta(days=1)).strftime("%Y-%m-%d")




def process_user_message(user_id, user_name, user_message, conversation_id):
    enriched_message, client_business_id, client_resource_id, client_toxonomy_id, client_date = enrich_user_message(user_message, conversation_id)
    print("enriched_message ", enriched_message)

    response = ask_gemini(enriched_message)

    print("response ", response)

    # Re-fetch latest IDs because they might have changed during enrich_user_message
    client_business_id = Chat.get_patient_business_id(conversation_id)
    client_resource_id = Chat.get_patient_resource_id(conversation_id)
    client_toxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
    client_date = Chat.get_patient_date(conversation_id)

    saved_convo_id = Chat.start_or_update_conversation(
        ownid=user_id,
        user_name=user_name,
        user_msg=enriched_message,
        bot_msg=response,
        conversation_id=conversation_id,
        business_id=client_business_id,
        resource_id=client_resource_id,
        taxonomy_id=client_toxonomy_id,
        date=client_date
        )

    return {
        "message": response,
        "conversation_id": saved_convo_id,
    }


businesses_ids = business_ids_from_network(networkID)
businesses_names, businesses_ids_names = get_business_names(businesses_ids)
print("businesses_names ", businesses_names)
print("businesses_names_ids ", businesses_ids_names)
name_to_id = {name: bus_id for bus_id, name in businesses_ids_names}


print("HHHH")
bussiness_and_its_doctors = {}
for bus_id, bus_name in businesses_ids_names:
    bussiness_and_its_doctors[bus_name] = get_business_doctors(bus_id)

print("hello")
print(list(bussiness_and_its_doctors.keys()))
print("hello")
print(bussiness_and_its_doctors["31200 - גסטרואנטרולוגיה"])
print("hello")
doctors_and_its_services_departments = {}

for department_name, doctors in bussiness_and_its_doctors.items():
    for doctor in doctors:
        name = doctor.get('name', 'Unnamed')
        if name:  # Only include entries with a name
            doctors_and_its_services_departments[name] = {
                'taxonomies': doctor.get('taxonomies', []),
                'id': doctor.get('id', ''),
                'department_name': department_name
            }
for name, data in doctors_and_its_services_departments.items():
    print(f"{name}: {data}")
doctor_and_services = {}
for name, data in doctors_and_its_services_departments.items():
    resource_id = data.get("id")
    business_name = data.get("department_name")

    # Find the corresponding business_id
    business_id = next((id_ for id_, name_ in businesses_ids_names if name_ == business_name), None)

    # Get doctor's services
    doctor_services = get_doctor_services(business_id, resource_id)

    # Add all info into one dictionary per doctor
    doctor_and_services[name] = {
        "business_id": business_id,
        "resource_id": resource_id,
        "services": [
            {
                "service_id": service.get("id"),
                "name": service.get("name")
            }
            for service in doctor_services
        ]
    }

#print("come on bitch")
#for name, data in doctor_and_services.items():
    #print(f"{name}: {data}")
#print("come on bitch")



#get_doctor_services(busid,docid)

user_message = "i want to set an appointment"
intent = predict_intent(user_message)
print("Predicted Intent:", intent)

department_aliases = {
    "cardiology": "30040 - קרדיולוגיה",
    "קרדיולוגיה": "30040 - קרדיולוגיה",
    "gastroenterology": "31200 - גסטרואנטרולוגיה",
    "גסטרואנטרולוגיה": "31200 - גסטרואנטרולוגיה",
    "neurology": "30300 - נוירולוגיה",
    "נוירולוגיה": "30300 - נוירולוגיה",
    "ct": "46350 - CT",
    "ct scan": "46350 - CT"
}

def normalize_department_input(user_input):
    user_input = user_input.strip().lower()
    return department_aliases.get(user_input)

#lazim tef7as show bser bel change date,doctor,service,department aza mn2ash el2eshe y3ni lzim ykon fe else
def enrich_user_message(user_message, conversation_id):
        intent = predict_intent(user_message)
        patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date = fetch_patient_info(conversation_id)
        if conversation_id:
            context_stage = Chat.get_context_stage(conversation_id)
        else:
            context_stage = "start"
        print("conversation_id ",conversation_id)
        print("intent ",intent)
        print("context_stage ", context_stage)
        response = ""
        #if intent == "chitchat" and context_stage == "start":

        #    return user_message, patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date

        if contains_fuzzy_keyword(user_message, "change department"):
            print("change department")
            Chat.set_patient_business_id(conversation_id, None)
            Chat.set_business_name(conversation_id, None)
            Chat.set_patient_resource_id(conversation_id, None)
            Chat.set_resource_name(conversation_id, None)
            Chat.set_patient_taxonomy_id(conversation_id, None)
            Chat.set_taxonomy_name(conversation_id, None)
            Chat.set_patient_date(conversation_id, None)
            Chat.set_patient_time(conversation_id, None)
            Chat.set_context_stage(conversation_id, "choose_department")
            response = "show the user those departments:\n" + "\n".join(businesses_names) +  "\n and tell him to write the department that he needs"
            return response, None, None, None, None
        elif contains_fuzzy_keyword(user_message, "change doctor"):
            print("change doctor")
            Chat.set_patient_resource_id(conversation_id, None)
            Chat.set_resource_name(conversation_id, None)
            Chat.set_patient_taxonomy_id(conversation_id, None)
            Chat.set_taxonomy_name(conversation_id, None)
            Chat.set_patient_date(conversation_id, None)
            Chat.set_patient_time(conversation_id, None)
            Chat.set_context_stage(conversation_id, "choose_doctor")
            doctors = bussiness_and_its_doctors.get((Chat.get_business_name(conversation_id)), [])
            print("doctors ", doctors)
            if not doctors:
                return f"Sorry, no doctors found in {Chat.get_business_name(conversation_id)}", str(patient_business_id), None, None, None
            doctor_names = "\n".join([doc["name"] for doc in doctors])

            response = "show the user those doctors:\n" + doctor_names +  "\n and tell him to write the doctor that he needs"
            return response, patient_business_id, None, None, None
        elif contains_fuzzy_keyword(user_message, "change service"):
            print("change service")
            Chat.set_patient_taxonomy_id(conversation_id, None)
            Chat.set_taxonomy_name(conversation_id, None)
            Chat.set_patient_date(conversation_id, None)
            Chat.set_patient_time(conversation_id, None)
            Chat.set_context_stage(conversation_id, "choose_service")
            doctor_info = doctor_and_services[Chat.get_resource_name(conversation_id)]
            services = doctor_info["services"]
            service_list = "\n".join([f"- {s['name']}" for s in services])

            response = (
                f"You selected Dr. {Chat.get_resource_name(conversation_id)}.\n"
                f"Here are the services available:\n{service_list}\n"
                f"➡️ Please select a service by name.\n"
                f"➡️ {add_Edit_choices('choose_doctor')}"
            )
            return response, patient_business_id, patient_resource_id, None, None
        elif contains_fuzzy_keyword(user_message, "change date"):
            print("change date")
            Chat.set_patient_date(conversation_id, None)
            Chat.set_patient_time(conversation_id, None)
            Chat.set_context_stage(conversation_id, "choose_date")
            fromDate = "2025-04-30T00:00:00.000Z"
            toDate = "2025-05-20T00:00:00.000Z"
            slots_data = get_available_slots(
                    business_id=patient_business_id,
                    resources_items=[{"id": patient_resource_id, "duration": 30}],
                    taxonomy_ids=[patient_taxonomy_id],
                    from_date=fromDate,
                    to_date=toDate,
                )
            if not slots_data:
                    return f"Sorry, there are no available slots for '{Chat.get_taxonomy_name(conversation_id)}' in the next 10 days.\n please select the service again {services}", business_id, resource_id, None, None
            slot_lines = []
            for entry in slots_data:
                date = entry["date"]
                times = ", ".join(entry["slots"].get(Chat.get_patient_resource_id(conversation_id), []))
                if times:
                    slot_lines.append(f"{date}")
            response = f"\nHere are the available slots:\n" + "\n".join(slot_lines) + "\nplease select a date" + add_Edit_choices("choose_date")
            return response, patient_business_id, patient_resource_id, patient_taxonomy_id, None
        elif contains_fuzzy_keyword(user_message, "change hour"):
            Chat.set_patient_time(conversation_id, None)
            Chat.set_context_stage(conversation_id, "choose_time")
            fromDate = "2025-04-30T00:00:00.000Z"
            toDate = "2025-05-20T00:00:00.000Z"
            slots_data = get_available_slots(
                    business_id=patient_business_id,
                    resources_items=[{"id": patient_resource_id, "duration": 30}],
                    taxonomy_ids=[patient_taxonomy_id],
                    from_date=fromDate,
                    to_date=toDate,
                )
            if not slots_data:
                    return f"Sorry, there are no available slots for '{Chat.get_taxonomy_name(conversation_id)}' in the next 10 days.\n please select the service again {services}", business_id, resource_id, None, None
            slot_lines = []
            for entry in slots_data:
                date = entry["date"]
                times = ", ".join(entry["slots"].get(Chat.get_patient_resource_id(conversation_id), []))
                if times:
                    slot_lines.append(f"{date} {times}")
                    available_dates = {}
            for line in slot_lines:
                if ": " in line:
                    date_part, times_part = line.split(": ", 1)  # Split only on ': ' (colon followed by space)
                    available_dates[date_part.strip()] = times_part.strip()
            print("available_dates ", available_dates)
            if (patient_date+"T00:00:00Z") in available_dates.keys():
                print("✅ Valid date selected by user.")
                available_times = available_dates[(patient_date+"T00:00:00Z")]
            response = (
                    f"➡️ Please choose one of the available time slots.\n"
                    f"🗓️ Available times on {Chat.get_patient_date(conversation_id)}:\n{available_times}\n"
                    f"{edit_choices}"
            )
            return response, patient_business_id, patient_resource_id, patient_taxonomy_id, Chat.get_patient_date(conversation_id)




        if intent == "start_booking" or intent == "choose_department" or intent == "chitchat":
            if context_stage == "start":
                print("im here")
                response = (
                    "Hello!, i'm here to help you to schedule an appintment, Here's how scheduling works:\n"
                    "1️⃣ Choose a department\n"
                    "2️⃣ Pick a doctor\n"
                    "3️⃣ Select a service\n"
                    "4️⃣ Choose a date\n"
                    "5️⃣ Pick an available time\n"
                    "➡️ Do you want to start with choosing the department?"
                )
                return ("Show the user this entire response: " + response), patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date
        elif intent == "confirmation":
            if context_stage == "start":
                Chat.set_context_stage(conversation_id, "choose_department")
                response = "show the user those departments:\n" + "\n".join(businesses_names) +  "\n and tell him to write the department that he needs"
                print("context stage : ",Chat.get_context_stage(conversation_id))
                return response, patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date
        if context_stage == "choose_department":
            selected_department = normalize_department_input(user_message)
            if not selected_department:
                # Try fuzzy match if not found directly
                for dept_name in bussiness_and_its_doctors.keys():
                    if contains_fuzzy_keyword(user_message, dept_name):
                        selected_department = dept_name
                        break
            print("selected_department ",selected_department)

            if selected_department: # selected_department need to check
                #Chat.set_context_stage(conversation_id, "choose_doctor")
                patient_business_id = name_to_id.get(selected_department)
                Chat.set_patient_business_id(conversation_id,str(patient_business_id))
                Chat.set_business_name(conversation_id, selected_department)
                Chat.set_context_stage(conversation_id, "choose_doctor")
                print("patient_business_id ", patient_business_id)
                doctors = bussiness_and_its_doctors.get(selected_department, [])
                if not doctors:
                    return f"Sorry, no availble doctors found in the selected department", str(patient_business_id), None, None, None
                doctor_names = "\n".join([doc["name"] for doc in doctors])
                print("doctor_names ", doctor_names)
                response = f"Here are the available doctors in {selected_department}:\n{doctor_names}\n➡️ Please choose a doctor by name. \n➡️ {add_Edit_choices('choose_department')}"
                return response, str(patient_business_id), None, None, None
            else:
                Chat.set_context_stage(conversation_id, "choose_department")
                return "Sorry, I didn't recognize that department. Please choose from the list shown again." +"\n".join(businesses_names), None, None, None, None
        doctors = bussiness_and_its_doctors.get((Chat.get_business_name(conversation_id)), [])
        if not doctors:
            Chat.set_context_stage(conversation_id, "choose_department")
            return f"Sorry, no available doctors found in the selected department"+ add_Edit_choices("choose_department"), str(patient_business_id), None, None, None
        doctor_names = "\n".join([doc["name"] for doc in doctors])
        doctor_names_only = [doc["name"] for doc in doctors if doc["name"]]

        if context_stage == "choose_doctor":
            selected_doctor = None
            normalized_message = user_message.strip().lower()

            for doc in doctor_names_only:
                doc_lower = doc.lower()
                if doc_lower in normalized_message:
                    print("doc ", doc)
                    print("doc_lower ", doc_lower)
                    print("normalized_message ", normalized_message)
                    print("ana hom")
                    selected_doctor = doc
                    break
                elif contains_fuzzy_keyword(normalized_message, doc_lower):
                    print("ana hon 2")
                    selected_doctor = doc
                    break

            print("selected_doctor ",selected_doctor)
            if selected_doctor:
                doctor_info = doctor_and_services[selected_doctor]
                resource_id = doctor_info["resource_id"]
                services = doctor_info["services"]

                # Update patient state
                Chat.set_context_stage(conversation_id, "choose_service")
                Chat.set_patient_resource_id(conversation_id, str(resource_id))
                Chat.set_resource_name(conversation_id, selected_doctor)

                if not services:
                    Chat.set_context_stage(conversation_id, "choose_doctor")
                    return f"Sorry, {selected_doctor} has no services available at the moment.", patient_business_id, str(resource_id), None, None
                print("services ",services)
                service_list = "\n".join([f"- {s['name']}" for s in services])
                print("service_list ",service_list)
                response = (
                    f"You selected Dr. {selected_doctor}.\n"
                    f"Here are the services available:\n{service_list}\n"
                    f"➡️ Please select a service by name.\n"
                    f"➡️ {add_Edit_choices('choose_doctor')}"
                )
                return response, patient_business_id, resource_id, None, None

            else:
                print("wooooooo")
                print(add_Edit_choices('choose_doctor'))
                print("wooooooo")
                edit_choices = add_Edit_choices('choose_doctor')
                Chat.set_context_stage(conversation_id, "choose_doctor")

                return (
                    f"Sorry, I couldn't match that doctor. Please choose a doctor from the list again.\n{doctor_names}\n{edit_choices}",
                    patient_business_id, None, None, None
                    )

        doctor_info = doctor_and_services[Chat.get_resource_name(conversation_id)]
        services = doctor_info["services"]
        if not services:
            Chat.set_context_stage(conversation_id, "choose_doctor")
            return f"Sorry, the doctor you selected has no available services at the moment." + add_Edit_choices("choose_doctor"), patient_business_id, patient_resource_id, None, None
        print("service_list ",services)
        if context_stage == "choose_service":
            selected_service = None
            selected_service_id = None
            normalized_message = user_message.strip().lower()

            for service in services:
                service_name = service["name"].lower()

                if service_name in normalized_message:
                    selected_service = service["name"]
                    selected_service_id = service["service_id"]
                    break
                elif contains_fuzzy_keyword(normalized_message, service_name):
                    selected_service = service["name"]
                    selected_service_id = service["service_id"]
                    break
            if selected_service:
                Chat.set_context_stage(conversation_id, "choose_date")
                Chat.set_patient_taxonomy_id(conversation_id, selected_service_id)
                Chat.set_taxonomy_name(conversation_id, selected_service)
                resource_id = Chat.get_patient_resource_id(conversation_id)
                taxonomy_id = selected_service_id
                fromDate = "2025-04-30T00:00:00.000Z"
                toDate = "2025-05-07T00:00:00.000Z"
                slots_data = get_available_slots(
                    business_id=patient_business_id,
                    resources_items=[{"id": patient_resource_id, "duration": 30}],
                    taxonomy_ids=[taxonomy_id],
                    from_date=fromDate,
                    to_date=toDate,
                )
                if not slots_data:
                    Chat.set_context_stage(conversation_id, "choose_service")
                    return f"Sorry, there are no available slots for the selected service in the next 10 days.\n please select the service again {services}" + add_Edit_choices("choose_service"), business_id, resource_id, None, None
                slot_lines = []
                for entry in slots_data:
                    date = entry["date"]
                    times = ", ".join(entry["slots"].get(resource_id, []))
                    if times:
                        slot_lines.append(f"{date}")
                response = f"You chose '{selected_service}'.\nHere are the available dates:\n" + "\n".join(slot_lines) + "\nplease select a date" + add_Edit_choices("choose_service")
                return response, business_id, resource_id, taxonomy_id, None


        fromDate = "2025-04-30T00:00:00.000Z"
        toDate = "2025-05-07T00:00:00.000Z"
        slots_data = get_available_slots(
            business_id=patient_business_id,
            resources_items=[{"id": patient_resource_id, "duration": 30}],
            taxonomy_ids=[patient_taxonomy_id],
            from_date=fromDate,
            to_date=toDate,
        )
        if not slots_data:
            Chat.set_context_stage(conversation_id, "choose_service")
            return f"Sorry, there are no available slots for the selected service in the next 10 days.\n please select the service again " + add_Edit_choices("choose_service"), business_id, resource_id, None, None
        slot_dates = []
        slot_lines = []
        for entry in slots_data:
            date = entry["date"]
            times = ", ".join(entry["slots"].get(patient_resource_id, []))
            if times:
                slot_dates.append(f"{date}")
                slot_lines.append(f"{date}: {times}")
        print("slot_lines ", slot_lines)
        if context_stage == "choose_date":
            extracted_date = extract_date_from_message(user_message)
            if extracted_date:
                print("User entered date:", extracted_date)
                available_dates = {}
                for line in slot_lines:
                    if ": " in line:
                        date_part, times_part = line.split(": ", 1)  # Split only on ': ' (colon followed by space)
                        available_dates[date_part.strip()] = times_part.strip()
                print("available_dates ", available_dates)
                # Check if the user's date is among the available dates
                if (extracted_date+"T00:00:00Z") in available_dates.keys():
                    print("✅ Valid date selected by user.")
                    print("extracted_date ", extracted_date)
                    patient_date = extracted_date
                    Chat.set_patient_date(conversation_id, patient_date)
                    available_times = available_dates[(extracted_date+"T00:00:00Z")]
                    Chat.set_context_stage(conversation_id, "choose_time")
                    edit_choices = add_Edit_choices('choose_date')
                    print("edit_choices ", edit_choices)
                    response = (
                            f"➡️ Please choose one of the available time slots.\n"
                            f"🗓️ Available times on {extracted_date}:\n{available_times}\n"
                            f"{edit_choices}"
                    )
                    return response, patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date
            else:
                Chat.set_context_stage(conversation_id, "choose_date")
                return (
                    f"❌ Couldn't recognize a valid available date in your message.\n"
                    f"📅 Please choose one of the following dates:\n{slot_dates}"
                    f"{add_Edit_choices('choose_date')}",
                    patient_business_id, patient_resource_id, patient_taxonomy_id, None
                )

        print("patient date ", patient_date)
        available_dates = {}
        for line in slot_lines:
            if ": " in line:
                date_part, times_part = line.split(": ", 1)  # Split only on ': ' (colon followed by space)
                available_dates[date_part.strip()] = times_part.strip()
        print("available_dates ", available_dates)
        if (patient_date+"T00:00:00Z") in available_dates.keys():
            print("✅ Valid date selected by user.")
            available_times = available_dates[(patient_date+"T00:00:00Z")]
            available_times_list = [time.strip() for time in available_times.split(",")]

        print("available_times ", available_times_list)
        if context_stage == "choose_time":
            selected_time = extract_time_from_message(user_message)
            if selected_time:
                print("User selected time:", selected_time)
                if selected_time and selected_time in available_times_list:
                    print("✅ Valid time selected by user: ", selected_time)
                    print("patient date: ", patient_date)
                    Chat.set_patient_time(conversation_id, selected_time)
                    edit_choices = add_Edit_choices('choose_time')
                    response =( f"To summurize your choices:\n1.Department name: {Chat.get_business_name(conversation_id)}"
                               f"\n2.Doctor name: {Chat.get_resource_name(conversation_id)}"
                               f"\n3.Service name: {Chat.get_taxonomy_name(conversation_id)}"
                               f"\n4.Date : {Chat.get_patient_date(conversation_id)}"
                               f"\n5. Hour : {Chat.get_patient_time(conversation_id)}"
                               f"\n{edit_choices}"
                    )
                    return response, patient_business_id, patient_resource_id, patient_taxonomy_id, Chat.get_patient_date(conversation_id)



            else:
                edit_choices = add_Edit_choices('choose_time')
                Chat.set_context_stage(conversation_id, "choose_time")
                return (
                    f"❌ Couldn't recognize a valid available time in your message.\n"
                    f"📅 Please choose one of the following dates:\n{available_times}"
                    f"\n{edit_choices}",
                    patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date
                )



        return user_message, patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date


def add_Edit_choices(edit):
    displays = []
    if edit in ["choose_department", "choose_doctor", "choose_service", "choose_date", "choose_time"]:
        displays.append("If you want to select a different department, please just type => change department")
    if edit in ["choose_doctor", "choose_service", "choose_date", "choose_time"]:
        displays.append("If you want to select a different doctor, please just type => change doctor")
    if edit in ["choose_service", "choose_date", "choose_time"]:
        displays.append("If you want to select a different service, please just type => change service")
    if edit in ["choose_date", "choose_time"]:
        displays.append("If you want to select a different date, please just type => change date")
    if edit in ["choose_time"]:
        displays.append("If you want to select a different hour, please just type => change hour")
    return "\n".join(displays)