# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displaying information from external systems within HubSpot contact, company, deal, and ticket records.

## Overview

HubSpot CRM cards enhance CRM records by embedding data from external applications.  Each public app can have up to 25 CRM cards. These cards differ from UI extensions created with projects; CRM cards are for public apps, offering less flexibility but simpler integration.  They operate by HubSpot making outbound requests to the app's specified URL to fetch data, then displaying it on the record page.  Custom actions can also be defined for user interaction.

**Key Differences from UI Extensions:** CRM cards are simpler to implement for public apps but lack the flexibility and interactivity of UI extensions built with projects.  For private apps or more complex integrations, consider UI extensions.


## Scope Requirements

To create CRM cards, your app needs appropriate OAuth scopes. For example, a card on contact records requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes. Removing CRM object scopes necessitates deleting all existing cards for those object types. Refer to the HubSpot OAuth documentation for more details on scopes and authorization URL setup.


## Creating a CRM Card

Cards are defined within your app's feature settings.  They can be created either through the API or the HubSpot UI:

**Via API (see Endpoints section below):**  Use the API to programmatically create and manage cards.

**Via HubSpot UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select your app.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card**.
5. Configure the card using the various tabs (Data fetch, Card Properties, Custom actions).


## Data Request

When a user views a relevant CRM record, HubSpot sends a `GET` request to the app's `targetUrl`. This request includes:

* **Default Parameters:**
    * `userId`: The ID of the HubSpot user.
    * `userEmail`: The email address of the HubSpot user.
    * `associatedObjectId`: The ID of the CRM record.
    * `associatedObjectType`: The type of CRM record (e.g., `CONTACT`, `COMPANY`, `DEAL`).
    * `portalId`: The ID of the HubSpot account.
* **Custom Parameters:** HubSpot properties specified in the card's settings (`propertiesToSend` array in the API).


**Example Request (for contacts with `firstname`, `email`, `lastname` properties):**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Timeout:** Requests will timeout after 5 seconds; a connection must be established within 3 seconds.


## Example Data Fetch Configuration (JSON):

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


## Example Response (JSON):

The response should contain an array of objects (`results`), each representing a card item.  Each object can include properties defined in the card settings and additional custom properties.

```json
{
  "results": [
    {
      "objectId": 245,
      "title": "API-22: APIs working too fast",
      "link": "http://example.com/1",
      "created": "2016-09-15",
      "priority": "HIGH",
      "project": "API",  //Custom Property
      "description": "Customer reported...",
      "actions": [ /* ...actions... */ ]
    }
  ],
  "settingsAction": { /* ... */ },
  "primaryAction": { /* ... */ }
}
```

**Response Elements:**

* `results`: Array of objects (max 5).  Each object should have:
    * `objectId`: Unique ID.
    * `title`: Title of the object.
    * `link`: (Optional) URL for more details (use `null` if no objects have links).
    * `created`: (Required) Date of object creation (formatted as yyyy-mm-dd).
    * `priority`: (Required) Priority level (string).
    * `properties`: Array of custom properties (defined dynamically, not in card settings).
    * `actions`: Array of actions.

* `settingsAction`:  An iframe action for updating app settings.
* `primaryAction`:  The primary action for a record type.
* `secondaryActions`: Array of secondary actions.


## Request Signatures

HubSpot includes the `X-HubSpot-Signature` header to validate requests. To verify:

1. Concatenate `<app secret>+<HTTP method>+<URL>+<request body>`.
2. Create a SHA-256 hash of the string.
3. Compare the hash with the signature.


## Card Properties

The "Card Properties" tab defines custom properties displayed on the card.  The response must include values for these properties.  Supported data types include: CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, STRING.


**Property Type Details:**

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Email address (displayed as a mailto link).
* **LINK:** URL; can include `linkLabel`.
* **NUMERIC:** Number.
* **STATUS:** Requires `optionType`: DEFAULT, SUCCESS, WARNING, DANGER, INFO.
* **STRING:** Text.


## Custom Actions

The "Custom Actions" tab defines URLs for action buttons.  Action types include:

* **IFRAME:** Opens a modal with an iframe.  No request signature.  Use `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request. Includes `X-HubSpot-Signature`.  `httpMethod` can be GET, POST, PUT, DELETE, PATCH.
* **CONFIRMATION_ACTION_HOOK:** Same as ACTION_HOOK, but with a confirmation dialog.  Includes `X-HubSpot-Signature`.


## API Endpoints

*(The provided text lacks specific API endpoint details.  This section would need to be added based on HubSpot's API documentation for CRM Cards.)*  This section should include:

*  Endpoint URLs for creating, updating, and deleting CRM cards.
*  Request methods (POST, PUT, DELETE).
*  Request body parameters (JSON).
*  Response codes and formats.
*  Authentication methods (API keys, OAuth).


## Example Iframe Action (JSON):

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


## Example Action Hook Action (JSON):

```json
{
  "type": "ACTION_HOOK",
  "httpMethod": "POST",
  "uri": "https://example.com/action-hook",
  "label": "Example action",
  "associatedObjectProperties": ["some_crm_property"]
}
```

## Example Confirmation Action Hook Action (JSON):

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


This comprehensive documentation provides a detailed overview and examples for implementing HubSpot CRM Cards.  Remember to consult the official HubSpot API documentation for the most up-to-date information on endpoints and API specifications.
