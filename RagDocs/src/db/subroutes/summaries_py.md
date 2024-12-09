# Summaries API Documentation

This document describes the API endpoints for managing summaries.  The API uses FastAPI and interacts with a database (likely MongoDB, based on the code).

## Endpoints

All endpoints are prefixed with `/summaries`.

### GET `/summaries/{conversation_id}`

Reads a summary for a given conversation ID.

* **Path Parameter:**
    * `conversation_id`: (str) The ID of the conversation.  Must be a valid conversation ID (validated by `valid_conversation_id` dependency).

* **Response:**
    * `200 OK`: Returns a `SummariesResponse` object containing the summary data.
    * `5xx`: Internal Server Error.  Generic error handling via `handle_error`.


### POST `/summaries/{conversation_id}`

Creates a new summary for a given conversation ID.

* **Path Parameter:**
    * `conversation_id`: (str) The ID of the conversation. Must be a valid conversation ID (validated by `valid_conversation_id` dependency).

* **Request Body:**
    * `summary_in`: (Summary)  A `Summary` object containing the summary data.

* **Response:**
    * `200 OK`: Returns a `SummariesResponse` object containing the newly created summary data.
    * `5xx`: Internal Server Error. Generic error handling via `handle_error`.


### PUT `/summaries/{conversation_id}`

Updates an existing summary for a given conversation ID.

* **Path Parameter:**
    * `conversation_id`: (str) The ID of the conversation. Must be a valid conversation ID (validated by `valid_conversation_id` dependency).

* **Request Body:**
    * `new_summary`: (Summary) A `Summary` object containing the updated summary data.

* **Response:**
    * `200 OK`: Returns a `SummariesResponse` object containing the updated summary data.
    * `424 Failed Dependency`: Unable to modify the summary document.
    * `5xx`: Internal Server Error. Generic error handling via `handle_error`.


### DELETE `/summaries/{conversation_id}`

Deletes a summary for a given conversation ID.

* **Path Parameter:**
    * `conversation_id`: (str) The ID of the conversation. Must be a valid conversation ID (validated by `valid_conversation_id` dependency).

* **Response:**
    * `200 OK`: Returns `{"message": "success"}` upon successful deletion.
    * `5xx`: Internal Server Error. Generic error handling via `handle_error`.


## Data Models

* **SummariesResponse:**  (Schema)  The response model for all successful API calls.  The exact structure is not defined here but it's inferred to be a representation of the `Summaries` database model.

* **Summary:** (Schema)  The request model for creating and updating summaries.  The exact structure is not defined here.

* **Summaries:** (Database Model) Represents the summaries in the database.  It's assumed to have at least `conversationId` and `summary` fields.  It likely uses a MongoDB-like library given the `to_mongo` method.


## Dependencies

* `valid_conversation_id`: A dependency function that validates the conversation ID.  It's not defined here, but it likely performs input sanitization and checks for existence.

* `handle_error`: A function that handles exceptions.  It's not defined here, but it's assumed to log errors appropriately.


## Error Handling

The API uses a generic `handle_error` function for exception handling. Specific error codes are returned only in cases where the error is predictable (e.g., 424 Failed Dependency when updating a summary fails).  More specific error handling might be beneficial for better API usability.
