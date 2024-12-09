# prompts.py Documentation

This module handles the retrieval of prompts, either from a database or a file system.  It utilizes several other modules for database interaction, configuration, logging, and enums.

## Imports

- `os.path.join`: For constructing file paths.
- `src.db.models.Personas`: Database model for personas.
- `src.db.models.Prompts`: Database model for prompts.
- `src.db.schemas.Persona`: Schema for persona data.
- `src.enums.CallTypes`: Enum for call types.
- `src.config.config`: Configuration settings (presumably containing `PROMPTS_PATH`).
- `src.logger.Logger`: Custom logging functionality.


## Global Variables

- `logger`: An instance of the `Logger` class, specifically for logging "prompts" related events.


## Functions

### `resolve_prompt_name(promptType: str, callType: str, callScenario: str = "default", difficultyLevel: str = "default") -> str`

Constructs a prompt name string by joining the provided parameters with underscores.  This is used to uniquely identify prompts in the database.

**Parameters:**

- `promptType: str`: The type of prompt.
- `callType: str`: The type of call.
- `callScenario: str`: The call scenario (defaults to "default").
- `difficultyLevel: str`: The difficulty level (defaults to "default").

**Returns:**

- `str`: The constructed prompt name.


### `get_prompt_from_file(prompt_name: str) -> str`

Retrieves a prompt from a file located in the path specified in the configuration (`config["PROMPTS_PATH"]`).

**Parameters:**

- `prompt_name: str`: The name of the prompt file (without the extension).

**Returns:**

- `str`: The content of the prompt file.


### `get_prompt(promptType: str, callType: CallTypes, persona: Persona | Personas = defaultPersona, defaultPromptFile: str = "") -> str`

Retrieves a prompt, prioritizing the database. If not found in the database, it falls back to retrieving from a file.

**Parameters:**

- `promptType: str`: The type of prompt.
- `callType: CallTypes`: The type of call (using the `CallTypes` enum).
- `persona: Persona | Personas`: The persona associated with the prompt (defaults to `defaultPersona`).
- `defaultPromptFile: str`: The name of the default prompt file to use if the prompt is not found in the database.

**Returns:**

- `str`: The prompt text.


### `defaultPersona: Persona`

A default `Persona` object used when no persona is explicitly specified in `get_prompt`.  It's initialized with default values for all attributes.


## Usage Example

```python
from src.prompts import get_prompt
from src.enums import CallTypes
from src.db.schemas import Persona

# Retrieve a prompt from the database or file
prompt_text = get_prompt(
    promptType="greeting",
    callType=CallTypes.INCOMING,
    persona=Persona(personaName="john_doe", callScenario="sales", difficultyLevel="easy"),
    defaultPromptFile="default_greeting.txt"
)

print(prompt_text)
```
