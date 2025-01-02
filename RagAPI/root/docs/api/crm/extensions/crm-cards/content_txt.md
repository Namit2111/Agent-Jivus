# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displayed on HubSpot contact, company, deal, and ticket records within public apps.  These cards differ from UI extensions created with projects; they are specifically for public apps and offer less flexibility.  Consider UI extensions for private apps or more complex integrations.

## Scope Requirements

Before creating CRM cards, your app requires the necessary OAuth scopes to read and write to the relevant CRM object. For example, a card on contact records needs `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing these scopes requires deleting all associated cards. See the HubSpot OAuth documentation for more details.

## Creating a CRM Card

CRM cards can be created via the API or HubSpot's UI.

**Via HubSpot UI:**

1. Navigate to "Apps" in your HubSpot developer account.
2. Select your app.
3. Select "CRM cards" in the sidebar.
4. Click "Create CRM card".


## API Endpoints (Not explicitly defined in provided text, but implied)

The documentation refers to API endpoints for creating and managing CRM cards.  These endpoints are not detailed here but are implied to exist within the HubSpot developer portal.  Further exploration of the HubSpot developer documentation is needed to find these specifics.


## Data Request

When a user views a CRM record with a card, HubSpot sends a `GET` request to the app's specified `targetUrl`. This request includes:

* **Default Parameters:**
    * `userId`: HubSpot user ID.
    * `userEmail`: User's email address.
    * `associatedObjectId`: ID of the CRM record.
    * `associatedObjectType`: Type of CRM record (e.g., `CONTACT`, `COMPANY`).
    * `portalId`: HubSpot account ID.
* **Custom Parameters:**  HubSpot properties selected in the card settings (`propertiesToSend` array in the API).  These are appended as query parameters to the `targetUrl`.

**Example Request Configuration (JSON):**

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

**Request Timeout:** Requests timeout after 5 seconds; a connection must be established within 3 seconds.


## Example Response (JSON)

The app should respond with a JSON object containing:

* `results`: An array of up to five objects (cards). Each object can include:
    * `objectId`: Unique ID.
    * `title`: Card title.
    * `link`: URL for more details (optional, use `null` if no link).
    * `created`, `priority`: Custom properties defined in the card settings.
    * `properties`: Array of additional custom properties.  Each property has `label`, `dataType`, and `value`.  Supported `dataType` values: `CURRENCY`, `DATE`, `DATETIME`, `EMAIL`, `LINK`, `NUMERIC`, `STATUS`, `STRING`.  `CURRENCY` properties need `currencyCode` (ISO 4217). `DATETIME` values are milliseconds since epoch.  `LINK` properties can include `linkLabel`. `STATUS` properties need `optionType`: `DEFAULT`, `SUCCESS`, `WARNING`, `DANGER`, `INFO`.
    * `actions`: Array of actions (see below).
* `settingsAction`: IFrame action for app settings.
* `primaryAction`: Primary action for the record.
* `secondaryActions`: Additional actions.

**Example Response (JSON):**

```json
{
  "results": [
    { /* ... object 1 ... */ },
    { /* ... object 2 ... */ }
  ],
  "settingsAction": { /* ... */ },
  "primaryAction": { /* ... */ }
}
```

(See the provided text for a detailed example of the `results` object structure.)


## Request Signatures

HubSpot includes the `X-HubSpot-Signature` header to verify requests.  The signature is a SHA-256 hash of `<app secret>+<HTTP method>+<URL>+<request body>`.  The app must verify this signature to prevent spoofing.


## Custom Actions

The app can define custom actions within the CRM card.  These are specified in the `actions` array in the response.  Actions can be:

* **IFRAME:** Opens a modal with an iframe. Uses `window.postMessage` to communicate with the parent window (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH).  Includes `X-HubSpot-Signature`.
* **CONFIRMATION_ACTION_HOOK:** Same as `ACTION_HOOK`, but requires user confirmation.  Includes `X-HubSpot-Signature`.


(See the provided text for detailed examples of each action type.)


This documentation provides a comprehensive overview of the HubSpot CRM Cards API. Remember to consult the official HubSpot developer documentation for the most up-to-date information and details on API endpoints.
