# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displaying information from external systems directly within HubSpot contact, company, deal, and ticket records.

## Overview

HubSpot CRM cards enable public apps to enrich CRM records with data from external sources.  Each app can have up to 25 cards.  These cards differ from UI extensions created with projects; CRM cards are for public apps, while UI extensions provide more flexibility and interactivity.

**Use Case Example:**  An app integrating bug tracking software can display bug information directly on HubSpot contact records.

**Workflow:**  The app defines the card's configuration. When a user views a CRM record, HubSpot makes an outbound request to the app's specified URL, receives the data, and displays it on the record.  The app can also define custom actions users can perform.

## Scope Requirements

To create CRM cards, your app requires OAuth scopes to read and write to the relevant CRM objects. For example, a contact card needs `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing CRM object scopes requires deleting all existing cards for those object types.  See the HubSpot OAuth documentation for more details.

## Creating a CRM Card

CRM cards are created either via the API (see Endpoints below) or through the HubSpot developer account UI:

1. Navigate to **Apps** in the HubSpot developer account.
2. Select your app.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card**.


## API Endpoints

*(Specific endpoint URLs are not provided in the source text.  This section would need to be populated with actual endpoint details from the HubSpot API documentation.)*

The API allows programmatic creation and management of CRM cards.  This would involve POST requests to create cards and PUT requests to update them.  The API likely accepts JSON payloads similar to those shown in the examples below.

## Data Request

When a user views a relevant CRM record, HubSpot sends a GET request to the app's configured `targetUrl`. This request includes:

* **Default Parameters:** `userId`, `userEmail`, `associatedObjectId`, `associatedObjectType`, `portalId`.
* **Custom Parameters:**  HubSpot properties specified in the card's settings (via `propertiesToSend` array in the API).

**Example Request:**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Parameters:**

| Parameter             | Type     | Description                                                                        |
|----------------------|----------|------------------------------------------------------------------------------------|
| `userId`              | Default  | HubSpot user ID who accessed the record.                                           |
| `userEmail`           | Default  | Email address of the user.                                                        |
| `associatedObjectId` | Default  | ID of the CRM record.                                                             |
| `associatedObjectType`| Default  | Type of CRM record (e.g., `CONTACT`, `COMPANY`, `DEAL`, `TICKET`).                 |
| `portalId`            | Default  | ID of the HubSpot account.                                                        |
| *Custom Properties*   | Custom   | HubSpot properties specified in the card's configuration (`propertiesToSend`). |


**Important:** Requests timeout after 5 seconds; a connection must be established within 3 seconds.

## Example Data Fetch Configuration (JSON)

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

## Example Response (JSON)

The app responds with a JSON payload containing card data.  The response should include `results` (an array of objects), and optionally `settingsAction`, `primaryAction`, and `secondaryActions`.

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
        // ... action definitions ...
      ]
    }
  ],
  "settingsAction": { /* ... */ },
  "primaryAction": { /* ... */ }
}
```


## Request Signatures

HubSpot verifies requests using the `X-HubSpot-Signature` header. This header contains a base64 encoded SHA-256 hash of: `<app secret>+<HTTP method>+<URL>+<request body>`.  The app must verify this signature to prevent spoofing.

## Card Properties

The `Card Properties` tab defines custom properties to be displayed on the card.  These properties must be included in the API response.  Supported data types are: `CURRENCY`, `DATE`, `DATETIME`, `EMAIL`, `LINK`, `NUMERIC`, `STATUS`, `STRING`.


## Custom Actions

The `Custom actions` tab defines actions users can take on the card.  Action types include:

* **IFRAME:** Opens a modal with an iframe.  No signature is sent for iframe actions.  The iframe should use `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH).  Includes a signature.
* **CONFIRMATION_ACTION_HOOK:** Similar to `ACTION_HOOK`, but includes a confirmation dialog.  Includes a signature.

## Example Custom Property Types

The following examples show how to format various property types in the API response:

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
  ```json
  { "dataType": "CURRENCY", "value": "94.34", "currencyCode": "GBP" }
  ```
* **DATE:** `yyyy-mm-dd` format.
  ```json
  { "dataType": "DATE", "value": "2023-10-13" }
  ```
* **DATETIME:** Milliseconds since epoch.
  ```json
  { "dataType": "DATETIME", "value": "1697233678777" }
  ```
* **EMAIL:** Email address (automatically displayed as a link).
  ```json
  { "dataType": "EMAIL", "value": "hobbes.baron@gmail.com" }
  ```
* **LINK:** URL; optionally includes `linkLabel`.
  ```json
  { "dataType": "LINK", "value": "https://www.hubspot.com", "linkLabel": "Test link" }
  ```
* **NUMERIC:** Number.
  ```json
  { "dataType": "NUMERIC", "value": "123.45" }
  ```
* **STATUS:** Status value and `optionType` (`DEFAULT`, `SUCCESS`, `WARNING`, `DANGER`, `INFO`).
  ```json
  { "dataType": "STATUS", "value": "Errors occurring", "optionType": "DANGER" }
  ```
* **STRING:** Text.
  ```json
  { "dataType": "STRING", "value": "Tim Robinson" }
  ```

This comprehensive documentation provides a solid foundation for understanding and utilizing the HubSpot CRM Cards API.  Remember to consult the official HubSpot API documentation for the most up-to-date information on endpoints and specific details.
