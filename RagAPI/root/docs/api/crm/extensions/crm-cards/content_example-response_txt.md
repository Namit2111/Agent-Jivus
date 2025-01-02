# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displayed on HubSpot contact, company, deal, and ticket records within a public app.  This differs from UI extensions created with projects; CRM cards are for public apps, offering less flexibility but simpler integration.

## Scope Requirements

To create CRM cards, your app requires the necessary OAuth scopes to read and write to the relevant CRM objects.  For example, a card on contact records needs `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing CRM object scopes requires deleting all existing cards for those object types.  See the HubSpot OAuth documentation for details on scopes and authorization.

## Creating a CRM Card

CRM cards can be created via the API or the HubSpot developer account UI. This document focuses on the API approach.

### API Endpoint (Not explicitly provided in the text, but inferred)

The exact endpoint for creating CRM cards isn't explicitly defined in the provided text.  However, based on the context, it would likely be a POST request to a `/crm/v3/cards` or similar endpoint within the HubSpot API.  This needs to be confirmed in the HubSpot API documentation.

### Request Body (Example)

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
  },
  // ... other card properties (see below) ...
}
```

* `"title"`: (string) The title of the card.
* `"fetch"`: (object) Configuration for data fetching.
    * `"targetUrl"`: (string) The URL HubSpot will request data from.
    * `"objectTypes"`: (array) An array of objects specifying the CRM object types and properties to send.
        * `"name"`: (string) The CRM object type (e.g., "contacts", "companies", "deals", "tickets").
        * `"propertiesToSend"`: (array) An array of HubSpot properties to include as query parameters.

## Data Request

HubSpot makes an outbound GET request to your `targetUrl` when a user views a relevant CRM record.  The request includes:

* **Default Parameters:**
    * `"userId"`: (number) ID of the HubSpot user.
    * `"userEmail"`: (string) Email of the HubSpot user.
    * `"associatedObjectId"`: (number) ID of the CRM record.
    * `"associatedObjectType"`: (string) Type of CRM record (e.g., "CONTACT", "COMPANY").
    * `"portalId"`: (number) ID of the HubSpot account.
* **Custom Parameters:** The properties specified in `propertiesToSend`.

**Example Request:**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Timeout:**  Requests timeout after 5 seconds; a connection must be established within 3 seconds.

## Example Response

Your app must respond with a JSON payload.

```json
{
  "results": [
    {
      "objectId": 245,
      "title": "API-22: APIs working too fast",
      "link": "http://example.com/1",
      "created": "2016-09-15",
      "priority": "HIGH",
      "project": "API", //Example Custom property
      "description": "Customer reported...",
      "actions": [ /* ... actions (see below) ... */ ]
    },
    // ... more results ...
  ],
  "settingsAction": { /* ... settings action (see below) ... */ },
  "primaryAction": { /* ... primary action (see below) ... */ },
  "secondaryActions": [/* ... secondary actions ... */]
}
```

* `"results"`: (array) An array of up to five objects, each representing a card item.  Each object can include:
    * `"objectId"`: (number) Unique ID for the object.
    * `"title"`: (string) Title of the object.
    * `"link"`: (string) URL for more details (optional, use `null` if none).
    * `"created"`: (string) Date of creation (yyyy-mm-dd format).
    * `"priority"`: (string) Priority level.
    * `"properties"`: (array)  Array of custom properties with `label`, `dataType`, and `value`.  Supported `dataType` values are `CURRENCY`, `DATE`, `DATETIME`, `EMAIL`, `LINK`, `NUMERIC`, `STATUS`, `STRING`.  See below for details on these data types.
    * `"actions"`: (array) Array of actions (see below).
* `"settingsAction"`: (object) Iframe action for app settings.  (See below)
* `"primaryAction"`: (object) Primary action for a record type. (See below)
* `"secondaryActions"`: (array) Additional actions for a record type. (See below)


## Request Signatures

HubSpot includes an `X-HubSpot-Signature` header to verify requests.  This header contains a SHA-256 hash of `<app secret>+<HTTP method>+<URL>+<request body>`.  Verify this signature on your end.


## Card Properties

Define custom properties displayed on the card. These properties are defined within the API call.

### Property Data Types

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:**  `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Displays as a mailto link.
* **LINK:** Displays as a hyperlink; use `linkLabel` for custom label.
* **NUMERIC:** Displays numbers.
* **STATUS:** Displays as colored indicators (DEFAULT, SUCCESS, WARNING, DANGER, INFO). Requires `optionType`.
* **STRING:** Displays text.


## Custom Actions

Define actions users can take on the card.

### Action Types

* **IFRAME:** Opens a modal with an iframe.  Uses `window.postMessage({"action": "DONE"})` or `{"action": "CANCEL"}` to close the modal.
* **ACTION_HOOK:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH). Includes `X-HubSpot-Signature`.
* **CONFIRMATION_ACTION_HOOK:** Same as `ACTION_HOOK`, but with a confirmation dialog. Includes `X-HubSpot-Signature`.


**Example Iframe Action:**

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

**Example Action Hook Action:**

```json
{
  "type": "ACTION_HOOK",
  "httpMethod": "POST",
  "uri": "https://example.com/action-hook",
  "label": "Example action",
  "associatedObjectProperties": ["some_crm_property"]
}
```

**Example Confirmation Action Hook:**

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


This comprehensive documentation provides a clearer understanding of the HubSpot CRM Cards API. Remember to consult the official HubSpot API documentation for the most up-to-date information on endpoints and specific requirements.
