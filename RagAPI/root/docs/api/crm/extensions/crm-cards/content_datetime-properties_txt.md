# HubSpot CRM API: CRM Cards

This document details how to create and manage custom CRM cards within HubSpot using the API.  CRM cards allow you to display information from external systems directly on HubSpot contact, company, deal, and ticket records within a public app.

## Key Differences from UI Extensions

The CRM cards described here differ from custom cards created as UI extensions using projects.  CRM cards are designed for public apps, while UI extensions offer greater flexibility, customizability, and interactivity using a more modern toolset.  If you're not building a public app, consider using React-based UI extensions.


## Use Case Example

Imagine integrating bug tracking software with the HubSpot App Marketplace.  You can create a CRM card to display tracked bugs on contact records, enabling support reps to access this information directly within HubSpot.


## Scope Requirements

To create CRM cards, your app requires OAuth scopes to modify the relevant CRM records. For example, a card on contact records needs `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes. Removing CRM object scopes requires deleting all existing cards for those object types.  Refer to the HubSpot OAuth documentation for more details on scopes and authorization URL setup.


## Creating a CRM Card

CRM cards can be created via the API or through the HubSpot developer account UI.  This document focuses on the API. For UI instructions, see the "Create a CRM Card" section within the original documentation.


## Data Request

When a user views a CRM record displaying a card, HubSpot sends a data fetch request to the app's specified URL. This request includes default query parameters and additional parameters containing property data defined in the card's settings.

**Data Fetch URL:**  The URL where HubSpot fetches data (the `targetUrl` field in the API).

**Target Record Types:** Specify which CRM records (contacts, companies, deals, tickets) will display the card.  Select HubSpot properties to include as query parameters in the request URL (`objectTypes` array in the API).

**Example Data Fetch Configuration (JSON):**

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

**Example Request:**

The above configuration results in a GET request like this:

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Parameters:**

| Parameter             | Type    | Description                                                                     |
|----------------------|---------|---------------------------------------------------------------------------------|
| `userId`              | Default | HubSpot user ID who loaded the CRM record.                                     |
| `userEmail`           | Default | Email address of the user who loaded the CRM record.                            |
| `associatedObjectId`  | Default | ID of the loaded CRM record.                                                  |
| `associatedObjectType` | Default | Type of CRM record (e.g., CONTACT, COMPANY, DEAL).                             |
| `portalId`            | Default | ID of the HubSpot account where the record loaded.                             |
| `firstname`, `email`, `lastname` | Custom  | Contact properties (as specified in `propertiesToSend`).                      |


**Timeout:** Requests time out after 5 seconds; a connection must be established within 3 seconds.


## Example Response

HubSpot expects a response like this:

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

**Response Structure:**

*   `results`: An array (up to 5 objects) containing card data.
*   `objectId`: Unique ID for the object.
*   `title`: Title of the object.
*   `link`: URL for more details (optional; use `null` if no links).
*   `created`, `priority`: Example custom properties (defined in card settings).
*   `actions`: Array of actions users can take.
*   `properties`: Array of additional custom properties not defined in card settings.
*   `settingsAction`: Iframe action to update app settings.
*   `primaryAction`: Primary action for a record type.
*   `secondaryActions`: List of additional actions.


## Request Signatures

HubSpot uses the `X-HubSpot-Signature` header to verify requests.  To validate:

1.  Concatenate the app secret, HTTP method, URL, and request body (if any).
2.  Create a SHA-256 hash of the concatenated string.
3.  Compare the hash to the signature in the header.


## Card Properties

Define custom properties to display on the CRM card.  Specify the property name, label, and data type (CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, STRING).


## Property Types

*   **CURRENCY:** Requires `currencyCode` (ISO 4217).
*   **DATE:**  `yyyy-mm-dd` format.
*   **DATETIME:** Milliseconds since epoch.
*   **EMAIL:** Displays as a mailto link.
*   **LINK:** Displays a hyperlink; `linkLabel` is optional.
*   **NUMERIC:** Displays numbers.
*   **STATUS:** Displays colored indicators (DEFAULT, SUCCESS, WARNING, DANGER, INFO). Requires `optionType`.
*   **STRING:** Displays text.


## Custom Actions

Define URLs for action buttons on the card.  Actions can be:

*   **IFRAME:** Opens a modal with an iframe.  Uses `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
*   **ACTION_HOOK:** Sends a server-side request; only shows success/error messages.
*   **CONFIRMATION_ACTION_HOOK:**  Similar to `ACTION_HOOK`, but displays a confirmation dialog.


All actions except IFRAMEs include the `X-HubSpot-Signature` header.  The `associatedObjectProperties` field allows adding custom query parameters or request body properties.


This markdown documentation provides a comprehensive overview of HubSpot's CRM Card API, covering essential aspects from setup to advanced features.  Remember to consult the official HubSpot documentation for the most up-to-date information and specific API details.
