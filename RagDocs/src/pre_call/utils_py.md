# prompt_utils.py Documentation

This module provides utility functions for generating prompts for various scenarios, primarily leveraging OpenAI's API and external services like Nubela and Prospeo for data enrichment.

## Functions

### `get_linkedin_profile_nubela(linkedin_url)`

Retrieves LinkedIn profile data using the Nubela API if `config["USE_NUBELA"]` is True; otherwise, it loads sample data from a local JSON file.

**Parameters:**

* `linkedin_url (str)`: The URL of the LinkedIn profile.

**Returns:**

* `dict`:  A dictionary containing the LinkedIn profile data.

**Raises:**

* `Exception`: If the Nubela API request fails.


### `linkedin_summary_generation(url: str)`

Generates a summary of a LinkedIn profile using OpenAI's API.  It fetches profile data via `get_linkedin_profile_nubela`, constructs a prompt, and uses OpenAI's function calling capabilities to generate a structured response.

**Parameters:**

* `url (str)`: The URL of the LinkedIn profile.

**Returns:**

* `tuple`: A tuple containing:
    * `dict`: The raw LinkedIn profile data from the API.
    * `str`: The generated personality summary.
    * `str`: The generated buying style information.


### `website_summary_generation(url: str = "")`

Generates a summary of a website using OpenAI's API.  It uses `scrape_url` (from `src.utils.website_scraper`) to extract text content, constructs a prompt, and uses OpenAI's function calling to structure the output.  If no URL is provided, it uses a dummy website dump.

**Parameters:**

* `url (str, optional)`: The URL of the website. Defaults to "".

**Returns:**

* `tuple`: A tuple containing:
    * `dict`: The raw website text content.
    * `str`: The generated product description.


### `get_persona_profile_info(persona)`

Retrieves or generates profile information for a given persona.  If LinkedIn data is available, it calls `linkedin_summary_generation` to generate a summary and updates the database (`ProfileInfos`).

**Parameters:**

* `persona`: A persona object (presumably from the database).

**Returns:**

* `tuple`: A tuple containing:
    * `dict`: The raw LinkedIn profile data.
    * `str`: The generated LinkedIn summary.
    * `str`: The generated buying style information.


### `training_call_prompt_generation(persona_id, user_info: User)`

Generates a prompt for a training call based on persona and user information.  It retrieves persona and user profile information, including website and LinkedIn summaries (using previously defined functions), and fills a prompt template.

**Parameters:**

* `persona_id`: The ID of the persona.
* `user_info (User)`: A User object containing user information.

**Returns:**

* `str`: The generated training call prompt.


### `get_training_call_prompt(conversation_id: str)`

Retrieves a training call prompt from the database (`ModelInfos`) based on the conversation ID.

**Parameters:**

* `conversation_id (str)`: The ID of the conversation.

**Returns:**

* `str`: The training call prompt.


### `get_linkedin_profile_prospeo(linkedin_url)`

Retrieves LinkedIn profile data using the Prospeo API.

**Parameters:**

* `linkedin_url (str)`: The URL of the LinkedIn profile.

**Returns:**

* `dict`: The LinkedIn profile data from Prospeo API.


### `get_auth_response(auth_token: str = Depends(oauth2_scheme)) -> dict`

Authenticates a user based on the provided authentication token using `authenticate_user` from `src.db.utils`. Raises a 401 Unauthorized exception if authentication fails.

**Parameters:**

* `auth_token (str)`: The authentication token.

**Returns:**

* `dict`: The authentication response.

**Raises:**

* `HTTPException`: If authentication fails (401 Unauthorized).


## Global Variables

* `logger`: A Logger instance for logging.
* `openai.api_key`:  The OpenAI API key, loaded from the config.


## Dependencies

This module depends on several other modules within the project, including:

* `json`
* `fastapi`
* `openai`
* `requests`
* `os.path`
* `src.db.schemas`
* `src.db.utils`
* `src.logger`
* `src.config`
* `src.enums`
* `src.utils.prompts`
* `src.utils.website_scraper`
* `src.utils.prompt_formatter`
* `src.db.subroutes.personas`
* `src.db.models`


This documentation provides a comprehensive overview of the `prompt_utils.py` module's functionality.  Remember to consult the linked modules for further details on their respective functions and classes.
