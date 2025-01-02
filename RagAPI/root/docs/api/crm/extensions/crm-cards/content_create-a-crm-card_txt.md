# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displaying information from external systems within HubSpot contact, company, deal, and ticket records.  This differs from UI extensions; CRM cards are specifically for public apps.

## Scope Requirements

Before creating CRM cards, your app needs the necessary OAuth scopes to read and write to the relevant CRM objects.  For example, a card on contact records requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes. Removing CRM object scopes necessitates deleting all existing cards for those object types. Refer to the HubSpot OAuth documentation for details on scopes and authorization URLs.

## Creating a CRM Card

CRM cards can be created via the API or through the HubSpot developer account UI.

**Using the HubSpot UI:**

1. Navigate to "Apps" in your HubSpot developer account.
2. Select the app.
3. Select "CRM cards" in the left sidebar.
4. Click "Create CRM Card".
5. Configure the card's settings (detailed below).

**Using the API:** (Endpoint details not provided in the source text, refer to HubSpot's API documentation for specific endpoints).

## Data Request

When a user views a CRM record with a CRM card, HubSpot makes an outbound request to the app's specified URL.  This request includes:

* **Default Query Parameters:**
    * `userId`: HubSpot user ID.
    * `userEmail`: HubSpot user email.
    * `associatedObjectId`: CRM record ID.
    * `associatedObjectType`: CRM record type (e.g., `CONTACT`, `COMPANY`).
    * `portalId`: HubSpot account ID.
* **Custom Query Parameters:**  These are specified in the card's settings and include HubSpot properties selected to be sent (e.g., `firstname`, `email`, `lastname`).

**Example Request:**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Configuration (JSON):**

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

**Important:** Requests timeout after 5 seconds; connection must be established within 3 seconds.


## Example Response

The app should respond with a JSON object containing the data to display on the card.

**Example Response:**

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

**Response Structure:**

* `results`: An array of objects (max 5), each representing a data item to display.  Each object can include:
    * `objectId`: Unique ID.
    * `title`: Title of the object.
    * `link`: URL for more details (optional; use `null` if no links).
    * `created`: Date of creation (custom property).
    * `priority`: Priority level (custom property).
    * `properties`: Array of additional custom properties (label, dataType, value).
    * `actions`: Array of actions (see below).
* `settingsAction`: Iframe action for app settings.
* `primaryAction`: Primary action for a record type.


## Request Signatures

HubSpot includes the `X-HubSpot-Signature` header to verify request authenticity.  To validate:

1. Concatenate `<app secret> + <HTTP method> + <URL> + <request body>`.
2. Generate a SHA-256 hash of the concatenated string.
3. Compare the hash to the signature in the header.


## Card Properties

Define custom properties to display on the card.  Specify name, label, and data type (CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, STRING).

**Property Type Details:**

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Displays as a mailto link.
* **LINK:** Displays a hyperlink; `linkLabel` is optional.
* **NUMERIC:** Displays a number.
* **STATUS:** Displays as a colored indicator (DEFAULT, SUCCESS, WARNING, DANGER, INFO).  Requires `optionType`.
* **STRING:** Displays text.


## Custom Actions

Define action URLs for buttons on the card.  Action types include:

* **IFRAME:** Opens a modal with an iframe.  Uses `window.postMessage` to communicate with the parent window ({"action": "DONE"} or {"action": "CANCEL"}).
* **ACTION_HOOK:** Sends a server-side request; only success/error message shown to the user.  Includes `X-HubSpot-Signature`.
* **CONFIRMATION_ACTION_HOOK:**  Similar to ACTION_HOOK, but displays a confirmation dialog.  Includes `X-HubSpot-Signature`.


All action types use the `uri` field for the action URL.  `associatedObjectProperties` can be used to include additional query parameters (for GET/DELETE requests, appended to the URL; for POST/PUT/PATCH, sent in the request body).  `httpMethod` can be GET, POST, PUT, DELETE, or PATCH.


This documentation provides a comprehensive overview.  Consult the official HubSpot API documentation for detailed endpoint specifications and error handling.
