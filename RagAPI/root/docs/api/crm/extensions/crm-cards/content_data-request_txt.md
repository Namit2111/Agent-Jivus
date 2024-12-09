# HubSpot CRM API: CRM Cards

This document details how to create and use custom CRM cards within HubSpot public apps.  These cards allow you to display information from external systems directly on HubSpot contact, company, deal, and ticket records.  Note that these CRM cards are distinct from custom cards created as UI extensions using projects.  UI extensions offer greater flexibility and interactivity.

## Overview

CRM cards are defined as part of your app's feature settings. When a user views a relevant CRM record, HubSpot makes an outbound request to your app, retrieves data, and displays it in a card on the record page.  You can also define custom actions users can take based on the displayed information.  Each app can include up to 25 CRM cards.

**Example Use Case:**  An integration for the App Marketplace displays tracked bugs from your bug tracking software directly on HubSpot contact records for support reps.

## Scope Requirements

To create CRM cards, your app requires OAuth scopes to modify the CRM records. For example, a card on contact records needs `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing CRM object scopes requires deleting all existing cards for those object types.  See the OAuth documentation for more details.

## Creating a CRM Card

You can create cards via the API or through the HubSpot developer account UI.  API details are in the **Endpoints** tab (not included in this markdown).  UI instructions:

1. In your HubSpot developer account, navigate to **Apps**.
2. Select the app where you want to add a card.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card**.
5. Configure options in each tab (detailed below).


If not building a public app, consider React-based UI extensions. See the [CRM development tools overview](link-to-overview-needed) and [UI extensions quickstart guide](link-to-quickstart-needed).


## Data Request

HubSpot sends a data fetch request to your app's specified URL when a user views a relevant CRM record.  This request includes default query parameters and extra parameters containing property data from the card's settings.

**Data Fetch URL:**  The URL where data is fetched (the `targetUrl` field in the API).

**Target Record Types:** Select which CRM records the card appears on.  Select HubSpot properties to include as query parameters (`propertiesToSend` array in the API).

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

| Parameter             | Type     | Description                                                                    |
|----------------------|----------|--------------------------------------------------------------------------------|
| `userId`              | Default  | HubSpot user ID.                                                              |
| `userEmail`           | Default  | Email address of the user.                                                    |
| `associatedObjectId`  | Default  | ID of the CRM record.                                                          |
| `associatedObjectType` | Default  | Type of CRM record (e.g., `CONTACT`, `COMPANY`).                             |
| `portalId`            | Default  | HubSpot account ID.                                                            |
| `firstname`, `email`, `lastname` | Custom   | Contact properties (as specified in `propertiesToSend`).                      |


**Note:** Requests timeout after 5 seconds (connection within 3 seconds).


## Example Response

```json
{
  "results": [
    {
      "objectId": 245,
      "title": "API-22: APIs working too fast",
      "link": "http://example.com/1",
      "created": "2016-09-15",
      "priority": "HIGH",
      // ... more properties ...
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

* `results`: Array of up to 5 card properties.
* `objectId`: Unique ID for the object.
* `title`: Title of the object.
* `link`: URL for more details (optional, use `null` if none).
* `created`, `priority`: Custom properties (defined in card settings).
* `actions`: Array of available actions.
* `properties`: Array of additional custom properties not defined in card settings.
* `settingsAction`, `primaryAction`, `secondaryActions`: Actions for settings, primary action, and secondary actions respectively.


## Request Signatures

HubSpot includes the `X-HubSpot-Signature` header for request verification.  This header contains a base64 encoded SHA-256 hash of: `<app secret> + <HTTP method> + <URL> + <request body>`.  Verify this signature on your end to ensure request authenticity.  See the [validating requests from HubSpot](link-to-validation-needed) documentation for details.


## Card Properties

The **Card Properties** tab defines custom properties displayed on the CRM card.  Add properties with a unique name, display label, and data type (Currency, Date, Datetime, Email, Link, Numeric, Status, String).

**Example Custom Property (JSON):**

```json
{
  "label": "Resolution impact",
  "dataType": "CURRENCY",
  "value": "94.34",
  "currencyCode": "GBP"
}
```

### Property Types

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Displays as a mailto link.
* **LINK:** Displays a hyperlink (can include `linkLabel`).
* **NUMERIC:** Displays a number.
* **STATUS:** Displays a colored indicator (`optionType`: DEFAULT, SUCCESS, WARNING, DANGER, INFO).
* **STRING:** Displays text.


## Custom Actions

The **Custom actions** tab defines URLs for action buttons.  Action hooks and confirmation hooks include `X-HubSpot-Signature` for verification; iframes do not.

### Action Types

* **IFRAME:** Opens a modal with an iframe.  Use `window.postMessage` to close the modal (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH).  `associatedObjectProperties` are appended as query parameters (GET, DELETE) or sent in the request body (POST, PUT, PATCH).
* **CONFIRMATION_ACTION_HOOK:** Same as `ACTION_HOOK`, but with a confirmation dialog.


This detailed markdown provides a comprehensive guide to HubSpot CRM cards, covering creation, data requests, responses, signature verification, property types, and action types. Remember to replace placeholder links with the actual links to relevant HubSpot documentation.
