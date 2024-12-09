# Configuration Module Documentation

This module (`src/config.py`) provides configuration settings for the application, loading environment variables from `.env` files.  It uses the `pydantic-settings` library for type validation and environment variable management.


## How to Use

1. **Import:** Import the configuration object using `from src.config import config`. This makes all configuration settings accessible as a dictionary.

2. **Environment Variable:** Set the `ENV` environment variable to specify the environment ("dev" or "prod").  This determines which `.env` file is loaded.

3. **Defaults:** If the `ENV` variable is not set, the configuration defaults to the "dev" environment.

4. **Access Configuration:** Access settings using dictionary lookup (e.g., `config["DEEPGRAM_API_KEY"]`).


## Configuration Settings

The configuration settings are defined within the `BaseConfig`, `DevConfig`, and `ProdConfig` classes.  `DevConfig` and `ProdConfig` inherit from `BaseConfig` and specify the `.env` file to load.

The following settings are available:

**General Settings:**

* `ENV`:  (str) The environment ("dev" or "prod").  Defaults to "dev".
* `SUPER_ADMIN_EMAIL`: (EmailStr) Email address of the super administrator.
* `SUPER_ADMIN_PASSWORD`: (str) Password of the super administrator.
* `PROMPTS_PATH`: (DirectoryPath) Path to the prompts directory.
* `PARAMETER_SCHEMAS_PATH`: (DirectoryPath) Path to the parameter schemas directory.


**API Keys:**

* `DEEPGRAM_API_KEY`: (str) Deepgram API key.
* `OPENAI_API_KEY`: (str) OpenAI API key.
* `NUBELA_API_KEY`: (str) Nubela API key.
* `ELEVEN_LABS_API_KEY`: (str) ElevenLabs API key.
* `AZURE_SPEECH_KEY`: (str) Azure Speech API key.
* `AZURE_SPEECH_REGION`: (str) Azure Speech API region.
* `RECALL_API_KEY`: (str) Recall API key.
* `RECALL_API_BASE_URL`: (str) Recall API base URL.
* `HUBSPOT_BASE_URL`: (str) HubSpot base URL.
* `HUBSPOT_REDIRECT_URI`: (str) HubSpot redirect URI.
* `HUBSPOT_CLIENT_ID`: (str) HubSpot client ID.
* `HUBSPOT_CLIENT_SECRET`: (str) HubSpot client secret.
* `GOOGLE_CLIENT_ID`: (str) Google client ID.
* `GOOGLE_CLIENT_SECRET`: (str) Google client secret.
* `GOOGLE_TOKEN_URI`: (str) Google token URI.
* `VAPI_AUTH_TOKEN`: (str) VAPI authentication token.
* `PHONE_NUMBER_ID`: (str) Phone number ID.
* `VAPI_CALL_URL`: (str) VAPI call URL.
* `VAPI_ASSISTANT_ID`: (str) VAPI assistant ID.
* `GROQ_API`: (str) GROQ API endpoint


**Database Settings:**

* `DB_URI`: (str) Database URI.  (TODO: Change type to `AnyUrl` after pydantic update).
* `DB_NAME`: (str) Database name.


**Service URLs:**

* `NODE_BACKEND`: (str) Node backend URL. (TODO: Change type to `AnyUrl` after pydantic update).
* `ZOOM_BOT_BACKEND`: (str) Zoom bot backend URL. (TODO: Change type to `AnyUrl` after pydantic update).
* `RABBITMQ_URL`: (str) RabbitMQ URL. (TODO: Change type to `AnyUrl` after pydantic update).
* `RECALL_TRANSCRIPTION_URL`: (str) Recall transcription URL. (TODO: Change type to `AnyUrl` after pydantic update).


**OpenAI Defaults:**

* `OPENAI_DEFAULT_MODEL_NAME`: (str) Default OpenAI model name.
* `OPENAI_DEFAULT_TEMPERATURE`: (float) Default OpenAI temperature.
* `OPENAI_DEFAULT_TOP_P`: (float) Default OpenAI top_p.
* `OPENAI_DEFAULT_FREQUENCY_PENALTY`: (float) Default OpenAI frequency penalty.
* `OPENAI_DEFAULT_PRESENCE_PENALTY`: (float) Default OpenAI presence penalty.
* `OPENAI_DEFAULT_MAX_TOKENS`: (int) Default OpenAI max tokens.
* `USE_NUBELA`: (bool) Flag to use Nubela.


**Live Call Settings:**

* `LIVE_CALL_SUMMARY_MODEL_NAME`: (str) Model name for live call summarization.
* `LIVE_CALL_SUMMARY_TEMPERATURE`: (float) Temperature for live call summarization.
* `LIVE_CALL_SUMMARY_TOP_P`: (float) Top_p for live call summarization.
* `LIVE_CALL_SUMMARY_FREQUENCY_PENALTY`: (float) Frequency penalty for live call summarization.
* `LIVE_CALL_SUMMARY_PRESENCE_PENALTY`: (float) Presence penalty for live call summarization.
* `LIVE_CALL_SUMMARY_MAX_TOKENS`: (int) Max tokens for live call summarization.


**Training Call Settings:**

* `TRAINING_CALL_SUMMARY_MODEL_NAME`: (str) Model name for training call summarization.
* `TRAINING_CALL_SUMMARY_TEMPERATURE`: (float) Temperature for training call summarization.
* `TRAINING_CALL_SUMMARY_TOP_P`: (float) Top_p for training call summarization.
* `TRAINING_CALL_SUMMARY_FREQUENCY_PENALTY`: (float) Frequency penalty for training call summarization.
* `TRAINING_CALL_SUMMARY_PRESENCE_PENALTY`: (float) Presence penalty for training call summarization.
* `TRAINING_CALL_SUMMARY_MAX_TOKENS`: (int) Max tokens for training call summarization.


**Website Summary Generation Settings:**

* `WEBSITE_SUMMARY_GENERATION_MODEL_NAME`: (str) Model name for website summary generation.
* `WEBSITE_SUMMARY_GENERATION_TEMPERATURE`: (float) Temperature for website summary generation.
* `WEBSITE_SUMMARY_GENERATION_TOP_P`: (float) Top_p for website summary generation.
* `WEBSITE_SUMMARY_GENERATION_FREQUENCY_PENALTY`: (float) Frequency penalty for website summary generation.
* `WEBSITE_SUMMARY_GENERATION_PRESENCE_PENALTY`: (float) Presence penalty for website summary generation.


**LLMAgent Settings:**

* `LLMAGENT_MODEL_NAME`: (str) Model name for LLMAgent.
* `LLMAGENT_ALT_INSIGHT_PIPELINE`: (bool) Flag for alternate insight pipeline.
* `LLMAGENT_STREAM_OUTPUT`: (bool) Flag for streaming output.
* `LLMAGENT_IGNORE_AGENT_TRANSCRIPTIONS`: (bool) Flag to ignore agent transcriptions.
* `LLMAGENT_USE_SIMPLIFICATION`: (bool) Flag to use simplification.
* `LLMAGENT_PREVIOUS_INSIGHT_HANDLING`: (InsightHandling) Enum for handling previous insights.


**Note:** The `...` in the default values indicates that these values are loaded from the corresponding `.env` file.  The `Field` object handles type validation.  The `extra="ignore"` setting in the `SettingsConfigDict` prevents unknown keys in the `.env` file from raising exceptions.
