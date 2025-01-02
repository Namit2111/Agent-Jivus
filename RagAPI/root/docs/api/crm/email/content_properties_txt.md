# HubSpot Email Engagement API Documentation

This document describes the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with the API via various HTTP methods.  Note that all endpoints are under the `/crm/v3/objects/emails` base path.


## API Endpoints

All endpoints below use the base URL `/crm/v3/objects/emails`.  Replace `{emailId}` and `{toObjectId}` with the respective IDs.

### 1. Create an Email (POST)

**Endpoint:** `/crm/v3/objects/emails`

**Method:** `POST`

**Request Body:**

The request body requires a `properties` object, and optionally an `associations` object.

* **`properties` object:** Contains email details.  Required fields are marked with an asterisk (*).

| Field                 | Description                                                                                                 | Example                     | Type      | Required |
|----------------------|-------------------------------------------------------------------------------------------------------------|-----------------------------|-----------|----------|
| `hs_timestamp`*      | Email creation timestamp (Unix timestamp in milliseconds or UTC format).                                      | `1678886400000` or `"2023-03-15T12:00:00Z"` | String    | Yes      |
| `hubspot_owner_id`   | ID of the email owner.                                                                                      | `47550177`                  | String    | No       |
| `hs_email_direction` | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                             | `"EMAIL"`                    | String    | No       |
| `hs_email_html`      | Email body (HTML) – Sent from CRM record.                                                                    | `<p>Hello</p>`             | String    | No       |
| `hs_email_status`    | Email send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                                   | `"SENT"`                     | String    | No       |
| `hs_email_subject`   | Email subject.                                                                                             | `"Let's talk"`               | String    | No       |
| `hs_email_text`      | Email body (plain text).                                                                                    | `Thanks for your email`       | String    | No       |
| `hs_attachment_ids`  | IDs of attached files (semicolon-separated).                                                              | `"123;456"`                 | String    | No       |
| `hs_email_headers`   | JSON-escaped string containing email headers (see "Set Email Headers").                                     | See Example Below           | String    | No       |


**Example Request Body (with Associations):**

```json
{
  "properties": {
    "hs_timestamp": "2024-03-15T12:00:00Z",
    "hubspot_owner_id": "11349275740",
    "hs_email_direction": "EMAIL",
    "hs_email_status": "SENT",
    "hs_email_subject": "Let's talk",
    "hs_email_text": "Thanks for your interest",
    "hs_email_headers": "{\"from\":{\"email\":\"from@domain.com\",\"firstName\":\"FromFirst\",\"lastName\":\"FromLast\"},\"to\":[{\"email\":\"to@test.com\",\"firstName\":\"ToFirst\",\"lastName\":\"ToLast\"}],\"cc\":[],\"bcc\":[]}"
  },
  "associations": [
    {
      "to": {"id": 601},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}]
    },
    {
      "to": {"id": 602},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 198}]
    }
  ]
}
```


**Response:** Standard HubSpot API response containing the created email object.


### 2. Retrieve an Email (GET)

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

**Method:** `GET`

**Query Parameters:**

| Parameter    | Description                                                         | Example          |
|--------------|---------------------------------------------------------------------|-------------------|
| `properties` | Comma-separated list of properties to return.                       | `hs_email_subject,hs_timestamp` |
| `associations`| Comma-separated list of object types to retrieve associated IDs for. | `contact,company`  |


**Example:** `/crm/v3/objects/emails/123?properties=hs_email_subject,hs_timestamp`


**Response:**  The email object with specified properties.


### 3. Retrieve Emails (GET)

**Endpoint:** `/crm/v3/objects/emails`

**Method:** `GET`

**Query Parameters:**

| Parameter | Description                                         | Example |
|-----------|-----------------------------------------------------|---------|
| `limit`   | Maximum number of results per page.                | `10`     |
| `properties` | Comma-separated list of properties to return.     | `hs_email_subject,hs_timestamp` |


**Response:** A paginated list of email objects.


### 4. Update an Email (PATCH)

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

**Method:** `PATCH`

**Request Body:**  Similar to create, but only includes properties to update.  Read-only properties are ignored.


**Example Request Body:**

```json
{
  "properties": {
    "hs_email_subject": "Updated Subject"
  }
}
```

**Response:** Updated email object.


### 5. Associate Existing Email with Records (PUT)

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**URL Parameters:**

| Parameter       | Description                                         | Example    |
|-----------------|-----------------------------------------------------|------------|
| `emailId`        | ID of the email.                                     | `123`       |
| `toObjectType`  | Object type to associate (e.g., `contact`, `company`). | `contact`   |
| `toObjectId`    | ID of the record to associate.                       | `456`       |
| `associationTypeId` | Association type ID (obtainable via Associations API). | `198`       |


**Response:**  Success/failure indication.


### 6. Remove Association (DELETE)

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

**URL Parameters:** Same as above.

**Response:** Success/failure indication.


### 7. Delete an Email (DELETE)

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

**Method:** `DELETE`

**Response:** Success/failure indication.


## Set Email Headers

Email headers are crucial for populating read-only properties. Use a JSON-escaped string with the following structure:

```json
{
  "from": {
    "email": "from@domain.com",
    "firstName": "FromFirst",
    "lastName": "FromLast"
  },
  "to": [
    {
      "email": "to@test.com",
      "firstName": "ToFirst",
      "lastName": "ToLast"
    }
  ],
  "cc": [],
  "bcc": []
}
```

This will populate `hs_email_from_email`, `hs_email_from_firstname`, etc.


## Read-Only Properties

These properties are automatically populated from `hs_email_headers`:

* `hs_email_from_email`
* `hs_email_from_firstname`
* `hs_email_from_lastname`
* `hs_email_to_email`
* `hs_email_to_firstname`
* `hs_email_to_lastname`


## Pinning Emails

To pin an email to a record's timeline, include the email's `id` in the `hs_pinned_engagement_id` field when updating the record via its respective object API (contacts, companies, etc.).  Only one activity can be pinned per record.


## Error Handling

The API returns standard HubSpot error responses with details about failures.  Refer to the HubSpot API documentation for details on error codes and handling.


This documentation provides a comprehensive overview of the HubSpot Email Engagement API. Remember to consult the official HubSpot API documentation for the most up-to-date information and details on authentication and rate limits.
