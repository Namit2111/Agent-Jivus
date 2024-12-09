from logging import Logger
from typing import List
from fastapi import WebSocket
from vocode.streaming.action.factory import ActionFactory
from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent, ChatGPTAgentConfig
from vocode.streaming.models.websocket import AudioConfigStartMessage
from vocode.streaming.output_device.websocket_output_device import WebsocketOutputDevice
from vocode.streaming.streaming_conversation import StreamingConversation
from vocode.streaming.telephony import conversation
from vocode.streaming.vector_db.factory import VectorDBFactory
from src.logger import Logger
from src.db.subroutes.transcripts import update_transcript
from src.db.subroutes.personas import get_persona
from src.db.subroutes.conversations import get_base_conversation
from vocode.streaming.client_backend.conversation import ConversationRouter
from vocode.streaming.client_backend.conversation import TranscriptEventManager
from vocode.streaming.agent.utils import format_openai_chat_messages_from_transcript

CHAT_GPT_AGENT_4_MODEL_NAME = "gpt-4o"
LLM_AGENT_PS_MAX_TOKENS = 100
LLM_AGENT_PS_TEMPERATURE = 1.0
LLM_AGENT_PS_PRESENCE_PENALTY = 0.4
LLM_AGENT_PS_FREQUENCY_PENALTY = 0.2


class ChatGPTPerfectsproutAgentConfig(ChatGPTAgentConfig):
    conversation_id: str
    model_name: str = CHAT_GPT_AGENT_4_MODEL_NAME
    temperature: float = LLM_AGENT_PS_TEMPERATURE
    max_tokens: int = LLM_AGENT_PS_MAX_TOKENS
    presence_penalty: float = LLM_AGENT_PS_PRESENCE_PENALTY
    frequency_penalty: float = LLM_AGENT_PS_FREQUENCY_PENALTY


class ChatGPTPerfectsproutAgent(ChatGPTAgent):
    def __init__(
        self,
        agent_config: ChatGPTPerfectsproutAgentConfig,
        action_factory: ActionFactory = ActionFactory(),
        logger: Logger | None = Logger("pre-call"),
        openai_api_key: str | None = None,
        vector_db_factory=VectorDBFactory(),
    ):
        self.agent_config = agent_config
        super().__init__(
            agent_config, action_factory, logger, openai_api_key, vector_db_factory
        )
        if self.agent_config.conversation_id:
            self.update_model_config()
    
    def update_model_config(self):
        conversation = get_base_conversation(conversation_id=self.agent_config.conversation_id)
        persona = get_persona(persona_id=conversation.persona.id)
        if persona.difficultyLevel == "Hard" and persona.callScenario == "cold call":
            self.agent_config.temperature = 1.1
            self.agent_config.frequency_penalty = 0.2
            self.agent_config.presence_penalty = 0.4
        elif persona.callScenario == "cold call":
            self.agent_config.temperature = 1.2
            self.agent_config.frequency_penalty = 0.5
            self.agent_config.presence_penalty = 0.5

    def get_chat_parameters(
        self, messages: List | None = None, use_functions: bool = True
    ):
        assert self.transcript is not None
        messages = messages or format_openai_chat_messages_from_transcript(
            self.transcript, self.agent_config.prompt_preamble
        )
        if self.agent_config.conversation_id:            
            if messages:
                update_transcript(messages, self.agent_config.conversation_id)
        return super().get_chat_parameters(messages, use_functions)


class CustomRouter(ConversationRouter):
    def get_conversation(
        self,
        output_device: WebsocketOutputDevice,
        start_message: AudioConfigStartMessage,
    ) -> StreamingConversation:
        transcriber = self.transcriber_thunk(start_message.input_audio_config)
        synthesizer = self.synthesizer_thunk(start_message.output_audio_config)
        synthesizer.synthesizer_config.should_encode_as_wav = True
        return StreamingConversation(
            output_device=output_device,
            transcriber=transcriber,
            agent=self.agent_thunk(self.conversationId),  # type: ignore
            synthesizer=synthesizer,
            conversation_id=start_message.conversation_id,
            events_manager=(
                TranscriptEventManager(output_device, self.logger)
                if start_message.subscribe_transcript
                else None
            ),
            logger=self.logger,
        )

    async def conversation(self, websocket: WebSocket):
        self.conversationId = websocket.query_params["conversationId"]
        return await super().conversation(websocket)
