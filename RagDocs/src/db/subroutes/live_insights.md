# Live Insights API Documentation

This document describes the API endpoints for managing live insights.  The API is built using FastAPI and interacts with a database (likely MongoDB, given the use of `to_mongo`).

## Dependencies

- `datetime`
- `src.logger`: Custom logger module.
- `src.db.schemas`: Contains Pydantic schemas `LiveInsight` and `LiveInsightsResponse`.
- `src.db.utils`: Contains utility functions `handle_error` and `valid_conversation_id`.
- `src.db.models`: Contains the `LiveInsights` model (likely a MongoDB model).
- `fastapi`: Web framework.


## API Endpoints

All endpoints are prefixed with `/live-insights` and are tagged as "live-insights".

### 1. GET `/live-insights/{conversation_id}`

Reads a live insight for a given conversation ID.

**Parameters:**

- `conversation_id`: (str, path, required) The ID of the conversation.  Validation is performed by the `valid_conversation_id` dependency.

**Response:**

- `200 OK`: Returns a `LiveInsightsResponse` object containing the live insight data.
- `5xx`: Internal server error.  Error details are handled by `handle_error`.


### 2. POST `/live-insights/{conversation_id}`

Creates a new live insight for a given conversation ID.

**Parameters:**

- `conversation_id`: (str, path, required) The ID of the conversation. Validation is performed by the `valid_conversation_id` dependency.
- `insights`: (`LiveInsight`, body, required) The live insight data to be created.

**Response:**

- `200 OK`: Returns a `LiveInsightsResponse` object containing the newly created live insight data.
- `5xx`: Internal server error.  Error details are handled by `handle_error`.


### 3. PUT `/live-insights/{conversation_id}`

Updates an existing live insight for a given conversation ID.  This endpoint appends data to the existing `insights` field.

**Parameters:**

- `conversation_id`: (str, path, required) The ID of the conversation.
- `insight_dict`: (dict, body, required) A dictionary containing the data to be appended to the existing `insights` field.

**Response:**

- `200 OK`: Returns `True` on success, `False` on failure.
- `5xx`: Internal server error.  Error details are handled by `handle_error`.


### 4. DELETE `/live-insights/{conversation_id}`

Deletes a live insight for a given conversation ID.

**Parameters:**

- `conversation_id`: (str, path, required) The ID of the conversation. Validation is performed by the `valid_conversation_id` dependency.

**Response:**

- `200 OK`: Returns `{"message": "success"}` on success.
- `5xx`: Internal server error. Error details are handled by `handle_error`.


## Helper Functions

- `get_live_insight(conversation_id)`: Retrieves a live insight from the database based on the conversation ID.  Raises an assertion error if no live insight is found.
- `handle_error(e)`: Handles exceptions, likely logging the error and returning an appropriate response (not explicitly defined in the provided code).
- `valid_conversation_id`: A dependency injection function that validates the conversation ID.


## Data Models

- `LiveInsight`: A Pydantic schema defining the structure of a single live insight.  The specific fields are not defined in the provided code.
- `LiveInsightsResponse`: A Pydantic schema defining the structure of the response object for live insight endpoints.  The specific fields are not defined in the provided code.
- `LiveInsights`: A database model (likely MongoDB) representing live insights.


This documentation assumes a basic understanding of FastAPI, Pydantic, and MongoDB.  More detailed information about the data models and error handling would require access to the `src` directory.
