# prompts.py

This module handles the retrieval of prompts, prioritizing database lookups over default files.

## Functions

### `resolve_prompt_name(promptType: str, callType: str, callScenario: str = "default", difficultyLevel: str = "default") -> str`

Constructs a prompt name by joining the provided parameters with underscores.  Used to uniquely identify prompts.

* **Parameters:**
    * `promptType: str`: The type of prompt.
    * `callType: str`: The type of call.
    * `callScenario: str`: The call scenario (defaults to "default").
    * `difficultyLevel: str`: The difficulty level (defaults to "default").
* **Returns:**
    * `str`: The constructed prompt name.


### `get_prompt_from_file(prompt_name: str) -> str`

Reads a prompt from a file located in the directory specified by `config["PROMPTS_PATH"]`.

* **Parameters:**
    * `prompt_name: str`: The name of the prompt file (without extension).
* **Returns:**
    * `str`: The content of the prompt file.


### `get_prompt(promptType: str, callType: CallTypes, persona: Persona | Personas = defaultPersona, defaultPromptFile: str = "") -> str`

Retrieves a prompt, first checking the database and falling back to a default file if not found.

* **Parameters:**
    * `promptType: str`: The type of prompt.
    * `callType: CallTypes`: The type of call (using the `CallTypes` enum).
    * `persona: Persona | Personas`: The persona associated with the prompt (defaults to `defaultPersona`).
    * `defaultPromptFile: str`: The name of the default prompt file (used if no database entry is found).
* **Returns:**
    * `str`: The prompt text.  Returns the content from the database if found, otherwise reads from the specified default file.


## Variables

### `logger: Logger`

An instance of the `Logger` class for logging messages.  Initialized with the name "prompts".

### `defaultPersona: Persona`

A default `Persona` object used when no persona is explicitly provided to `get_prompt`.


## Imports

* `os.path`: Used for `join` to construct file paths.
* `src.db.models`: Imports `Personas` and `Prompts` database models.
* `src.db.schemas`: Imports the `Persona` schema.
* `src.enums`: Imports `CallTypes`.
* `src.config`: Imports the `config` object (presumably containing configuration settings).
* `src.logger`: Imports the `Logger` class.


## Notes

The function uses the `config["PROMPTS_PATH"]` variable to locate prompt files.  Ensure this is correctly configured.  The database interaction suggests the use of a database like MongoDB.  Error handling is basic; more robust error handling might be beneficial in a production environment.
