# HubSpot CRM API: CRM Cards

This document details how to create and manage custom CRM cards within HubSpot using its API.  These cards allow you to display information from external systems directly on HubSpot contact, company, deal, and ticket records within public apps.

## Key Differences from UI Extensions

The CRM cards described here are distinct from custom cards created as UI extensions using projects.  CRM cards are designed for public apps and have limitations in flexibility and customizability compared to the more modern and powerful UI extensions.  If you're not building a public app, consider using React-based UI extensions.

## Use Case Example

Imagine integrating bug tracking software with the HubSpot App Marketplace.  You could create a custom CRM card that displays tracked bugs directly on contact records for easier access by support representatives.

## Card Workflow

Cards are defined within your app's feature settings.  Upon installation and when a user views a relevant CRM record, HubSpot sends an outbound request to your app. Your app retrieves the data and returns it to HubSpot for display.  Custom actions can also be defined to enable user interaction.


## Scope Requirements

To create CRM cards, your app requires the necessary OAuth scopes to access and modify the CRM objects. For example, to display a card on contact records, your app needs `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing these scopes requires deleting all existing cards for those object types.  Refer to the HubSpot OAuth documentation for details on scopes and setting up the authorization URL.

## Creating a CRM Card

CRM cards can be created via the API or through the HubSpot developer account UI.

**Using the HubSpot UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select the app where you want to add a card.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card**.
5. Configure the card using the provided tabs.

## Data Request

When a user views a CRM record, HubSpot makes a data fetch request to the URL specified in your app's configuration. This request includes default query parameters and additional parameters based on selected HubSpot properties.

**Configuration (Example):**

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

| Parameter           | Type    | Description                                                                   |
|--------------------|---------|-------------------------------------------------------------------------------|
| `userId`            | Default | HubSpot user ID.                                                              |
| `userEmail`         | Default | Email address of the user.                                                    |
| `associatedObjectId` | Default | ID of the CRM record.                                                          |
| `associatedObjectType` | Default | Type of CRM record (e.g., `CONTACT`, `COMPANY`).                               |
| `portalId`          | Default | HubSpot account ID.                                                            |
| `firstname`, `email`, `lastname` | Custom  | HubSpot properties specified in the configuration (`propertiesToSend`).          |


**Timeout:** Requests timeout after 5 seconds; connection must be established within 3 seconds.

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

**Response Structure:**

* `results`: Array of objects (up to 5), each representing a card item.
* `objectId`: Unique ID for the object.
* `title`: Title of the object.
* `link`: URL for more details (optional, use `null` if none).
* `created`, `priority`: Custom properties defined in card settings.
* `actions`: Array of custom actions.
* `properties`: Array of additional custom properties not defined in card settings.
* `settingsAction`: Iframe action for app settings.
* `primaryAction`: Primary action for the record type.
* `secondaryActions`:  Additional actions.


## Request Signatures

HubSpot includes the `X-HubSpot-Signature` header to authenticate requests.  To verify:

1. Concatenate your app secret, HTTP method, URL, and request body.
2. Generate a SHA-256 hash of the concatenated string.
3. Compare the hash with the signature in the header.


## Card Properties

Define custom properties to display on the card.  These are defined in the "Card Properties" tab and then populated in the response.  Supported data types include: `CURRENCY`, `DATE`, `DATETIME`, `EMAIL`, `LINK`, `NUMERIC`, `STATUS`, and `STRING`.

### Property Type Details

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:**  `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:**  Displayed as a mailto link.
* **LINK:** Displays a hyperlink; `linkLabel` is optional.
* **NUMERIC:** Displays numbers.
* **STATUS:** Displays colored indicators (`DEFAULT`, `SUCCESS`, `WARNING`, `DANGER`, `INFO`).  Requires `optionType`.
* **STRING:** Displays text.


## Custom Actions

Define custom actions with associated URLs.  Actions are triggered when users click buttons on the card.  Action types include:

### Action Types:

* **IFRAME:** Opens a modal with an iframe.  Uses `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).  No request signature is included.

* **ACTION_HOOK:** Sends a server-side request.  Uses `X-HubSpot-Signature` for verification.  `httpMethod` can be `GET`, `POST`, `PUT`, `DELETE`, or `PATCH`.

* **CONFIRMATION_ACTION_HOOK:** Similar to `ACTION_HOOK`, but shows a confirmation dialog before the request.  Uses `X-HubSpot-Signature` for verification.  `httpMethod` can be `GET`, `POST`, `PUT`, `DELETE`, or `PATCH`.


This documentation provides a comprehensive guide to creating and managing CRM cards in the HubSpot API.  Remember to consult the official HubSpot developer documentation for the most up-to-date information and best practices.
