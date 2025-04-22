import requests
from datetime import datetime, timedelta
import json
GBOOKING_API_URL = "https://apiv2.gbooking.ru/rpc"

GBOOKING_CRED = {
    "token": "8e7d61be4f200e39ea29b1231006a248de108d9a",
    "user": "5b1035dcaff15607133b523f"
}

BUSINESS_ID = "4000000008542"
HEADERS = {"Content-Type": "application/json"}

def call_gbooking_api(method, params=None):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": GBOOKING_CRED,
        "method": method,
        "params": params or {}
    }

    try:
        response = requests.post(GBOOKING_API_URL,headers = HEADERS ,json=payload)
        response.raise_for_status()
        return response.json().get("result")
    except requests.RequestException as e:
        print(f"[GBooking API Error] {method}: {e}")
        return None


def get_services():
    result = call_gbooking_api("business.get_profile_by_id", {
        "business": {"id": BUSINESS_ID},
        "with_networks": True
    })
    if not result:
        return []

    services = result.get("business", {}).get("taxonomies", [])
   
    return [s.get("alias", {}).get("ru-ru", "Unnamed") for s in services]

def replace_doctor_ids_with_names(structured_data, doctors):
    # Create a map from id to name
    id_to_name = {doc['id']: doc['name'] for doc in doctors}

    # Replace each doctor_id in structured_data with the name
    updated_data = []
    for date_entry in structured_data:
        date = date_entry[0]
        updated_entry = [date]
        for doctor_info in date_entry[1:]:
            doctor_id = doctor_info[0]
            time_slots = doctor_info[1]
            doctor_name = id_to_name.get(doctor_id, doctor_id)  # fallback to ID if name not found
            updated_entry.append([doctor_name, time_slots])
        updated_data.append(updated_entry)

    return updated_data


def get_doctors():
    result = call_gbooking_api("business.get_profile_by_id", {
        "business": {"id": BUSINESS_ID},
        "with_networks": True
    })
    if not result:
        return []

    doctors = []
    
    for worker in result.get("business", {}).get("resources", []):
        if worker.get("status") == "ACTIVE" and worker.get("displayInWidget", False):
            doctors.append({
                "name": worker.get("name", "Unnamed"),
                "profession": worker.get("profession", "Doctor"),
                "id": worker.get("id", "Doctor")
            })
    print(doctors)
    return doctors


def minutes_to_time(minutes):
    """Convert minutes to HH:MM format."""
    time = timedelta(minutes=minutes)
    return str(time)

def get_available_slots(business_id, resources_items, taxonomy_ids, from_date, to_date):
    url = "https://cracslots.gbooking.ru/rpc"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {},  # Add credentials here if required
        "method": "CracSlots.GetCRACResourcesAndRooms",
        "params": {
            "business": {
                "id": business_id,
                "widget_configuration": {
                    "cracServer": "CRAC_PROD3",
                    "mostFreeEnable": True
                },
                "general_info": {
                    "timezone": "Europe/Moscow"
                }
            },
            "filters": {
                "resources": resources_items,
                "taxonomies": taxonomy_ids,
                "rooms": [],
                "date": {
                    "from": from_date,
                    "to": to_date
                }
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    structured_data = []
    result = response_data.get("result", {})
    slots = result.get("slots", [])

    for day_slot in slots:
        date = day_slot['date']
        doctor_slots_map = {}

        for resource in day_slot.get("resources", []):
            resource_id = resource.get("resourceId")
            for slot in resource.get("cutSlots", []):
                if slot.get("available"):
                    start = minutes_to_time(slot['start'])
                    end = minutes_to_time(slot['end'])
                    doctor_slots_map.setdefault(resource_id, []).append([start, end])

        if doctor_slots_map:
            day_entry = [date]
            for doctor_id, time_ranges in doctor_slots_map.items():
                day_entry.append([doctor_id, time_ranges])
            structured_data.append(day_entry)

    doctors = get_doctors()
    readable_data = replace_doctor_ids_with_names(structured_data, doctors)
    print(json.dumps(readable_data, indent=2, ensure_ascii=False))  # Nice readable output
    return readable_data


# Example usage
get_available_slots(
    business_id=BUSINESS_ID,
    resources_items=[
        {"id": "66e6b856b57b88c54a2ab1b9", "duration": 30},
        {"id": "66e6b669bbe2b5c4faf5bdd7", "duration": 30}
    ],
    taxonomy_ids=["9175163"],
    from_date="2025-05-13T00:00:00.000Z",
    to_date="2025-05-16T00:00:00.000Z"
)