# HubSpot CRM API: CRM Cards

This document details the HubSpot CRM API's functionality for creating custom CRM cards within public apps.  These cards allow you to display information from external systems directly on HubSpot contact, company, deal, and ticket records.  Note that these CRM cards differ from custom cards created as UI extensions using projects.  UI extensions offer greater flexibility and interactivity.

## Overview

Within a public app, you can create up to 25 CRM cards.  These cards dynamically fetch and display data from your app when a user views a relevant HubSpot CRM record.  You can also define custom actions users can take based on the displayed information.

**Example Use Case:** An App Marketplace integration for bug tracking software.  The app displays tracked bugs directly on contact records for support representatives.

**Data Flow:**  When a user views a CRM record, HubSpot makes an outbound request to your app's specified URL. Your app processes this request, retrieves data, and returns a response to HubSpot for display.

## Scope Requirements

To create CRM cards, your app needs the necessary OAuth scopes to read and write to the relevant CRM object types. For example, to display a card on contact records, your app requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing these scopes requires deleting all existing cards for those object types.  See the OAuth documentation for more details.

## Creating CRM Cards

CRM cards can be created via the API or through the HubSpot developer account UI.

**Using the HubSpot UI:**

1. Navigate to **Apps** in the main navigation of your HubSpot developer account.
2. Select the app where you want to add a card.
3. Select **CRM cards** in the left sidebar menu.
4. Click **Create CRM Card**.
5. Configure the card settings (detailed below).

For more flexible options, consider using React-based UI extensions.

## Data Request

HubSpot makes a data fetch request to your app's specified URL when a user views a relevant CRM record. This request includes default query parameters and additional parameters containing CRM record properties.

**Configuration:**

* **Data fetch URL (`targetUrl`):** The URL where HubSpot fetches data.
* **Target record types (`objectTypes`):** Specify which CRM records the card appears on.
* **Properties sent from HubSpot (`propertiesToSend`):** Select HubSpot properties to include as query parameters in the request URL.


**Example Data Fetch Configuration:**

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

| Parameter             | Type    | Description                                                                     |
|-----------------------|---------|---------------------------------------------------------------------------------|
| `userId`              | Default | HubSpot user ID.                                                                 |
| `userEmail`           | Default | Email address of the user.                                                       |
| `associatedObjectId`  | Default | ID of the CRM record.                                                            |
| `associatedObjectType` | Default | Type of CRM record (e.g., CONTACT, COMPANY).                                     |
| `portalId`            | Default | HubSpot account ID.                                                              |
| `firstname`, `email`, `lastname` | Custom  | CRM record properties (specified in `propertiesToSend`).                        |

**Timeout:** Requests timeout after 5 seconds (connection within 3 seconds).


## Example Response

Your app's response should include the following structure:

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
  "primaryAction": { ... },
  "secondaryActions": [ ... ]
}
```


## Request Signatures

HubSpot includes an `X-HubSpot-Signature` header to verify request authenticity.  Validate this signature using SHA-256 hashing of a concatenated string: `<app secret> + <HTTP method> + <URL> + <request body>`.

## Card Properties

Define custom properties to display on the CRM card using the **Card Properties** tab.  These properties should be included in your app's response.  Supported data types include: CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, and STRING.

### Property Types

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Displays as a mailto link.
* **LINK:** Displays a hyperlink; use `linkLabel` for custom text.
* **NUMERIC:** Displays numbers.
* **STATUS:** Displays colored indicators (DEFAULT, SUCCESS, WARNING, DANGER, INFO).  Requires `optionType`.
* **STRING:** Displays text.


## Custom Actions

Define custom actions users can perform on the card using the **Custom Actions** tab.  Action types include:

* **IFRAME:** Opens a modal with an iframe.  Uses `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request; only displays success/error messages.  Includes `X-HubSpot-Signature`.  Supports GET, POST, PUT, DELETE, and PATCH HTTP methods.
* **CONFIRMATION_ACTION_HOOK:** Same as ACTION_HOOK, but prompts for confirmation.  Includes `X-HubSpot-Signature`. Supports GET, POST, PUT, DELETE, and PATCH HTTP methods.


This document provides a comprehensive guide to integrating custom CRM cards into your HubSpot public apps using the CRM API.  Remember to consult the official HubSpot documentation for the most up-to-date information and detailed specifications.
