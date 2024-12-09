# Transcripts API Documentation

This document outlines the API endpoints for managing transcripts.  The API uses FastAPI and interacts with a database (likely MongoDB based on the use of `to_mongo`).

## Table of Contents

* [Data Models](#data-models)
* [Endpoints](#endpoints)
    * [`GET /transcripts/{conversation_id}`](#get-transcriptsconversation_id)
    * [`POST /transcripts/{conversation_id}`](#post-transcriptsconversation_id)
    * [`PUT /transcripts/{conversation_id}`](#put-transcriptsconversation_id)
    * [`PATCH /transcripts/{conversation_id}`](#patch-transcriptsconversation_id)
    * [`DELETE /transcripts/{conversation_id}`](#delete-transcriptsconversation_id)


## Data Models

* **`TranscriptResponse`**:  (Details needed from `src.db.schemas`)  This schema likely represents the structure of the response for transcript data.
* **`TranscriptTurns`**: (Details needed from `src.db.schemas`) This schema likely represents the structure of a single turn in a conversation transcript.
* **`Conversations`**: (Details needed from `src.db.models`) This model likely represents the conversations in the database.
* **`Transcripts`**: (Details needed from `src.db.models`) This model likely represents the transcripts themselves in the database.  It appears to have fields like `conversationId` and `turns`.

## Endpoints

All endpoints use the `/transcripts` prefix and require a valid `conversation_id` which is validated using a `valid_conversation_id` dependency.  Error handling is centralized using the `handle_error` function.  The specific details of the error handling are not defined here but are presumably logged appropriately.


### `GET /transcripts/{conversation_id}`

**Description:** Retrieves a transcript for a given conversation ID.

**Parameters:**

* `conversation_id` (str): The ID of the conversation.  Must be valid according to the `valid_conversation_id` function.

**Response:**

* `200 OK`:  Returns a `TranscriptResponse` object containing the transcript data.
* `Error`:  Handles potential exceptions using `handle_error`.  The specific error response is not defined in this code but would likely include status codes and details.


### `POST /transcripts/{conversation_id}`

**Description:** Creates a new transcript for a given conversation ID.

**Parameters:**

* `turns` (list[dict]): A list of dictionaries, each representing a turn in the conversation.  The expected structure of each dictionary is not explicitly defined here but is inferred from the `update_transcript` endpoint.
* `conversation_id` (str): The ID of the conversation. Must be valid.

**Response:**

* `200 OK`: Returns a `TranscriptResponse` object representing the newly created transcript.
* `Error`: Handles exceptions using `handle_error`.


### `PUT /transcripts/{conversation_id}`

**Description:** Updates an existing transcript for a given conversation ID.  This replaces the entire transcript.

**Parameters:**

* `turns` (list[dict]):  A list of dictionaries representing the updated turns.  The expected structure is:
    ```json
    [
      {
        "speaker": "user",
        "transcript": "User's message",
        "start_time": "timestamp",
        "end_time": "timestamp"
      },
      // ... more turns
    ]
    ```
* `conversation_id` (str): The ID of the conversation. Must be valid.

**Response:**

* `200 OK`: Returns an updated `TranscriptResponse` object.
* `424 Failed Dependency`: If the update fails.
* `Error`: Handles exceptions using `handle_error`.


### `PATCH /transcripts/{conversation_id}`

**Description:** Appends a single turn to an existing transcript.

**Parameters:**

* `transcript_turn` (`TranscriptTurns`): A single turn to be added to the transcript.
* `conversation_id` (str): The ID of the conversation. Must be valid.

**Response:**

* `200 OK`: Returns `True` on success.
* `Error`: Handles exceptions using `handle_error` and returns `False`.


### `DELETE /transcripts/{conversation_id}`

**Description:** Deletes a transcript for a given conversation ID.

**Parameters:**

* `conversation_id` (str): The ID of the conversation. Must be valid.

**Response:**

* `200 OK`: Returns `{"message": "success"}` on success.
* `Error`: Handles exceptions using `handle_error`.


This documentation provides a comprehensive overview of the Transcripts API.  To fully understand the API behavior and responses, refer to the schemas and models defined in the `src.db` package.
