# HubSpot Email Engagement API Documentation

This document details the HubSpot API for managing email engagements.  It covers creating, retrieving, updating, associating, and deleting emails within the HubSpot CRM.

## Email Engagement API Overview

The email engagement API allows you to log and manage emails associated with CRM records directly within HubSpot or through the API.  This provides a comprehensive view of email interactions within the context of your CRM data.

## Key Methods

This section outlines the core API methods for managing emails.  For a complete list of endpoints and their specifications, refer to the "Endpoints" tab (not included in provided text, but assumed to exist within the HubSpot documentation).

### 1. Create an Email

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/emails`

**Request Body:**

The request body requires a `properties` object containing email details and an optional `associations` object to link the email to existing records.

**Properties Object:**

| Field                | Description                                                                                                                                   | Required | Data Type    |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------|
| `hs_timestamp`       | Timestamp of email creation (Unix timestamp in milliseconds or UTC format).  Determines timeline position.                                      | Yes      | String/Number |
| `hubspot_owner_id`   | ID of the email owner (user ID). Determines the creator listed in the record timeline.                                                        | No       | String        |
| `hs_email_direction` | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                                                              | No       | String        |
| `hs_email_html`      | HTML body of the email (sent from a CRM record).                                                                                             | No       | String        |
| `hs_email_status`    | Email send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                                                                  | No       | String        |
| `hs_email_subject`   | Email subject line.                                                                                                                           | No       | String        |
| `hs_email_text`      | Plain text body of the email.                                                                                                                  | No       | String        |
| `hs_attachment_ids`  | IDs of email attachments (semicolon-separated).                                                                                               | No       | String        |
| `hs_email_headers`   | JSON escaped string containing email headers.  Populates read-only properties.  See "Set Email Headers" section for formatting.                 | No       | String        |


**Read-Only Properties (Automatically Populated from `hs_email_headers`):**

| Field                   | Description                                      |
|------------------------|--------------------------------------------------|
| `hs_email_from_email`    | Sender's email address.                         |
| `hs_email_from_firstname`| Sender's first name.                             |
| `hs_email_from_lastname` | Sender's last name.                              |
| `hs_email_to_email`     | Recipient's email address(es).                    |
| `hs_email_to_firstname` | Recipient's first name(s).                       |
| `hs_email_to_lastname`  | Recipient's last name(s).                        |


**Set Email Headers:**

The `hs_email_headers` property accepts a JSON escaped string with the following structure:

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

**Associations Object:**

Used to link the email to existing records.

| Field       | Description                                                                         |
|-------------|-------------------------------------------------------------------------------------|
| `to`        | Object containing the `id` of the record to associate (e.g., contact, deal).       |
| `types`     | Array of association types. Each type requires `associationCategory` and `associationTypeId`.|


### 2. Retrieve Emails

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/emails/{emailId}` (individual email) or `/crm/v3/objects/emails` (all emails)

**Parameters:**

| Parameter   | Description                                                                   |
|-------------|-------------------------------------------------------------------------------|
| `emailId`   | (For individual email) The ID of the email to retrieve.                       |
| `limit`     | (For all emails) Maximum number of results per page.                         |
| `properties` | Comma-separated list of properties to return.                                |
| `associations` | Comma-separated list of object types to retrieve associated IDs for.           |


### 3. Update Emails

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

**Request Body:**  Contains the `properties` object with fields to update.  Read-only properties are ignored.  An empty string clears a property value.

### 4. Associate Existing Emails with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**URL Parameters:**

| Field           | Description                                                                      |
|-----------------|----------------------------------------------------------------------------------|
| `emailId`       | ID of the email.                                                                  |
| `toObjectType`  | Type of object to associate (e.g., `contact`, `company`).                           |
| `toObjectId`    | ID of the record to associate.                                                    |
| `associationTypeId` | Unique identifier for the association type.  Obtainable via the associations API. |


### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}` (Same as associating)


### 6. Pin an Email

To pin an email to a record's timeline, include the email's `id` in the `hs_pinned_engagement_id` field when creating or updating the record via object APIs (companies, contacts, deals, tickets, custom objects).  Only one activity can be pinned per record.

### 7. Delete Emails

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

Deleting an email is permanent and cannot be undone.


##  Error Handling (Not Explicitly Defined in Provided Text)

The documentation should include details on error handling, including HTTP status codes and error responses returned by the API.

## Rate Limiting (Not Explicitly Defined in Provided Text)

The documentation should include information on API rate limits and best practices for handling them.  This is crucial for avoiding API request failures.


This enhanced markdown documentation provides a more structured and comprehensive overview of the HubSpot Email Engagement API.  Remember to consult the full HubSpot API documentation for the most up-to-date and complete information, including the "Endpoints" tab mentioned throughout the original text.
