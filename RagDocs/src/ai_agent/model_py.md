# Python Classes for Call Data Management

This document describes the Python classes used for managing call data, including call initiation, persona information, and call status.

## Class `CallData`

This class encapsulates the data required for initiating a phone call.

**Attributes:**

* `data (dict)`: A dictionary containing all the call data.  This includes:
    * `assistant`: Details about the AI assistant.
        * `firstMessage (str)`: The initial message sent by the assistant. Defaults to "Hey, what's up?".
        * `model`: Details about the language model used.
            * `provider (str)`: The provider of the language model (e.g., "openai"). Defaults to "openai".
            * `model (str)`: The specific model name (e.g., "gpt-3.5-turbo"). Defaults to "gpt-3.5-turbo".
            * `messages (list)`: A list of messages, initially containing a system message.
                * `role (str)`: The role of the message ("system").
                * `content (str)`: The content of the system message. Defaults to "You are an assistant."
        * `voice (str)`: The voice used by the assistant (e.g., "jennifer-playht"). Defaults to "jennifer-playht".
    * `phoneNumberId (str)`: The ID of the phone number used for the call.  Obtained from `src.ai_agent.config.PHONE_NUMBER_ID`.
    * `customer`: Details about the customer.
        * `number (str)`: The customer's phone number.


**Methods:**

* `__init__(self, customer_number: str, first_message: str = "Hey, what's up?", provider: str = "openai", model: str = "gpt-3.5-turbo", content: str = "You are an assistant.", voice: str = "jennifer-playht")`: Constructor to initialize the `CallData` object.
* `get_data(self) -> dict`: Returns the `data` dictionary.


## Class `Persona`

This class stores information about a persona.

**Attributes:**

* `data (dict)`: A dictionary containing persona information.
    * `phoneNumber (str)`: Phone number of the persona.
    * `linkedinUrl (str)`: LinkedIn URL of the persona.
    * `websiteUrl (str)`: Website URL of the persona.

**Methods:**

* `__init__(self, phoneNumber, linkedinUrl, websiteUrl)`: Constructor to initialize the `Persona` object.


## Class `preData`

This class prepares data for the AI agent, including prompts from files.

**Attributes:**

* `assistant_id (str)`: The ID of the assistant. Obtained from `src.ai_agent.config.assistant_id`.
* `phone_number_id (str)`: The ID of the phone number. Obtained from `src.ai_agent.config.PHONE_NUMBER_ID`.
* `customer_number (str)`: The customer's phone number.
* `first_message (str)`: The first message to be sent, formatted using a template from `first_msg_ai_agent.txt`.
* `prompt (str)`: The main prompt for the AI agent, formatted using a template from `ai_agentmain_prompt.txt`.
* `data (dict)`: A dictionary containing all the prepared data for the AI agent.  Similar structure to `CallData.data`, but using `first_message` and `prompt`  defined above.

**Methods:**

* `__init__(self, customer_number, sales_person_name, company_name, product_summary)`: Constructor to initialize the `preData` object.
* `get_data(self)`: Returns the `data` dictionary.


## Class `CallStatusData`

This class represents the status of a phone call.

**Attributes:**

All attributes are populated from a JSON response.  See the constructor for details.

* `call_id (str)`: ID of the call.
* `assistant_id (str)`: ID of the assistant.
* `type (str)`: Type of the call.
* `status (str)`: Status of the call.
* `started_at (datetime)`: Call start time.
* `ended_at (datetime)`: Call end time.
* `transcript (str)`: Transcript of the call.
* `recording_url (str)`: URL of the call recording.
* `summary (str)`: Summary of the call.
* `phone_call_provider (str)`: Provider of the phone call.
* `ended_reason (str)`: Reason for call termination.
* `created_at (datetime)`: Creation timestamp.
* `updated_at (datetime)`: Last update timestamp.
* `messages (list)`: List of messages exchanged during the call.


**Methods:**

* `__init__(self, response_json)`: Constructor that populates attributes from a JSON response.
* `to_dict(self)`: Returns a dictionary representation of the call status data.


## Imports

* `src.ai_agent.config`: Imports `PHONE_NUMBER_ID` and `assistant_id`.
* `src.utils.prompts`: Imports `get_prompt_from_file`.  This function is used to load and format prompts from text files.

