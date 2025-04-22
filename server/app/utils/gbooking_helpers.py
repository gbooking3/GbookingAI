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

def get_available_slots(business_id, resource_id, taxonomy_ids, from_date, to_date):
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
                "resources": [
                    {"id": resource_id, "duration": 30}
                ],
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

    if response.status_code == 200:
        response_data = response.json()
        result = response_data.get("result", {})
        slots = result.get("slots", [])

        for day_slot in slots:
            date = day_slot['date']
            resources = day_slot.get("resources", [])

            if resources:
                resource_info = resources[0]
                resource_id = resource_info.get("resourceId")
                cut_slots = resource_info.get("cutSlots", [])

                print(f"\nDate: {date}")
                print(f"Resource ID: {resource_id}")

                if not cut_slots:
                    print("No available slots.")
                else:
                    for slot in cut_slots:
                        if slot.get("available"):
                            start_time = minutes_to_time(slot['start'])
                            end_time = minutes_to_time(slot['end'])
                            print(f"Available from {start_time} to {end_time}")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)

# Example usage:
get_available_slots(
    business_id="4000000008542",
    resource_id="66e6b856b57b88c54a2ab1b9",
    taxonomy_ids=["9175163"],
    from_date="2025-05-13T00:00:00.000Z",
    to_date="2025-05-16T00:00:00.000Z"
)
