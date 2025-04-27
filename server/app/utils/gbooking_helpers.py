import requests
from datetime import datetime, timedelta
import json

GBOOKING_API_URL = "https://apiv2.gbooking.ru/rpc"

GBOOKING_CRED = {
    "token": "02ccadf0487e1e7ae27fea5048c3f53e7330fa45",
    "user": "67e16c86c43bdd3739a7b415"
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
        response = requests.post(GBOOKING_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json().get("result")
    except requests.RequestException as e:
        print(f"[GBooking API Error] {method}: {e}")
        return None


def get_all_businesses_services(business_ids):
    all_services = []

    for business_id in business_ids:
        result = call_gbooking_api("business.get_profile_by_id", {
            "business": {"id": business_id},
            "with_networks": True
        })

        if not result:
            continue

        services = result.get("business", {}).get("taxonomies", [])

        for service in services:
            service_id = service.get("id")
            service_name = service.get("alias", {}).get("ru-ru", "Unnamed")
            all_services.append({
                "id": service_id,
                "name": service_name
            })

    return all_services


def get_services(business_id):
    result = call_gbooking_api("business.get_profile_by_id", {
        "business": {"id": business_id},
        "with_networks": True
    })
    if not result:
        return []

    services = result.get("business", {}).get("taxonomies", [])

    return [
        {
            "id": service.get("id"),
            "name": service.get("alias", {}).get("ru-ru", "Unnamed")
        }
        for service in services
    ]


def get_doctor_services(business_id, resource_id):
    response = call_gbooking_api("business.get_profile_by_id", {
        "business": {"id": business_id},
        "with_networks": True
    })

    if not response:
        return []

    business = response.get("business", {})
    resources = business.get("resources", [])
    taxonomies = business.get("taxonomies", [])

    # Find the doctor with matching resource_id
    doctor = next((r for r in resources if r.get("id") == resource_id), None)
    if not doctor:
        return []

    doctor_taxonomy_ids = doctor.get("taxonomies", [])

    # Filter and format only the taxonomies this doctor provides
    doctor_services = [
        {
            "id": t.get("id"),
            "name": t.get("alias", {}).get("ru-ru", "Unnamed")
        }
        for t in taxonomies
        if t.get("id") in doctor_taxonomy_ids
    ]

    return doctor_services


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
                "name": worker.get("nickname", "Unnamed"),
                "taxonomies": worker.get("taxonomies", "Doctor"),
                "id": worker.get("id", "Doctor")
            })
    print(doctors)
    return doctors


def get_business_doctors(business_id):
    result = call_gbooking_api("business.get_profile_by_id", {
        "business": {"id": business_id},
        "with_networks": True
    })
    if not result:
        return []

    doctors = []

    for worker in result.get("business", {}).get("resources", []):
        if worker.get("status") == "ACTIVE" and worker.get("displayInWidget", False):
            doctors.append({
                "name": worker.get("nickname", "Unnamed"),
                "taxonomies": worker.get("taxonomies", "Doctor"),
                "id": worker.get("id", "Doctor")
            })
    print(doctors)
    return doctors


def minutes_to_time(minutes):
    """Convert minutes to HH:MM format."""
    time = timedelta(minutes=minutes)
    return str(time)


import requests
import json
from datetime import datetime, timedelta


def minutes_to_time(minutes):
    """Helper function to convert minutes since midnight to HH:MM format."""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def get_available_slots(business_id, resources_items, taxonomy_ids, from_date, to_date):
    url = "https://cracslots.gbooking.ru/rpc"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {},  # Add credentials here if needed
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

    result = response_data.get("result", {})
    slots = result.get("slots", [])

    structured_data = []

    for day_slot in slots:
        date = day_slot.get("date")
        doctor_slots_map = {}

        for resource in day_slot.get("resources", []):
            resource_id = resource.get("resourceId")
            for slot in resource.get("cutSlots", []):
                if slot.get("available"):
                    start_time = minutes_to_time(slot["start"])
                    doctor_slots_map.setdefault(resource_id, []).append(start_time)

        if doctor_slots_map:
            structured_data.append({
                "date": date,
                "slots": doctor_slots_map
            })

    return structured_data


def reserve_appointment(
        token,
        user,
        business_id,
        taxonomy_id,
        resource_id,
        start_time,
        duration=30,
        source="web",
        price_amount=0,
        currency="RUB"
):
    url = "https://apiv2.gbooking.ru/rpc"

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": token,
            "user": user
        },
        "method": "appointment.reserve_appointment",
        "params": {
            "appointment": {
                "start": start_time,
                "duration": duration,
                "price": {
                    "amount": price_amount,
                    "currency": currency
                }
            },
            "source": source,
            "business": {
                "id": business_id
            },
            "taxonomy": {
                "id": taxonomy_id
            },
            "client_appear": "NONE",
            "resource": {
                "id": resource_id
            }
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    try:
        res_json = response.json()
        if "result" in res_json:
            appointment_info = res_json["result"]
            start = appointment_info["appointment"]["start"]
            dur = appointment_info["appointment"]["duration"]
            return f"✅ Appointment successfully reserved starting at {start} for {dur} minutes."
        elif "error" in res_json:
            error_message = res_json["error"].get("message", "Unknown error.")
            return f"❌ Failed to reserve appointment: {error_message}"
        else:
            return "⚠️ Unexpected response format."
    except Exception as e:
        return f"❌ Error parsing response: {e}"


def business_ids_from_network(network_id):
    url = "https://apiv2.gbooking.ru/rpc"

    payload = {
        "jsonrpc": "2.0",
        "id": 7,
        "cred": {
            "token": "02ccadf0487e1e7ae27fea5048c3f53e7330fa45",
            "user": "67e16c86c43bdd3739a7b415"
        },
        "method": "business.get_network_data",
        "params": {
            "networkID": network_id
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    try:
        result = response.json()
        if "result" in result:
            businesses = result["result"].get("businesses", [])
            business_ids = sorted(int(biz["businessID"]) for biz in businesses)
            return business_ids
        elif "error" in result:
            print(f"❌ Error: {result['error'].get('message', 'Unknown error')}")
            return []
        else:
            print("⚠️ Unexpected response format.")
            return []
    except Exception as e:
        print(f"❌ Failed to parse response: {e}")
        return []


def get_business_names(business_ids):
    url = "https://apiv2.gbooking.ru/rpc"
    headers = {"Content-Type": "application/json"}

    names = []
    idsAndNames = []

    for business_id in business_ids:
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "cred": {
                "token": "e0197978f235b1fbe2ecc386af12ddf5c1594219",
                "user": "67e16c3d5ce3f65a969705a0"
            },
            "method": "business.get_profile_by_id",
            "params": {
                "business": {
                    "id": str(business_id)
                },
                "skip_worker_sorting": True
            }
        }

        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            result = response.json()
            if "result" in result:
                name = result["result"]["business"]["general_info"].get("name", "Name not found")
                names.append(name)
                idsAndNames.append((business_id, name))
            elif "error" in result:
                names.append(f"❌ Error for ID {business_id}")
            else:
                names.append(f"⚠️ Unexpected format for ID {business_id}")
        except Exception as e:
            names.append(f"❌ Failed for ID {business_id}: {e}")

    return names, idsAndNames



def add_client(ID, business_id, client_name, client_surname, client_phone, client_email):
    # Define the URL for the API endpoint
    url = "https://apiv2.gbooking.ru/rpc"

    # Set up the headers, if needed (e.g., content type)
    headers = {
        "Content-Type": "application/json"
    }

    # Define the data payload with the 'id' parameter
    data = {
        "jsonrpc": "2.0",
        "id": ID,  # The 'id' parameter passed in the function
        "cred": {
            "token": "02ccadf0487e1e7ae27fea5048c3f53e7330fa45",  # Token passed as parameter
            "user": "67e16c86c43bdd3739a7b415"    # User passed as parameter
        },
        "method": "client.add_client",
        "params": {
            "business": {
                "id": business_id  # Business ID passed as parameter
            },
            "client": {
                "name": client_name,  # Client name passed as parameter
                "surname": client_surname,  # Client surname passed as parameter
                "phone": [
                    {
                        "country_code": client_phone['country_code'],  # Country code passed in dictionary
                        "area_code": client_phone['area_code'],  # Area code passed in dictionary
                        "number": client_phone['number']  # Phone number passed in dictionary
                    }
                ],
                "email": [client_email]  # Client email passed as parameter
            }
        }
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print("Client added successfully!")
        print(json.dumps(response.json(), indent=2))  # Pretty print the JSON response
    else:
        print(f"Failed to add client: {response.status_code}")
        print(response.text)



def confirm_appointment(appointment_id, client_id):
    api_url="https://apiv2.gbooking.ru/rpc"
    # Prepare the JSON payload for the request
    payload = {
        "jsonrpc": "2.0",
        "id": 19,  # Request ID, this can be modified to a dynamic value if necessary
        "cred": {},
        "method": "appointment.client_confirm_appointment",
        "params": {
            "appointment": {
                "id": appointment_id
            },
            "client": {
                "id": client_id
            }
        }
    }

    # Set the headers for the request
    headers = {
        'Content-Type': 'application/json',
    }

    try:
        # Send POST request to the API
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        # Check if the response is successful (HTTP 200)
        response.raise_for_status()

        # Parse the JSON response
        response_data = response.json()

        # Check if the response contains an error or result
        if "result" in response_data:
            return response_data["result"]
        elif "error" in response_data:
            error_code = response_data["error"].get("code")
            error_message = response_data["error"].get("message")
            return f"Error {error_code}: {error_message}"

    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"
    except ValueError as e:
        return f"Error parsing response: {str(e)}"

