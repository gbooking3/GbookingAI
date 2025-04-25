# server/app/services/chat_service.py
import difflib
from app.ai.init_ai import ask_gemini
from app.utils.gbooking_helpers import get_services, get_doctors, get_available_slots, reserve_appointment, \
    get_business_names, business_ids_from_network, get_business_doctors, get_doctor_services, \
    get_all_businesses_services
from app.models.chat import Chat

networkID = 456
businesses_ids = [4000000008541, 4000000008542, 4000000008543, 4000000008544]

english_to_hebrew = {
    "Cardiology": "קרדיולוגיה",
    "Gastroenterology": "גסטרואנטרולוגיה",
    "Neurology": "נוירולוגיה",
    "CT": "CT",  # if it's written the same
}
doctor_keywords = ["dr", "dr.", "doctor", "doctor.", "Dr", "Dr.", "Doctor", "Doctor.", "דר"]

business_services_4000000008541 = [{'id': '3090100', 'name': 'Наращивание ногтей на руках'},
                                   {'id': '3090000', 'name': 'Наращивание ногтей'},
                                   {'id': '9265719', 'name': 'מעקב רפואי לנבדק עם קוצב לב דפ'},
                                   {'id': '9265720', 'name': 'CONSULTATION CARDIOLOGY CLINIC'},
                                   {'id': '9265721', 'name': 'TTE, child'},
                                   {'id': '9265722', 'name': 'TTE  echocardiography'},
                                   {'id': '9265723', 'name': 'ERGOMETERY'},
                                   {'id': '9265724', 'name': 'Dobutamine stress echo'},
                                   {'id': '9267352', 'name': 'בדיקת הולטר לב'}, {'id': '9371271', 'name': 'א.ק.ג'},
                                   {'id': '9395698', 'name': 'אקוקרדיוגרפיה דרך הוושט, TEE'}]
business_services_4000000008542 = [{'id': '3090100', 'name': 'Наращивание ногтей на руках'},
                                   {'id': '3090000', 'name': 'Наращивание ногтей'},
                                   {'id': '9265739', 'name': 'GASTROSTOMYA PEG'}, {'id': '9265740', 'name': 'ERCP'},
                                   {'id': '9265741', 'name': 'כריתת פוליפ בשיטת EMR'},
                                   {'id': '9265742', 'name': 'אזופגוסקופיה עם הזרקת חומר חוס'},
                                   {'id': '9265743', 'name': 'Colonoscopy'}, {'id': '9265744', 'name': 'UGI endoscopy'},
                                   {'id': '9265745', 'name': 'מבחן רפלוקס בושט עם ניטור PH'},
                                   {'id': '9265746', 'name': 'Anorectal manometry'},
                                   {'id': '9265747', 'name': 'Esophageal motility'},
                                   {'id': '9267696', 'name': 'Endoscopy + Colonscopy'},
                                   {'id': '9268431', 'name': 'בדיקת רופא מרדים'},
                                   {'id': '9346291', 'name': 'רופא מרדים במכון גסטרו'},
                                   {'id': '9384398', 'name': '44360'}]
business_services_4000000008543 = [{'id': '3090100', 'name': 'Наращивание ногтей на руках'},
                                   {'id': '3090000', 'name': 'Наращивание ногтей'},
                                   {'id': '9265734', 'name': 'EMG, אלקטרומיוגרפיה ממוחשבת כמ'},
                                   {'id': '9266556', 'name': 'EEG בשינה'}, {'id': '9277998', 'name': 'EEG רגיל'},
                                   {'id': '9058391', 'name': '1'}]

businesses_id = business_ids_from_network(networkID)
businesses_names, businesses_names_ids = get_business_names(businesses_id)


def contains_fuzzy_keyword(message, target="services", threshold=0.8):
    words = message.lower().split()
    matches = difflib.get_close_matches(target, words, n=1, cutoff=threshold)
    return bool(matches)


def enrich_user_message(user_message, conversation_id):
    try:
        if contains_fuzzy_keyword(user_message, target="departments") or contains_fuzzy_keyword(user_message,
                                                                                                target="business"):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)

            businesses_id = business_ids_from_network(networkID)
            businesses_names, _ = get_business_names(businesses_id)
            print(f'{ businesses_names= }')
            businesses_names_str = ", ".join(businesses_names)
            return f"These are our departments in the hosptial: {businesses_names_str}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id

        if contains_fuzzy_keyword(user_message, target="Cardiology") or contains_fuzzy_keyword(user_message,
                                                                                               target="30040"):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)

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
            return f"These are our available doctors: {doctorsOfBusiness_str}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id

        if contains_fuzzy_keyword(user_message, target="Gastroenterology") or contains_fuzzy_keyword(user_message,
                                                                                                     target="31200"):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)

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
            return f"These are our available doctors: {doctorsOfBusiness_str}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id

        if contains_fuzzy_keyword(user_message, target="Neurology") or contains_fuzzy_keyword(user_message,
                                                                                              target="30300"):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)

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
            return f"These are our available doctors: {doctorsOfBusiness_str}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id

        if contains_fuzzy_keyword(user_message, target="CT") or contains_fuzzy_keyword(user_message, target="46350"):

            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)

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
            return f"These are our available doctors: {doctorsOfBusiness_str}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id

        if any(keyword in user_message for keyword in doctor_keywords):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)

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
            return f"This is the doctor you choose: {doctor_name}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id

        if contains_fuzzy_keyword(user_message, target="services"):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)

            print(user_message)

            print("patient_business_id ", patient_business_id)
            print("patient_reource_id ", patient_reource_id)
            dcotor_services = get_doctor_services(patient_business_id, patient_reource_id)
            print("dcotor_services ", dcotor_services)

            return f"These are our available dcotor_services: {dcotor_services}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id

        if any(service["name"] in user_message for service in business_services_4000000008542) or any(
                service["name"] in user_message for service in business_services_4000000008543) or any(
                service["name"] in user_message for service in business_services_4000000008541):
            print(user_message)
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)

            dcotor_services = get_doctor_services(patient_business_id, patient_reource_id)

            service_name = ""
            for service in dcotor_services:
                if service["name"] in user_message:
                    Chat.set_patient_taxonomy_id(conversation_id, service["id"])
                    service_name = service["name"]
                    break
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)
            print("The service that the paitent pick is: ", service_name, " and it's id is: ", patient_taxonomy_id)
            return f"This is the service you choose: {service_name}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id

        if any(service["name"] in user_message for service in get_services(4000000008544)):
            print(user_message)
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)

            dcotor_services = get_doctor_services(patient_business_id, patient_reource_id)

            print("business_id ", patient_business_id)
            service_name = ""
            for service in dcotor_services:
                if service["name"] in user_message:
                    Chat.set_patient_taxonomy_id(conversation_id, service["id"])
                    service_name = service["name"]
                    break
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)

            return f"This is the service you choose: {service_name}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id

        if contains_fuzzy_keyword(user_message, target="dates"):
            patient_business_id = Chat.get_patient_business_id(conversation_id)
            patient_reource_id = Chat.get_patient_resource_id(conversation_id)
            patient_taxonomy_id = Chat.get_patient_toxonomy_id(conversation_id)

            print("buss id ", patient_business_id)
            print("resource id ", patient_reource_id)
            print("tax id ", patient_taxonomy_id)



            dates = get_available_slots(
                business_id=str(patient_business_id),
                resources_items=[
                    {"id": patient_reource_id, "duration": 30}
                ],
                taxonomy_ids=[patient_taxonomy_id],
                from_date="2025-05-13T00:00:00.000Z",
                to_date="2025-06-01T00:00:00.000Z"
            )

            print(f'{ dates= }')

            return f"These are our available dates and hours each seperated by half hour: {dates}. {user_message}", patient_business_id, patient_reource_id, patient_taxonomy_id

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
            book = reserve_appointment(
                token="02ccadf0487e1e7ae27fea5048c3f53e7330fa45",
                user="67e16c86c43bdd3739a7b415",
                business_id="4000000008542",
                taxonomy_id="9346291",
                resource_id="66e6b669bbe2b5c4faf5bdd7",
                start_time="2025-05-15T08:20:00"
            )
            print(f'{ book= }')
            return f" {book}. {user_message}", ""


    except Exception as e:
        print("Error enriching message:", e)

    return user_message, ""


def process_user_message(user_id, user_name, user_message, conversation_id):
    enriched_message, client_business_id, client_resource_id, client_toxonomy_id = enrich_user_message(user_message,
                                                                                                       conversation_id)
    response = ask_gemini(enriched_message)

    saved_convo_id = Chat.start_or_update_conversation(
        ownid=user_id,
        user_name=user_name,
        user_msg=enriched_message,
        bot_msg=response,
        conversation_id=conversation_id,
        business_id=client_business_id,
        resource_id=client_resource_id,
        taxonomy_id=client_toxonomy_id
    )

    return {
        "message": response,
        "conversation_id": saved_convo_id,
    }
