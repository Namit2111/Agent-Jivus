# Transcripts API Documentation

This document outlines the API endpoints for managing transcripts within the application.  The API uses FastAPI and interacts with a database (likely MongoDB, based on the use of `to_mongo()`).

## Dependencies

* `datetime`: For timestamping updates.
* `src.db.schemas`: Defines the `TranscriptResponse` and `TranscriptTurns` schemas for data validation and serialization.
* `src.db.utils`: Contains utility functions, including `handle_error` and `valid_conversation_id`.
* `src.db.models`: Contains the `Conversations` and `Transcripts` database models.
* `fastapi`: The web framework used to build the API.


## API Endpoints

All endpoints are prefixed with `/transcripts` and are tagged as `transcripts`.

### GET `/transcripts/{conversation_id}`

Reads a transcript for a given conversation ID.

**Parameters:**

* `conversation_id`: (str, path parameter, required) The ID of the conversation whose transcript is to be retrieved.  Validated by `valid_conversation_id` dependency.

**Response:**

* `200 OK`: Returns a `TranscriptResponse` object containing the transcript data.
* `Error`: Returns an error as handled by `handle_error`.  Specific HTTP status codes depend on the nature of the error.

### POST `/transcripts/{conversation_id}`

Creates a new transcript for a given conversation ID.

**Parameters:**

* `conversation_id`: (str, path parameter, required) The ID of the conversation for which the transcript is being created. Validated by `valid_conversation_id` dependency.
* `turns`: (list[dict], body parameter, required) A list of dictionaries, each representing a turn in the conversation.  The expected structure isn't explicitly defined here but likely includes `speaker`, `transcript`, `start_time`, and `end_time` keys.

**Response:**

* `200 OK`: Returns a `TranscriptResponse` object containing the newly created transcript data.
* `Error`: Returns an error as handled by `handle_error`.  Specific HTTP status codes depend on the nature of the error.


### PUT `/transcripts/{conversation_id}`

Updates an existing transcript for a given conversation ID.  This endpoint completely replaces the existing transcript.

**Parameters:**

* `conversation_id`: (str, path parameter, required) The ID of the conversation whose transcript is to be updated.  Validated by `valid_conversation_id` dependency.
* `turns`: (list[dict], body parameter, required) A list of dictionaries, each representing a turn in the conversation.  The data is transformed into a standardized format before updating the database.

**Response:**

* `200 OK`: Returns a `TranscriptResponse` object containing the updated transcript data.
* `424 Failed Dependency`: If the update fails.
* `Error`: Returns an error as handled by `handle_error`.

### PATCH `/transcripts/{conversation_id}`

Adds a new turn to an existing transcript.

**Parameters:**

* `conversation_id`: (str, path parameter, required) The ID of the conversation whose transcript is to be patched. Validated by `valid_conversation_id` dependency.
* `transcript_turn`: (`TranscriptTurns`, body parameter, required) A single turn to be added to the transcript, conforming to the `TranscriptTurns` schema.

**Response:**

* `200 OK`: Returns `True` upon successful update.
* `False`: Indicates failure (Error handled by `handle_error`).


### DELETE `/transcripts/{conversation_id}`

Deletes a transcript for a given conversation ID.

**Parameters:**

* `conversation_id`: (str, path parameter, required) The ID of the conversation whose transcript is to be deleted.  Validated by `valid_conversation_id` dependency.

**Response:**

* `200 OK`: Returns `{"message": "success"}` upon successful deletion.
* `Error`: Returns an error as handled by `handle_error`.


## Error Handling

The `handle_error` function is used to manage exceptions across all endpoints.  The specific handling of errors is not detailed here, but it likely involves logging and potentially returning more informative error messages to the client.


## Data Models

The code uses data models (`Conversations`, `Transcripts`) likely interacting with a database. The details of these models are not included in the provided snippet.  The `TranscriptResponse` and `TranscriptTurns` schemas define the structure of data exchanged with the API.


This documentation provides a comprehensive overview of the Transcripts API.  For more detailed information on specific error handling or data structures, refer to the source code and associated schema definitions.
