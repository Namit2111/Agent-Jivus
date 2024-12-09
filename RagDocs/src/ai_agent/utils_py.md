# Python Documentation: LinkedIn & Website Summary Extraction

This Python script utilizes several APIs (OpenAI, Nebula, Groq) and libraries (requests, BeautifulSoup) to extract and summarize information from LinkedIn profiles and websites.  It leverages a caching mechanism to avoid redundant API calls.

## Modules Imported

* `requests`: For making HTTP requests.
* `groq`: For interacting with the Groq API (likely a large language model).
* `bs4 (BeautifulSoup)`: For parsing HTML content.
* `json`: For working with JSON data.
* `src.ai_agent.config`:  A custom module containing API keys and other configurations (HEADERS, NEBULA_API, OPENAI_API_KEY, GROQ_API).
* `openai`: For interacting with the OpenAI API.
* `src.utils.prompts`:  A custom module for loading prompts from files (presumably `.txt` files).
* `os`: For interacting with the operating system (checking file existence).
* `src.utils.prompt_formatter`: A custom module (likely for formatting prompts).


## Functions

### 1. `check_linkedin_json(url)`

Checks if a LinkedIn profile summary for a given URL already exists in `linkedinSummaryAiagent.json`.

* **Args:**
    * `url`: The LinkedIn profile URL (str).
* **Returns:**
    * A tuple: `(bool, str)` where the boolean indicates if the summary exists, and the string is the summary if it exists, otherwise `None`.

### 2. `check_website_json(url)`

Checks if a website summary for a given URL already exists in `websiteSummaryAiagent.json`.

* **Args:**
    * `url`: The website URL (str).
* **Returns:**
    * A tuple: `(bool, dict)` where the boolean indicates if the summary exists, and the dictionary is the summary if it exists, otherwise `None`.


### 3. `get_linkedin_profile_nubela(linkedin_url)`

Retrieves LinkedIn profile data using the Nebula API.

* **Args:**
    * `linkedin_url`: The LinkedIn profile URL (str).
* **Returns:**
    * A dictionary containing the LinkedIn profile data from the Nebula API response.  Raises an exception if the API call fails.


### 4. `get_linkedin_summary(url)`

Extracts a summary of a LinkedIn profile using OpenAI's API.  Caches summaries in `linkedinSummaryAiagent.json`.

* **Args:**
    * `url`: The LinkedIn profile URL (str).
* **Returns:**
    * A string containing the summarized LinkedIn profile information.


### 5. `extract_text_from_website(url)`

Extracts text content from a website, removing script and style elements.  Includes a user agent header to improve access.

* **Args:**
    * `url`: The website URL (str).
* **Returns:**
    * A string containing the extracted text from the website.


### 6. `get_website_summary(url)`

Extracts and summarizes information from a website using OpenAI's API. Caches summaries in `websiteSummaryAiagent.json`.

* **Args:**
    * `url`: The website URL (str).
* **Returns:**
    * A dictionary containing the extracted product name and description.


### 7. `get_calls()`

Retrieves data from "https://api.vapi.ai/call" using the HEADERS.  The purpose of this function is unclear without more context on `vapi.ai`.

* **Returns:**
    * The response object from the requests.get call.


### 8. `llama_chat_json(prompt)`

Sends a prompt to the Groq API using the `llama-3.2-1b-preview` model and expects a JSON object response.

* **Args:**
    * `prompt`: The prompt to send to the LLM.
* **Returns:**
    * The content of the response (JSON object).


### 9. `llama_chat(prompt)`

Sends a prompt to the Groq API using the `llama-3.2-3b-preview` model.

* **Args:**
    * `prompt`: The prompt to send to the LLM.
* **Returns:**
    * The content of the response (string).


## Configuration

The script relies on configuration values from `src.ai_agent.config`, including API keys and other parameters.  These should be properly set for the script to function correctly.

##  Prompts

The script uses prompts loaded from files (e.g., `linkedin_summary_prompt.txt`, `website_summary_prompt.txt`) located in the `prompts` directory (relative path assumed).  These prompts are crucial for guiding the OpenAI model's response generation.


## Error Handling

The script includes basic error handling for API calls (checking response codes), but more robust error handling might be beneficial in a production environment.


## File Handling

The script manages JSON files (`linkedinSummaryAiagent.json`, `websiteSummaryAiagent.json`) for caching summaries.  It handles file creation and updates appropriately.
