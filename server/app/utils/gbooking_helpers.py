import requests
from datetime import datetime, timedelta

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

