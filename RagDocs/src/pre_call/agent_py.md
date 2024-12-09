# Vocode Custom Agent and Router Documentation

This document describes custom classes extending Vocode's streaming capabilities, specifically a custom agent and router for handling conversations.

## 1. Constants

```python
CHAT_GPT_AGENT_4_MODEL_NAME = "gpt-4o"
LLM_AGENT_PS_MAX_TOKENS = 100
LLM_AGENT_PS_TEMPERATURE = 1.0
LLM_AGENT_PS_PRESENCE_PENALTY = 0.4
LLM_AGENT_PS_FREQUENCY_PENALTY = 0.2
```

These constants define default parameters for the ChatGPT agent, including the model name, maximum tokens, temperature, presence penalty, and frequency penalty.


## 2. `ChatGPTPerfectsproutAgentConfig` Class

```python
class ChatGPTPerfectsproutAgentConfig(ChatGPTAgentConfig):
    conversation_id: str
    model_name: str = CHAT_GPT_AGENT_4_MODEL_NAME
    temperature: float = LLM_AGENT_PS_TEMPERATURE
    max_tokens: int = LLM_AGENT_PS_MAX_TOKENS
    presence_penalty: float = LLM_AGENT_PS_PRESENCE_PENALTY
    frequency_penalty: float = LLM_AGENT_PS_FREQUENCY_PENALTY
```

This class extends `ChatGPTAgentConfig` to include a `conversation_id` and overrides default parameters for temperature, max_tokens, presence_penalty, and frequency_penalty.  It provides configuration settings for the `ChatGPTPerfectsproutAgent`.


## 3. `ChatGPTPerfectsproutAgent` Class

```python
class ChatGPTPerfectsproutAgent(ChatGPTAgent):
    def __init__(
        self,
        agent_config: ChatGPTPerfectsproutAgentConfig,
        action_factory: ActionFactory = ActionFactory(),
        logger: Logger | None = Logger("pre-call"),
        openai_api_key: str | None = None,
        vector_db_factory=VectorDBFactory(),
    ):
        # ... (Initialization logic) ...

    def update_model_config(self):
        # Fetches conversation and persona details from the database to adjust agent parameters based on difficulty and scenario.
        # Modifies agent_config parameters based on persona data.

    def get_chat_parameters(
        self, messages: List | None = None, use_functions: bool = True
    ):
        # ... (Logic to format messages and update transcript in DB) ...
```

This class extends `ChatGPTAgent`.  The `__init__` method initializes the agent with a configuration, action factory, logger, OpenAI API key, and vector database factory.  The `update_model_config` method dynamically adjusts agent parameters (temperature, frequency_penalty, presence_penalty) based on the conversation's persona difficulty and scenario fetched from a database.  The `get_chat_parameters` method formats messages for OpenAI and updates the transcript in the database.


## 4. `CustomRouter` Class

```python
class CustomRouter(ConversationRouter):
    def get_conversation(
        self,
        output_device: WebsocketOutputDevice,
        start_message: AudioConfigStartMessage,
    ) -> StreamingConversation:
        # ... (Creates and returns a StreamingConversation instance) ...

    async def conversation(self, websocket: WebSocket):
        # Extracts conversationId from websocket query parameters and calls the parent class's conversation method.
        self.conversationId = websocket.query_params["conversationId"]
        return await super().conversation(websocket)
```

This class extends `ConversationRouter`. The `get_conversation` method creates a `StreamingConversation` object, customizing the synthesizer to encode audio as WAV. The `conversation` method extracts the `conversationId` from the websocket query parameters and then calls the parent class's `conversation` method.


## 5. Dependencies

The code relies on several external libraries:

* `logging`
* `typing`
* `fastapi`
* `vocode` (various modules)
* Custom modules: `src.logger`, `src.db.subroutes.transcripts`, `src.db.subroutes.personas`, `src.db.subroutes.conversations`


This documentation provides a comprehensive overview of the custom agent and router classes, highlighting their functionality and dependencies.  Further details on the internal logic of the methods can be found within the code itself.
