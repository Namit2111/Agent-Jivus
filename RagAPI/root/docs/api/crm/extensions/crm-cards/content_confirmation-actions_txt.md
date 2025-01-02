# HubSpot CRM Card Integration Guide

This document details the integration process for creating custom CRM cards within HubSpot public apps.  These cards display information from external systems directly on HubSpot contact, company, deal, and ticket records.  This differs from UI extensions built using developer projects which offer more flexibility and customizability.

## Scope Requirements

Before creating CRM cards, your app needs the necessary OAuth scopes to read and write to the relevant CRM objects.  For example, to display a card on contact records, your app requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing object scopes requires deleting all existing cards for those object types.  Refer to the HubSpot OAuth documentation for details on scopes and setting up authorization URLs.


## Creating a CRM Card

CRM cards can be created either via the API or through the HubSpot developer account UI.

**Using the HubSpot UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select the app where you want to add a card.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card**.
5. Configure the card using the provided tabs (detailed below).


## Data Fetch Request

When a user views a CRM record, HubSpot sends a data fetch request to your app's specified URL. This request includes default and custom query parameters.

**Data Fetch URL Configuration:**

* **`targetUrl`:** The URL where HubSpot will fetch data (e.g., `"https://www.example.com/demo-fetch"`).
* **`objectTypes`:** An array of objects, each specifying a CRM object type and the HubSpot properties to include as query parameters.

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

The above configuration results in a GET request like this:

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Parameters:**

| Parameter             | Type    | Description                                                                         |
|----------------------|---------|-------------------------------------------------------------------------------------|
| `userId`              | Default | HubSpot user ID.                                                                     |
| `userEmail`           | Default | Email address of the logged-in user.                                                 |
| `associatedObjectId`  | Default | ID of the CRM record.                                                              |
| `associatedObjectType` | Default | Type of CRM record (e.g., CONTACT, COMPANY, DEAL).                                  |
| `portalId`            | Default | ID of the HubSpot account.                                                          |
| `firstname`, `email`, `lastname` | Custom  | HubSpot properties specified in `propertiesToSend`.                               |


**Important:** Requests timeout after 5 seconds; a connection must be established within 3 seconds.


## Example Response

Your app should respond with a JSON structure containing the data for the CRM card.

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
      "actions": [ /* ... actions ... */ ]
    },
    // ... more results ...
  ],
  "settingsAction": { /* ... */ },
  "primaryAction": { /* ... */ }
}
```

**Response Structure:**

* **`results`:** An array of objects (up to 5).  Each object represents a data item to display on the card.
* **`objectId`:** (required) Unique ID for the object.
* **`title`:** (required) Title of the object.
* **`link`:** (optional) URL for more details. Use `null` if no objects have a link.
* **`created`, `priority` etc.:** Custom properties defined in the card settings.
* **`properties`:** An array of additional custom properties not defined in card settings.
* **`actions`:** An array of custom actions.
* **`settingsAction`:** An iframe action to update app settings.
* **`primaryAction`:** The primary action for a record type.
* **`secondaryActions`:** Additional actions.


## Request Signatures

HubSpot includes an `X-HubSpot-Signature` header to verify request authenticity.  To validate:

1. Concatenate your app secret, HTTP method, URL, and request body (if any).
2. Generate a SHA-256 hash of the concatenated string.
3. Compare the hash with the signature in the header.


## Card Properties

Define custom properties to display on the card using the **Card Properties** tab.  Specify a unique name, display label, and data type (CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, STRING).


## Custom Properties Data Types

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Email address (displayed as a mailto link).
* **LINK:** URL (with optional `linkLabel`).
* **NUMERIC:** Number.
* **STATUS:**  Requires `optionType` (DEFAULT, SUCCESS, WARNING, DANGER, INFO).
* **STRING:** Text.


## Custom Actions

Define custom actions (buttons) on the **Custom Actions** tab.  Actions can be:

* **IFRAME:** Opens a modal with an iframe.  Uses `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH). Includes `X-HubSpot-Signature`.
* **CONFIRMATION_ACTION_HOOK:** Similar to `ACTION_HOOK`, but shows a confirmation dialog. Includes `X-HubSpot-Signature`.


## Example Iframe Action:

```json
{
  "type": "IFRAME",
  "width": 890,
  "height": 748,
  "uri": "https://example.com/iframe-contents",
  "label": "Edit",
  "associatedObjectProperties": ["some_crm_property"]
}
```

## Example Action Hook Action:

```json
{
  "type": "ACTION_HOOK",
  "httpMethod": "POST",
  "uri": "https://example.com/action-hook",
  "label": "Example action",
  "associatedObjectProperties": ["some_crm_property"]
}
```

Remember to consult the HubSpot API documentation for the most up-to-date information and details.
