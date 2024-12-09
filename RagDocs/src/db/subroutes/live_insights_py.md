# Live Insights API Documentation

This document outlines the API endpoints for managing live insights.  The API uses FastAPI and interacts with a database (presumably MongoDB based on the use of `to_mongo`).

## Imports

- `datetime`: Used for timestamping updates.
- `src.logger`: Custom logger for error handling.
- `src.db.schemas`: Defines Pydantic schemas for `LiveInsight` and `LiveInsightsResponse`.
- `src.db.utils`: Contains utility functions, including `handle_error` and `valid_conversation_id`.
- `src.db.models`: Defines the `LiveInsights` model.
- `fastapi`: The FastAPI framework.


## API Endpoints

All endpoints are prefixed with `/live-insights` and are tagged as `"live-insights"`.

### GET `/live-insights/{conversation_id}`

Retrieves live insights for a given conversation ID.

**Parameters:**

- `conversation_id`:  (str, path) The ID of the conversation.  Validated using `valid_conversation_id` dependency.

**Response:**

- `200 OK`: Returns a `LiveInsightsResponse` object containing the live insights.
- `5xx`: Server error, details logged using `handle_error`.


### POST `/live-insights/{conversation_id}`

Creates a new live insight for a given conversation ID.

**Parameters:**

- `conversation_id`: (str, path) The ID of the conversation. Validated using `valid_conversation_id` dependency.
- `insights`: (`LiveInsight`, body)  A `LiveInsight` object containing the insight data.

**Response:**

- `200 OK`: Returns a `LiveInsightsResponse` object containing the newly created live insight.
- `5xx`: Server error, details logged using `handle_error`.


### PUT `/live-insights/{conversation_id}`

Updates existing live insights for a given conversation ID.  This appends new insights to the existing data.

**Parameters:**

- `conversation_id`: (str, path) The ID of the conversation.
- `insight_dict`: (dict, body) A dictionary containing the new insight data to be appended.

**Response:**

- `200 OK`: Returns `True` on success.
- `5xx`: Server error, returns `False` and logs details using `handle_error`.


### DELETE `/live-insights/{conversation_id}`

Deletes live insights for a given conversation ID.

**Parameters:**

- `conversation_id`: (str, path) The ID of the conversation. Validated using `valid_conversation_id` dependency.

**Response:**

- `200 OK`: Returns `{"message": "success"}` on success.
- `5xx`: Server error, details logged using `handle_error`.


## Helper Functions

- **`get_live_insight(conversation_id: str)`:** Retrieves a `LiveInsights` object from the database based on the conversation ID.  Raises an assertion error if no matching object is found.
- **`handle_error(e)`:**  A function (presumably from `src.db.utils`) that handles exceptions, likely logging the error.


## Error Handling

The API uses a centralized error handling mechanism (`handle_error`) to log exceptions.  Specific HTTP status codes are not explicitly defined for errors, but it's implied that 5xx codes are used for server errors.


## Data Models

The documentation should include details about the `LiveInsight` and `LiveInsightsResponse` schemas from `src.db.schemas` and the `LiveInsights` model from `src.db.models`.  This information is missing from the provided code snippet and would significantly enhance this documentation.
