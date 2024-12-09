# HubSpot CRM API: CRM Cards

This document details how to create and manage custom CRM cards within HubSpot's public apps using their API.  These cards allow you to display information from external systems directly on HubSpot contact, company, deal, and ticket records.  Note that these CRM cards differ from custom cards created as UI extensions using projects.  UI extensions offer greater flexibility and interactivity.


## Overview

CRM cards enhance HubSpot records by displaying data from your integrated app.  Your app defines the card's appearance and functionality, including actions users can perform.  HubSpot fetches data from your app when a user views a relevant record.


##  Key Differences from UI Extensions

* **Target Audience:** CRM cards are designed for public apps, while UI extensions are more suitable for private apps or situations needing greater customizability.
* **Functionality:** UI extensions offer more advanced interactivity and design options.  CRM cards provide a simpler, more streamlined integration.
* **Toolset:** UI extensions utilize a modern toolset (likely React-based), while CRM cards rely on a different, less modern approach.


## Getting Started: Scope Requirements

To create CRM cards, your app needs the necessary OAuth scopes.  For example, displaying a card on contact records requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing these scopes necessitates deleting all associated cards.  Refer to HubSpot's OAuth documentation for detailed information on scopes and authorization URLs.


## Creating a CRM Card

CRM cards can be created via the HubSpot API or through the HubSpot developer account UI.

**Using the HubSpot UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select the app where you want to add the card.
3. Choose **CRM cards** from the left sidebar.
4. Click **Create CRM card**.
5. Configure the card using the provided tabs.


## Data Request

When a user views a record, HubSpot sends a data fetch request to your app's specified URL. This request includes default parameters and custom parameters based on the card's settings.

**Data Fetch URL:** This URL (the `targetUrl` in the API) is where HubSpot will fetch data.

**Target Record Types & Properties Sent from HubSpot:**  Specify the CRM record types (contacts, companies, deals, tickets) where the card will appear and select the HubSpot properties to send as query parameters.  These are defined within the `objectTypes` array in the API.


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
}
```

**Example Request:**

A `GET` request might look like this:

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Parameters:**

| Parameter             | Type    | Description                                                                        |
|-----------------------|---------|------------------------------------------------------------------------------------|
| `userId`              | Default | HubSpot user ID.                                                                  |
| `userEmail`           | Default | Email of the user viewing the record.                                             |
| `associatedObjectId`   | Default | ID of the CRM record.                                                              |
| `associatedObjectType` | Default | Type of CRM record (e.g., CONTACT, COMPANY).                                      |
| `portalId`            | Default | HubSpot account ID.                                                               |
| `firstname`, `email`, `lastname` | Custom  | Contact properties (example; determined by `propertiesToSend`).                   |


**Important:** Requests timeout after 5 seconds; connection must be established within 3 seconds.


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
      // ... other properties
      "actions": [
        // ... action objects
      ]
    }
  ],
  "settingsAction": { /* ... */ },
  "primaryAction": { /* ... */ },
  "secondaryActions": [ /* ... */ ]
}
```

**Response Fields:**

* `results`: Array of objects (up to 5), each representing a data item.
* `objectId`: Unique ID for the object.
* `title`: Title of the object.
* `link`: URL for more details (optional; use `null` if no links).
* `created`, `priority`: Example custom properties (defined in card settings).
* `actions`: Array of action objects.
* `properties`: Array of additional custom properties not defined in the card settings.
* `settingsAction`, `primaryAction`, `secondaryActions`: Action objects for specific functionalities.


## Request Signatures

HubSpot includes an `X-HubSpot-Signature` header to verify requests.  To validate:

1. Concatenate your app secret, HTTP method, URL, and request body.
2. Create a SHA-256 hash of this string.
3. Compare the hash to the signature in the header.


## Card Properties

Define custom properties to display on the card.  Add properties via the UI, specifying name, label, and data type (CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, STRING).  These are defined in the `results` array of your response.


## Property Types

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Displays as a mailto link.
* **LINK:** Displays a hyperlink; optional `linkLabel`.
* **NUMERIC:** Displays numbers.
* **STATUS:** Displays colored indicators (DEFAULT, SUCCESS, WARNING, DANGER, INFO). Requires `optionType`.
* **STRING:** Displays text.


## Custom Actions

Define action URLs for buttons on the card.  Actions can be:

* **IFRAME:** Opens a modal with an iframe. Uses `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH); includes `X-HubSpot-Signature`.
* **CONFIRMATION_ACTION_HOOK:**  Like ACTION_HOOK, but prompts for confirmation. Includes `X-HubSpot-Signature`.


## Conclusion

By following these guidelines, you can effectively integrate custom CRM cards into your HubSpot public app, enhancing the user experience and providing valuable data integration within the HubSpot platform. Remember to consult HubSpot's official documentation for the most up-to-date information and best practices.
