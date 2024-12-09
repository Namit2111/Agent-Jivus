# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with emails either directly within HubSpot or via this API.

## Managing Emails via the API

This section outlines the basic methods for managing emails using the HubSpot API.  For a complete list of endpoints and their requirements, refer to the "Endpoints" tab (not included in provided text, assumed to exist on the actual HubSpot documentation page).


### Create an Email

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/emails`

**Request Body:**

The request body should include a `properties` object containing email details and optionally an `associations` object to link the email to existing records (e.g., contacts, companies).

**Properties Object:**

| Field             | Description                                                                                                   | Required | Data Type |
|----------------------|---------------------------------------------------------------------------------------------------------------|----------|------------|
| `hs_timestamp`      | Email creation time (Unix timestamp in milliseconds or UTC format).                                          | Yes      | String     |
| `hubspot_owner_id`  | ID of the email owner (user listed as creator on the record timeline).                                       | No       | String     |
| `hs_email_direction` | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                              | No       | String     |
| `hs_email_html`     | Email body (if sent from a CRM record).                                                                     | No       | String     |
| `hs_email_status`   | Email send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                                   | No       | String     |
| `hs_email_subject`  | Email subject line.                                                                                          | No       | String     |
| `hs_email_text`     | Email body.                                                                                                | No       | String     |
| `hs_attachment_ids` | IDs of email attachments (multiple IDs separated by semicolons).                                            | No       | String     |
| `hs_email_headers`  | Email headers (JSON escaped string; populates read-only properties; see "Set Email Headers" section below). | No       | String     |


**Example Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2019-10-30T03:30:17.883Z",
    "hubspot_owner_id": "47550177",
    "hs_email_direction": "EMAIL",
    "hs_email_status": "SENT",
    "hs_email_subject": "Let's talk",
    "hs_email_text": "Thanks for your email",
    "hs_email_headers": "{\"from\":{\"email\":\"from@domain.com\",\"firstName\":\"FromFirst\",\"lastName\":\"FromLast\"},\"sender\":{\"email\":\"sender@domain.com\",\"firstName\":\"SenderFirst\",\"lastName\":\"SenderLast\"},\"to\":[{\"email\":\"ToFirst+ToLast<to@test.com>\",\"firstName\":\"ToFirst\",\"lastName\":\"ToLast\"}],\"cc\":[],\"bcc\":[]}"
  }
}
```

### Read-Only Properties

These properties are automatically populated by HubSpot from the `hs_email_headers` value:

| Field                 | Description                                         |
|-------------------------|-----------------------------------------------------|
| `hs_email_from_email`  | Sender's email address.                             |
| `hs_email_from_firstname` | Sender's first name.                               |
| `hs_email_from_lastname` | Sender's last name.                                |
| `hs_email_to_email`    | Recipient's email addresses.                         |
| `hs_email_to_firstname` | Recipient's first names.                            |
| `hs_email_to_lastname`  | Recipient's last names.                             |


**Note:**  Differences between `From` and `Sender` headers are explained in the original document.


### Set Email Headers

To manually set email headers, use a JSON escaped string with the following structure within `hs_email_headers`:

```json
{
  "from": {
    "email": "from@domain.com",
    "firstName": "FromFirst",
    "lastName": "FromLast"
  },
  "to": [
    {
      "email": "ToFirst ToLast<to@test.com>",
      "firstName": "ToFirst",
      "lastName": "ToLast"
    }
  ],
  "cc": [],
  "bcc": []
}
```


### Associations

To associate an email with records, include an `associations` object in your request.

**Associations Object:**

| Field             | Description                                                                                                          |
|----------------------|----------------------------------------------------------------------------------------------------------------------|
| `to`               | Record to associate (specified by its `id`).                                                                     |
| `types`            | Association type (includes `associationCategory` and `associationTypeId`).  Default IDs are listed [here](link-needed).  Custom types can be retrieved via the associations API. |


**Example Associations Object:**

```json
"associations": [
  {
    "to": { "id": 601 },
    "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210 } ]
  },
  {
    "to": { "id": 602 },
    "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 198 } ]
  }
]
```


### Retrieve Emails

**Individual Email:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

**Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.


**All Emails:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/emails`

**Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.


### Update Emails

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

**Request Body:**

Include the `properties` object with the fields you want to update.  HubSpot ignores read-only and non-existent properties.  Pass an empty string to clear a property value.


**Example Request Body:**

```json
{
  "properties": {
    "hs_email_subject": "Let's talk tomorrow",
    "hs_email_text": "Thanks for your interest let's find a time to connect!"
  }
}
```


### Associate Existing Emails with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**URL Parameters:**

* `emailId`: Email ID.
* `toObjectType`: Object type to associate (e.g., `contact`, `company`).
* `toObjectId`: ID of the record to associate.
* `associationTypeId`: Association type ID (can be numerical or snake case; retrieved via the associations API).


### Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### Pin an Email on a Record

To pin an email, include its `id` in the `hs_pinned_engagement_id` field when creating or updating a record via the object APIs (companies, contacts, deals, tickets, custom objects).


### Delete Emails

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

Deleting an email is permanent and cannot be undone.


This documentation provides a summary of the HubSpot Email Engagement API.  Always refer to the official HubSpot documentation for the most up-to-date information and details.
