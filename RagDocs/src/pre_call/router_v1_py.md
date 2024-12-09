# Pre-Call API Documentation

This document describes the Pre-Call API, a FastAPI application responsible for setting up conversations and fetching LinkedIn information.  The current implementation uses MongoDB models directly, which needs refactoring (see TODOs).


## TODOs

* **More Refactoring:**  The code requires significant refactoring.
* **Database Model Abstraction:** Remove direct usage of MongoDB models. Package them into the `db` folder and access them through functions for better modularity and maintainability.


## API Endpoints

The API is located at `/v1/pre-call` and uses the following endpoints:

### `/v1/pre-call/setup` (POST)

Sets up a new conversation.

**Request Body:**

```json
{
  "conversationId": "string",  // Unique ID for the conversation
  "personaId": "string" // ID of the persona to use
}
```

**Response:**

```json
{
  "conversationId": "string" // ID of the created conversation
}
```

**Request Parameters:**  None

**Authentication:** Requires authentication via `Depends(get_auth_response)`.  The authentication mechanism is not explicitly detailed here, but it provides a `user_info` dictionary containing at least a `user_id`.

**Error Handling:**

* **401 Unauthorized:** If the persona does not belong to the authenticated user.
* **500 Internal Server Error:** For any other error during conversation setup.


**Example Request:**

```bash
curl -X POST \
  http://localhost:8000/v1/pre-call/setup \
  -H 'Content-Type: application/json' \
  -d '{
  "conversationId": "conv123",
  "personaId": "persona456"
}'
```


### `/v1/pre-call/fetch_linkedin` (POST)

Fetches LinkedIn information based on a provided URL.

**Request Body:**

```json
{
  "linkedinUrl": "string",  // URL of the LinkedIn profile
  "profile_id": "string" // ID of the profile to update
}
```

**Response:**

```json
{
  "response": "object", // Raw response from LinkedIn API
  "summary": "string"   // Summarized information from LinkedIn
}
```

**Request Parameters:** None

**Error Handling:**

* **500 Internal Server Error:** For any error during LinkedIn data fetching or processing.

**Example Request:**

```bash
curl -X POST \
  http://localhost:8000/v1/pre-call/fetch_linkedin \
  -H 'Content-Type: application/json' \
  -d '{
  "linkedinUrl": "https://www.linkedin.com/in/example",
  "profile_id": "profile789"
}'
```


## Data Models

* **`src.db.schemas.Conversation`**: Represents a conversation.
* **`src.db.schemas.LinkedInInfo`**: Represents LinkedIn profile information.
* **`src.db.schemas.Persona`**: Represents a persona.
* **`src.db.schemas.User`**: Represents a user.
* **`src.pre_call.schemas.ConversationCreateReq`**: Request schema for creating a conversation.


## Dependencies and Utilities

The API utilizes several dependencies and utilities:

* **FastAPI:** Web framework.
* **Pydantic:** Data validation.
* **Various Thunks:** Asynchronous functions for different services (e.g., transcription, synthesis, AI agent).
* **Logger:** Custom logging utility.
* **`get_auth_response`**: Authentication function (implementation not shown).
* **`linkedin_summary_generation`**: Function to fetch and summarize LinkedIn data.
* **`training_call_prompt_generation`**: Function to generate prompts for training calls.


This documentation provides a high-level overview of the Pre-Call API.  More detailed information about the internal functions and data structures can be found within the source code.  Note that the code requires refactoring to improve structure and maintainability.
