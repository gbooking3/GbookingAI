import requests

# Base URL from the Postman docs
base_url = "https://api.wirelesscar.net/"

# Replace this with the endpoint you want to test, e.g. vehicles for a network
endpoint = f"core/vehicles?networkId=456"

# Full URL
url = base_url + endpoint

# Headers with token authentication
headers = {
    "Content-Type": "application/json",
    "X-Auth-Token": "02ccadf0487e1e7ae27fea5048c3f53e7330fa45",
    "X-User-Id": "67e16c86c43bdd3739a7b415"
}

# Make the request
response = requests.get(url, headers=headers)

# Print the response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
