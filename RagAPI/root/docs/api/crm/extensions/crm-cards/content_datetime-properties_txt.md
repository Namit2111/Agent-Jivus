# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displaying information from external systems within HubSpot contact, company, deal, and ticket records.

## Overview

HubSpot CRM cards provide a way to integrate external data sources into HubSpot's CRM interface.  This integration enhances the CRM by surfacing relevant information directly on the record page without requiring users to navigate to external systems.  Each app can have up to 25 CRM cards.  These cards are distinct from UI extensions built using developer projects; they are intended specifically for public apps.

**Use Case Example:** An app integrating bug tracking software can display tracked bugs directly on contact records, improving support rep efficiency.


## Scope Requirements

To create CRM cards, your app requires OAuth scopes to read and write to the CRM objects where the cards will appear.  For example, a card on contact records needs `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing CRM object scopes requires deleting all existing cards for those object types.  Refer to the HubSpot OAuth documentation for details on scopes and authorization URL setup.


## Creating a CRM Card

CRM cards can be created via the API or HubSpot's developer account UI.  The UI method is outlined below; API details are provided in the following sections.

**Using HubSpot's UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select the app where you want to add a card.
3. In the left sidebar, select **CRM cards**.
4. Click **Create CRM card** in the upper right.
5. Configure the card using the provided tabs (detailed below).


## API Endpoints (Not explicitly provided in source, requires further HubSpot documentation)

The provided text lacks specific API endpoint details (e.g., POST/PUT URLs, request body structures).  Consult HubSpot's official API documentation for the precise endpoints and methods for creating, updating, and deleting CRM cards.


## Data Request

When a user views a CRM record, HubSpot makes a data fetch request to the app's specified `targetUrl`. This request includes default query parameters and custom properties specified in the card settings.

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

| Parameter             | Type    | Description                                                                   |
|----------------------|---------|-------------------------------------------------------------------------------|
| `userId`              | Default | HubSpot user ID who loaded the CRM record.                                     |
| `userEmail`           | Default | Email address of the user who loaded the CRM record.                         |
| `associatedObjectId`   | Default | ID of the loaded CRM record.                                                  |
| `associatedObjectType` | Default | Type of CRM record (e.g., CONTACT, COMPANY, DEAL).                            |
| `portalId`            | Default | ID of the HubSpot account.                                                   |
| `firstname`, `email`, `lastname` | Custom | CRM properties specified in `propertiesToSend` (others can be added).         |


**Request Timeouts:**  Requests timeout after 5 seconds; a connection must be established within 3 seconds.


## Example Response (JSON)

The app should respond with a JSON structure containing card data.

```json
{
  "results": [
    {
      "objectId": 245,
      "title": "API-22: APIs working too fast",
      // ... other properties
      "actions": [
        // ... action objects
      ]
    },
    // ... more results
  ],
  "settingsAction": { ... },
  "primaryAction": { ... }
}
```

**Response Structure:**

* `results`: Array of up to five card objects.
* `objectId`: Unique ID for each object.
* `title`: Title of the object.
* `link`: URL for more details (optional; use `null` if no links).
* `created`, `priority`: Example custom properties (defined in card settings).
* `properties`: Array of additional custom properties.
* `actions`: Array of action objects (see below).
* `settingsAction`: Iframe action for app settings.
* `primaryAction`: Primary action for the record type.
* `secondaryActions`: Additional actions displayed on the card.


## Request Signatures

HubSpot verifies requests using the `X-HubSpot-Signature` header.  This header contains a SHA-256 hash of: `<app secret> + <HTTP method> + <URL> + <request body>`.  Verify the signature on the server-side to prevent unauthorized requests.  See HubSpot's documentation on request validation for details.


## Card Properties

Define custom properties to display on the CRM card.  Specify name, label, and data type (CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, STRING) for each property.  These properties' values should be included in the API response.


## Property Type Details

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:**  Displayed as a mailto link.
* **LINK:**  Displays a hyperlink; can include `linkLabel`.
* **NUMERIC:** Displays a number.
* **STATUS:** Displays a colored indicator (DEFAULT, SUCCESS, WARNING, DANGER, INFO). Requires `optionType`.
* **STRING:** Displays text.


## Custom Actions

Define action URLs for buttons on the card. Actions can be:

* **IFRAME:** Opens a modal with an iframe.  Uses `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH). Includes `X-HubSpot-Signature`.
* **CONFIRMATION_ACTION_HOOK:** Same as `ACTION_HOOK`, but shows a confirmation dialog.  Includes `X-HubSpot-Signature`.


##  Example Custom Actions (JSON)

* **IFRAME:**

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

* **ACTION_HOOK:**

```json
{
  "type": "ACTION_HOOK",
  "httpMethod": "POST",
  "uri": "https://example.com/action-hook",
  "label": "Example action",
  "associatedObjectProperties": ["some_crm_property"]
}
```

* **CONFIRMATION_ACTION_HOOK:**

```json
{
  "type": "CONFIRMATION_ACTION_HOOK",
  "httpMethod": "POST",
  "uri": "https://example.com/action-hook",
  "label": "Example action",
  "associatedObjectProperties": ["some_crm_property"],
  "confirmationMessage": "Are you sure?",
  "confirmButtonText": "Yes",
  "cancelButtonText": "No"
}
```

Remember to consult HubSpot's official API documentation for the most up-to-date and complete information on endpoints, request/response formats, and error handling.
