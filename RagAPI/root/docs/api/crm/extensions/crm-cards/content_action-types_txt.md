# HubSpot CRM API: CRM Cards

This document details how to create and manage custom CRM cards within HubSpot's public apps using their API.  These cards differ from UI extensions created with developer projects; they are specifically designed for public apps and offer less flexibility but simpler integration.

## Overview

CRM cards allow you to display information from external systems directly on HubSpot contact, company, deal, and ticket records.  Each app can have up to 25 CRM cards.  This is useful for surfacing data from integrated applications within the HubSpot context, improving workflow efficiency for users.

**Key Differences from UI Extensions:** CRM cards are simpler to implement than UI extensions but offer less customization. If you need more advanced features or are not building a public app, consider using React-based UI extensions.

**Example Use Case:**  An integration with bug tracking software, displaying tracked bugs on contact records for support reps.


## Scope Requirements

Your app needs specific OAuth scopes to create CRM cards.  For example, a card on contact records requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing object scopes requires deleting all associated cards.  Refer to the HubSpot OAuth documentation for details on scopes and authorization URLs.


## Creating a CRM Card

CRM cards can be created via the API or HubSpot's UI:

**Using the HubSpot UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select the app.
3. Select **CRM cards** in the sidebar.
4. Click **Create CRM card**.


## Data Request

When a user views a relevant CRM record, HubSpot sends a data fetch request to your app's specified URL. This request includes default query parameters and custom properties selected in the card's settings.

**Data Fetch URL:**  The URL where your app receives the data request (the `targetUrl` field in the API).

**Target Record Types and Properties:**  Specify which CRM object types (contacts, companies, deals, tickets) the card appears on and which HubSpot properties to include as query parameters.  This is configured via the UI or the `objectTypes` array in the API.


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

**Example Request:**

A GET request might look like this:

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Parameters:**

| Parameter             | Type     | Description                                                                 |
|-----------------------|----------|-----------------------------------------------------------------------------|
| `userId`              | Default  | HubSpot user ID.                                                            |
| `userEmail`           | Default  | User's email address.                                                       |
| `associatedObjectId`  | Default  | ID of the CRM record.                                                        |
| `associatedObjectType` | Default  | CRM record type (CONTACT, COMPANY, DEAL, TICKET).                            |
| `portalId`            | Default  | HubSpot account ID.                                                          |
| `firstname`, `email`, `lastname` | Custom   | Contact properties (example; depends on `propertiesToSend`).                 |

**Timeout:** Requests timeout after 5 seconds (connection within 3 seconds).


## Example Response

Your app should return a JSON response like this:

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
  "settingsAction": {
    // ... settings action ...
  },
  "primaryAction": {
    // ... primary action ...
  }
}
```

**Response Fields:**

* `results`: Array of objects (up to 5).
    * `objectId`: Unique ID.
    * `title`: Object title.
    * `link`: URL for details (optional, `null` if no links).
    * `created`, `priority`: Example custom properties.
    * `actions`: Array of actions.
    * `properties`: Array of additional custom properties.
* `settingsAction`: Iframe action for app settings.
* `primaryAction`: Primary action for the record.
* `secondaryActions`: Additional actions.


## Request Signatures

HubSpot uses a signature header (`X-HubSpot-Signature`) to verify requests.  To verify:

1. Concatenate your app secret, HTTP method, URL, and request body.
2. Create a SHA-256 hash of the string.
3. Compare the hash with the signature.


## Card Properties

Define custom properties to display on the card using the **Card Properties** tab.  Specify name, label, and data type (CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, STRING).


## Property Types

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Email address (displayed as a link).
* **LINK:** URL (can specify `linkLabel`).
* **NUMERIC:** Number.
* **STATUS:** Status indicator (DEFAULT, SUCCESS, WARNING, DANGER, INFO). Requires `optionType`.
* **STRING:** Text.


## Custom Actions

Define action URLs on the **Custom Actions** tab.  Actions can be:

* **IFRAME:** Opens a modal with an iframe.  Uses `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH). Includes request signature.
* **CONFIRMATION_ACTION_HOOK:** Same as ACTION_HOOK, but with a confirmation dialog. Includes request signature.


## Conclusion

By following these guidelines, you can effectively integrate custom CRM cards into your HubSpot public apps, enriching the user experience and streamlining workflows.  Remember to consult the HubSpot API documentation for the most up-to-date information and details.
