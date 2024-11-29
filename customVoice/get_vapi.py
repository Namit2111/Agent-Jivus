import requests
import json
# Define the API endpoint and token
url = "https://api.vapi.ai/assistant/989bd2af-2bab-4560-881e-3e5f29d6c679"
token = "b8491eab-0dad-4aab-8999-c76ad6957047"   # Replace with your actual bearer token

# Define the headers
headers = {
    "Authorization": f"Bearer {token}",
}

# Send the GET request
response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    print("Request successful!")
    with open('response.json', mode='w', encoding='utf-8') as f:
        json.dump(response.json(), f,indent=4)
    # print("Response:", response.json())
else:
    print("Request failed with status code:", response.status_code)
    print("Error message:", response.text)
