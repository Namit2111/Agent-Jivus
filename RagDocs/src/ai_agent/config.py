from src.config import config
GROQ_API = config["GROQ_API"]
OPENAI_API_KEY = config["OPENAI_API_KEY"]
AUTH_TOKEN = config["VAPI_AUTH_TOKEN"]
PHONE_NUMBER_ID = config["PHONE_NUMBER_ID"]
HEADERS = {
    'Authorization': f'Bearer {AUTH_TOKEN}',
    'Content-Type': 'application/json',
}

VAPI_CALL_URL = config["VAPI_CALL_URL"]
assistant_id = config["VAPI_ASSISTANT_ID"]
NEBULA_API = config["NUBELA_API_KEY"]
test_vars = ['OPENAI_API_KEY','VAPI_AUTH_TOKEN', 'PHONE_NUMBER_ID', 'VAPI_CALL_URL', 'VAPI_ASSISTANT_ID', 'NUBELA_API_KEY']
for var in test_vars:
    if config[var] is None:
        print(f"{var} is not loaded")
    else:
        print("config loaded successfully", config[var])