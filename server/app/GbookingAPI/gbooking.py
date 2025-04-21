import requests
import json

# Define the API URL
url = "https://crac-prod3.gbooking.ru/rpc"

# Define the headers
headers = {
    "Content-Type": "application/json"
}

# Define the request body
body = {
    "jsonrpc": "2.0",
    "id": 1,
    "cred": {},
    "method": "Crac.GetCRACResourcesAndRooms",
    "params": [{
        "business": {
            "id": "4000000006304"
        },
        "filters": {
            "resources": ["59f05563854202eb6f86569c"],
            "date": {
                "from": "2017-11-01T00:00:00.000Z",
                "to": "2017-11-30T00:00:00.000Z"
            }
        }
    }]
}

# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(body))

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    timetable = response.json()
    print("Timetable slots received:", json.dumps(timetable, indent=4))
else:
    print(f"Error: {response.status_code} - {response.text}")
