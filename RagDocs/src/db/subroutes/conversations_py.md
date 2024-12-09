# Conversations API Documentation

This document outlines the API endpoints for managing conversations.  The API uses FastAPI and assumes the existence of a database (likely MongoDB based on the code).

## Table of Contents

* [Endpoints](#endpoints)
    * [/conversations/user](#get-conversationsuser)
    * [/conversations/{conversation_id}](#get-conversationsconversation_id)
    * [/conversations/](#post-conversations)
    * [/conversations/{conversation_id}](#put-conversationsconversation_id)
    * [/conversations/{conversation_id}](#delete-conversationsconversation_id)
* [Data Models](#data-models)
* [Error Handling](#error-handling)
* [Authentication](#authentication)


## Endpoints

### GET /conversations/user

Lists conversations for a user or their subordinates (if the user is a manager).

**Request Parameters:**

* `call_type`: (Required) `CallTypes` enum value specifying the type of call.
* `page`: (Optional, default 1) Page number for pagination (starting from 1).  Must be greater than or equal to 1.
* `size`: (Optional, default 20) Number of conversations per page. Must be greater than or equal to 1.
* `agent_id`: (Optional) ID of the agent whose conversations to retrieve.  Requires Manager privileges.
* `auth_token`: (Required) OAuth2 authentication token.

**Response:**

* `200 OK`: `ConversationsListResponse` containing a list of `ConversationsResponse` objects and pagination metadata.
* `401 Unauthorized`: Invalid authentication token or insufficient permissions.

### GET /conversations/{conversation_id}

Retrieves a specific conversation.

**Request Parameters:**

* `conversation_id`: (Required) ID of the conversation.

**Response:**

* `200 OK`: `ConversationsResponse` object representing the conversation.
* `404 Not Found`: Conversation not found.


### POST /conversations

Creates a new conversation.

**Request Body:**

* `conversation_in`: `Conversation` object containing conversation details.

**Response:**

* `201 Created`: `ConversationsResponse` object representing the newly created conversation.


### PUT /conversations/{conversation_id}

Updates an existing conversation.

**Request Parameters:**

* `conversation_id`: (Required) ID of the conversation to update.

**Request Body:**

* `new_conversation`: `Conversation` object containing updated conversation details.

**Response:**

* `200 OK`: `ConversationsResponse` object representing the updated conversation.
* `424 Failed Dependency`: Unable to update the conversation.


### DELETE /conversations/{conversation_id}

Deletes a conversation.

**Request Parameters:**

* `conversation_id`: (Required) ID of the conversation to delete.

**Response:**

* `200 OK`: `{"message": "success"}`


## Data Models

The API uses several data models defined in `src.db.schemas`:

* `Conversation`: Represents a conversation.
* `ConversationsListResponse`: Contains a list of conversations and pagination information.
* `ConversationsResponse`: Represents a single conversation in the response.
* `Persona`:  Represents persona information associated with a conversation.
* `PageParams`: Contains pagination parameters (totalItems, totalPages, page, size).
* `ProfileInfo`: Represents profile information associated with a conversation.


## Error Handling

The API uses `handle_error` for exception handling (implementation not shown).  Error responses typically include a status code and a descriptive message.

## Authentication

The API uses OAuth2 authentication via the `oauth2_scheme` (defined using `OAuth2PasswordBearer`).  An authentication token is required for most endpoints.  Manager roles have access to retrieve conversations for their subordinates.
