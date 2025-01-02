# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displaying information from external systems within HubSpot contact, company, deal, and ticket records.

## Overview

HubSpot CRM cards enhance CRM records by displaying data from integrated applications.  Each app can have up to 25 CRM cards.  These cards are distinct from UI extensions built using developer projects; they are designed for public apps and offer less flexibility than UI extensions.  If you are not building a public app, consider using React-based UI extensions.

**Use Case Example:**  An app integrating bug tracking software can display tracked bugs directly on contact records for support representatives.

**Workflow:** The app defines cards within its settings.  Upon viewing a relevant CRM record, HubSpot makes an outbound request to the app, receives data, and displays it as a card.  Custom actions can be included for user interaction (e.g., opening a modal with the app's UI).

## Scope Requirements

To create CRM cards, your app needs OAuth scopes to read and write to the relevant CRM object.  For example, a card on contact records requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes. Removing CRM object scopes requires deleting all existing cards for those object types.  See the HubSpot OAuth documentation for details.

## Creating CRM Cards

Cards can be created via the API or HubSpot's UI:

**Via API (see Endpoints section below):**  Use the API endpoints to programmatically create and manage CRM cards.

**Via HubSpot UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select your app.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card**.

## Data Request

When a user views a CRM record, HubSpot sends a data fetch request to the app's specified URL. This request includes default and custom query parameters:

**Default Parameters:**

* `userId`: HubSpot user ID.
* `userEmail`: User's email address.
* `associatedObjectId`: CRM record ID.
* `associatedObjectType`: CRM record type (e.g., `CONTACT`, `COMPANY`).
* `portalId`: HubSpot account ID.

**Custom Parameters:**  These are HubSpot properties selected in the card's settings (in-app) or `propertiesToSend` array (API).

**Example Data Fetch Configuration (JSON):**

```json
{
  "title": "New CRM Card",
  "fetch": {
    "targetUrl": "https://www.example.com/demo-fetch",
    "objectTypes": [
      {
        "name": "contacts",
        "propertiesToSend": ["firstname", "email", "lastname"]
      }
    ]
  }
}
```

**Example Request URL:**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Timeout:** Requests timeout after 5 seconds; a connection must be established within 3 seconds.


## Example Response (JSON)

```json
{
  "results": [
    {
      "objectId": 245,
      "title": "API-22: APIs working too fast",
      "link": "http://example.com/1",
      "created": "2016-09-15",
      "priority": "HIGH",
      // ... other properties ...
      "actions": [
        // ... actions ...
      ]
    },
    // ... more results ...
  ],
  "settingsAction": { /* ... */ },
  "primaryAction": { /* ... */ }
}
```

**Response Fields:**

* `results`: Array of card objects (max 5).  Each object can have:
    * `objectId`: Unique ID.
    * `title`: Object title.
    * `link`: URL for more details (optional, use `null` if none).
    * `created`: Creation date (custom property).
    * `priority`: Priority level (custom property).
    * `actions`: Array of custom actions.
    * `properties`: Array of additional custom properties.

* `settingsAction`: Iframe action for app settings.
* `primaryAction`: Primary action for a record type.
* `secondaryActions`: List of additional actions.


## Request Signatures

HubSpot includes the `X-HubSpot-Signature` header to verify requests.  To validate:

1. Concatenate `<app secret> + <HTTP method> + <URL> + <request body>`.
2. Create a SHA-256 hash of the concatenated string.
3. Compare the hash with the signature in the header.

See HubSpot's request validation documentation for details.


## Card Properties

Define custom properties displayed on the card.  Add properties via the UI or API.  Specify a unique name, display label, and data type:

* `CURRENCY`: Requires `currencyCode` (ISO 4217).
* `DATE`: `yyyy-mm-dd` format.
* `DATETIME`: Milliseconds since epoch.
* `EMAIL`: Email address (displayed as a link).
* `LINK`: URL (with optional `linkLabel`).
* `NUMERIC`: Number.
* `STATUS`: Status indicator (requires `optionType`: `DEFAULT`, `SUCCESS`, `WARNING`, `DANGER`, `INFO`).
* `STRING`: Text.

## Custom Actions

Define URLs for action buttons on the card.  Actions include:

* **Iframe Actions:** Open a modal with an iframe.  No signature is sent. Use `window.postMessage` to close the modal (e.g., `{"action": "DONE"}`).

* **Action Hook Actions:** Send a server-side request (GET, POST, PUT, DELETE, PATCH).  Includes a signature.

* **Confirmation Actions:** Similar to action hooks, but with a confirmation dialog. Includes a signature.


## API Endpoints

*(This section requires specifics from the actual API documentation not provided in the input text.  Replace placeholders with actual endpoint details.)*

**Create CRM Card:**  `POST /crm/v3/cards`

**Get CRM Card:**  `GET /crm/v3/cards/{cardId}`

**Update CRM Card:**  `PUT /crm/v3/cards/{cardId}`

**Delete CRM Card:**  `DELETE /crm/v3/cards/{cardId}`


This documentation provides a comprehensive overview of the HubSpot CRM Cards API. Refer to the HubSpot developer documentation for the most up-to-date information and detailed specifications.
