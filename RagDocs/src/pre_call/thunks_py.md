# Thunks for Synthesizers, Transcribers, and Agents

This Python module defines several "thunk" functions, which are essentially functions that return other functions.  These thunks create and configure instances of various speech synthesis, transcription, and agent classes, abstracting away the configuration details.  This promotes code reusability and cleaner code structure.


## Imports

The module begins by importing necessary classes and functions from various Vocode and local modules:

* `vocode.streaming.models.message`:  For the `BaseMessage` class.
* `vocode.streaming.synthesizer.*`: For synthesizer classes and configurations (`DeepgramSynthesizer`, `StreamElementsSynthesizer`, `AzureSynthesizer`, `DeepgramSynthesizerConfig`, `StreamElementsSynthesizerConfig`, `AzureSynthesizerConfig`).
* `vocode.streaming.transcriber.*`: For transcriber classes and configurations (`DeepgramTranscriber`, `DeepgramTranscriberConfig`, `TimeEndpointingConfig`).
* `src.pre_call.agent`: For the `ChatGPTPerfectsproutAgent` and its configuration.
* `src.pre_call.utils`: For the `get_training_call_prompt` function.
* `src.config`: For configuration parameters loaded from a config file.
* `src.logger`: For logging.


## Logger Initialization

A logger instance is created using `Logger("thunks")`:

```python
logger = Logger("thunks")
```


## Thunk Functions

The core of the module consists of several thunk functions, each creating and configuring a specific component:

### Synthesizer Thunks

* **`STREAM_ELEMENTS_SYNTHESIZER_THUNK`**: Creates a `StreamElementsSynthesizer` instance.  It takes an `output_audio_config` as input and uses it to create a `StreamElementsSynthesizerConfig`. The logger is also passed in for logging purposes.

* **`AZURE_SYNTHESIZER_THUNK`**: Creates an `AzureSynthesizer` instance. It takes an `output_audio_config` and utilizes it to generate an `AzureSynthesizerConfig`. It also requires `azure_speech_key` and `azure_speech_region` from the `config` object.  The logger is passed for logging.

* **`DEEPGRAM_SYNTHESIZER_THUNK`**: Creates a `DeepgramSynthesizer` instance. Similar to the others, it takes `output_audio_config`, creates a `DeepgramSynthesizerConfig`, and uses the `DEEPGRAM_API_KEY` from the `config` object. The logger is included for logging.


### Agent Thunk

* **`CHATGPT_AGENT_THUNK`**: Creates a `ChatGPTPerfectsproutAgent` instance.  It takes a `conversation_id` as input, uses it to construct a `ChatGPTPerfectsproutAgentConfig` (including an initial message and a prompt preamble obtained via `get_training_call_prompt`), and requires `OPENAI_API_KEY` from the `config` object.  The logger is passed for logging.


### Transcriber Thunk

* **`DEEPGRAM_TRANSCRIBER_THUNK`**: Creates a `DeepgramTranscriber` instance. It takes an `input_audio_config` and uses it to create a `DeepgramTranscriberConfig`, including a `TimeEndpointingConfig` with a 3-second time cutoff. The `DEEPGRAM_API_KEY` from the `config` object is also required.  The logger is used for logging.


## Configuration

The thunks rely on configuration parameters read from `src.config`, specifically:

* `config["AZURE_SPEECH_KEY"]`
* `config["AZURE_SPEECH_REGION"]`
* `config["DEEPGRAM_API_KEY"]`
* `config["OPENAI_API_KEY"]`


## Usage Example

The thunks are designed to be used to easily create and configure instances of the respective classes.  For example:

```python
synthesizer = DEEPGRAM_SYNTHESIZER_THUNK(some_output_audio_config)()
```

This would create a configured `DeepgramSynthesizer` instance.  The double parentheses are needed because the thunk returns a function that needs to be called to get the actual instance.
