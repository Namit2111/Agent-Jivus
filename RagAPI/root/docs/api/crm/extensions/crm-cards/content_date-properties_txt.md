# HubSpot CRM API: CRM Cards

This document details how to create and manage custom CRM cards within HubSpot public apps using the HubSpot API.  These cards display information from external systems directly on HubSpot contact, company, deal, and ticket records.  Note that these CRM cards are distinct from custom cards created as UI extensions using projects.  UI extensions offer greater flexibility and are recommended for non-public app integrations.

## Overview

CRM cards allow you to enrich HubSpot records with data from your app.  Your app defines the card, specifying a data fetch URL and properties to display. When a user views a relevant CRM record, HubSpot sends a request to your app's URL, retrieves the data, and renders it as a card on the record page.  You can also define custom actions for users to interact with the data.  Each app is limited to 25 CRM cards.

**Use Case Example:**  An app integrating bug tracking software can display tracked bugs directly on HubSpot contact records for support representatives.

## Scope Requirements

To create CRM cards, your app requires OAuth scopes to read and write to the relevant CRM objects.  For example, a card on contact records needs `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes. Removing object scopes requires deleting all existing cards for those object types.  See the HubSpot OAuth documentation for details on scopes and authorization URLs.

## Creating a CRM Card

CRM cards can be created via the API or the HubSpot developer account UI.  The API approach is detailed in the "Endpoints" section (not included in provided text, but would be a section in the full documentation).

**Using the HubSpot UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select the app where you want to add a card.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card**.
5. Configure the card settings (detailed below).

## Data Request

When a user views a CRM record, HubSpot makes a data fetch request to your app's specified URL. This request includes default query parameters and custom parameters based on the card's settings.

**Data Fetch URL:**  The URL your app uses to fetch data.  In the API, this is the `targetUrl` field.

**Target Record Types:**  Select the CRM object types (contacts, companies, deals, tickets) where the card should appear.  Select HubSpot properties to include as query parameters in the request URL using the UI's dropdown menus or the `propertiesToSend` array in the API.

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
  // ...
}
```

**Example Request:**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Parameters:**

* `userId`: HubSpot user ID.
* `userEmail`: HubSpot user email.
* `associatedObjectId`: ID of the CRM record.
* `associatedObjectType`: Type of CRM record (CONTACT, COMPANY, DEAL, TICKET).
* `portalId`: HubSpot account ID.
* **Custom Properties:**  Properties specified in the card settings (e.g., `firstname`, `email`, `lastname`).

**Timeout:** Requests timeout after 5 seconds; a connection must be established within 3 seconds.


## Example Response

Your app should respond with a JSON payload containing card data.

**Example Response (JSON):**

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
  "settingsAction": { ... },
  "primaryAction": { ... }
}
```

**Response Fields:**

* `results`: An array of up to five objects.  Each object represents an item displayed on the card.
* `objectId`: Unique ID for the object.
* `title`: Title of the object.
* `link`: URL for more details (optional, use `null` if no links).
* `created`, `priority`: Example custom properties defined in card settings.
* `properties`: Array of additional custom properties not defined in the settings.
* `actions`: Array of custom actions (see below).
* `settingsAction`: Iframe action for updating app settings.
* `primaryAction`: Primary action for the record type.
* `secondaryActions`: Additional actions.

## Request Signatures

HubSpot includes the `X-HubSpot-Signature` header to authenticate requests.  To verify:

1. Concatenate your app secret, HTTP method, URL, and request body.
2. Calculate the SHA-256 hash of the concatenated string.
3. Compare the hash to the signature in the header.

See the HubSpot documentation for detailed request validation instructions.


## Card Properties

The **Card Properties** tab defines custom properties displayed on the card.  You add properties specifying a name, label, and data type (CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, STRING).

**Property Data Types:**

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Email address, displayed as a mailto link.
* **LINK:** URL, with optional `linkLabel`.
* **NUMERIC:** Number.
* **STATUS:** Displays colored indicators (DEFAULT, SUCCESS, WARNING, DANGER, INFO). Requires `optionType`.
* **STRING:** Text.


## Custom Actions

The **Custom Actions** tab defines URLs for action buttons on the card.  Actions can be:

* **IFRAME Actions:** Open a modal with an iframe.  No request signature is included.  Use `window.postMessage` to signal completion or cancellation.
* **ACTION_HOOK Actions:** Send a server-side request. Includes an `X-HubSpot-Signature`.  HTTP methods: GET, POST, PUT, DELETE, PATCH.
* **CONFIRMATION_ACTION_HOOK Actions:** Similar to ACTION_HOOK, but requires user confirmation. Includes an `X-HubSpot-Signature`.  HTTP methods: GET, POST, PUT, DELETE, PATCH.


This markdown provides a structured overview based on the provided text.  The complete documentation would include API endpoint details,  more detailed examples, and error handling information.
