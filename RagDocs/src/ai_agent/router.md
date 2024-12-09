# ai-agent API Documentation

This document outlines the functionality of the `ai-agent` API, a FastAPI application designed to manage and process call data, integrate with HubSpot, and leverage large language models for summary generation.

## Dependencies

The API relies on several external libraries:

* `fastapi`:  For building the API itself.
* `pymongo`: For interacting with a MongoDB database.
* `aiohttp`: For asynchronous HTTP requests.
* `requests`: For synchronous HTTP requests.
* `vocode`: For telephony integration (likely for call handling).
* Various other libraries for authentication, templating (Jinja2), logging, etc.


## Database Setup

The API connects to a MongoDB database using configuration details from `src.config`.  It utilizes two collections:

* `calls`: Stores call data, including call ID, status, HubSpot contact ID, and authentication token.
* `categorized_product_info`: Contains categorized product information used for summary generation (appears to be for a specific product).


## API Endpoints

The API exposes several endpoints under the `/v1/ai-agent` prefix:


### `/v1/ai-agent/multi-call` (GET)

**Description:** Initiates multiple outbound calls based on specified lead status and authentication.

**Parameters:**

* `lead_status` (str):  A filter for HubSpot contacts based on their lead status.
* `auth_token` (str):  Authentication token (obtained via OAuth2).

**Functionality:**

1. Authenticates the user using the provided `auth_token`.
2. Fetches contacts from HubSpot based on `lead_status`.
3. For each contact with a phone number, it calls the `/v1/ai-agent/make-call` endpoint to initiate an outbound call.
4. Returns "Success" on successful completion, or raises HTTPExceptions for errors.


### `/v1/ai-agent/make-call` (POST)

**Description:** Initiates a single outbound call.

**Parameters:**

* `call_request` (dict):  A dictionary containing call details:
    * `customer_number` (str): The phone number to call.
    * `website_url` (str): The website URL for context.
    * `hsContactID` (str, optional): The HubSpot Contact ID.
* `auth_token` (str): Authentication token.

**Functionality:**

1. Authenticates the user.
2. Fetches website summary data using `get_website_summary`.
3. Sends a call request to VAPI using the data.
4. Saves call data to the MongoDB `calls` collection.
5. Returns the response from VAPI.


### `/v1/ai-agent/all-calls` (POST)

**Description:** Retrieves all calls.


**Functionality:** Calls `get_calls()` from `src.ai_agent.utils` to fetch call information and returns the data.

### `/v1/ai-agent/calls` (GET)

**Description:** Retrieves all calls from the database and formats them into conversations.

**Functionality:**

1. Retrieves all calls from the `calls` collection.
2. Formats the call messages into a conversational string.
3. Returns the conversations.


### `/v1/ai-agent/get-summary` (POST)

**Description:** Generates a summary of a conversation using a large language model (likely Llama).

**Parameters:**

* `request` (Request):  The FastAPI request object containing JSON data.  Data includes:
    * `message.toolCalls[0].function.arguments.categories`: Categories for the summary.
    * `message.toolCalls[0].function.arguments.conversation`: The conversation to summarize.

**Functionality:**

1. Retrieves categories and conversation from the request body.
2. Looks up category data in the `categorized_product_info` collection.
3. Uses Llama (`llama_chat_json` and `llama_chat`) to generate a summary based on the conversation and category data.
4. Returns the generated summary.


## Internal Functions

Several internal functions manage database operations, call processing, HubSpot integration, and other tasks.  These are well-commented within the code but noteworthy are:

* `save_call_data`: Inserts new call data into MongoDB.
* `update_call_status`: Updates the status of an existing call in MongoDB.
* `process_call`: Handles individual call processing, including updating call status, integrating with HubSpot, and sending emails.
* `update_db`: A background task that periodically updates the database with the latest call statuses.


##  Error Handling

The API uses `HTTPException` to handle errors, returning appropriate HTTP status codes (e.g., 401 Unauthorized, 400 Bad Request).


## Authentication

The API uses an OAuth2PasswordBearer scheme for authentication.  The `authenticate_user` function is used to verify authentication tokens.


This documentation provides a comprehensive overview of the `ai-agent` API.  Further details can be found in the source code.
