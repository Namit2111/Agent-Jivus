# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displayed on HubSpot contact, company, deal, and ticket records within a public app.  These cards differ from UI extensions; they're designed specifically for public apps and offer less flexibility.  For private apps or more complex integrations, consider UI extensions.

## Scope Requirements

Before creating CRM cards, your app needs the necessary OAuth scopes to read and write to the relevant CRM objects.  For example, to display a card on contact records, your app requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes. Removing CRM object scopes necessitates deleting all existing cards for those object types. See the HubSpot OAuth documentation for details on scopes and authorization.

## Creating a CRM Card

CRM cards can be created via the API or the HubSpot developer account UI.  This documentation focuses on the API approach.

### API Endpoint (Unspecified in provided text - needs to be added)

The exact API endpoint for creating CRM cards is missing from the provided text.  It should be included here in the format:

```
POST /crm/v3/objects/<object_type>/cards
```

where `<object_type>` is one of `contacts`, `companies`, `deals`, or `tickets`.

### Request Body

The request body should include the following:

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
  },
  // ... other properties (see below) ...
}
```

* **`title` (string):** The title displayed on the card.
* **`fetch.targetUrl` (string):** The URL HubSpot will use to fetch data for the card.  This URL will receive a GET request with query parameters.
* **`fetch.objectTypes` (array of objects):** An array specifying the CRM object types the card applies to and the properties to send in the request.  Each object within this array should have:
    * **`name` (string):** The CRM object type (e.g., "contacts").
    * **`propertiesToSend` (array of strings):** An array of HubSpot property names to include as query parameters.

  **(Add other properties as found in the API specification - not in the provided text.)**

### Response (Successful Card Creation)

A successful response will indicate the card has been created and provide a card ID (structure not provided in text and needs to be added).


## Data Fetch Request

When a user views a CRM record, HubSpot sends a GET request to `fetch.targetUrl` including default and custom query parameters.

### Request Example

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

* **`userId` (integer):** HubSpot user ID.
* **`userEmail` (string):** HubSpot user email.
* **`associatedObjectId` (integer):** ID of the CRM record.
* **`associatedObjectType` (string):** Type of CRM record (CONTACT, COMPANY, DEAL, TICKET).
* **`portalId` (integer):** HubSpot account ID.
* **`firstname`, `email`, `lastname` (strings):**  Custom properties specified in `propertiesToSend`.

### Request Signature

HubSpot includes the `X-HubSpot-Signature` header to verify the request's authenticity.  The signature is a SHA-256 hash of: `<app secret>+<HTTP method>+<URL>+<request body>`.  This hash should be base64 encoded.


## Data Fetch Response

The response from your `targetUrl` should be in JSON format.

### Response Example

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
        // ... action definitions ...
      ]
    },
    // ... more results ...
  ],
  "settingsAction": { ... },
  "primaryAction": { ... }
}
```

* **`results` (array of objects):** An array of up to five objects to display.  Each object should include:
    * **`objectId` (integer):** Unique ID for the object.
    * **`title` (string):** Object title.
    * **`link` (string, optional):** Link to more details (can be `null`).
    * **`created`, `priority` (strings):** Custom properties defined in card settings.
    * **`properties` (array of objects, optional):** Additional custom properties.
* **`settingsAction`, `primaryAction` (objects):** Action definitions (see below).

### Card Property Types

Custom properties within `results` and `properties` arrays can be one of the following types:

* **`CURRENCY`:** Requires `currencyCode` (ISO 4217).
* **`DATE`:** `yyyy-mm-dd` format.
* **`DATETIME`:** Milliseconds since epoch.
* **`EMAIL`:** Email address (displayed as a link).
* **`LINK`:** URL; optionally includes `linkLabel`.
* **`NUMERIC`:** Number.
* **`STATUS`:** Status indicator with `optionType` (DEFAULT, SUCCESS, WARNING, DANGER, INFO).
* **`STRING`:** Text.

## Custom Actions

Custom actions allow users to interact with your card.

### Action Types

* **`IFRAME`:** Opens a modal with an iframe.  The iframe should use `window.parent.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **`ACTION_HOOK`:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH).  Includes `X-HubSpot-Signature`.
* **`CONFIRMATION_ACTION_HOOK`:** Similar to `ACTION_HOOK`, but requires user confirmation. Includes `X-HubSpot-Signature`.

All actions require a `uri` field specifying the action URL.  `associatedObjectProperties` can be used to pass additional data.

**(Note:  The provided text lacks a complete API specification.  The endpoint URL, detailed response structure, and error handling are not fully defined.  This documentation should be augmented with that information.)**
