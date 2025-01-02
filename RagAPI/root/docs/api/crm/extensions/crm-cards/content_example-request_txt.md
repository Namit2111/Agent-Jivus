# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displayed on HubSpot contact, company, deal, and ticket records within public apps.  This differs from UI extensions; CRM cards are for public apps, while UI extensions offer greater flexibility for private apps.

## Scope Requirements

To create CRM cards, your app needs the necessary OAuth scopes to read and write to the relevant CRM objects. For example, a card on contact records requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing CRM object scopes necessitates deleting all existing cards for those object types.  Refer to the HubSpot OAuth documentation for details on scopes and authorization URLs.


## Creating a CRM Card

CRM cards can be created via the API or HubSpot's UI.

### UI Creation:

1. Navigate to **Apps** in your HubSpot developer account.
2. Select your app.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card**.


### API Creation (Endpoints - see below for details)

The API allows programmatic creation and management of CRM cards.  The specific endpoints are not detailed in the provided text but would be found in the "Endpoints" tab mentioned in the original document.


## Data Request

When a user views a CRM record, HubSpot sends a data fetch request to your app's specified URL. This request includes default and custom query parameters.

### Request Configuration (Example):

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

### Example Request:

A `GET` request based on the above configuration might look like this:

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Parameters:**

| Parameter             | Type    | Description                                                                     |
|----------------------|---------|---------------------------------------------------------------------------------|
| `userId`              | Default | HubSpot user ID viewing the record.                                             |
| `userEmail`           | Default | Email of the user viewing the record.                                          |
| `associatedObjectId` | Default | ID of the CRM record.                                                            |
| `associatedObjectType`| Default | Type of CRM record (e.g., `CONTACT`, `COMPANY`, `DEAL`).                         |
| `portalId`            | Default | ID of the HubSpot account.                                                      |
| `firstname`, `email`, `lastname` | Custom  | Contact properties (specified in `propertiesToSend`).  Can be any custom property. |


**Important:** Requests timeout after 5 seconds; a connection must be established within 3 seconds.


## Example Response

Your app should respond with a JSON payload.

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

**Response Structure:**

* **`results` (array):**  An array of up to 5 card objects.
    * **`objectId` (number):** Unique ID for the object.
    * **`title` (string):** Title of the object.
    * **`link` (string, optional):** URL for more details (use `null` if no links).
    * **`created`, `priority` (string):** Custom properties defined in the card settings.
    * **`properties` (array, optional):** Array of additional custom properties.
    * **`actions` (array, optional):** Array of actions the user can take.
* **`settingsAction` (object, optional):** Iframe action for app settings.
* **`primaryAction` (object, optional):** Primary action for a record type (often creation).
* **`secondaryActions` (array, optional):** Additional actions displayed on the card.


## Request Signatures

HubSpot includes an `X-HubSpot-Signature` header to verify requests.  To validate:

1. Concatenate your app secret, HTTP method, URL, and request body.
2. Create a SHA-256 hash of the concatenated string.
3. Compare the hash with the signature in the header.


## Card Properties

Define custom properties to display on the card using the "Card Properties" tab.  Supported data types are: `CURRENCY`, `DATE`, `DATETIME`, `EMAIL`, `LINK`, `NUMERIC`, `STATUS`, `STRING`.


### Property Details:

* **`CURRENCY`:** Requires `currencyCode` (ISO 4217).
* **`DATE`:**  `yyyy-mm-dd` format.
* **`DATETIME`:** Milliseconds since epoch.
* **`EMAIL`:** Email address (displayed as a mailto link).
* **`LINK`:** URL, optionally with `linkLabel`.
* **`NUMERIC`:** Number.
* **`STATUS`:**  Requires `optionType`: `DEFAULT`, `SUCCESS`, `WARNING`, `DANGER`, `INFO`.
* **`STRING`:** Text.


## Custom Actions

Define custom actions using the "Custom Actions" tab.  Action types include:

### Iframe Actions (`IFRAME`):

Open a modal with an iframe.  The iframe URL is provided in the response.  Use `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).

### Action Hook Actions (`ACTION_HOOK`):

Send a server-side request (GET, POST, PUT, DELETE, PATCH).  Includes `X-HubSpot-Signature`.

### Confirmation Actions (`CONFIRMATION_ACTION_HOOK`):

Similar to `ACTION_HOOK`, but displays a confirmation dialog. Includes `X-HubSpot-Signature`.


This documentation provides a comprehensive overview of the HubSpot CRM Cards API.  Consult the HubSpot Developer documentation for the latest information and complete API specifications (endpoints).
