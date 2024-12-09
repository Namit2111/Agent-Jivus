# pre-call API Documentation

This document outlines the functionality of the `/v1/pre-call` API endpoints.  This API appears to handle pre-call setup and LinkedIn data fetching for a conversational AI system.


## TODO:

* Remove usage of mongo models and package them to `db` folder and call via functions.


## Imports:

The API uses the following libraries:

* `fastapi`: For building the API.
* `pydantic`: For data validation.
* `src.db.subroutes.conversations`: For creating conversations (database interaction).
* `src.db.schemas`: For defining data schemas (Conversation, LinkedInInfo, Persona, User).
* `src.db.subroutes.personas`: For retrieving personas (database interaction).
* `src.db.subroutes.profile_info`: For patching LinkedIn profile information (database interaction).
* `src.pre_call.schemas`: For defining request schemas (ConversationCreateReq).
* `src.enums`: For enums (likely CallTypes).
* `src.db.models`: For database models (ModelInfos).
* `src.pre_call.agent`: For custom routing logic (CustomRouter).
* `src.logger`: For logging.
* `src.pre_call.utils`: For utility functions (get_auth_response, linkedin_summary_generation, training_call_prompt_generation).
* `src.pre_call.thunks`: For asynchronous operations (transcriber, agent, synthesizer).


## Endpoints:

### `/v1/pre-call/setup` (POST)

**Description:** Sets up a new conversation.

**Request Body:**

* `conversation`:  `ConversationCreateReq` object (details not provided in the snippet but likely includes `conversationId` and `personaId`).

**Authentication:**  Uses `get_auth_response` dependency to authenticate the user.

**Response:**

* On success: `{"conversationId": str(conversation_obj.conversationId)}`
* On failure (401 Unauthorized):  "Persona does not belong to the user"
* On failure (500 Internal Server Error):  Detailed error message.

**Logic:**

1. Retrieves the user ID from the authentication response.
2. Retrieves the persona using `get_persona(conversation.personaId)`.
3. Verifies that the persona belongs to the user.
4. Generates a training call prompt using `training_call_prompt_generation`.
5. Creates a new conversation object.
6. Creates a `ModelInfos` object and saves it.
7. Returns the conversation ID.

### `/v1/pre-call/fetch_linkedin` (POST)

**Description:** Fetches LinkedIn information and updates the profile.

**Request Parameters:**

* `linkedinUrl`:  The URL of the LinkedIn profile.
* `profile_id`: The ID of the profile to update.

**Response:**

* On success: `{"response": response, "summary": summary}`
* On failure (500 Internal Server Error): Detailed error message.


**Logic:**

1. Uses `linkedin_summary_generation(linkedinUrl)` to fetch LinkedIn data and generate a summary.
2. Creates a `LinkedInInfo` object.
3. Updates the profile using `patch_profile_linkedin`.
4. Returns the LinkedIn response and summary.


## Internal Components:

* **CustomRouter:**  A custom router likely managing the integration of different components (transcriber, agent, synthesizer).
* **Thunks:** Asynchronous functions for transcribing audio (`DEEPGRAM_TRANSCRIBER_THUNK`), using a conversational AI agent (`CHATGPT_AGENT_THUNK`), and synthesizing speech (`AZURE_SYNTHESIZER_THUNK`).
* **Logger:** A custom logger for logging events.


This documentation provides a high-level overview.  More detailed information on schemas and specific error handling is needed for complete understanding.  The TODO item highlights a crucial refactoring step to improve the code's organization and maintainability.
