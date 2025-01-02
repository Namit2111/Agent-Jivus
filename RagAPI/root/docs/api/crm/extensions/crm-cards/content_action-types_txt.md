# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displayed on HubSpot contact, company, deal, and ticket records within public apps.  This differs from UI extensions created with projects; CRM cards are for public apps, while UI extensions offer greater flexibility.


## Scope Requirements

To create CRM cards, your app requires OAuth scopes to read and write to the relevant CRM objects. For example, a card on contact records needs `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing these scopes requires deleting all associated cards. See HubSpot's OAuth documentation for more details.


## Creating a CRM Card

Cards are created either via the API (see Endpoints below) or through the HubSpot developer account UI:

1. Navigate to **Apps** in the main navigation.
2. Select the app.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card**.


## Data Request

When a user views a CRM record, HubSpot sends a data fetch request to your app's specified URL. This request includes:

* **Default Query Parameters:**
    * `userId`: HubSpot user ID.
    * `userEmail`: User's email address.
    * `associatedObjectId`: ID of the CRM record.
    * `associatedObjectType`: Type of CRM record (e.g., `CONTACT`, `COMPANY`).
    * `portalId`: HubSpot account ID.
* **Custom Query Parameters:**  HubSpot properties selected in the card settings (or `propertiesToSend` array in the API).


**Example Request (Contact Record):**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Data Fetch Configuration (JSON):**

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

**Request Timeout:** Requests timeout after 5 seconds; connection must be established within 3 seconds.


## Example Response

Your app responds with a JSON payload.  Here's an example:

```json
{
  "results": [
    {
      "objectId": 245,
      "title": "API-22: APIs working too fast",
      "link": "http://example.com/1",
      "created": "2016-09-15",
      "priority": "HIGH",
      "project": "API",
      "description": "...",
      "actions": [...]
    },
    // ... more results
  ],
  "settingsAction": { ... },
  "primaryAction": { ... }
}
```

**Response Fields:**

* `results`: Array of up to five objects (cards).  Can include links to additional objects if more than five exist.
    * `objectId`: Unique ID.
    * `title`: Card title.
    * `link`: URL for details (optional, use `null` if no link).
    * `created`, `priority`: Example custom properties (defined in card settings).
    * `properties`: Array of additional custom properties.
    * `actions`: Array of actions (see below).
* `settingsAction`: Iframe action to update app settings.
* `primaryAction`: Primary action for the record type.
* `secondaryActions`:  Additional actions.


## Request Signatures

HubSpot uses the `X-HubSpot-Signature` header to verify requests.  To validate:

1. Concatenate your app secret, HTTP method, URL, and request body.
2. Create a SHA-256 hash of this string.
3. Compare the hash to the signature in the header.


## Card Properties

Define custom properties displayed on the card via the "Card Properties" tab.  The response should include values for these properties.  Supported data types:

* `CURRENCY`: Requires `currencyCode` (ISO 4217).
* `DATE`: `yyyy-mm-dd` format.
* `DATETIME`: Milliseconds since epoch.
* `EMAIL`: Email address (displayed as a link).
* `LINK`: URL (can include `linkLabel`).
* `NUMERIC`: Number.
* `STATUS`: Status indicator (requires `optionType`: `DEFAULT`, `SUCCESS`, `WARNING`, `DANGER`, `INFO`).
* `STRING`: Text.


## Custom Actions

Define action URLs on the "Custom Actions" tab. Actions include:

* **IFRAME actions:** Open a modal with an iframe.  Use `window.postMessage` to close the modal (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK actions:** Send a server-side request (GET, POST, PUT, DELETE, PATCH). Includes `X-HubSpot-Signature`.
* **CONFIRMATION_ACTION_HOOK actions:** Same as ACTION_HOOK, but requires user confirmation. Includes `X-HubSpot-Signature`.


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

This comprehensive documentation provides a detailed overview of the HubSpot CRM Cards API, enabling developers to integrate their applications seamlessly with HubSpot. Remember to consult HubSpot's official documentation for the most up-to-date information and best practices.
