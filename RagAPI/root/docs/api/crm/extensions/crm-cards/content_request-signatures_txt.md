# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displaying information from external systems within HubSpot contact, company, deal, and ticket records.

## Overview

HubSpot CRM cards enable integrations to display data directly on HubSpot CRM records.  When a user views a record, HubSpot makes a request to the integrated app, which returns data formatted as a card.  These cards can also include custom actions. This differs from UI extensions built with projects; CRM cards are designed specifically for public apps.  If you are not building a public app, consider using React-based UI extensions instead.

**Maximum Cards per App:** 25

**Use Case Example:** An app for bug tracking software could display a card on contact records showing associated bugs, allowing support reps quick access to relevant information.

## Scope Requirements

To create CRM cards, your app needs the necessary OAuth scopes to read and write to the relevant CRM objects. For example, a card on contact records requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes. Removing CRM object scopes requires deleting all existing cards for those object types.  See HubSpot's OAuth documentation for more details.


## Creating a CRM Card

CRM cards can be created via the API or through the HubSpot developer account UI.

**Using the HubSpot UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select the app.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM Card**.

**Using the API (see Endpoints section below)**


## Data Request

When a user views a CRM record with a card, HubSpot sends a GET request to the app's specified URL.  This request includes several default parameters and custom parameters based on the card's settings.

**Data Fetch URL:**  The URL where HubSpot sends the data request (`targetUrl` in the API).

**Target Record Types:**  Specify which CRM object types (contacts, companies, deals, tickets) the card appears on.

**Properties Sent from HubSpot:** Select HubSpot properties to include as query parameters in the request. (`propertiesToSend` array in the API).


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

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Parameters:**

| Parameter             | Type    | Description                                                                  |
|----------------------|---------|------------------------------------------------------------------------------|
| `userId`              | Default | HubSpot user ID who loaded the record.                                      |
| `userEmail`           | Default | Email address of the user who loaded the record.                             |
| `associatedObjectId`  | Default | ID of the CRM record.                                                        |
| `associatedObjectType` | Default | Type of CRM record (e.g., CONTACT, COMPANY, DEAL).                           |
| `portalId`            | Default | ID of the HubSpot account.                                                  |
| `firstname`, `email`, `lastname` | Custom | HubSpot contact properties (example, depends on `propertiesToSend`). |


**Timeout:** Requests timeout after 5 seconds (connection within 3 seconds).


## Example Response

The app responds with a JSON payload.

```json
{
  "results": [
    {
      "objectId": 245,
      "title": "API-22: APIs working too fast",
      "link": "http://example.com/1",
      "created": "2016-09-15",
      "priority": "HIGH",
      // ... other properties
      "actions": [ /* array of actions */ ]
    },
    // ... more results
  ],
  "settingsAction": { /* iframe action for settings */ },
  "primaryAction": { /* primary action */ },
  "secondaryActions": [ /* array of secondary actions */ ]
}
```

**Response Fields:**

* `results`: Array of objects (up to 5). Each object represents an item displayed on the card.
* `objectId`: Unique ID for the object.
* `title`: Title of the object.
* `link`: URL for more details (optional, use `null` if no links).
* `created`, `priority`: Example custom properties (defined in Card Properties).
* `actions`: Array of custom actions.
* `properties`: Array of additional custom properties not defined in card settings.
* `settingsAction`, `primaryAction`, `secondaryActions`: Actions defined in Custom Actions.


## Request Signatures

HubSpot includes an `X-HubSpot-Signature` header to verify requests.  To validate:

1. Concatenate `<app secret> + <HTTP method> + <URL> + <request body>`.
2. Create a SHA-256 hash of the concatenated string.
3. Compare the hash to the signature in the header.

## Card Properties

Define custom properties displayed on the card.

* **Add Property:** Use the UI to add properties.
* **Property Name, Label, Data Type:**  Specify these details for each property.  Data types include: `CURRENCY`, `DATE`, `DATETIME`, `EMAIL`, `LINK`, `NUMERIC`, `STATUS`, `STRING`.
* **Payload:** The response must include values for these properties.


## Property Types

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Displays as a mailto link.
* **LINK:** Displays a hyperlink; use `linkLabel` to customize label.
* **NUMERIC:** Displays numbers.
* **STATUS:** Displays colored indicators (`optionType`: `DEFAULT`, `SUCCESS`, `WARNING`, `DANGER`, `INFO`).
* **STRING:** Displays text.

## Custom Actions

Define actions users can take on the card.  Actions are defined using the `actions` array within each object in the `results` array of the response.

* **Action Types:** `IFRAME`, `ACTION_HOOK`, `CONFIRMATION_ACTION_HOOK`
* **`IFRAME` Actions:** Opens a modal with an iframe.  Use `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **`ACTION_HOOK` Actions:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH). Includes `X-HubSpot-Signature`.
* **`CONFIRMATION_ACTION_HOOK` Actions:** Similar to `ACTION_HOOK`, but requires confirmation from the user. Includes `X-HubSpot-Signature`.


**Example Action (JSON):**

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


## API Endpoints

*(This section requires details not provided in the original text.  The provided text mentions an "Endpoints" tab but doesn't specify the actual API endpoints.  To complete this section, the actual API endpoints and their methods (POST, GET, etc.) would be needed.)*


This documentation provides a comprehensive overview of the HubSpot CRM Cards API. Remember to consult the official HubSpot documentation for the most up-to-date information and specific API endpoint details.
