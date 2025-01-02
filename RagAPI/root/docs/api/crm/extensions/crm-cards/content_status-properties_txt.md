# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displaying information from external systems within HubSpot contact, company, deal, and ticket records.  Each app can have up to 25 CRM cards.  Note that these cards differ from custom cards created as UI extensions with projects; these are for public apps.

## Scope Requirements

To create CRM cards, your app needs the necessary OAuth scopes to read and write to the relevant CRM objects.  For example, a card on contact records requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing CRM object scopes necessitates deleting all existing cards for those object types.  Refer to the HubSpot OAuth documentation for details on scopes and authorization URL setup.

## Creating a CRM Card

CRM cards can be created via the API or the HubSpot developer account UI.  This document focuses on the API approach.

### API Endpoint (Not explicitly defined, needs further information from HubSpot documentation)

The exact API endpoint for creating a CRM card is not provided in the source text.  This information is crucial and needs to be sourced from HubSpot's official API documentation.  The endpoint will likely be a POST request to a specific URL.

### Request Body (Example)

The following example shows a JSON payload for creating a CRM card.  Replace placeholders with your actual values.

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
  // ... other properties ...  (See Card Properties section for more details)
}
```


## Data Request

When a user views a relevant CRM record, HubSpot makes an outbound GET request to the `targetUrl` specified in the card configuration. This request includes default and custom query parameters.

### Example Request

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

| Parameter             | Type     | Description                                                                        |
|-----------------------|----------|------------------------------------------------------------------------------------|
| `userId`              | Default  | HubSpot user ID who loaded the CRM record.                                      |
| `userEmail`           | Default  | Email address of the user who loaded the CRM record.                               |
| `associatedObjectId`   | Default  | ID of the loaded CRM record.                                                    |
| `associatedObjectType` | Default  | Type of the loaded CRM record (e.g., CONTACT, COMPANY, DEAL).                     |
| `portalId`            | Default  | ID of the HubSpot account.                                                        |
| `firstname`, `email`, `lastname` | Custom   | HubSpot properties sent as query parameters (defined in `propertiesToSend`). |

**Note:** Requests time out after 5 seconds (connection within 3 seconds).

## Response

Your app must respond with a JSON payload containing card data.

### Example Response

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
        // ... action objects ... (See Custom Actions section)
      ]
    },
    // ... more results ...
  ],
  "settingsAction": { /* ... */ },
  "primaryAction": { /* ... */ },
  "secondaryActions": [ /* ... */ ]
}
```

* `results`: An array (up to 5) of card property objects.
* `objectId`: Unique ID for the object.
* `title`: Title of the object.
* `link`: URL for more details (optional, use `null` if no link).
* `created`, `priority`:  Custom properties (defined in Card Properties).
* `actions`: Array of action objects.
* `properties`: Array of additional custom properties not defined in card settings.
* `settingsAction`, `primaryAction`, `secondaryActions`: Action objects for settings, primary action, and secondary actions respectively.


## Request Signatures

HubSpot includes the `X-HubSpot-Signature` header to verify request authenticity.  To validate:

1. Concatenate your app secret, HTTP method, URL, and request body.
2. Generate a SHA-256 hash of the concatenated string.
3. Compare the hash to the signature in the header.

## Card Properties

Define custom properties to display on the card.  Specify name, label, and data type (CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, STRING).


### Property Type Details

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:**  `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:**  Displayed as a mailto link.
* **LINK:** Displays a hyperlink; `linkLabel` is optional.
* **NUMERIC:** Displays numbers.
* **STATUS:** Displays colored indicators (DEFAULT, SUCCESS, WARNING, DANGER, INFO).  Requires `optionType`.
* **STRING:** Displays text.


## Custom Actions

Define actions users can take.  Actions use the `uri` field to specify the URL.

### Action Types

* **IFRAME:** Opens a modal with an iframe.  No request signature is included.  Use `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH).  Includes `X-HubSpot-Signature`.
* **CONFIRMATION_ACTION_HOOK:**  Same as `ACTION_HOOK`, but with a confirmation dialog.  Includes `X-HubSpot-Signature`.


## Example Code Snippets (already included in the original text)

The original text contains numerous code snippets illustrating requests, responses, and action definitions.


This enhanced documentation provides a more structured and comprehensive overview of the HubSpot CRM Cards API.  Remember to consult HubSpot's official API documentation for the most up-to-date information and details on API endpoints.
