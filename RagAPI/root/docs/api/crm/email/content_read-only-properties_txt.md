# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with emails either directly within HubSpot or through this API.

## API Endpoints Base URL: `/crm/v3/objects/emails`

All endpoints below utilize the base URL `/crm/v3/objects/emails`.  Replace `{emailId}` with the specific email ID.


## API Methods

### 1. Create an Email (POST)

Creates a new email engagement.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00.000Z", // Required. Unix timestamp (milliseconds) or UTC format.
    "hubspot_owner_id": "12345", // ID of the email owner.
    "hs_email_direction": "EMAIL", // EMAIL, INCOMING_EMAIL, or FORWARDED_EMAIL
    "hs_email_status": "SENT", // BOUNCED, FAILED, SCHEDULED, SENDING, or SENT
    "hs_email_subject": "Test Email",
    "hs_email_text": "This is a test email.",
    "hs_email_html": "<html>...</html>", // Optional HTML body
    "hs_attachment_ids": "123;456", // Optional; multiple IDs separated by semicolons
    "hs_email_headers": "{\"from\":{\"email\":\"from@domain.com\",\"firstName\":\"FromFirst\",\"lastName\":\"FromLast\"},\"to\":[{\"email\":\"to@domain.com\",\"firstName\":\"ToFirst\",\"lastName\":\"ToLast\"}],\"cc\":[],\"bcc\":[]}" // JSON escaped string; see "Set Email Headers" below
  },
  "associations": [ // Optional: Associate with existing records
    {
      "to": {"id": 601}, // ID of the record
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}] // Association type (see below)
    }
  ]
}
```

**Response:**  A JSON object representing the created email, including its ID.

**Example Request (curl):**

```bash
curl -X POST \
  https://api.hubspot.com/crm/v3/objects/emails \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{ /* Request body as above */ }'
```

### 2. Retrieve an Email (GET)

Retrieves a single email by ID.

**Request URL:** `/crm/v3/objects/emails/{emailId}?properties=property1,property2&associations=contact,company`

**Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Response:** A JSON object representing the email.

**Example Request (curl):**

```bash
curl -X GET \
  https://api.hubspot.com/crm/v3/objects/emails/123?properties=hs_email_subject,hs_email_text \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### 3. Retrieve Emails (GET)

Retrieves a list of emails.

**Request URL:** `/crm/v3/objects/emails?limit=10&properties=property1,property2`

**Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

**Response:** A JSON object containing a list of emails and pagination information.


### 4. Update an Email (PATCH)

Updates an existing email.  Only specified properties are updated; others remain unchanged.  Read-only properties are ignored.

**Request Body:** (Similar structure to POST, but only include properties to update.)

```json
{
  "properties": {
    "hs_email_subject": "Updated Subject",
    "hs_email_text": "Updated Email Body"
  }
}
```

**Response:** A JSON object representing the updated email.

### 5. Associate Existing Email with Records (PUT)

Associates an existing email with a record.

**Request URL:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

* `emailId`: ID of the email.
* `toObjectType`: Type of object (e.g., `contact`, `company`, `deal`).
* `toObjectId`: ID of the object.
* `associationTypeId`: Unique ID for the association type (obtainable via the Associations API).


### 6. Remove an Association (DELETE)

Removes an association between an email and a record. Uses the same URL as the `Associate Existing Email` endpoint.

### 7. Pin an Email (Create/Update Record)

To pin an email to a record, include the email's `id` in the `hs_pinned_engagement_id` field when creating or updating the record using the respective object APIs (Contacts, Companies, Deals, etc.).

### 8. Delete an Email (DELETE)

Permanently deletes an email.

**Request URL:** `/crm/v3/objects/emails/{emailId}`


##  Set Email Headers

Manually set email headers using a JSON escaped string within the `hs_email_headers` property. This populates read-only properties.

**Example JSON escaped string:**

```json
"{\"from\":{\"email\":\"from@domain.com\",\"firstName\":\"FromFirst\",\"lastName\":\"FromLast\"},\"to\":[{\"email\":\"to@domain.com\",\"firstName\":\"ToFirst\",\"lastName\":\"ToLast\"}],\"cc\":[],\"bcc\":[]}"
```

## Read-Only Properties

These properties are automatically populated from `hs_email_headers`.

* `hs_email_from_email`
* `hs_email_from_firstname`
* `hs_email_from_lastname`
* `hs_email_to_email`
* `hs_email_to_firstname`
* `hs_email_to_lastname`


##  Association Types

The `associationTypeId` values are defined within HubSpot. You can use default IDs or retrieve custom ones via the HubSpot Associations API.  Consult the HubSpot documentation for a complete list.


## Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Error responses include detailed error messages in JSON format.


This documentation provides a comprehensive overview.  Refer to the official HubSpot API documentation for the most up-to-date information and details on batch operations. Remember to replace `YOUR_API_KEY` with your actual HubSpot API key.
