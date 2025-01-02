# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displaying information from external systems within HubSpot contact, company, deal, and ticket records.

## Overview

HubSpot CRM cards enable extensions to integrate with HubSpot CRM by displaying custom information directly on CRM records.  This allows for richer context and streamlined workflows without leaving the HubSpot interface.  Each app can have up to 25 CRM cards.  These cards differ from UI extensions created with projects; CRM cards are for public apps, while UI extensions offer greater flexibility and are better suited for private apps.

**Key Features:**

* Display data from external systems on HubSpot CRM records.
* Define custom actions users can take directly from the card.
* Support for various data types (currency, date, datetime, email, link, numeric, status, string).
* Request signature verification to ensure data integrity.

## API Endpoints (Not explicitly defined in the provided text, but implied)

The documentation mentions creating cards through the API, but does not provide specific endpoint URLs.  Assume endpoints exist for:

* **Creating a CRM Card:**  `/crm/v3/cards` (POST)  This would likely take a JSON payload specifying card properties.
* **Updating a CRM Card:** `/crm/v3/cards/{cardId}` (PUT)
* **Deleting a CRM Card:** `/crm/v3/cards/{cardId}` (DELETE)


## Scope Requirements

To create and display cards on specific CRM objects, your app requires appropriate OAuth scopes:

* `crm.objects.contacts.read` & `crm.objects.contacts.write` (for Contact records)
* Similar scopes for Companies, Deals, and Tickets.

Removing these scopes requires deleting all associated cards.


## Creating a CRM Card

Cards can be created either via the HubSpot UI or the API.  The UI approach is outlined in the original text. The API approach would involve a POST request to the "Creating a CRM Card" endpoint with a JSON payload.

## Data Request

When a user views a CRM record, HubSpot makes an outbound request to the app's specified `targetUrl`.  This request includes:

* **Default Parameters:** `userId`, `userEmail`, `associatedObjectId`, `associatedObjectType`, `portalId`.
* **Custom Parameters:**  HubSpot properties selected during card configuration (`propertiesToSend` in the API).


**Example Request (GET):**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Parameters:**

| Parameter             | Type    | Description                                                                     |
|----------------------|---------|---------------------------------------------------------------------------------|
| `userId`              | Default | HubSpot user ID viewing the record.                                             |
| `userEmail`           | Default | Email address of the viewing user.                                              |
| `associatedObjectId`  | Default | ID of the CRM record.                                                            |
| `associatedObjectType` | Default | Type of CRM record (CONTACT, COMPANY, DEAL, TICKET).                             |
| `portalId`            | Default | ID of the HubSpot account.                                                      |
| Custom Properties     | Custom  |  Properties specified in `propertiesToSend` (e.g., `firstname`, `email`).     |


**Important:** Requests timeout after 5 seconds; connection must be established within 3 seconds.


## Example Response

The app's response should be a JSON object containing:

```json
{
  "results": [ // Array of objects (up to 5)
    {
      "objectId": 245,
      "title": "API-22: APIs working too fast",
      "link": "http://example.com/1",
      "created": "2016-09-15",
      "priority": "HIGH",
      // ... other properties ...
      "actions": [ // Array of actions
        // ...
      ]
    },
    // ... more objects ...
  ],
  "settingsAction": { /* ... */ },
  "primaryAction": { /* ... */ },
  "secondaryActions": [ /* ... */ ]
}
```

**Response Fields:**

* `results`: Array of objects representing data to display on the card.
* `objectId`: Unique ID for each object.
* `title`: Title of the object.
* `link`: URL for more details (optional, use `null` if no links).
* `created`, `priority`, etc.: Custom properties defined in card settings.
* `properties`: Array of additional custom properties not defined in card settings.
* `actions`: Array of custom actions users can perform.
* `settingsAction`, `primaryAction`, `secondaryActions`: Actions related to app settings and primary/secondary actions for a record.


## Request Signatures

HubSpot includes the `X-HubSpot-Signature` header to verify request authenticity.  This header contains a SHA-256 hash of: `<app secret> + <HTTP method> + <URL> + <request body>`.


## Card Properties

Define custom properties to be displayed on the card using the `Card Properties` tab (UI) or within the API payload. Supported data types are: CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, STRING.  Each type has specific formatting requirements (e.g., CURRENCY needs `currencyCode`).


## Custom Actions

Define action URLs for buttons on the card.  Actions can be:

* **IFRAME:** Opens a modal with an iframe.  Uses `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request.  Includes `X-HubSpot-Signature`.
* **CONFIRMATION_ACTION_HOOK:** Similar to `ACTION_HOOK`, but with a confirmation dialog.  Includes `X-HubSpot-Signature`.


##  Property Type Details

This section details the specifics of each data type within the `properties` array in the response.

**CURRENCY:** Requires `currencyCode` (ISO 4217).  Example: `"currencyCode": "GBP"`.

**DATE:**  `yyyy-mm-dd` format.

**DATETIME:** Milliseconds since epoch.

**EMAIL:**  Displayed as a mailto link.

**LINK:**  Displays a hyperlink; use `linkLabel` for custom text.

**NUMERIC:**  Displays a number.

**STATUS:** Displays a colored indicator (DEFAULT, SUCCESS, WARNING, DANGER, INFO). Requires `optionType`.

**STRING:**  Displays text.


This expanded documentation provides a clearer understanding of the HubSpot CRM Cards API, including API calls, request/response examples, and detailed information about data types and actions. Remember to replace placeholder URLs and values with your actual implementation details.
