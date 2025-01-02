# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displaying information from external systems within HubSpot contact, company, deal, and ticket records.  This differs from UI extensions; CRM cards are specifically for public apps.

## Scope Requirements

To create CRM cards, your app needs the necessary OAuth scopes to read and write to the relevant CRM objects. For example, a card on contact records requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing these scopes necessitates deleting all associated cards.  See HubSpot's OAuth documentation for details.


## Creating a CRM Card

Cards are created either via the API or through the HubSpot developer account UI.  The UI approach involves:

1. Navigating to **Apps** in the HubSpot developer account.
2. Selecting the target app.
3. Choosing **CRM cards** from the sidebar.
4. Clicking **Create CRM card**.

## Data Request

When a user views a CRM record, HubSpot sends a data fetch request to the app's specified `targetUrl`. This request includes default query parameters and custom parameters based on the card's settings.

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

**Request Parameters:**

| Parameter             | Type    | Description                                                                     |
|-----------------------|---------|---------------------------------------------------------------------------------|
| `userId`              | Default | HubSpot user ID who loaded the record.                                           |
| `userEmail`           | Default | Email address of the user.                                                      |
| `associatedObjectId`  | Default | ID of the CRM record.                                                           |
| `associatedObjectType` | Default | Type of CRM record (e.g., CONTACT, COMPANY).                                     |
| `portalId`            | Default | ID of the HubSpot account.                                                      |
| `firstname`, `email`, `lastname` | Custom | HubSpot properties specified in `propertiesToSend`; vary based on object type. |


**Important:** Requests timeout after 5 seconds (connection within 3 seconds).


## Example Response (JSON)

The app should respond with a JSON payload like this:

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
  "settingsAction": { ... },
  "primaryAction": { ... }
}
```

**Response Fields:**

* `results`: Array of card objects (max 5).  Each object can have:
    * `objectId`: Unique ID.
    * `title`: Title of the object.
    * `link`: URL for more details (optional; use `null` if no links).
    * `created`, `priority`, etc.: Custom properties defined in card settings.
    * `properties`: Array of additional custom properties not defined in settings.
    * `actions`: Array of available actions.
* `settingsAction`: Iframe action for app settings.
* `primaryAction`: Primary action for the record type.


## Request Signatures

HubSpot includes an `X-HubSpot-Signature` header to verify request authenticity.  This header is a base64 encoded SHA-256 hash of: `<app secret>+<HTTP method>+<URL>+<request body>`.


## Card Properties

Custom properties are defined on the **Card Properties** tab.  The response must include values for these properties.  Supported data types: `CURRENCY`, `DATE`, `DATETIME`, `EMAIL`, `LINK`, `NUMERIC`, `STATUS`, `STRING`.

**Example Custom Property (CURRENCY):**

```json
{
  "label": "Resolution impact",
  "dataType": "CURRENCY",
  "value": "94.34",
  "currencyCode": "GBP"
}
```

Specific formatting is required for each type (see detailed examples in the original text for DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, STRING).


## Custom Actions

Custom actions define URLs triggered by user clicks.  Actions include:

* **IFRAME Actions:** Open a modal with an iframe.  Uses `window.postMessage` to communicate with the CRM (`{"action": "DONE"}` or `{"action": "CANCEL"}`).

* **ACTION_HOOK Actions:** Send a server-side request (GET, POST, PUT, DELETE, PATCH).  Includes `X-HubSpot-Signature`.

* **CONFIRMATION_ACTION_HOOK Actions:** Similar to `ACTION_HOOK`, but with a confirmation dialog.  Includes `X-HubSpot-Signature`.


**Example Iframe Action (JSON):**

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

**Example ACTION_HOOK Action (JSON):**

```json
{
  "type": "ACTION_HOOK",
  "httpMethod": "POST",
  "uri": "https://example.com/action-hook",
  "label": "Example action",
  "associatedObjectProperties": ["some_crm_property"]
}
```

Remember to handle `X-HubSpot-Signature` verification for action hooks and confirmation actions.  Consult HubSpot's documentation for details on request validation and other aspects not fully covered here.
