# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displaying information from external systems within HubSpot contact, company, deal, and ticket records.

## Overview

HubSpot CRM cards enable public apps to enrich CRM records by displaying data from external sources.  Each app can have up to 25 cards.  These cards differ from UI extensions; they're designed for public apps and offer less flexibility than React-based UI extensions suitable for private apps.

**Use Case:**  Imagine integrating a bug tracking system.  A CRM card could display associated bugs directly on a contact record, improving support rep efficiency.

**Mechanism:**  Upon viewing a CRM record, HubSpot makes an outbound request to the app's specified URL, retrieves data, and renders it as a card.  The app can also define custom actions (e.g., opening a modal with the app's UI).


## Scope Requirements

Creating CRM cards requires requesting OAuth scopes to read and write to the relevant CRM objects. For example, a card on contact records needs `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes. Removing object scopes necessitates deleting all existing cards for those object types first.  See the HubSpot OAuth documentation for details.


## Creating a CRM Card

Cards can be created via the API or HubSpot's UI.

**UI-based Creation:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select your app.
3. Choose **CRM cards** in the sidebar.
4. Click **Create CRM card**.

### API-based Card Creation (Endpoints -  *Specific endpoint details are missing from the provided text, this section requires further information from the HubSpot API documentation*)

The API likely involves a POST request to a specific endpoint with a JSON payload defining the card's configuration.  This would include:

* `title`: Card title.
* `fetch`:  Configuration for data fetching.


## Data Request

When a user views a relevant CRM record, HubSpot sends a GET request to the app's `targetUrl`. This request includes:

* **Default Parameters:**
    * `userId`: HubSpot user ID.
    * `userEmail`: User's email address.
    * `associatedObjectId`: ID of the CRM record.
    * `associatedObjectType`: Type of CRM record (e.g., `CONTACT`, `COMPANY`).
    * `portalId`: HubSpot account ID.
* **Custom Parameters:**  HubSpot properties specified in the card's settings (`propertiesToSend` array in the API).


**Example Request:**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Timeout:** Requests time out after 5 seconds; connection must be established within 3 seconds.

### Example Data Fetch Configuration (JSON):

```json
{
  "title": "New CRM Card",
  "fetch": {
    "targetUrl": "https://www.example.com/demo-fetch",
    "objectTypes": [
      {
        "name": "contacts",
        "propertiesToSend": [
          "firstname",
          "email",
          "lastname"
        ]
      }
    ]
  }
}
```


## Example Response (JSON)

The app responds with a JSON payload containing card data.  This payload may include:

* `results`: An array of up to five objects (more can be handled with pagination via links). Each object contains:
    * `objectId`: Unique ID.
    * `title`: Object title.
    * `link`: URL for details (optional, `null` if no links).
    * `created`, `priority`:  Custom properties defined in card settings.
    * `properties`: Array of additional custom properties not defined in the card settings.
    * `actions`:  Array of custom actions.

* `settingsAction`: Iframe action for updating app settings.
* `primaryAction`: Primary action for the record type.
* `secondaryActions`: Additional actions.


```json
{
  "results": [
    {
      "objectId": 245,
      "title": "API-22: APIs working too fast",
      "link": "http://example.com/1",
      "created": "2016-09-15",
      "priority": "HIGH",
      "project": "API",
      "description": "...",
      "actions": [...]
    },
    // ... more results
  ],
  "settingsAction": {...},
  "primaryAction": {...}
}
```


## Request Signatures

HubSpot verifies requests using the `X-HubSpot-Signature` header.  This header contains a Base64-encoded SHA-256 hash of: `<app secret> + <HTTP method> + <URL> + <request body>`.  The app must verify this signature to prevent spoofing.


## Card Properties

The card's properties are defined on the "Card Properties" tab.  You specify the property name, label, and data type (CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, STRING).  Each type might have specific requirements (e.g., `currencyCode` for CURRENCY).


## Custom Actions

Custom actions are defined on the "Custom actions" tab.  Action types include:

* **IFRAME:** Opens a modal containing an iframe.  No signature is used.  The iframe should use `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH). Includes `X-HubSpot-Signature`.
* **CONFIRMATION_ACTION_HOOK:**  Similar to ACTION_HOOK, but shows a confirmation dialog.  Includes `X-HubSpot-Signature`.


## Property Data Types

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Email address (displayed as a mailto link).
* **LINK:** URL; optionally, `linkLabel`.
* **NUMERIC:** Number.
* **STATUS:** Requires `optionType` (DEFAULT, SUCCESS, WARNING, DANGER, INFO).
* **STRING:** Text.


This documentation provides a comprehensive overview. Consult the official HubSpot API documentation for the most up-to-date and detailed information, including specific endpoint details for API-based card creation.
