# server/app/services/chat_service.py
import difflib
from app.ai.init_ai import ask_gemini
from app.utils.gbooking_helpers import get_services, get_doctors, get_available_slots, reserve_appointment, \
    get_business_names, business_ids_from_network, get_business_doctors, get_doctor_services, \
    get_all_businesses_services
from app.models.chat import Chat
import re
from datetime import datetime, timedelta


networkID = 456
businesses_ids = [4000000008541, 4000000008542, 4000000008543, 4000000008544]

english_to_hebrew = {
    "Cardiology": "קרדיולוגיה",
    "Gastroenterology": "גסטרואנטרולוגיה",
    "Neurology": "נוירולוגיה",
    "CT": "CT",  # if it's written the same
}
doctor_keywords = ["dr", "dr.", "doctor", "doctor.", "Dr", "Dr.", "Doctor", "Doctor.", "דר"]

business_services_4000000008541 = get_services("4000000008541")
business_services_4000000008542 = get_services("4000000008542")
business_services_4000000008543 =   get_services("4000000008543")


businesses_id = business_ids_from_network(networkID)
businesses_names, businesses_names_ids = get_business_names(businesses_id)


def contains_fuzzy_keyword(message, target="services", threshold=0.8):
    words = message.lower().split()
    matches = difflib.get_close_matches(target, words, n=1, cutoff=threshold)
    return bool(matches)


def enrich_user_message(user_message, conversation_id):
    try:
        if contains_fuzzy_keyword(user_message, target="Departments") or contains_fuzzy_keyword(user_message,
                                                                                                target="business"):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            patient_date = Chat.get_patient_date(conversation_id)

            businesses_id = business_ids_from_network(networkID)
            businesses_names, _ = get_business_names(businesses_id)
            print(f'{ businesses_names= }')
            businesses_names_str = ", ".join(businesses_names)
            return f"These are our departments in the hosptial: {businesses_names_str}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id, patient_date

        if contains_fuzzy_keyword(user_message, target="Cardiology ") or contains_fuzzy_keyword(user_message,
                                                                                               target="30040"):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            patient_date = Chat.get_patient_date(conversation_id)


            hebrew_department = english_to_hebrew.get("Cardiology")
            matching_id = None
            business_name = ""
            for dept_id, label in businesses_names_ids:
                if hebrew_department in label:
                    matching_id = dept_id
                    business_name = label
                    Chat.set_patient_business_id(conversation_id, dept_id)
                    break
            patient_business_id = Chat.get_patient_business_id(conversation_id)

            doctorsOfBusiness = get_business_doctors(matching_id)
            print("The doctors of the  ", business_name, " with the id ", matching_id, " are:")
            print(f'{ doctorsOfBusiness= }')
            doctorsOfBusiness_str = ", ".join([f"Dr. {doc['name']}" for doc in doctorsOfBusiness])
            return f"These are our available doctors: {doctorsOfBusiness_str}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id, patient_date

        if contains_fuzzy_keyword(user_message, target="Gastroenterology ") or contains_fuzzy_keyword(user_message,
                                                                                                     target="31200"):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            patient_date = Chat.get_patient_date(conversation_id)


            hebrew_department = english_to_hebrew.get("Gastroenterology")
            matching_id = None
            business_name = ""
            for dept_id, label in businesses_names_ids:
                if hebrew_department in label:
                    matching_id = dept_id
                    business_name = label
                    Chat.set_patient_business_id(conversation_id, dept_id)
                    break
            patient_business_id = Chat.get_patient_business_id(conversation_id)

            doctorsOfBusiness = get_business_doctors(matching_id)
            print("The doctors of the  ", business_name, " with the id ", matching_id, " are:")
            print(f'{ doctorsOfBusiness= }')
            doctorsOfBusiness_str = ", ".join([f"Dr. {doc['name']}" for doc in doctorsOfBusiness])
            print("kkkkkkkkkkkkkkkkkkkkkkkkpatient_business_id_curr ", patient_business_id)
            return f"These are our available doctors: {doctorsOfBusiness_str}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id, patient_date

        if contains_fuzzy_keyword(user_message, target="Neurology ") or contains_fuzzy_keyword(user_message,
                                                                                              target="30300"):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            patient_date = Chat.get_patient_date(conversation_id)


            hebrew_department = english_to_hebrew.get("Neurology")
            matching_id = None
            business_name = ""
            for dept_id, label in businesses_names_ids:
                if hebrew_department in label:
                    matching_id = dept_id
                    business_name = label
                    Chat.set_patient_business_id(conversation_id, dept_id)
                    break
            patient_business_id = Chat.get_patient_business_id(conversation_id)

            doctorsOfBusiness = get_business_doctors(matching_id)
            print("The doctors of the  ", business_name, " with the id ", matching_id, " are:")
            print(f'{ doctorsOfBusiness= }')
            doctorsOfBusiness_str = ", ".join([f"Dr. {doc['name']}" for doc in doctorsOfBusiness])
            return f"These are our available doctors: {doctorsOfBusiness_str}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id, patient_date

        if contains_fuzzy_keyword(user_message, target="CT") or contains_fuzzy_keyword(user_message, target="46350"):

            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            patient_date = Chat.get_patient_date(conversation_id)


            hebrew_department = english_to_hebrew.get("CT")
            matching_id = None
            business_name = ""
            for dept_id, label in businesses_names_ids:
                if hebrew_department in label:
                    matching_id = dept_id
                    business_name = label
                    Chat.set_patient_business_id(conversation_id, dept_id)
                    break
            patient_business_id = Chat.get_patient_business_id(conversation_id)

            doctorsOfBusiness = get_business_doctors(matching_id)
            print("The doctors of the  ", business_name, " with the id ", matching_id, " are:")
            print(f'{ doctorsOfBusiness= }')
            doctorsOfBusiness_str = ", ".join([f"Dr. {doc['name']}" for doc in doctorsOfBusiness])
            return f"These are our available doctors: {doctorsOfBusiness_str}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id, patient_date

        if any(keyword in user_message for keyword in doctor_keywords):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            patient_date = Chat.get_patient_date(conversation_id)


            print(user_message)
            print("business_id ", patient_business_id)
            doctorsOfBusiness = get_business_doctors(patient_business_id)
            print(doctorsOfBusiness)
            doctor_name = ""
            for doctor in doctorsOfBusiness:
                if doctor["name"] in user_message:
                    matched_doctor_id = doctor["id"]
                    doctor_name = doctor["name"]
                    Chat.set_patient_resource_id(conversation_id, matched_doctor_id)
                    break
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            print("matched_doctor_id ", patient_reource_id, "matched_doctor_name ", doctor_name)
            return f"This is the doctor you choose: {doctor_name}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id, patient_date

        if contains_fuzzy_keyword(user_message, target="services"):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            patient_date = Chat.get_patient_date(conversation_id)


            print(user_message)

            print("patient_business_id ", patient_business_id)
            print("patient_reource_id ", patient_reource_id)
            dcotor_services = get_doctor_services(patient_business_id, patient_reource_id)
            print("dcotor_services ", dcotor_services)

            return f"These are our available dcotor_services: {dcotor_services}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id, patient_date
        
        
        extracted_time = extract_time_from_message(user_message)
        print("extracted_time ", extracted_time)
        if extracted_time:
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            patient_date = Chat.get_patient_date(conversation_id)

            cleaned_date = patient_date.split('T')[0]
            Chat.set_patient_date(conversation_id, cleaned_date)
            Chat.set_patient_time(conversation_id, extracted_time)
            hebrew_business_name = "Name not found"
            for business_id, name in businesses_names_ids:
                if business_id == patient_business_id:
                    # Extract the name part after the number (if any)
                    hebrew_business_name = name
                    break
            hebrew_name = hebrew_business_name.split(" - ")[1]
            business_name = next((key for key, value in english_to_hebrew.items() if value == hebrew_name), "Business Name not found")
            doctorsOfBusiness = get_business_doctors(patient_business_id)
            doctor_name = next((doctor['name'] for doctor in doctorsOfBusiness if doctor['id'] == patient_reource_id), "Doctor not found")
            dcotor_services = get_doctor_services(patient_business_id, patient_reource_id)
            service_name = next((service['name'] for service in dcotor_services if service['id'] == patient_taxonomy_id), "Service not found")
            patient_date = Chat.get_patient_date(conversation_id)

            return (
                f"To confirm your appointment, you have selected the following:\n"
                f"Department: {business_name}\n"
                f"Doctor: {doctor_name}\n"
                f"Service: {service_name}\n"
                f"Date and Time: {patient_date} {extracted_time}\n"
                f"Please review the details and let me know if everything looks correct.\n"
                f"If this is correct, type 'book' or 'yes, appoint me' to confirm your appointment.\n"
                f"{user_message}"
            ), patient_business_id, patient_reource_id, patient_taxonomy_id, patient_date








        print("user_message ", user_message)
        print("extract_date_from_message(user_message) ", extract_date_from_message(user_message))
        if extract_date_from_message(user_message):
            print("hii")
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            patient_date = Chat.get_patient_date(conversation_id)
            extracted_date = extract_date_from_message(user_message)
            if extracted_date:
                Chat.set_patient_date(conversation_id, extracted_date)
            
            fromDate = extracted_date + "T00:00:00.000Z"
            toDate = add_one_day(extracted_date) + "T00:00:00.000Z"


            available_slots = get_available_slots(
                business_id=str(patient_business_id),
                resources_items=[
                    {"id": patient_reource_id, "duration": 30}
                ],
                taxonomy_ids=[patient_taxonomy_id],
                from_date = fromDate,
                to_date = toDate
            )
            dates = []
            hours = {}

            for day in available_slots:
                date = day.get("date")
                resource_slots = day.get("slots", {})

                all_hours = []
                for resource_id, times in resource_slots.items():
                    all_hours.extend(times)

                if date and all_hours:
                    dates.append(date)
                    hours[date] = all_hours

            print("Dates:", dates)
            print("Hours:", hours)
            
            return f"The date you choose is {extracted_date} and the available hours are {hours}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id, extracted_date

        if any(service["name"] in user_message for service in business_services_4000000008542) or any(
                service["name"] in user_message for service in business_services_4000000008543) or any(
                service["name"] in user_message for service in business_services_4000000008541):
            print(user_message)
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            patient_date = Chat.get_patient_date(conversation_id)


            dcotor_services = get_doctor_services(patient_business_id, patient_reource_id)

            service_name = ""
            for service in dcotor_services:
                if service["name"] in user_message:
                    Chat.set_patient_taxonomy_id(conversation_id, service["id"])
                    service_name = service["name"]
                    break
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            print("The service that the paitent picked is: ", service_name, " and it's id is: ", patient_taxonomy_id)
            return f"This is the service you choose: {service_name}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id, patient_date

        if any(service["name"] in user_message for service in get_services(4000000008544)):
            print(user_message)
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            patient_date = Chat.get_patient_date(conversation_id)


            dcotor_services = get_doctor_services(patient_business_id, patient_reource_id)

            print("business_id ", patient_business_id)
            service_name = ""
            for service in dcotor_services:
                if service["name"] in user_message:
                    Chat.set_patient_taxonomy_id(conversation_id, service["id"])
                    service_name = service["name"]
                    break
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)

            return f"This is the service you choose: {service_name}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id ,patient_date

        if contains_fuzzy_keyword(user_message, target="dates"):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            patient_date = Chat.get_patient_date(conversation_id)


            print("buss id ", patient_business_id)
            print("resource id ", patient_reource_id)
            print("tax id ", patient_taxonomy_id)



            dates = get_available_slots(
                business_id=str(patient_business_id),
                resources_items=[
                    {"id": patient_reource_id, "duration": 30}
                ],
                taxonomy_ids=[patient_taxonomy_id],
                from_date="2025-04-30T00:00:00.000Z",
                to_date="2025-05-20T00:00:00.000Z"
            )

            print(f'{ dates= }')

            return f"These are our available dates and hours each seperated by half hour: {dates}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id, patient_date
        print("user_message ", user_message)
        print("extract_date_from_message(user_message) ", extract_date_from_message(user_message))

    # 2. Match departments/businesses
        
        
        # elif contains_fuzzy_keyword(user_message, target="services"):
        #    services_list = get_services()
        #    print(f'{ services_list= }')
        #    services_str = ", ".join(services_list)
        #    return f"We offer the following services: {services_str}. {user_message}", ""

        # elif contains_fuzzy_keyword(user_message, target="doctors"):
        #    doctors = get_doctors()
        #    print(f'{ doctors= }')
        #    doctor_str = ", ".join([f"Dr. {doc['name']} ({doc['taxonomies']})" for doc in doctors])
        #    return f"These are our available doctors: {doctor_str}. {user_message}", ""

        # elif contains_fuzzy_keyword(user_message, target="dates") or contains_fuzzy_keyword(user_message, target="hours"):
        #    dates = get_available_slots(
        #    business_id="4000000008542",
        #    resources_items=[
        #        {"id": "67e16c86c43bdd3739a7b415", "duration": 30},
        #        {"id": "66e6b669bbe2b5c4faf5bdd7", "duration": 30}
        #    ],
        #    taxonomy_ids=["9268431"],
        #    from_date="2025-05-13T00:00:00.000Z",
        #    to_date="2025-05-16T00:00:00.000Z"
        #    )
        #    print(f'{ dates= }')
        #    return f"These are our available dates: {dates}. {user_message}", ""

        if contains_fuzzy_keyword(user_message, target="book"):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            patient_date = Chat.get_patient_date(conversation_id)
            print("buss id ", patient_business_id)
            print("resource id ", patient_reource_id)
            print("tax id ", patient_taxonomy_id)
            print("date :" ,patient_date)
            book = reserve_appointment(
                token="02ccadf0487e1e7ae27fea5048c3f53e7330fa45",
                user="67e16c86c43bdd3739a7b415",
                business_id=patient_business_id,
                taxonomy_id=patient_taxonomy_id,
                resource_id=patient_reource_id,
                start_time=patient_date
            )
            print(f'{ book= }')
            return f" {book}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id, patient_date


    except Exception as e:
        print("Error enriching message:", e)

    return user_message, ""


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
            # Parse the month name to month number
            date_obj = datetime.strptime(f"{month_str} {day} {year}", "%B %d %Y")
            # Return it as 'YYYY-MM-DD' format
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            pass  # If parsing fails, ignore and continue

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



