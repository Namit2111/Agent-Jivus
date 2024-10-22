import requests

url = "http://localhost:3000/integrations/hubspot/contacts"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "properties": {
        "email": "johndoe@example.com",
        "firstname": "John",
        "lastname": "Doe",
        "phone": "+1234567890",
        "linkedin_url": "https://www.linkedin.com/in/johndoe"
    }
}

response = requests.post(url, headers=headers, json=data)

print("Status Code:", response.status_code)
print("Response Text:", response.text)  # Print the raw response text

if response.status_code == 201:
    print("Object created successfully:", response.json())
else:
    print("Error:", response.status_code)
    try:
        error_response = response.json()
        print("Error Response JSON:", error_response)
    except ValueError:
        print("Response is not in JSON format")
