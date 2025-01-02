# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displaying information from external systems within HubSpot contact, company, deal, and ticket records.

## Overview

HubSpot CRM cards enable public apps to extend HubSpot's functionality by displaying data from external sources directly on CRM records.  Each app can have up to 25 cards.  These cards differ from UI extensions created using developer projects; CRM cards are designed for public apps, while UI extensions offer greater flexibility and are better suited for private apps.

**Use Case Example:** An app integrating bug tracking software can display tracked bugs on contact records for support representatives.

**Workflow:**  The app defines cards in its feature settings. When a user views a relevant CRM record, HubSpot makes an outbound request to the app's specified URL, receives data, and displays it as a card.  The app can also define custom actions for user interaction.


## API Endpoints

The API allows for creation and management of CRM cards.  Details on specific endpoints are not provided in the source text, but the documentation implies the existence of endpoints for creating and managing cards. Refer to the HubSpot developer portal for detailed endpoint specifications.


## Creating a CRM Card

CRM cards can be created either via the API or through the HubSpot developer account UI.

**UI Creation Steps:**

1. Navigate to *Apps* in the HubSpot developer account.
2. Select the app where you want to add a card.
3. Select *CRM cards* in the left sidebar.
4. Click *Create CRM card*.
5. Configure the card using the provided tabs.

## Data Request

When a user views a CRM record, HubSpot sends a GET request to the app's specified `targetUrl`. This request includes default and custom query parameters.

**Request Parameters:**

| Parameter             | Type    | Description                                                                     |
|----------------------|---------|---------------------------------------------------------------------------------|
| `userId`              | Default | HubSpot user ID who loaded the CRM record.                                      |
| `userEmail`           | Default | Email address of the user who loaded the CRM record.                            |
| `associatedObjectId` | Default | ID of the loaded CRM record.                                                   |
| `associatedObjectType`| Default | Type of the loaded CRM record (e.g., `CONTACT`, `COMPANY`, `DEAL`).             |
| `portalId`            | Default | ID of the HubSpot account where the record was loaded.                         |
| Custom Properties     | Custom  | HubSpot properties specified in `propertiesToSend` (see example below).          |


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

**Example GET Request:**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Timeout:** Requests timeout after 5 seconds; a connection must be established within 3 seconds.


## Example Response (JSON)

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
    // ... other results ...
  ],
  "settingsAction": { /* ... */ },
  "primaryAction": { /* ... */ }
}
```

**Response Fields:**

* `results`: Array of up to five card properties.
* `objectId`: Unique ID for the object.
* `title`: Title of the object.
* `link`: URL for more details (optional; use `null` if no link).
* `created`, `priority`: Custom properties defined in card settings.
* `actions`: Array of available actions.
* `properties`: Array of custom properties not defined in card settings.
* `settingsAction`, `primaryAction`, `secondaryActions`:  Actions objects (see below).


## Request Signatures

HubSpot includes an `X-HubSpot-Signature` header to verify request authenticity.  This header contains a base64 encoded SHA-256 hash of: `<app secret> + <HTTP method> + <URL> + <request body>`.  The app must verify this signature.  See HubSpot's documentation on request validation for details.


## Card Properties

Custom properties displayed on the card are defined in the *Card Properties* tab.  The response must include values for these properties. Property types include: `CURRENCY`, `DATE`, `DATETIME`, `EMAIL`, `LINK`, `NUMERIC`, `STATUS`, and `STRING`.  See below for details on each type.


## Property Types

* **CURRENCY:** Requires `currencyCode` (ISO 4217).  Example: `{"currencyCode": "GBP", "value": "94.34"}`
* **DATE:** `yyyy-mm-dd` format. Example: `"2023-10-13"`
* **DATETIME:** Milliseconds since epoch. Example: `1697233678777`
* **EMAIL:** Email address (displayed as a mailto link). Example: `"hobbes.baron@gmail.com"`
* **LINK:** URL; optionally include `linkLabel`. Example: `{"value": "https://www.hubspot.com", "linkLabel": "Test link"}`
* **NUMERIC:** Number. Example: `123.45`
* **STATUS:** Requires `optionType`: `DEFAULT`, `SUCCESS`, `WARNING`, `DANGER`, `INFO`. Example: `{"value": "Errors occurring", "optionType": "DANGER"}`
* **STRING:** Text. Example: `"Tim Robinson"`


## Custom Actions

Custom actions define URLs triggered when users click action buttons.  Action types include: `IFRAME`, `ACTION_HOOK`, and `CONFIRMATION_ACTION_HOOK`.


## Action Types

* **IFRAME:** Opens a modal with an iframe.  The iframe must use `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH).  Includes `X-HubSpot-Signature`.
* **CONFIRMATION_ACTION_HOOK:** Same as `ACTION_HOOK`, but shows a confirmation dialog. Includes `X-HubSpot-Signature`.


## Example Iframe Action (JSON)

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

## Example Action Hook Action (JSON)

```json
{
  "type": "ACTION_HOOK",
  "httpMethod": "POST",
  "uri": "https://example.com/action-hook",
  "label": "Example action",
  "associatedObjectProperties": ["some_crm_property"]
}
```

## Example Confirmation Action Hook Action (JSON)

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


This documentation provides a comprehensive overview of the HubSpot CRM Cards API.  Refer to the official HubSpot developer documentation for the most up-to-date information and details on API endpoints and error handling.
