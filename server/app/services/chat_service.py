# server/app/services/chat_service.py
import difflib
from app.ai.init_ai import ask_gemini
from app.utils.gbooking_helpers import get_services, get_doctors, get_available_slots, reserve_appointment, \
    get_business_names, business_ids_from_network, get_business_doctors, get_doctor_services, \
    get_all_businesses_services
from app.models.chat import Chat
import re
from datetime import datetime, timedelta
import string

networkID = 456

english_to_hebrew = {
    "Cardiology": "קרדיולוגיה",
    "Gastroenterology": "גסטרואנטרולוגיה",
    "Neurology": "נוירולוגיה",
    "CT": "CT",
}
doctor_keywords = ["dr", "dr.", "doctor", "doctor.", "Dr", "Dr.", "Doctor", "Doctor.", "דר"]

service_lists = [
    get_services(4000000008541),
    get_services(4000000008542),
    get_services(4000000008543),
    get_services(4000000008544),
]

businesses_id = business_ids_from_network(networkID)
businesses_names, businesses_names_ids = get_business_names(businesses_id)

def contains_fuzzy_keyword(message, target="services", threshold=0.8):
    translator = str.maketrans('', '', string.punctuation)
    message = message.translate(translator)
    words = message.lower().split()
    matches = difflib.get_close_matches(target, words, n=1, cutoff=threshold)
    return bool(matches)

def fetch_patient_info(conversation_id):
    return (
        Chat.get_patient_business_id(conversation_id),
        Chat.get_patient_resource_id(conversation_id),
        Chat.get_patient_toxonomy_id(conversation_id),
        Chat.get_patient_date(conversation_id)
    )

def find_department_business(english_name):
    hebrew_department = english_to_hebrew.get(english_name)
    for dept_id, label in businesses_names_ids:
        if hebrew_department in label:
            return dept_id, label
    return None, None

def get_doctors_message(business_id, user_message):
    doctors = get_business_doctors(business_id)
    doctors_str = ", ".join([f"Dr. {doc['name']}" for doc in doctors])
    return f"These are our available doctors: {doctors_str}. {user_message}, choose a doctor of these doctors please"

def enrich_user_message(user_message, conversation_id):
    try:
        if contains_fuzzy_keyword(user_message, target="departments") or contains_fuzzy_keyword(user_message, target="business"):
            patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date = fetch_patient_info(conversation_id)
            businesses_id = business_ids_from_network(networkID)
            businesses_names, _ = get_business_names(businesses_id)
            businesses_names_str = ", ".join(businesses_names)
            return (f"These are our departments in the hospital: {businesses_names_str}. {user_message}, "
                    "if you would like to see the doctors of a specific department, write the name of the department"), \
                   patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date

        department_keywords = {
            "Cardiology": ["Cardiology", "30040"],
            "Gastroenterology": ["Gastroenterology", "31200"],
            "Neurology": ["Neurology", "30300"],
            "CT": ["CT", "46350"]
        }

        for department, keywords in department_keywords.items():    ## display doctors
            if any(contains_fuzzy_keyword(user_message, target=kw) for kw in keywords):
                patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date = fetch_patient_info(conversation_id)
                matching_id, business_name = find_department_business(department)
                if matching_id:
                    Chat.set_patient_business_id(conversation_id, matching_id)
                    Chat.set_business_name(conversation_id, business_name)
                    message = get_doctors_message(matching_id, user_message)
                    return message, matching_id, patient_resource_id, patient_taxonomy_id, patient_date

        if any(keyword in user_message for keyword in doctor_keywords):     # writing the doctor to get it's id
                patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date = fetch_patient_info(conversation_id)
                doctors_of_business = get_business_doctors(patient_business_id)
                doctor_name = ""

                for doctor in doctors_of_business:
                    doctor_real_name = clean_name(doctor["name"])
                    doctor_name_words = doctor_real_name.split()

                    if any(word in user_message for word in doctor_name_words):
                        matched_doctor_id = doctor["id"]
                        doctor_name = doctor["name"]
                        Chat.set_patient_resource_id(conversation_id, matched_doctor_id)
                        Chat.set_resource_name(conversation_id, doctor_name)
                        break

                patient_resource_id = Chat.get_patient_resource_id(conversation_id)

                return (
                    f"This is the doctor you chose: {doctor_name}. {user_message}, would you like to know what are the services of this doctor?",
                    patient_business_id,
                    patient_resource_id,
                    patient_taxonomy_id,
                    patient_date,
                )

        if contains_fuzzy_keyword(user_message, target="services"):     #displaying the services of the doctor
            patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date = fetch_patient_info(conversation_id)
            doctor_services = get_doctor_services(patient_business_id, patient_resource_id)

            return (
                f"These are our available doctor services: {doctor_services}. {user_message}, type the name of the service you want, please.",
                patient_business_id,
                patient_resource_id,
                patient_taxonomy_id,
                patient_date,
            )

        extracted_time = extract_time_from_message(user_message)    #Time
        if extracted_time:
            patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date = fetch_patient_info(conversation_id)
            cleaned_date = patient_date.split('T')[0]
            Chat.set_patient_date(conversation_id, cleaned_date)
            Chat.set_patient_time(conversation_id, extracted_time)

            business_name = Chat.get_business_name(conversation_id)
            doctor_name = Chat.get_resource_name(conversation_id)
            service_name = Chat.get_taxonomy_name(conversation_id)
            patient_date = Chat.get_patient_date(conversation_id)
            return (
                f"To confirm your appointment, you selected:\n"
                f"Department: {business_name}\n"
                f"Doctor: {doctor_name}\n"
                f"Service: {service_name}\n"
                f"Date and Time: {patient_date} {extracted_time}\n"
                f"Please review and type 'book' or 'yes, appoint me' to confirm.\n"
                f"{user_message}",
                patient_business_id,
                patient_resource_id,
                patient_taxonomy_id,
                patient_date,
            )

        extracted_date = extract_date_from_message(user_message)    #DATE
        if extracted_date:
            patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date = fetch_patient_info(conversation_id)
            Chat.set_patient_date(conversation_id, extracted_date)

            fromDate = extracted_date + "T00:00:00.000Z"
            toDate = add_one_day(extracted_date) + "T00:00:00.000Z"

            available_slots = get_available_slots(
                business_id=str(patient_business_id),
                resources_items=[{"id": patient_resource_id, "duration": 30}],
                taxonomy_ids=[patient_taxonomy_id],
                from_date=fromDate,
                to_date=toDate,
            )

            dates = []
            hours = {}

            for day in available_slots:
                date = day.get("date")
                resource_slots = day.get("slots", {})
                all_hours = [time for times in resource_slots.values() for time in times]

                if date and all_hours:
                    dates.append(date)
                    hours[date] = all_hours

            return (
                f"The date you chose is {extracted_date} and the available hours are {hours}. {user_message}, to complete the reservation, please enter the hour you want.",
                patient_business_id,
                patient_resource_id,
                patient_taxonomy_id,
                extracted_date,
            )

        # Handle selecting a service from service lists


        if any(service["name"] in user_message for services in service_lists for service in services):      #get the service id
            patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date = fetch_patient_info(conversation_id)
            doctor_services = get_doctor_services(patient_business_id, patient_resource_id)

            service_name = ""
            for service in doctor_services:
                if service["name"] in user_message:
                    Chat.set_patient_taxonomy_id(conversation_id, service["id"])
                    Chat.set_taxonomy_name(conversation_id, service["name"])
                    service_name = service["name"]
                    break

            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)

            return (
                f"This is the service you chose: {service_name}. {user_message}, if you would like to see the available dates, just write 'what are the available dates?'",
                patient_business_id,
                patient_resource_id,
                patient_taxonomy_id,
                patient_date,
            )

        if contains_fuzzy_keyword(user_message, target="dates"):    #get the dates
            patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date = fetch_patient_info(conversation_id)
            dates = get_available_slots(
                business_id=str(patient_business_id),
                resources_items=[{"id": patient_resource_id, "duration": 30}],
                taxonomy_ids=[patient_taxonomy_id],
                from_date="2025-04-30T00:00:00.000Z",
                to_date="2025-05-20T00:00:00.000Z",
            )

            return (
                f"These are our available dates and hours, each separated by half an hour: {dates}. {user_message}, to complete the reservation, please first enter the date you want.",
                patient_business_id,
                patient_resource_id,
                patient_taxonomy_id,
                patient_date,
            )

        if contains_fuzzy_keyword(user_message, target="book"):     #Book
            patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date = fetch_patient_info(conversation_id)
            booking = reserve_appointment(
                token="02ccadf0487e1e7ae27fea5048c3f53e7330fa45",
                user="67e16c86c43bdd3739a7b415",
                business_id=patient_business_id,
                taxonomy_id=patient_taxonomy_id,
                resource_id=patient_resource_id,
                start_time=patient_date,
            )

            return f"{booking}. {user_message}", patient_business_id, patient_resource_id, patient_taxonomy_id, patient_date

    except Exception as e:
        print("Error enriching message:", e)

    return user_message, ""

def clean_name(name):
    return name.replace("דר ", "").replace("Dr. ", "").strip()

def extract_date_from_message(message):
    # Try to match standard YYYY-MM-DD format first
    iso_date_pattern = r'\d{4}-\d{2}-\d{2}'
    iso_match = re.search(iso_date_pattern, message)
    if iso_match:
        return iso_match.group()

    # Try to match natural language date formats like "May 1st, 2025"
    # This regex captures Month Day, Year
    natural_date_pattern = r'([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})'
    natural_match = re.search(natural_date_pattern, message)
    if natural_match:
        month_str, day, year = natural_match.groups()

        try:
            date_obj = datetime.strptime(f"{month_str} {day} {year}", "%B %d %Y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            pass

    return None

def add_one_day(date_str):
    # Parse the input date string (in format YYYY-MM-DD)
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    # Add one day
    next_day = date_obj + timedelta(days=1)
    # Return the new date as a string in "YYYY-MM-DD" format
    return next_day.strftime("%Y-%m-%d")

def extract_time_from_message(message):
    # Regular expression to match times like 08:00, 08:30, 09:00, etc.
    time_pattern = r'\b([01]?[0-9]|2[0-3]):([0-5][0-9])\b'
    match = re.search(time_pattern, message)
    if match:
        return match.group()
    return None

def process_user_message(user_id, user_name, user_message, conversation_id):
    enriched_message, client_business_id, client_resource_id, client_toxonomy_id, client_date = enrich_user_message(user_message,conversation_id)
    response = ask_gemini(enriched_message)
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
        date = client_date
    )
    return {
        "message": response,
        "conversation_id": saved_convo_id,
    }