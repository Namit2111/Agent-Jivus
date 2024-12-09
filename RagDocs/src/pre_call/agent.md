# Documentation for `chatgpt_perfectsprout_agent.py`

This file defines a custom ChatGPT agent and a conversation router for a streaming conversation application.  It extends Vocode's functionality to incorporate custom logic based on persona and conversation details retrieved from a database.

## Classes

### `ChatGPTPerfectsproutAgentConfig(ChatGPTAgentConfig)`

This class extends `ChatGPTAgentConfig` to add a `conversation_id` field and sets default values for parameters like `model_name`, `temperature`, `max_tokens`, `presence_penalty`, and `frequency_penalty`.  These defaults are based on constants defined at the top of the file.

**Attributes:**

* `conversation_id: str`:  The ID of the conversation.
* `model_name: str = CHAT_GPT_AGENT_4_MODEL_NAME`: The name of the OpenAI model to use (defaults to "gpt-4o").
* `temperature: float = LLM_AGENT_PS_TEMPERATURE`:  The temperature parameter for the LLM (defaults to 1.0).
* `max_tokens: int = LLM_AGENT_PS_MAX_TOKENS`: The maximum number of tokens for the LLM (defaults to 100).
* `presence_penalty: float = LLM_AGENT_PS_PRESENCE_PENALTY`: The presence penalty for the LLM (defaults to 0.4).
* `frequency_penalty: float = LLM_AGENT_PS_FREQUENCY_PENALTY`: The frequency penalty for the LLM (defaults to 0.2).


### `ChatGPTPerfectsproutAgent(ChatGPTAgent)`

This class extends `ChatGPTAgent` to customize the agent's behavior based on the conversation's persona. It fetches persona details from the database and adjusts the agent's parameters accordingly.  It also updates the transcript in the database after each message.


**Constructor:**

* `agent_config: ChatGPTPerfectsproutAgentConfig`: Configuration for the agent.
* `action_factory: ActionFactory = ActionFactory()`: Factory for creating actions.
* `logger: Logger | None = Logger("pre-call")`: Logger instance.
* `openai_api_key: str | None = None`: OpenAI API key.
* `vector_db_factory=VectorDBFactory()`: Factory for creating vector databases.

**Methods:**

* `update_model_config()`: Updates the agent's configuration based on the conversation's persona (difficulty level and call scenario).  It retrieves persona information from the database using `get_persona` and `get_base_conversation`.
* `get_chat_parameters(messages: List | None = None, use_functions: bool = True)`:  Overrides the base class method to update the transcript in the database using `update_transcript` if a `conversation_id` is present.


### `CustomRouter(ConversationRouter)`

This class extends `ConversationRouter` to customize the creation of `StreamingConversation`.  It adds logic to set `should_encode_as_wav` to `True` for the synthesizer and handles transcript event management based on the start message.  It also extracts the `conversationId` from the websocket query parameters.

**Methods:**

* `get_conversation(output_device: WebsocketOutputDevice, start_message: AudioConfigStartMessage) -> StreamingConversation`: Creates a `StreamingConversation` instance with customized settings.
* `async conversation(websocket: WebSocket)`:  Extracts the `conversationId` from the websocket query parameters before calling the superclass method.


## Constants

* `CHAT_GPT_AGENT_4_MODEL_NAME`:  String specifying the default model name ("gpt-4o").
* `LLM_AGENT_PS_MAX_TOKENS`: Integer specifying the default max tokens (100).
* `LLM_AGENT_PS_TEMPERATURE`: Float specifying the default temperature (1.0).
* `LLM_AGENT_PS_PRESENCE_PENALTY`: Float specifying the default presence penalty (0.4).
* `LLM_AGENT_PS_FREQUENCY_PENALTY`: Float specifying the default frequency penalty (0.2).


## Imports

The file imports necessary modules from `logging`, `typing`, `fastapi`, `vocode`, and custom modules (`src.logger`, `src.db.subroutes`).


## Dependencies

This file depends on several external libraries, including `vocode`, `fastapi`, and `openai`.  It also relies on internal modules for database interaction and logging.
