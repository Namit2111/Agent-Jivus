# HubSpot CRM API: CRM Cards

This document details the HubSpot CRM API's functionality for creating custom CRM cards within public apps.  These cards display information from external systems directly on HubSpot contact, company, deal, and ticket records.  Note that these CRM cards differ from custom cards created as UI extensions using projects.  UI extensions offer more flexibility and are recommended for non-public app integrations.

## Overview

CRM cards allow developers to enrich HubSpot CRM records with data from their applications.  Each public app can include up to 25 cards.  When a user views a relevant CRM record, HubSpot sends a request to the app, receives the data, and displays it in a card. Apps can also define custom actions users can take within the card.

**Example Use Case:** An app integrating bug tracking software can display tracked bugs directly on HubSpot contact records for easy access by support reps.

## Scope Requirements

To create CRM cards, your app needs OAuth scopes to read and write to the target CRM object types (e.g., `crm.objects.contacts.read` and `crm.objects.contacts.write` for contact records). Removing CRM object scopes requires deleting all existing cards for those object types.  Refer to the HubSpot OAuth documentation for more details on scopes and setting up authorization URLs.

## Creating a CRM Card

CRM cards can be created via the API or through the HubSpot developer account UI.

**Using the HubSpot UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select the app where you want to add a card.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card**.

## Data Request

When a user views a CRM record, HubSpot sends a data fetch request to the app's specified `targetUrl`. This request includes default query parameters and additional parameters containing property data as defined in the card's settings.

**Example Configuration (JSON):**

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

| Parameter             | Type     | Description                                                                     |
|----------------------|----------|---------------------------------------------------------------------------------|
| `userId`              | Default  | HubSpot user ID.                                                              |
| `userEmail`           | Default  | Email address of the logged-in user.                                           |
| `associatedObjectId`  | Default  | ID of the CRM record.                                                          |
| `associatedObjectType` | Default  | Type of CRM record (e.g., CONTACT, COMPANY, DEAL).                             |
| `portalId`            | Default  | ID of the HubSpot account.                                                      |
| `firstname`, `email`, `lastname` | Custom   | CRM properties specified in `propertiesToSend` (example).                      |

**Important:** Requests timeout after 5 seconds, with a connection required within 3 seconds.


## Example Response

The app should return a JSON response like this:

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

**Response Structure:**

* **`results`**: Array of objects (up to 5).  Each object represents a data item to display on the card.
* **`objectId`**: Unique ID for each object.
* **`title`**: Title of the object.
* **`link`**: URL for more details (optional, `null` if none).
* **`created`, `priority`**: Example custom properties.
* **`actions`**: Array of available actions.
* **`properties`**: Array of additional custom properties not defined in card settings.
* **`settingsAction`**: Iframe action for app settings.
* **`primaryAction`**: Primary action for the record type.
* **`secondaryActions`**: List of secondary actions.


## Request Signatures

HubSpot includes an `X-HubSpot-Signature` header to verify request authenticity.  To verify:

1. Concatenate the app secret, HTTP method, URL, and request body.
2. Create a SHA-256 hash of the concatenated string.
3. Compare the hash to the signature in the header.


## Card Properties

The **Card Properties** tab defines custom properties displayed on the card.  The app's response should include values for these properties.  Supported data types are: `CURRENCY`, `DATE`, `DATETIME`, `EMAIL`, `LINK`, `NUMERIC`, `STATUS`, and `STRING`.


## Currency Properties

Requires `currencyCode` (ISO 4217).

## Date Properties

Format: `yyyy-mm-dd`.

## Datetime Properties

Milliseconds since epoch.

## Email Properties

Displayed as mailto links.

## Link Properties

Displays hyperlinks.  Can include `linkLabel`.

## Numeric Properties

Displays numbers.

## Status Properties

Displayed as colored indicators (`DEFAULT`, `SUCCESS`, `WARNING`, `DANGER`, `INFO`). Requires `optionType`.

## String Properties

Displays text.


## Custom Actions

The **Custom actions** tab defines URLs for action buttons.  Actions can be:

* **Iframe actions (`IFRAME`)**: Opens a modal with an iframe.  No request signature. Uses `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **Action hook actions (`ACTION_HOOK`)**: Sends a server-side request. Includes `X-HubSpot-Signature`.  `httpMethod` can be `GET`, `POST`, `PUT`, `DELETE`, or `PATCH`.
* **Confirmation actions (`CONFIRMATION_ACTION_HOOK`)**: Similar to action hooks, but with a confirmation dialog. Includes `X-HubSpot-Signature`.  `httpMethod` can be `GET`, `POST`, `PUT`, `DELETE`, or `PATCH`.


This document provides a comprehensive guide to building and utilizing CRM cards within the HubSpot CRM API.  Remember to consult the HubSpot Developer Documentation for the most up-to-date information and additional details.
