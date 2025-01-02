# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with the API via HTTP requests.  All endpoints are located under the `/crm/v3/objects/emails` base path.

## API Endpoints

The following table summarizes the main API endpoints.  For complete endpoint details including request parameters and potential error responses, refer to the HubSpot Developer documentation's "Endpoints" tab (link not provided in the source text).

| Method | Endpoint                     | Description                                                                    |
|--------|------------------------------|--------------------------------------------------------------------------------|
| POST   | `/crm/v3/objects/emails`      | Create a new email engagement.                                                  |
| GET    | `/crm/v3/objects/emails/{emailId}` | Retrieve a specific email engagement by ID.                                     |
| GET    | `/crm/v3/objects/emails`      | Retrieve a list of email engagements.                                           |
| PATCH  | `/crm/v3/objects/emails/{emailId}` | Update an existing email engagement.                                            |
| PUT    | `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}` | Associate an existing email with a record.                                     |
| DELETE | `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}` | Remove an association between an email and a record.                          |
| DELETE | `/crm/v3/objects/emails/{emailId}` | Delete an email engagement.                                                     |


##  Create an Email (POST /crm/v3/objects/emails)

Creates a new email engagement.  The request body must include a `properties` object and can optionally include an `associations` object.

**Request Body (Example):**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00.000Z", // UTC timestamp in milliseconds or ISO 8601 format
    "hubspot_owner_id": "12345", // HubSpot user ID
    "hs_email_direction": "EMAIL", // EMAIL, INCOMING_EMAIL, or FORWARDED_EMAIL
    "hs_email_status": "SENT", // SENT, BOUNCED, FAILED, SCHEDULED, SENDING
    "hs_email_subject": "Test Email",
    "hs_email_text": "This is a test email.",
    "hs_email_html": "<html>This is a test email.</html>", // Optional HTML body
    "hs_attachment_ids": "123;456", // Optional; Multiple IDs separated by semicolons
    "hs_email_headers": "{\"from\":{\"email\":\"from@example.com\",\"firstName\":\"From\",\"lastName\":\"User\"},\"to\":[{\"email\":\"to@example.com\",\"firstName\":\"To\",\"lastName\":\"User\"}]}" //JSON escaped string
  },
  "associations": [
    {
      "to": {"id": 601}, // ID of the associated record (e.g., contact, deal)
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}] // Association type
    }
  ]
}
```

**Response (Example - Success):**

```json
{
  "id": "newly_created_email_id",
  // ... other properties ...
}
```


## Properties

**Required Properties:**

* `hs_timestamp`: Email creation timestamp (Unix timestamp in milliseconds or UTC format).
* `hs_email_direction`: Direction of the email (EMAIL, INCOMING_EMAIL, FORWARDED_EMAIL).

**Other Properties:**

* `hubspot_owner_id`: ID of the email owner (HubSpot user).
* `hs_email_html`: HTML body of the email.
* `hs_email_status`: Status of the email (SENT, BOUNCED, FAILED, SCHEDULED, SENDING).
* `hs_email_subject`: Subject of the email.
* `hs_email_text`: Plain text body of the email.
* `hs_attachment_ids`: Semicolon-separated list of attachment IDs.
* `hs_email_headers`: JSON escaped string containing email headers (influences read-only properties).


## Read-Only Properties

These properties are automatically populated from `hs_email_headers`:

* `hs_email_from_email`, `hs_email_from_firstname`, `hs_email_from_lastname`
* `hs_email_to_email`, `hs_email_to_firstname`, `hs_email_to_lastname`


## Setting Email Headers (`hs_email_headers`)

Use a JSON escaped string within `hs_email_headers` to set the email headers. This affects read-only properties.

**Example `hs_email_headers` JSON:**

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


## Associations

Associate emails with records (e.g., contacts, deals) using the `associations` object in the request body.

**Example `associations` object:**

```json
{
  "to": {"id": 601}, // Record ID
  "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}] // Association type
}
```

`associationTypeId` values can be found in the HubSpot documentation.


## Retrieve Emails (GET /crm/v3/objects/emails)

Retrieve emails individually by ID or in bulk. Use query parameters `limit` and `properties` to control results.


## Update Emails (PATCH /crm/v3/objects/emails/{emailId})

Update existing email properties.  HubSpot ignores read-only and non-existent properties.  Use an empty string to clear a property value.


## Associate/Remove Associations (PUT/DELETE /crm/v3/objects/emails/{emailId}/associations/{...})

Manage associations between emails and records using PUT (associate) and DELETE (remove) requests.


## Pinning Emails

Pin an email to a record's timeline using the `hs_pinned_engagement_id` field when updating the record via other HubSpot object APIs (contacts, deals, etc.).


## Delete Emails (DELETE /crm/v3/objects/emails/{emailId})

Permanently deletes an email.  Deletion is irreversible.



This documentation provides a concise overview.  Always consult the official HubSpot API documentation for the most up-to-date information, including details on error handling, authentication, rate limits, and pagination.
