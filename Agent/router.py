from fastapi import FastAPI, HTTPException, Body
from agent import CallData
from config import HEADERS,VAPI_CALL_URL
import requests

app = FastAPI()

@app.post("/make-call")
def make_call(call_request):
    data = CallData(call_request.customer_number)

    response = requests.post(
        VAPI_CALL_URL, headers=HEADERS, json=data)

    if response.status_code == 201:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

