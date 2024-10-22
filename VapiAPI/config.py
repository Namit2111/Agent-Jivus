import os
from dotenv import load_dotenv
load_dotenv() 
OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
#configuration variables
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
HEADERS = {
    'Authorization': f'Bearer {AUTH_TOKEN}',
    'Content-Type': 'application/json',
}

VAPI_CALL_URL = os.getenv('VAPI_CALL_URL')
assistant_id = os.getenv('ASSISTANT_ID')
NEBULA_API = os.getenv('NEBULA_API')


mongo_url = os.getenv('MONGO_URL')
db_name=os.getenv('DB_NAME')
collection_name=os.getenv('COLLECTION_NAME')
test_vars = ['AUTH_TOKEN', 'PHONE_NUMBER_ID', 'VAPI_CALL_URL', 'ASSISTANT_ID', 'NEBULA_API']
for var in test_vars:
    if os.getenv(var) is None:
        print(f"{var} is not loaded")
    else:
        print("config loaded successfully")
