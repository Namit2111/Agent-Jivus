from vocode.streaming.models.message import BaseMessage
from vocode.streaming.synthesizer.deepgram_synthesizer import DeepgramSynthesizer
from vocode.streaming.synthesizer.stream_elements_synthesizer import (
    StreamElementsSynthesizer,
)
from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
from vocode.streaming.models.synthesizer import (
    DeepgramSynthesizerConfig,
    StreamElementsSynthesizerConfig,
)
from vocode.streaming.models.synthesizer import AzureSynthesizerConfig
from vocode.streaming.synthesizer.azure_synthesizer import AzureSynthesizer
from vocode.streaming.models.transcriber import (
    DeepgramTranscriberConfig,
    TimeEndpointingConfig,
)

from src.pre_call.agent import (
    ChatGPTPerfectsproutAgentConfig,
    ChatGPTPerfectsproutAgent,
)
from src.pre_call.utils import get_training_call_prompt
from src.config import config
from src.logger import Logger

logger = Logger("thunks")

STREAM_ELEMENTS_SYNTHESIZER_THUNK = (
    lambda output_audio_config: StreamElementsSynthesizer(
        StreamElementsSynthesizerConfig.from_output_audio_config(output_audio_config),
        logger=logger,
    )
)

AZURE_SYNTHESIZER_THUNK = lambda output_audio_config: AzureSynthesizer(
    AzureSynthesizerConfig.from_output_audio_config(output_audio_config),
    azure_speech_key=config["AZURE_SPEECH_KEY"],
    azure_speech_region=config["AZURE_SPEECH_REGION"],
    logger=logger,
)

DEEPGRAM_SYNTHESIZER_THUNK = lambda output_audio_config: DeepgramSynthesizer(
    DeepgramSynthesizerConfig.from_output_audio_config(output_audio_config),
    api_key=config["DEEPGRAM_API_KEY"],
    logger=logger,
)

CHATGPT_AGENT_THUNK = lambda conversation_id: ChatGPTPerfectsproutAgent(  # type: ignore
    ChatGPTPerfectsproutAgentConfig(
        initial_message=BaseMessage(text="Hello!"),
        prompt_preamble=get_training_call_prompt(conversation_id),
        conversation_id=conversation_id,
        generate_responses=True,
    ),
    openai_api_key=config["OPENAI_API_KEY"],
    logger=logger,
)

DEEPGRAM_TRANSCRIBER_THUNK = lambda input_audio_config: DeepgramTranscriber(
    DeepgramTranscriberConfig.from_input_audio_config(
        input_audio_config=input_audio_config,
        endpointing_config=TimeEndpointingConfig(time_cutoff_seconds=3.0),
    ),
    api_key=config["DEEPGRAM_API_KEY"],
    logger=logger,
)
