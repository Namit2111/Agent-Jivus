# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displaying information from external systems within HubSpot contact, company, deal, and ticket records.

## Overview

HubSpot CRM cards enable public apps to extend the functionality of HubSpot CRM records by displaying data from external sources.  Each app can have up to 25 CRM cards.  These cards differ from UI extensions built with developer projects; CRM cards are designed for public apps, while UI extensions offer greater flexibility and customizability.  If you're not building a public app, consider using React-based UI extensions.

**Use Case Example:**  An app integrating bug tracking software could display tracked bugs directly on HubSpot contact records for support reps.

**Workflow:** The app defines cards within its feature settings. Upon a user viewing a CRM record, HubSpot makes an outbound request to the app, fetches data, and displays it in a card.  Custom actions can also be defined, such as opening a modal with the app's UI within HubSpot.


## Scope Requirements

Creating custom CRM cards requires requesting appropriate OAuth scopes.  For example, a card appearing on contact records needs `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing CRM object scopes requires deleting all existing cards for those object types. See HubSpot's OAuth documentation for details.

## Creating a CRM Card

Cards can be created via the API or HubSpot's UI.

**Using the HubSpot UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select the relevant app.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card**.


## Data Request

HubSpot sends a data fetch request to the app's specified URL when a user views a relevant CRM record. This request includes default query parameters and additional parameters containing CRM property data as specified in the card's settings.

**Data Fetch URL Configuration (Example):**

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

**Example Request:**

The above configuration might result in the following GET request:

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Parameters:**

| Parameter             | Type     | Description                                                                     |
|----------------------|----------|---------------------------------------------------------------------------------|
| `userId`              | Default  | HubSpot user ID.                                                                |
| `userEmail`           | Default  | Email address of the logged-in user.                                             |
| `associatedObjectId`  | Default  | ID of the CRM record.                                                            |
| `associatedObjectType` | Default  | Type of CRM record (e.g., CONTACT, COMPANY, DEAL).                               |
| `portalId`            | Default  | HubSpot account ID.                                                              |
| `firstname`, `email`, `lastname` | Custom   | CRM properties specified in `propertiesToSend`.                               |


**Request Timeout:** Requests timeout after 5 seconds; connection must be established within 3 seconds.

## Example Response

The app should respond with data in the following format:

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


## Request Signatures

HubSpot includes an `X-HubSpot-Signature` header for request verification.  This header contains a SHA-256 hash of the app secret concatenated with the HTTP method, URL, and request body (if any).  Verify the signature on the server-side to prevent unauthorized requests.

## Card Properties

Define custom properties displayed on the card.  The app's response should include values for these properties.  Supported data types include CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, and STRING.

**Example Custom Property (Currency):**

```json
{
  "label": "Resolution impact",
  "dataType": "CURRENCY",
  "value": "94.34",
  "currencyCode": "GBP"
}
```

**Property Type Details:**

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Displays as a mailto link.
* **LINK:** Displays a hyperlink; `linkLabel` is optional.
* **NUMERIC:** Displays a number.
* **STATUS:** Displays a colored indicator (DEFAULT, SUCCESS, WARNING, DANGER, INFO). Requires `optionType`.
* **STRING:** Displays text.


## Custom Actions

Define actions users can take on the card.  Actions can be:

* **IFRAME:** Opens a modal with an iframe.  No request signature is sent. The iframe should use `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).

* **ACTION_HOOK:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH). Includes `X-HubSpot-Signature`.

* **CONFIRMATION_ACTION_HOOK:**  Similar to ACTION_HOOK, but shows a confirmation dialog before the request.  Includes `X-HubSpot-Signature`.

**Example IFRAME Action:**

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

**Example ACTION_HOOK Action:**

```json
{
  "type": "ACTION_HOOK",
  "httpMethod": "POST",
  "uri": "https://example.com/action-hook",
  "label": "Example action",
  "associatedObjectProperties": ["some_crm_property"]
}
```

This comprehensive documentation provides a detailed understanding of the HubSpot CRM Cards API, enabling developers to build robust integrations.  Remember to consult the HubSpot Developer documentation for the most up-to-date information and best practices.
