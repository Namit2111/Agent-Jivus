import os

AUTH_TOKEN = os.getenv('AUTH_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
HEADERS = {
    'Authorization': f'Bearer {AUTH_TOKEN}',
    'Content-Type': 'application/json',
}

VAPI_CALL_URL = 'https://api.vapi.ai/call/phone'
