import requests

# Define the API endpoint and token
url = "https://api.vapi.ai/assistant/989bd2af-2bab-4560-881e-3e5f29d6c679"
token = "b8491eab-0dad-4aab-8999-c76ad6957047"  # Replace with your actual token

# Define the headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Define the data payload
data = {

"voice":{
    "provider":"custom-voice",
    "server":{
        "url":"https://2090-2404-7c80-64-239a-913d-d40c-c849-4f8a.ngrok-free.app/voice"
    }
}
    
}

# Send the PATCH request
response = requests.patch(url, headers=headers, json=data)

# Check the response
if response.status_code == 200:
    print("Request successful!")
    print("Response:", response.json())
else:
    print("Request failed with status code:", response.status_code)
    print("Error message:", response.text)
