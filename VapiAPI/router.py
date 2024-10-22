from fastapi import FastAPI, APIRouter, HTTPException, Body, Request
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
import requests
import asyncio
# Object Imports
from model import CallData, preData,CallStatusData
# Custom functions imports
from config import HEADERS, VAPI_CALL_URL, AUTH_TOKEN
from utils import get_calls, get_linkedin_summary, get_website_summary

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["call_db"]
calls_collection = db["calls"]

# Save call data to MongoDB
def save_call_data(call_id, status):
    calls_collection.insert_one({"call_id": call_id, "status": status})

# Update the call status in MongoDB
def update_call_status(call_id, new_data):
    calls_collection.replace_one({"call_id": call_id}, new_data.to_dict())

# Periodically update the database with the latest call status
async def update_db():
    while True:
        pending_calls = list(calls_collection.find({"status": "queued"}))
        for call in pending_calls:
            call_id = call.get("call_id")
            url = f"https://api.vapi.ai/call/{call_id}"
            headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                call_status = response.json().get("status")
                if call_status == "ended":
                    new_data = CallStatusData(response.json())
                    update_call_status(call_id, new_data)
                    print(f"Call {call_id} ended and status updated in DB.")
            else:
                print(f"Failed to retrieve status for call {call_id}")

        # Wait for 5 minutes (300 seconds) before running the task again
        await asyncio.sleep(300)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_db())

# Temporary landing page
@app.get('/')
def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Multi-call handler
@app.get("/multi-call")
def multi_call(authToken: str):
    website_url = "www.test.com"
    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {authToken}",
        "Content-Type": "application/json"
    }
    params = {
        "properties": "firstname,lastname,phone,linkedinbio"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        contacts = response.json().get('results', [])

        for contact in contacts:
            properties = contact.get('properties', {})
            firstname = properties.get('firstname', 'N/A')
            lastname = properties.get('lastname', 'N/A')
            phone = properties.get('phone', 'N/A')
            linkedinbio = properties.get('linkedinbio', 'N/A')
            if firstname and lastname and phone and linkedinbio:
                make_call(
                    call_request={
                        "customer_number": phone,
                        "linkedin_url": linkedinbio,
                        "website_url": website_url
                    }
                )
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch contacts.")

# Outbound calls
@app.post("/make-call")
def make_call(call_request: dict = Body(...)):
    customer_number = call_request.get("customer_number")
    linkedin_url = call_request.get("linkedin_url")
    website_url = call_request.get("website_url")

    linkedin_data = get_linkedin_summary(url=linkedin_url)
    product_data = get_website_summary(url=website_url)

    data = preData(
        customer_number=customer_number,
        sales_person_name="john doe",
        company_name="abc",
        product_summary=product_data.get("product_description")
    ).get_data()

    response = requests.post(VAPI_CALL_URL, headers=HEADERS, json=data)

    if response.status_code == 201:
        response_json = response.json()
        call_id = response_json.get("id")
        status = response_json.get("status")

        save_call_data(call_id, status)
        return response_json
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

# Display all calls
@app.get("/all-calls")
def get_all_calls(request: Request):
    return templates.TemplateResponse("all_calls.html", {"request": request})

@app.post("/all-calls")
def post_all_calls():
    return get_calls().json()
