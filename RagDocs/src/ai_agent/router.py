from ast import Num
from fastapi import FastAPI, APIRouter, HTTPException, Body, status, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
import aiohttp
import requests
import asyncio
import json
from src.config import config
# Object Imports
from src.ai_agent.model import CallData, preData,CallStatusData
# Custom functions imports
from src.ai_agent.config import HEADERS, VAPI_CALL_URL, AUTH_TOKEN
from src.ai_agent.utils import get_calls, get_linkedin_summary, get_website_summary,llama_chat,llama_chat_json
from src.db.utils import authenticate_user
from src.integrations.hubspot.objects import get_object_by_id
from src.integrations.hubspot.utils import get_valid_access_token, validate_object_type
from src.live_call.utils import ai_agent_summary_generation, update_hubspot_and_send_email_ai_agent
from src.logger import Logger
from vocode.streaming.telephony import conversation
# app = FastAPI()
aiAgent = APIRouter(prefix="/v1/ai-agent", tags=["ai-agent"])


logger = Logger("ai_agent")

# MongoDB setup
client = MongoClient(config["DB_URI"])
db = client[config["DB_NAME"]]
calls_collection = db["calls"]
db_test = client['test'] 
test_collection = db['categorized_product_info']   

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Save call data to MongoDB
def save_call_data(call_id, status, hsContactID, auth_token):
    calls_collection.insert_one({"call_id": call_id, "status": status, "hsContactID": hsContactID, "auth_token": auth_token})

# Update the call status in MongoDB
def update_call_status(call_id, new_data):
    calls_collection.replace_one({"call_id": call_id}, new_data.to_dict())


async def process_call(call):
    call_id = call.get("call_id")
    try:
        url = f"https://api.vapi.ai/call/{call_id}"
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    call_status = await response.json()
                    if call_status.get("status") == "ended":
                        new_data = CallStatusData(call_status)
                        
                        auth_token = call.get("auth_token")
                        hsContactID = call.get("hsContactID")
                        
                        if hsContactID is None:
                            logger.debug("hsContactID is None")
                        elif auth_token is None:
                            logger.debug("auth_token is None")
                        else:
                            try:
                                hubspotInfo = await get_object_by_id(
                                    "contacts", hsContactID, 'email,email_chain,notes', auth_token=auth_token
                                )
                                conversation = {
                                    "transcripts": new_data.messages,
                                    "hubspotInfo": hubspotInfo.get('properties')
                                }
                                update_call_status(call_id, new_data)
                                logger.debug(f"Call {str(call_id)} ended and status updated in DB.")
                                await update_hubspot_and_send_email_ai_agent(conversation, auth_token)
                            except Exception as inner_e:
                                logger.debug(f"Error in update_hubspot_and_send_email_ai_agent for call {call_id}: {str(inner_e)}")
                else:
                    logger.debug(f"Failed to retrieve status for call {str(call_id)}")
    except Exception as e:
        logger.debug(f"Error processing call {str(call_id)}: {str(e)}")

# Periodically update the database with the latest call status
async def update_db():
    while True:
        pending_calls = list(calls_collection.find({"status": "queued"}))
        logger.debug(f"Pending calls: {pending_calls}")

        # Create tasks for each call in the pending calls list
        tasks = [asyncio.create_task(process_call(call)) for call in pending_calls]

        # Wait for all tasks to complete
        await asyncio.gather(*tasks)

        # Wait for 5 minutes before running the task again
        await asyncio.sleep(300)  # 300 seconds = 5 minutes

@aiAgent.on_event("startup")
async def startup_event():
    asyncio.create_task(update_db())

# Multi-call handler
@aiAgent.get("/multi-call")
def multi_call(lead_status: str, auth_token: str = Depends(oauth2_scheme)):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        
        user_id = auth_response.get("user_info").get("id")  # type:ignore
        ACCESS_TOKEN = get_valid_access_token(user_id);
            
        website_url = "https://linkedin.com/in/vasu-tiwari"  #change it according to the further updates 
        url = "https://api.hubapi.com/crm/v3/objects/contacts"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        params = {
            "properties": "firstname,lastname,phone,linkedinbio,hs_lead_status"
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
                user_lead_status = properties.get('hs_lead_status', 'N/A')

                if phone and user_lead_status in lead_status:
                        make_call(
                        call_request={
                            "customer_number": phone,
                            "linkedin_url": linkedinbio,
                            "website_url": website_url,
                            "hsContactID": contact.get('id')
                        },
                        auth_token=auth_token
                    )
            return "Success"
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch contacts.")

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
# Outbound calls
@aiAgent.post("/make-call")
def make_call(call_request: dict = Body(...), auth_token: str = Depends(oauth2_scheme) ):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        
        name = auth_response.get("user_info").get("name")
        companyName = auth_response.get("user_info").get("companyName")
        
        customer_number = call_request.get("customer_number")
        # linkedin_url = call_request.get("linkedin_url")
        website_url = call_request.get("website_url")

        # linkedin_data = get_linkedin_summary(url=linkedin_url)
        product_data = get_website_summary(url=website_url)

        data = preData(
            customer_number=customer_number,
            sales_person_name=name,
            company_name=companyName,
            product_summary=product_data.get("product_description")
        ).get_data()

        response = requests.post(VAPI_CALL_URL, headers=HEADERS, json=data)

        if response.status_code == 201:
            response_json = response.json()
            call_id = response_json.get("id")
            status = response_json.get("status")

            save_call_data(call_id, status, call_request.get("hsContactID"), auth_token)
            return response_json
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@aiAgent.post("/all-calls")
def post_all_calls():
    return get_calls().json()


@aiAgent.get("/calls")
def get_all_calls():
    # Retrieve all calls from the MongoDB collection
    calls = list(calls_collection.find({}, {"_id": 0}))  # Exclude the MongoDB internal '_id' field from the result
    if not calls:
        raise HTTPException(status_code=404, detail="No calls found.")
    
    # Create a conversation string from the messages
    conversations = []
    for call in calls:
        convo = ""
        for message in call["messages"]:
            if message["role"] == "system":
                continue
            convo += f'{message["role"]}: {message["message"]}\n'
        conversations.append(convo)

    return {"conversations": conversations}

@aiAgent.post("/get-summary")
async def get_summary(request: Request):
    data = await request.json()

    categories = data['message']['toolCalls'][0]['function']['arguments'].get('categories')
    conversation = data['message']['toolCalls'][0]['function']['arguments'].get('conversation')
    tool_calls = data.get('message', {}).get('toolCalls', [])
    tool_call_id = tool_calls[0].get('id', None) if tool_calls else ""

    unique_pair = {"product_name": "SmartHealth Tracker Pro"} # change it with some unique pair like product ID
    result = test_collection.find_one(unique_pair) 
    print(result)
    if result:
        material = result.get('categories')

        meta_desciption = {key:value['meta']['description'] for key,value in material.items() if key in categories}

        res = llama_chat_json(prompt="Given categories and their descriptions are: {} and the conversation is: {}. Choose which category is related to the conversation and return in the json format:follow this schema in every condition, key will always be the word type and value will always be the chosen category name. '{{type: chosen category name}}' . Remeber to choose only one category and follow the json format".format(meta_desciption, conversation))
        
        category = json.loads(res)['type']
        category_data = {key:value['data'] for key,value in material.items() if key in category}
     
        summary = llama_chat(prompt="using the given category and its data: {} and the conversation is: {}.  Generate a summary in 10-15 lines of categroy data . Summary should be oriented towards the conversation.".format(category_data, conversation))
        response_value = {
        "results": [
            {
                "toolCallId": tool_call_id,
                "result": summary
            }
        ]
    }
        return response_value
       
    else:
        response_value={
            "results": [
                {
                    "toolCallId": tool_call_id,
                    "result": "Category not found"
                }
            ]
        }
        return response_value