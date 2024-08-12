import os

AUTH_TOKEN = os.getenv('AUTH_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
HEADERS = {
    'Authorization': f'Bearer {AUTH_TOKEN}',
    'Content-Type': 'application/json',
}

VAPI_CALL_URL = os.getenv('VAPI_CALL_URL')
assistant_id = os.getenv('ASSISTANT_ID')
NEBULA_API = os.getenv('NEBULA_API')