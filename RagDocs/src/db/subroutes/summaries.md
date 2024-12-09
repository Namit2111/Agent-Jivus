# Summaries API Documentation

This document outlines the API endpoints for managing summaries.  The API uses FastAPI and interacts with a database (likely MongoDB, based on the use of `to_mongo`).

## Endpoints

All endpoints are prefixed with `/summaries` and are tagged as `"summaries"`.

### `GET /summaries/{conversation_id}`

Reads a summary for a given conversation ID.

**Parameters:**

* `conversation_id` (str, path): The ID of the conversation.  Validation is performed using `valid_conversation_id` dependency.

**Response:**

* `200 OK`: Returns a `SummariesResponse` object containing the summary data.
* `Error`:  Generic error handling via `handle_error`.  Specific error codes may be returned depending on the underlying database error.

**Example Request:**

```bash
GET /summaries/12345
```


### `POST /summaries/{conversation_id}`

Creates a new summary for a given conversation ID.

**Parameters:**

* `conversation_id` (str, path): The ID of the conversation. Validation is performed using `valid_conversation_id` dependency.
* `summary_in` (Summary): The summary data to create.  This is likely a Pydantic model.

**Response:**

* `200 OK`: Returns a `SummariesResponse` object containing the newly created summary data.
* `Error`: Generic error handling via `handle_error`.


**Example Request (using curl):**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"summary": "This is a test summary"}' /summaries/12345
```

### `PUT /summaries/{conversation_id}`

Updates an existing summary for a given conversation ID.

**Parameters:**

* `conversation_id` (str, path): The ID of the conversation. Validation is performed using `valid_conversation_id` dependency.
* `new_summary` (Summary): The updated summary data.

**Response:**

* `200 OK`: Returns a `SummariesResponse` object containing the updated summary data.
* `424 Failed Dependency`: If the summary document could not be modified.
* `Error`: Generic error handling via `handle_error`.


### `DELETE /summaries/{conversation_id}`

Deletes a summary for a given conversation ID.

**Parameters:**

* `conversation_id` (str, path): The ID of the conversation. Validation is performed using `valid_conversation_id` dependency.

**Response:**

* `200 OK`: Returns `{"message": "success"}` upon successful deletion.
* `Error`: Generic error handling via `handle_error`.


## Dependencies

* `valid_conversation_id`: A dependency function that validates the conversation ID.  The specifics of this validation are not detailed here.
* `handle_error`: A function that handles exceptions and potentially logs errors.  The specifics of error handling are not detailed here.

## Data Models

* `SummariesResponse`: A Pydantic model representing the response structure for summary data.
* `Summary`: A Pydantic model representing the structure of a summary.
* `Summaries`:  Likely a MongoDB model representing summaries in the database.


## Notes

* The code uses `assert summary` which means that if a summary isn't found for a given conversation ID, it will raise an `AssertionError`. This should be handled gracefully with better error handling. The current error handling uses a generic `except Exception as e:` which is generally discouraged in production code. More specific exception handling should be implemented for better error reporting and debugging.
* The use of `use_db_field=False` in `to_mongo` suggests that the database field names might differ from the Pydantic model field names.

This documentation provides a high-level overview. For more detailed information, refer to the source code and the database schema.
