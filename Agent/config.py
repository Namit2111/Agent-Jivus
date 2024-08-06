AUTH_TOKEN = '<YOUR AUTH TOKEN>'
PHONE_NUMBER_ID = '<PHONE NUMBER ID FROM DASHBOARD>'

HEADERS = {
    'Authorization': f'Bearer {AUTH_TOKEN}',
    'Content-Type': 'application/json',
}

VAPI_CALL_URL = 'https://api.vapi.ai/call/phone'