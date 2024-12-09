# src/config.py Documentation

This module handles loading configuration settings from `.env` files based on the environment.  It utilizes the `pydantic-settings` library for type validation and environment variable management.


## How to Use

1. **Import:**  Import the `config` object into any file needing access to configuration values:

   ```python
   from src.config import config
   ```

2. **Environment Variable:** Set the `ENV` environment variable to select the `.env` file to load:

   - `ENV=dev`: Loads settings from `env/.env.dev`.
   - `ENV=prod`: Loads settings from `env/.env.prod`.

3. **Default:** If `ENV` is not set, it defaults to `dev`.


## Configuration Settings

The configuration is structured using Pydantic's `BaseSettings` for type validation.  The following settings are available, with their respective types:


| Setting                      | Type                     | Description                                                                     |
|-------------------------------|--------------------------|---------------------------------------------------------------------------------|
| `ENV`                         | `str`                    | Environment ('dev' or 'prod').                                                  |
| `DEEPGRAM_API_KEY`           | `str`                    | Deepgram API key.                                                              |
| `OPENAI_API_KEY`             | `str`                    | OpenAI API key.                                                                |
| `NUBELA_API_KEY`             | `str`                    | Nubela API key.                                                                |
| `ELEVEN_LABS_API_KEY`        | `str`                    | Eleven Labs API key.                                                            |
| `AZURE_SPEECH_KEY`           | `str`                    | Azure Speech key.                                                              |
| `AZURE_SPEECH_REGION`        | `str`                    | Azure Speech region.                                                            |
| `RECALL_API_KEY`             | `str`                    | Recall API key.                                                                |
| `RECALL_API_BASE_URL`        | `str`                    | Recall API base URL.                                                            |
| `HUBSPOT_BASE_URL`           | `str`                    | HubSpot base URL.                                                              |
| `HUBSPOT_REDIRECT_URI`       | `str`                    | HubSpot redirect URI.                                                           |
| `HUBSPOT_CLIENT_ID`          | `str`                    | HubSpot client ID.                                                             |
| `HUBSPOT_CLIENT_SECRET`      | `str`                    | HubSpot client secret.                                                          |
| `GOOGLE_CLIENT_ID`          | `str`                    | Google Client ID.                                                              |
| `GOOGLE_CLIENT_SECRET`       | `str`                    | Google Client Secret.                                                           |
| `GOOGLE_TOKEN_URI`           | `str`                    | Google Token URI.                                                              |
| `DB_URI`                     | `str`                    | Database URI.  (TODO: Change to `AnyUrl` after pydantic update)                 |
| `DB_NAME`                    | `str`                    | Database name.                                                                 |
| `NODE_BACKEND`               | `str`                    | Node backend URL. (TODO: Change to `AnyUrl` after pydantic update)             |
| `ZOOM_BOT_BACKEND`           | `str`                    | Zoom bot backend URL. (TODO: Change to `AnyUrl` after pydantic update)         |
| `RABBITMQ_URL`               | `str`                    | RabbitMQ URL. (TODO: Change to `AnyUrl` after pydantic update)                 |
| `RECALL_TRANSCRIPTION_URL`   | `str`                    | Recall transcription URL. (TODO: Change to `AnyUrl` after pydantic update)     |
| `SUPER_ADMIN_EMAIL`          | `EmailStr`               | Super admin email address.                                                       |
| `SUPER_ADMIN_PASSWORD`       | `str`                    | Super admin password.                                                           |
| `PROMPTS_PATH`               | `DirectoryPath`          | Path to prompts directory.                                                      |
| `PARAMETER_SCHEMAS_PATH`     | `DirectoryPath`          | Path to parameter schemas directory.                                             |
| `OPENAI_DEFAULT_MODEL_NAME`  | `str`                    | Default OpenAI model name.                                                      |
| `OPENAI_DEFAULT_TEMPERATURE` | `float`                  | Default OpenAI temperature.                                                     |
| `OPENAI_DEFAULT_TOP_P`       | `float`                  | Default OpenAI top_p.                                                           |
| `OPENAI_DEFAULT_FREQUENCY_PENALTY` | `float` | Default OpenAI frequency penalty.                                                |
| `OPENAI_DEFAULT_PRESENCE_PENALTY` | `float` | Default OpenAI presence penalty.                                                |
| `OPENAI_DEFAULT_MAX_TOKENS`  | `int`                    | Default OpenAI max tokens.                                                      |
| `USE_NUBELA`                 | `bool`                   | Whether to use Nubela.                                                          |
| `LIVE_CALL_SUMMARY_MODEL_NAME` | `str` | Model name for live call summarization.                                         |
| `LIVE_CALL_SUMMARY_TEMPERATURE` | `float` | Temperature for live call summarization.                                        |
| `LIVE_CALL_SUMMARY_TOP_P`    | `float` | Top P for live call summarization.                                             |
| `LIVE_CALL_SUMMARY_FREQUENCY_PENALTY` | `float` | Frequency penalty for live call summarization.                                  |
| `LIVE_CALL_SUMMARY_PRESENCE_PENALTY` | `float` | Presence penalty for live call summarization.                                   |
| `LIVE_CALL_SUMMARY_MAX_TOKENS` | `int` | Max tokens for live call summarization.                                         |
| `TRAINING_CALL_SUMMARY_MODEL_NAME` | `str` | Model name for training call summarization.                                     |
| `TRAINING_CALL_SUMMARY_TEMPERATURE` | `float` | Temperature for training call summarization.                                    |
| `TRAINING_CALL_SUMMARY_TOP_P` | `float` | Top P for training call summarization.                                          |
| `TRAINING_CALL_SUMMARY_FREQUENCY_PENALTY` | `float` | Frequency penalty for training call summarization.                              |
| `TRAINING_CALL_SUMMARY_PRESENCE_PENALTY` | `float` | Presence penalty for training call summarization.                               |
| `TRAINING_CALL_SUMMARY_MAX_TOKENS` | `int` | Max tokens for training call summarization.                                     |
| `WEBSITE_SUMMARY_GENERATION_MODEL_NAME` | `str` | Model name for website summary generation.                                       |
| `WEBSITE_SUMMARY_GENERATION_TEMPERATURE` | `float` | Temperature for website summary generation.                                      |
| `WEBSITE_SUMMARY_GENERATION_TOP_P` | `float` | Top P for website summary generation.                                           |
| `WEBSITE_SUMMARY_GENERATION_FREQUENCY_PENALTY` | `float` | Frequency penalty for website summary generation.                               |
| `WEBSITE_SUMMARY_GENERATION_PRESENCE_PENALTY` | `float` | Presence penalty for website summary generation.                                |
| `LLMAGENT_MODEL_NAME` | `str` | Model name for LLMAgent.                                                       |
| `LLMAGENT_ALT_INSIGHT_PIPELINE` | `bool` | Use alternative insight pipeline for LLMAgent.                                 |
| `LLMAGENT_STREAM_OUTPUT` | `bool` | Stream output for LLMAgent.                                                    |
| `LLMAGENT_IGNORE_AGENT_TRANSCRIPTIONS` | `bool` | Ignore agent transcriptions for LLMAgent.                                      |
| `LLMAGENT_USE_SIMPLIFICATION` | `bool` | Use simplification for LLMAgent.                                               |
| `LLMAGENT_PREVIOUS_INSIGHT_HANDLING` | `InsightHandling` | Previous insight handling for LLMAgent.                                      |
| `VAPI_AUTH_TOKEN` | `str` | VAPI authentication token.                                                    |
| `PHONE_NUMBER_ID` | `str` | Phone number ID.                                                              |
| `VAPI_CALL_URL` | `str` | VAPI call URL.                                                              |
| `VAPI_ASSISTANT_ID` | `str` | VAPI assistant ID.                                                            |
| `GROQ_API` | `str` | GROQ API endpoint.                                                          |


**Note:**  The `...` indicates values that should be set in the respective `.env` files.


The `config` object is a dictionary containing the loaded settings.  Access settings using standard dictionary access:  `config["OPENAI_API_KEY"]`.


## Classes

- **`BaseConfig(BaseSettings)`:** Base configuration class defining the settings.
- **`DevConfig(BaseConfig)`:** Configuration for the development environment.
- **`ProdConfig(BaseConfig)`:** Configuration for the production environment.


