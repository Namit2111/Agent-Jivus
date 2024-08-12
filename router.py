# FastApi Imports
from fastapi import FastAPI, HTTPException, Body,Request
from fastapi.templating import Jinja2Templates
# Object Imports
from model import CallData,preData
# custom functions imports
from config import HEADERS,VAPI_CALL_URL
from utils import get_linkedin_profile_nubela,extract_text_from_website,get_calls
# other imports
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

#temporary landing page
@app.get('/')
def get_form(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})


#outbound calls
@app.post("/make-call")
def make_call(call_request: dict = Body(...)):
    #get all the req params
    customer_number = call_request.get("customer_number")
    linkedin_url = call_request.get("linkedin_url")
    website_url = call_request.get("website_url")
    
    #get linkedin and product data 
    # linkedin_data = get_linkedin_profile_nubela(linkedin_url)
    # product_description = extract_text_from_website(website_url)
    
    #create datya for api call
    data = preData(customer_number=customer_number).get_data()

    #make api call
    response = requests.post(VAPI_CALL_URL, headers=HEADERS, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

#display all calls
@app.get("/all-calls")
def get_all_calls(request: Request):
    return templates.TemplateResponse("all_calls.html",{"request": request})

@app.post("/all-calls")
def get_all_calls(request: Request):
    return get_calls().json()