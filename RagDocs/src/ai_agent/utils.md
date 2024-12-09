# Python Documentation: AI Agent Functions

This Python file contains functions for interacting with various APIs (LinkedIn, OpenAI, Groq), extracting website text, and generating summaries.  It leverages libraries like `requests`, `BeautifulSoup`, `openai`, and `groq`.

## Table of Contents

* [Import Statements](#import-statements)
* [API Key Initialization](#api-key-initialization)
* [LinkedIn Profile Summary Functions](#linkedin-profile-summary-functions)
    * [`check_linkedin_json(url)`](#check_linkedin_jsonurl)
    * [`get_linkedin_profile_nubela(linkedin_url)`](#get_linkedin_profile_nubelalinkein_url)
    * [`get_linkedin_summary(url)`](#get_linkedin_summaryurl)
* [Website Summary Functions](#website-summary-functions)
    * [`check_website_json(url)`](#check_website_jsonurl)
    * [`extract_text_from_website(url)`](#extract_text_from_websiteurl)
    * [`get_website_summary(url)`](#get_website_summaryurl)
* [Groq (Llama) Chat Functions](#groq-llama-chat-functions)
    * [`llama_chat_json(prompt)`](#llama_chat_jsonprompt)
    * [`llama_chat(prompt)`](#llama_chatprompt)
* [Other Functions](#other-functions)
    * [`get_calls()`](#get_calls)


## <a name="import-statements"></a>Import Statements

```python
import requests
from groq import Groq
from bs4 import BeautifulSoup
import json
from src.ai_agent.config import HEADERS,NEBULA_API,OPENAI_API_KEY,GROQ_API
from openai import OpenAI
from src.utils.prompts import get_prompt_from_file
import os
from src.utils.prompt_formatter import PromptTemplate
```

Imports necessary libraries for HTTP requests, HTML parsing, JSON handling, OpenAI and Groq API interaction, prompt management, and file system operations.


## <a name="api-key-initialization"></a>API Key Initialization

```python
openai = OpenAI(api_key="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")
groq = Groq(api_key=GROQ_API)
```

Initializes OpenAI and Groq clients with API keys loaded from the `config` module.


## <a name="linkedin-profile-summary-functions"></a>LinkedIn Profile Summary Functions

### <a name="check_linkedin_json(url)"></a>`check_linkedin_json(url)`

```python
def check_linkedin_json(url):
    # ... (function body) ...
```

Checks if a LinkedIn profile summary for a given URL already exists in a local JSON file (`linkedinSummaryAiagent.json`). Returns `True` and the summary if found, `False` and `None` otherwise.

### <a name="get_linkedin_profile_nubela(linkedin_url)"></a>`get_linkedin_profile_nubela(linkedin_url)`

```python
def get_linkedin_profile_nubela(linkedin_url):
    # ... (function body) ...
```

Retrieves LinkedIn profile data using the Nubela API. Handles API requests, error responses, and potentially uses a cached response.

### <a name="get_linkedin_summary(url)"></a>`get_linkedin_summary(url)`

```python
def get_linkedin_summary(url):
    # ... (function body) ...
```

Generates a summary of a LinkedIn profile using OpenAI's API.  First checks for a cached summary. If not found, it fetches the profile data via `get_linkedin_profile_nubela`, constructs a prompt, and sends it to OpenAI. The generated summary is then cached locally.



## <a name="website-summary-functions"></a>Website Summary Functions

### <a name="check_website_json(url)"></a>`check_website_json(url)`

```python
def check_website_json(url):
    # ... (function body) ...
```

Similar to `check_linkedin_json`, but for website summaries stored in `websiteSummaryAiagent.json`.


### <a name="extract_text_from_website(url)"></a>`extract_text_from_website(url)`

```python
def extract_text_from_website(url):
    # ... (function body) ...
```

Extracts text content from a given website URL using `requests` and `BeautifulSoup`.  It removes script and style elements and cleans up the extracted text.


### <a name="get_website_summary(url)"></a>`get_website_summary(url)`

```python
def get_website_summary(url):
    # ... (function body) ...
```

Generates a summary of a website's content using OpenAI's API.  Similar to `get_linkedin_summary`, it checks for a cached summary, extracts text using `extract_text_from_website`, constructs a prompt, and sends it to OpenAI for processing. The result is then cached locally.


## <a name="groq-llama-chat-functions"></a>Groq (Llama) Chat Functions

### <a name="llama_chat_json(prompt)"></a>`llama_chat_json(prompt)`

```python
def llama_chat_json(prompt):
    # ... (function body) ...
```

Sends a prompt to the Groq API using the `llama-3.2-1b-preview` model and expects a JSON object as a response.


### <a name="llama_chat(prompt)"></a>`llama_chat(prompt)`

```python
def llama_chat(prompt):
    # ... (function body) ...
```

Sends a prompt to the Groq API using the `llama-3.2-3b-preview` model.



## <a name="other-functions"></a>Other Functions

### <a name="get_calls()"></a>`get_calls()`

```python
def get_calls():
    # ... (function body) ...
```

Makes a GET request to a specific API endpoint (`https://api.vapi.ai/call`).  The purpose of this endpoint is not explicitly defined in the provided code.


This documentation provides a comprehensive overview of the functions within the Python file.  Each function's purpose, inputs, outputs, and dependencies are clearly explained.  The use of caching mechanisms for improved efficiency is also noted.
