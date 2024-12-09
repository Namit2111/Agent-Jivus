"""
How to Use:
1. Use `from src.config import config` in any file that requires .env variables.
2. Set "ENV" variable in the console/terminal/cmd to choose which .env is loaded.
3. Valid "ENV" values = "dev" | "prod"
3. Defaults to using dev.
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl, EmailStr, Field, DirectoryPath

from src.live_call.enums import InsightHandling


class BaseConfig(BaseSettings):
    # Environment
    ENV: str = os.environ.get("ENV", "dev").lower()

    # API Keys
    DEEPGRAM_API_KEY: str = Field(default=...)
    OPENAI_API_KEY: str = Field(default=...)
    NUBELA_API_KEY: str = Field(default=...)
    ELEVEN_LABS_API_KEY: str = Field(default=...)
    AZURE_SPEECH_KEY: str = Field(default=...)
    AZURE_SPEECH_REGION: str = Field(default=...)
    RECALL_API_KEY: str = Field(default=...)
    RECALL_API_BASE_URL: str = Field(default=...)

    HUBSPOT_BASE_URL: str = Field(default=...)
    HUBSPOT_REDIRECT_URI: str = Field(default=...)
    HUBSPOT_CLIENT_ID: str = Field(default=...)
    HUBSPOT_CLIENT_SECRET: str = Field(default=...)
    
    GOOGLE_CLIENT_ID: str = Field(default=...)
    GOOGLE_CLIENT_SECRET: str = Field(default=...)
    GOOGLE_TOKEN_URI: str = Field(default=...)
    
    # DB
    DB_URI: str = Field(
        default=...
    )  # TODO: change type to AnyUrl, after pydantic update
    DB_NAME: str = Field(default=...)

    # Services URLs
    NODE_BACKEND: str = Field(
        default=...
    )  # TODO: change type to AnyUrl, after pydantic update
    ZOOM_BOT_BACKEND: str = Field(
        default=...
    )  # TODO: change type to AnyUrl, after pydantic update
    RABBITMQ_URL: str = Field(
        default=...
    )  # TODO: change type to AnyUrl, after pydantic update
    RECALL_TRANSCRIPTION_URL: str = Field(
        default=...
    )  # TODO: change type to AnyUrl, after pydantic update

    # Super Admin
    SUPER_ADMIN_EMAIL: EmailStr = Field(default=...)
    SUPER_ADMIN_PASSWORD: str = Field(default=...)

    # Paths
    PROMPTS_PATH: DirectoryPath = Field(default=...)
    PARAMETER_SCHEMAS_PATH: DirectoryPath = Field(default=...)

    # Defaults
    OPENAI_DEFAULT_MODEL_NAME: str = Field(default=...)
    OPENAI_DEFAULT_TEMPERATURE: float = Field(default=...)
    OPENAI_DEFAULT_TOP_P: float = Field(default=...)
    OPENAI_DEFAULT_FREQUENCY_PENALTY: float = Field(default=...)
    OPENAI_DEFAULT_PRESENCE_PENALTY: float = Field(default=...)
    OPENAI_DEFAULT_MAX_TOKENS: int = Field(default=...)
    USE_NUBELA: bool = Field(default=...)
    
    # Live Call
    LIVE_CALL_SUMMARY_MODEL_NAME: str = Field(default=...)
    LIVE_CALL_SUMMARY_TEMPERATURE: float = Field(default=...)
    LIVE_CALL_SUMMARY_TOP_P: float = Field(default=...)
    LIVE_CALL_SUMMARY_FREQUENCY_PENALTY: float = Field(default=...)
    LIVE_CALL_SUMMARY_PRESENCE_PENALTY: float = Field(default=...)
    LIVE_CALL_SUMMARY_MAX_TOKENS: int = Field(default=...)

    # Training Call
    TRAINING_CALL_SUMMARY_MODEL_NAME: str = Field(default=...)
    TRAINING_CALL_SUMMARY_TEMPERATURE: float = Field(default=...)
    TRAINING_CALL_SUMMARY_TOP_P: float = Field(default=...)
    TRAINING_CALL_SUMMARY_FREQUENCY_PENALTY: float = Field(default=...)
    TRAINING_CALL_SUMMARY_PRESENCE_PENALTY: float = Field(default=...)
    TRAINING_CALL_SUMMARY_MAX_TOKENS: int = Field(default=...)

    # Training Call
    WEBSITE_SUMMARY_GENERATION_MODEL_NAME: str = Field(default=...)
    WEBSITE_SUMMARY_GENERATION_TEMPERATURE: float = Field(default=...)
    WEBSITE_SUMMARY_GENERATION_TOP_P: float = Field(default=...)
    WEBSITE_SUMMARY_GENERATION_FREQUENCY_PENALTY: float = Field(default=...)
    WEBSITE_SUMMARY_GENERATION_PRESENCE_PENALTY: float = Field(default=...)

    # LLMAgent Config
    LLMAGENT_MODEL_NAME: str = Field(default=...)
    LLMAGENT_ALT_INSIGHT_PIPELINE: bool = Field(default=...)
    LLMAGENT_STREAM_OUTPUT: bool = Field(default=...)
    LLMAGENT_IGNORE_AGENT_TRANSCRIPTIONS: bool = Field(default=...)
    LLMAGENT_USE_SIMPLIFICATION: bool = Field(default=...)
    LLMAGENT_PREVIOUS_INSIGHT_HANDLING: InsightHandling = Field(default=...)

    # AI Agent Config
    VAPI_AUTH_TOKEN: str = Field(default=...)
    PHONE_NUMBER_ID: str = Field(default=...)
    VAPI_CALL_URL: str = Field(default=...)
    VAPI_ASSISTANT_ID: str = Field(default=...)
    GROQ_API: str = Field(default=...)


class DevConfig(BaseConfig):
    model_config = SettingsConfigDict(env_file="env/.env.dev", extra="ignore")


class ProdConfig(BaseConfig):
    model_config = SettingsConfigDict(env_file="env/.env.prod", extra="ignore")


configs = {"dev": DevConfig, "prod": ProdConfig}

config = configs[os.environ.get("ENV", "dev").lower()]().model_dump()
