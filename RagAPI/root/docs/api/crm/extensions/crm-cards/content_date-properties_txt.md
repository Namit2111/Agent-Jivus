# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displaying information from external systems within HubSpot contact, company, deal, and ticket records.  This differs from UI extensions; CRM cards are for public apps, while UI extensions offer greater flexibility for private apps.

## Scope Requirements

To create CRM cards, your app needs the necessary OAuth scopes to read and write to the relevant CRM object. For example, a card on contact records requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes. Removing CRM object scopes requires deleting all existing cards for those object types.  See the HubSpot OAuth documentation for more details on scopes and authorization URLs.


## Creating a CRM Card

CRM cards can be created via the API or HubSpot's UI.  The UI approach is outlined below; API details are covered in the "Endpoints" section (which is unfortunately missing from the provided text, and would need to be added for completeness).

**UI Creation Steps:**

1. Navigate to "Apps" in your HubSpot developer account.
2. Select the app where you want to add the card.
3. Select "CRM Cards" in the left sidebar.
4. Click "Create CRM Card" in the upper right.
5. Configure the card settings in the provided tabs.


## Data Request

When a user views a CRM record, HubSpot sends a data fetch request to your app's specified URL. This request includes default and custom query parameters:


**Request Parameters:**

| Parameter             | Type    | Description                                                                    |
|-----------------------|---------|--------------------------------------------------------------------------------|
| `userId`              | Default | HubSpot user ID who loaded the record.                                          |
| `userEmail`           | Default | Email address of the user who loaded the record.                               |
| `associatedObjectId`  | Default | ID of the loaded CRM record.                                                  |
| `associatedObjectType` | Default | Type of CRM record (e.g., `CONTACT`, `COMPANY`, `DEAL`).                       |
| `portalId`            | Default | ID of the HubSpot account.                                                     |
| Other Properties     | Custom  | HubSpot properties specified in the card's settings (`propertiesToSend` array). |


**Example Request:**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Configuration (Example):**

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

**Timeout:** Requests timeout after 5 seconds; a connection must be established within 3 seconds.


## Example Response

Your app responds with a JSON object containing card data.

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
      // ... other properties ...
      "actions": [
        // ... action objects ...
      ]
    },
    // ... other result objects ...
  ],
  "settingsAction": { /* ... */ },
  "primaryAction": { /* ... */ },
  "secondaryActions": [ /* ... */ ]
}
```

**Response Structure:**

*   `results`: An array of up to five card objects.
*   `objectId`: Unique ID for the object.
*   `title`: Title of the object.
*   `link`: URL for more details (optional, use `null` if no link).
*   `created`, `priority`: Example custom properties (defined in card settings).
*   `actions`: An array of action objects.
*   `properties`: Array of additional custom properties not defined in card settings.
*   `settingsAction`, `primaryAction`, `secondaryActions`: Action objects for settings, primary action, and secondary actions respectively.


## Request Signatures

HubSpot uses the `X-HubSpot-Signature` header to verify requests. To validate:

1.  Concatenate your app secret, HTTP method, URL, and request body.
2.  Generate a SHA-256 hash of the concatenated string.
3.  Compare the hash to the signature in the header.


## Card Properties

The "Card Properties" tab lets you define custom properties displayed on the card.  These properties should be included in your response.  Supported data types include: `CURRENCY`, `DATE`, `DATETIME`, `EMAIL`, `LINK`, `NUMERIC`, `STATUS`, and `STRING`.  Specific formatting requirements exist for each type (detailed below).

### Property Data Types

*   **CURRENCY:** Requires `currencyCode` (ISO 4217).
*   **DATE:** `yyyy-mm-dd` format.
*   **DATETIME:** Milliseconds since epoch.
*   **EMAIL:** Email address (displayed as a mailto link).
*   **LINK:** URL; `linkLabel` is optional.
*   **NUMERIC:** Number.
*   **STATUS:** Requires `optionType`: `DEFAULT`, `SUCCESS`, `WARNING`, `DANGER`, `INFO`.
*   **STRING:** Text.


## Custom Actions

The "Custom Actions" tab lets you define action URLs.  These URLs are used in action objects within your response.

### Action Types

*   **IFRAME:** Opens a modal with an iframe. Uses `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
*   **ACTION_HOOK:** Sends a server-side request (includes `X-HubSpot-Signature`).  HTTP methods: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`.
*   **CONFIRMATION_ACTION_HOOK:** Similar to `ACTION_HOOK`, but displays a confirmation dialog.


This documentation provides a comprehensive overview of the HubSpot CRM Cards API.  Remember that the API endpoint specifications are missing from the original text and would need to be added for complete functionality.
