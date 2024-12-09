# Conversations API Documentation

This document outlines the API endpoints for managing conversations.  The API is built using FastAPI.

## Table of Contents

* [Import Statements](#import-statements)
* [API Router](#api-router)
* [Authentication](#authentication)
* [Helper Functions](#helper-functions)
* [Endpoints](#endpoints)
    * [/conversations/user](#get-conversationsuser)
    * [/conversations/{conversation_id}](#get-conversationsconversation_id)
    * [/conversations/](#post-conversations)
    * [/conversations/{conversation_id}](#put-conversationsconversation_id)
    * [/conversations/{conversation_id}](#delete-conversationsconversation_id)


## Import Statements

The API utilizes several libraries:

* `math.ceil`: For ceiling calculations in pagination.
* `typing.Annotated`: For type hinting with query parameter annotations.
* `datetime`: For handling date and time information.
* `fastapi`: The core framework for building the API.
* `fastapi.security.OAuth2PasswordBearer`: For OAuth2 authentication.
* `src.db.schemas`: Contains Pydantic schemas for data validation and serialization (`Conversation`, `ConversationsListResponse`, `ConversationsResponse`, `Persona`, `PageParams`, `ProfileInfo`).
* `src.db.utils`: Contains helper functions (`authenticate_user`, `handle_error`, `valid_conversation_id`, `valid_agent_id`).
* `src.enums`: Contains enums (`CallTypes`, `UserRoles`).
* `src.db.models`: Contains MongoDB models (`Conversations`, `LiveInsights`, `Summaries`, `Transcripts`).


## API Router

The API is defined using FastAPI's `APIRouter` with the prefix `/conversations` and tag `conversations`.

```python
router = APIRouter(prefix="/conversations", tags=["conversations"])
```

## Authentication

The API uses OAuth2 for authentication:

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

Authentication is handled by the `authenticate_user` function from `src.db.utils`.


## Helper Functions

Several helper functions are defined:

* `get_base_conversation(conversation_id)`: Retrieves a base conversation object from the database.
* `get_conversation(conversation_id)`: Retrieves a fully populated conversation object from the database.
* `valid_conversation_id`: Dependency function for validating conversation IDs.
* `valid_agent_id`: Dependency function for validating agent IDs.


## Endpoints

### GET /conversations/user

Lists conversations for a user.  Requires authentication.  Managers can view subordinates' conversations.

**Parameters:**

* `call_type: CallTypes`: The type of call to filter by.
* `page: Annotated[int, Query(ge=1)] = 1`: Page number (default: 1).
* `size: Annotated[int, Query(ge=1)] = 20`: Page size (default: 20).
* `agent_id: str | None = Depends(valid_agent_id)`:  Optional agent ID for managers to view subordinate's conversations.
* `auth_token: str = Depends(oauth2_scheme)`: OAuth2 authentication token.

**Response:** `ConversationsListResponse` (containing a list of `ConversationsResponse` and pagination details).

**Error Handling:**  Handles authentication errors and other exceptions using `handle_error`.

### GET /conversations/{conversation_id}

Retrieves a specific conversation by ID.

**Parameters:**

* `conversation_id: str = Depends(valid_conversation_id)`: The ID of the conversation.

**Response:** `ConversationsResponse`

**Error Handling:** Handles exceptions using `handle_error`.


### POST /conversations

Creates a new conversation.

**Request Body:** `Conversation`

**Response:** `ConversationsResponse`

**Error Handling:** Handles exceptions using `handle_error`.  Creates associated `LiveInsights`, `Transcripts`, and `Summaries` records.


### PUT /conversations/{conversation_id}

Updates an existing conversation.

**Parameters:**

* `new_conversation: Conversation`: The updated conversation data.
* `conversation_id: str = Depends(valid_conversation_id)`: The ID of the conversation to update.

**Response:** `ConversationsResponse`

**Error Handling:** Handles exceptions using `handle_error`.


### DELETE /conversations/{conversation_id}

Deletes a conversation.

**Parameters:**

* `conversation_id: str = Depends(valid_conversation_id)`: The ID of the conversation to delete.

**Response:** `{"message": "success"}`

**Error Handling:** Handles exceptions using `handle_error`.

