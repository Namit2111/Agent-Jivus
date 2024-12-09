# HubSpot CRM API: CRM Cards

This document details how to create and manage custom CRM cards within HubSpot public apps using the HubSpot CRM API.  These cards allow you to display information from external systems directly on HubSpot contact, company, deal, and ticket records.  Note that these CRM cards differ from custom cards created as UI extensions using projects.  UI extensions offer more flexibility and are recommended for private apps or situations requiring more advanced customization.


## Overview

CRM cards in HubSpot public apps enable developers to surface data from external systems within HubSpot.  Each app can have up to 25 CRM cards.  When a user views a relevant HubSpot record, HubSpot sends a request to the app's specified URL, retrieves data, and displays it in a card on the record page.  Custom actions can also be defined, such as opening a modal displaying the app's UI.


## Scope Requirements

To create CRM cards, your app requires OAuth scopes to read and write to the relevant CRM object types. For example, displaying a card on contact records requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes. Removing these scopes necessitates deleting all associated cards. See the [HubSpot OAuth documentation](link-to-oauth-docs-here) for more details.


## Creating a CRM Card

CRM cards can be created via the API or the HubSpot developer UI.  API details are covered in the *Endpoints* section (link to that section).  The UI process is as follows:

1. Navigate to **Apps** in your HubSpot developer account.
2. Select the app.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card**.


## Data Request

HubSpot makes a data fetch request to your app when a user views a relevant CRM record. This request is sent to the `targetUrl` specified in your app's configuration and includes default query parameters and custom properties.


### Example Data Fetch Configuration (JSON):

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


### Example Request:

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

| Parameter            | Type    | Description                                                                         |
|-----------------------|---------|-------------------------------------------------------------------------------------|
| `userId`              | Default | HubSpot user ID that loaded the CRM record.                                        |
| `userEmail`           | Default | Email address of the user.                                                          |
| `associatedObjectId`  | Default | ID of the loaded CRM record.                                                        |
| `associatedObjectType` | Default | Type of CRM record (e.g., CONTACT, COMPANY, DEAL).                               |
| `portalId`            | Default | ID of the HubSpot account.                                                          |
| `firstname`, `email`, `lastname` | Custom | Contact properties, specified in `propertiesToSend`.                              |


**Note:** Requests time out after 5 seconds; a connection must be established within 3 seconds.


### Example Response (JSON):

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
  "settingsAction": { /* ... */ },
  "primaryAction": { /* ... */ },
  "secondaryActions": [ /* ... */ ]
}
```

* **`results`:** An array of up to five objects.  Additional objects can be linked.
* **`objectId`:** Unique ID for the object (required).
* **`title`:** Object title (required).
* **`link`:** URL for more details (optional, use `null` if no links exist).
* **`created`, `priority`:**  Example custom properties.
* **`actions`:** Array of custom actions.
* **`properties`:** Array of additional custom properties not defined in the card settings.
* **`settingsAction`, `primaryAction`, `secondaryActions`:**  Actions for settings, primary action, and secondary actions, respectively.



## Request Signatures

HubSpot includes the `X-HubSpot-Signature` header to verify requests. To validate:

1. Concatenate the app secret, HTTP method, URL, and request body.
2. Create a SHA-256 hash of this string.
3. Compare the hash to the signature.  Mismatch indicates a potential security breach.  See the [HubSpot request validation documentation](link-to-request-validation-docs-here) for details.


## Card Properties

The **Card Properties** tab allows defining custom properties displayed on the card.  Add properties and specify their name, label, and data type (CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, STRING).  The response must include values for these properties.  Additional custom properties can be included in the `properties` array of the response.


### Property Types

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Displays as a mailto link.
* **LINK:** Displays a hyperlink; `linkLabel` can be specified.
* **NUMERIC:** Displays numbers.
* **STATUS:** Displays as a colored indicator (DEFAULT, SUCCESS, WARNING, DANGER, INFO). Requires `optionType`.
* **STRING:** Displays text.



## Custom Actions

The **Custom actions** tab defines URLs for action buttons.  Actions use `uri` and can include `associatedObjectProperties`.  Action hooks and confirmation actions include `X-HubSpot-Signature` for verification; iframe actions do not.


### Action Types

* **IFRAME:** Opens a modal with an iframe.  Uses `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).

* **ACTION_HOOK:** Sends a server-side request; only success/error messages are shown to the user.  Supports GET, POST, PUT, DELETE, and PATCH.


* **CONFIRMATION_ACTION_HOOK:** Same as `ACTION_HOOK`, but includes a confirmation dialog. Supports GET, POST, PUT, DELETE, and PATCH.


**(Remember to replace placeholder links with actual HubSpot documentation URLs.)**
