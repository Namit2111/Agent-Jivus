# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displayed on HubSpot contact, company, deal, and ticket records within a public app.  This differs from UI extensions created with projects; CRM cards are for public apps, while UI extensions offer more flexibility.

## Scope Requirements

To create CRM cards, your app needs the necessary OAuth scopes to read and write to the relevant CRM objects.  For example, a card on contact records requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing object scopes necessitates deleting all existing cards for those object types.  See the HubSpot OAuth documentation for details on scopes and authorization URLs.

## Creating a CRM Card

CRM cards can be created via the API or the HubSpot developer account UI.

**Using the HubSpot UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select your app.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card**.

**Using the API (see Endpoints section below):**  The API provides a more programmatic way to create and manage CRM cards.


## Data Request

When a user views a CRM record with a CRM card, HubSpot makes an outbound request to your app's specified URL. This request includes default and custom query parameters:

**Request Parameters:**

| Parameter             | Type    | Description                                                                   |
|------------------------|---------|-------------------------------------------------------------------------------|
| `userId`               | Default | HubSpot user ID viewing the record.                                             |
| `userEmail`            | Default | Email address of the user viewing the record.                                   |
| `associatedObjectId`   | Default | ID of the CRM record.                                                        |
| `associatedObjectType` | Default | Type of CRM record (e.g., `CONTACT`, `COMPANY`, `DEAL`).                      |
| `portalId`             | Default | ID of the HubSpot account.                                                   |
| Custom Properties     | Custom  | HubSpot properties selected in the app UI (`propertiesToSend` array in API). |


**Example Request (Contact Card):**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Configuration (API Example):**

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

**Request Timeouts:** The request will timeout after 5 seconds; a connection must be established within 3 seconds.


## Example Response

Your app should respond with a JSON object containing card data.

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
      "actions": [ /* ... actions ... */ ]
    }
  ],
  "settingsAction": { /* ... settings action ... */ },
  "primaryAction": { /* ... primary action ... */ }
}
```

**Response Structure:**

* `results`: An array of objects (max 5). Each object represents a card item.
    * `objectId`: (required) Unique ID for the object.
    * `title`: (required) Title of the object.
    * `link`: (optional) URL for details; use `null` if no links are available.
    * `created`, `priority`:  Example custom properties (defined in Card Properties).
    * `actions`: An array of actions the user can take.
    * `properties`: An array of additional custom properties not defined in the card settings.


## Request Signatures

HubSpot includes the `X-HubSpot-Signature` header to verify requests.  To validate:

1. Concatenate your app secret, HTTP method, URL, and request body.
2. Generate a SHA-256 hash of the concatenated string.
3. Compare the hash to the signature in the header.


## Card Properties

Define custom properties to display on the card.  Specify a unique name, label, and data type for each property. Supported data types include: `CURRENCY`, `DATE`, `DATETIME`, `EMAIL`, `LINK`, `NUMERIC`, `STATUS`, `STRING`.

**Property Type Details:**

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Displays as a mailto link.
* **LINK:** Displays a hyperlink; optional `linkLabel`.
* **NUMERIC:** Displays a number.
* **STATUS:** Displays a colored indicator (`optionType`: `DEFAULT`, `SUCCESS`, `WARNING`, `DANGER`, `INFO`).
* **STRING:** Displays text.


## Custom Actions

Define URLs for actions displayed on the card. Actions can be:

* **IFRAME:** Opens a modal with an iframe.  Uses `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request; success/error message shown to the user.  Supports `GET`, `POST`, `PUT`, `DELETE`, `PATCH` HTTP methods.
* **CONFIRMATION_ACTION_HOOK:**  Similar to `ACTION_HOOK`, but with a confirmation dialog.


## API Endpoints

(This section requires specifics from the actual API documentation that was not fully included in the provided text.  It should include details on the endpoints for creating, updating, and deleting CRM cards, along with request/response examples for each endpoint.)


##  Example IFrame Action:

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

## Example `window.postMessage` for IFrame Actions:

```javascript
window.parent.postMessage(JSON.stringify({"action": "DONE"}), "*");
```


This documentation provides a comprehensive overview of the HubSpot CRM Cards API. Remember to consult the official HubSpot API documentation for the most up-to-date information and details on API endpoints.
