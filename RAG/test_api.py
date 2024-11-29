import requests

# Define the URL for the FastAPI endpoint
url = "http://localhost:8000/v1/ai-agent/get-summary"  # Update with the actual URL if different

# Define the data payload
data = {
    "message": {
        "toolCalls": [
            {
                "id": "12345",
                "function": {
                    "arguments": {
                        "categories": ["Company_overview", "Testimonials"],
                        "conversation": (
                            "bot: I have called to tell you about SmartHealth Tracker Pro.\n"
                            "user: What does the product do?\n"
                            "bot: It is a health tracker app that allows you to track your health and fitness goals.\n"
                            "user: Can I get company overview?"
                        )
                    }
                }
            }
        ]
    }
}

# Set headers (optional, depending on your API)
headers = {
    "Content-Type": "application/json",
}

# Make the POST request
try:
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()  # Raise an HTTPError if the response code is 4xx/5xx
    print("Response:")
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
