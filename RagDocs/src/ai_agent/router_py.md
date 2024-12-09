# AI Agent API Documentation

This document outlines the API endpoints for the AI Agent service.  The service utilizes FastAPI, MongoDB, and various external APIs (VAPI, HubSpot, LinkedIn) to manage and process call data, generate summaries, and integrate with CRM systems.

## Table of Contents

* [Authentication](#authentication)
* [Endpoints](#endpoints)
    * [/v1/ai-agent/multi-call](#v1aia-agentmulti-call)
    * [/v1/ai-agent/make-call](#v1aia-agentmake-call)
    * [/v1/ai-agent/all-calls](#v1aia-agentall-calls)
    * [/v1/ai-agent/calls](#v1aia-agentcalls)
    * [/v1/ai-agent/get-summary](#v1aia-agentget-summary)


## Authentication

The API uses OAuth 2.0 for authentication.  A valid access token must be provided in the `Authorization` header as `Bearer {token}`.  The token is obtained via the `/token` endpoint (not explicitly defined here, assumed to exist).


## Endpoints

### `/v1/ai-agent/multi-call`

**Method:** `GET`

**Description:** Initiates multiple outbound calls based on specified lead status and authenticated user. Fetches contact information from HubSpot, filters by lead status, and makes calls using the `/make-call` endpoint for each matching contact.

**Parameters:**

* `lead_status` (str, required):  A string representing the lead status to filter contacts by.
* `auth_token` (str, required): OAuth 2.0 access token.

**Response:**

* `200 OK`: "Success" if calls are initiated successfully.
* `401 Unauthorized`: Invalid or missing authentication token.
* `400 Bad Request`:  Error fetching contacts or other errors during processing.


### `/v1/ai-agent/make-call`

**Method:** `POST`

**Description:** Makes an outbound call using the VAPI.ai API.  Requires customer number, optionally LinkedIn and website URLs.  Generates a pre-call summary based on website data. Saves call data to MongoDB.


**Request Body (`call_request`):**

* `customer_number` (str, required): Phone number of the customer.
* `linkedin_url` (str, optional): LinkedIn profile URL of the customer. (Currently not used)
* `website_url` (str, optional): Website URL of the customer or company.
* `hsContactID` (str, optional): HubSpot Contact ID.

**Parameters:**

* `auth_token` (str, required): OAuth 2.0 access token.

**Response:**

* `201 Created`: Call successfully initiated, returns call ID and status.
* `401 Unauthorized`: Invalid or missing authentication token.
* `400 Bad Request`: Error making the call or saving call data.


### `/v1/ai-agent/all-calls`

**Method:** `POST`

**Description:** Retrieves all calls from the database.

**Parameters:** None

**Response:** JSON array of all calls.  Error handling not explicitly specified in code.


### `/v1/ai-agent/calls`

**Method:** `GET`

**Description:** Retrieves all calls from the MongoDB collection,  formats the messages into conversation strings.

**Parameters:** None

**Response:**

* `200 OK`: JSON object with a `conversations` array containing conversation strings for each call.
* `404 Not Found`: No calls found.


### `/v1/ai-agent/get-summary`

**Method:** `POST`

**Description:** Generates a summary of a conversation based on provided categories and conversation text. Uses a MongoDB collection (`categorized_product_info`) to fetch category data.  Utilizes Llama-chat for summary generation.

**Request Body:**

* `message`: A JSON object containing the conversation and categories.  Structure is assumed based on the code.

**Response:**

* `200 OK`: JSON object containing the generated summary.
* Error handling (if the category is not found) returns "Category not found".


## Database Interactions

The application interacts with a MongoDB database (`calls` collection) to store and manage call data.  A second collection (`categorized_product_info`) is used for product category information.


## Error Handling

The code includes basic error handling using `HTTPException` for authentication failures and other issues.  More robust error handling (e.g., specific status codes for different error types) would improve the API.

## Logging

The application uses a custom logger (`Logger`) for debugging and informational messages.  Log levels used are `debug`.


## Dependencies

The application depends on several external libraries including:

* `fastapi`
* `pymongo`
* `aiohttp`
* `requests`
* `vocode` (used in `conversation` import, purpose unclear from provided code)
* `hubspot` (integration library)
* `llama-cpp-python` (inferred based on usage of llama_chat)



This documentation provides a comprehensive overview of the AI Agent API.  Remember to consult the code for specific details and edge cases not explicitly documented here.
