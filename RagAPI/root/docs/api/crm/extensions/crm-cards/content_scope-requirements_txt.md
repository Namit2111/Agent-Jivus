# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displayed on HubSpot contact, company, deal, and ticket records within a public app.  This differs from UI extensions built with developer projects; CRM cards are specifically for public apps.

## Overview

CRM cards enhance HubSpot records by displaying information from external systems.  Each app can have up to 25 cards.  When a user views a relevant record, HubSpot makes an outbound request to the app's specified URL, receives data, and displays it on the record page.  The app can also define custom actions users can perform.

**Example Use Case:** An app integrating bug tracking software displays tracked bugs directly on HubSpot contact records for support reps.

## Scope Requirements

To create CRM cards, your app requires OAuth scopes to read and write to the relevant CRM objects.  For example, a card on contact records needs `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes. Removing object scopes requires deleting all associated cards.  See the HubSpot OAuth documentation for details on scopes and authorization URLs.


## Creating a CRM Card

Cards can be created via the API or HubSpot's UI:

**Via HubSpot's UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select your app.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card**.

**Via API (See Endpoints section below)**


## Data Request

HubSpot sends a data fetch request to the app's target URL when a user views a relevant CRM record. The request includes default and custom query parameters based on the card's settings.

**Data Fetch URL:**  Specifies the URL where HubSpot fetches data. (In API: `targetUrl`)

**Target Record Types:** Specifies which CRM record types display the card. (In API: `objectTypes.name`)

**Properties Sent from HubSpot:** Selects HubSpot properties included as query parameters in the request URL. (In API: `objectTypes.propertiesToSend`)

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

**Example Request (GET):**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Parameters:**

| Parameter             | Type     | Description                                                                        |
|----------------------|----------|------------------------------------------------------------------------------------|
| `userId`              | Default  | HubSpot user ID who loaded the CRM record.                                         |
| `userEmail`           | Default  | Email address of the user who loaded the CRM record.                               |
| `associatedObjectId`  | Default  | ID of the loaded CRM record.                                                       |
| `associatedObjectType`| Default  | Type of the loaded CRM record (e.g., CONTACT, COMPANY, DEAL).                     |
| `portalId`            | Default  | ID of the HubSpot account where the record loaded.                                 |
| `firstname`, `email`, `lastname` | Custom  | Contact properties specified in the settings (propertiesToSend array in the API). |

**Timeout:** Requests timeout after 5 seconds; connection must be established within 3 seconds.


## Example Response

The app responds with a JSON payload.  The `results` array contains up to five card properties.

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
      // ... other properties
      "actions": [ /* Array of actions */ ]
    },
    // ... more results
  ],
  "settingsAction": { /* Iframe action for settings */ },
  "primaryAction": { /* Primary action */ },
  "secondaryActions": [ /* Array of secondary actions */ ]
}
```

**Response Properties:**

* **`results` (array):** Array of objects (up to 5).
    * **`objectId` (number, required):** Unique ID for the object.
    * **`title` (string, required):** Title of the object.
    * **`link` (string, optional):** URL for more details (use `null` if no objects have a link).
    * **`created` (string, required):** Custom date property (defined in card settings).
    * **`priority` (string, required):** Custom string property (defined in card settings).
    * **`actions` (array):** Array of actions.
    * **`properties` (array):**  Array of custom properties not defined in card settings.


## Request Signatures

HubSpot includes the `X-HubSpot-Signature` header to verify request authenticity.  This header contains a base64 encoded SHA-256 hash of: `<app secret> + <HTTP method> + <URL> + <request body>`.  Verify the signature on your server to prevent spoofing.  See HubSpot's documentation on validating requests for details.


## Card Properties

The "Card Properties" tab defines custom properties displayed on the card.  The app's response must include values for these properties.  Supported data types include: `CURRENCY`, `DATE`, `DATETIME`, `EMAIL`, `LINK`, `NUMERIC`, `STATUS`, `STRING`.  Each type might require additional fields (e.g., `currencyCode` for `CURRENCY`).

**Example Custom Property (CURRENCY):**

```json
{
  "label": "Resolution impact",
  "dataType": "CURRENCY",
  "value": "94.34",
  "currencyCode": "GBP"
}
```

* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Email address (displayed as a mailto link).
* **LINK:** URL (can include `linkLabel`).
* **NUMERIC:** Number.
* **STATUS:**  Includes `optionType`: `DEFAULT`, `SUCCESS`, `WARNING`, `DANGER`, `INFO`.
* **STRING:** Text.



## Custom Actions

The "Custom actions" tab defines URLs for action buttons.  Actions can be:

* **IFRAME:** Opens a modal with an iframe.  No request signature is sent.  Use `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).

* **ACTION_HOOK:** Sends a server-side request.  Includes `X-HubSpot-Signature` header.  Supports `GET`, `POST`, `PUT`, `DELETE`, `PATCH` methods.

* **CONFIRMATION_ACTION_HOOK:** Similar to `ACTION_HOOK`, but shows a confirmation dialog. Includes `X-HubSpot-Signature` header.


**Example Action (IFRAME):**

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

**Example Action (ACTION_HOOK):**

```json
{
  "type": "ACTION_HOOK",
  "httpMethod": "POST",
  "uri": "https://example.com/action-hook",
  "label": "Example action",
  "associatedObjectProperties": ["some_crm_property"]
}
```


**Example `window.postMessage`:**

```javascript
window.parent.postMessage(JSON.stringify({"action": "DONE"}), "*");
```

## API Endpoints

*(Specific API endpoint details were not provided in the original text.  This section would need to be populated with actual API endpoint specifications for creating, updating, and deleting CRM cards.)*  This would likely include details such as HTTP methods (POST, PUT, DELETE), request body parameters, and response formats.


This comprehensive documentation provides a detailed understanding of the HubSpot CRM Cards API, enabling developers to build robust integrations. Remember to consult the official HubSpot developer documentation for the most up-to-date information and API endpoint specifications.
