# HubSpot CRM API: CRM Cards

This document details how to create and manage custom CRM cards within HubSpot using its API.  These cards allow you to display information from external systems directly on HubSpot contact, company, deal, and ticket records within a public app.  Note that these CRM cards differ from custom cards created as UI extensions using projects.

## Key Differences from UI Extensions

The CRM cards described here are specifically for **public apps**. They offer a simpler integration method compared to UI extensions built with projects. UI extensions provide greater flexibility, customizability, and interactivity using a more modern toolset.  If you are not building a public app, consider using React-based UI extensions.

## Use Case Example

Imagine integrating bug tracking software with the HubSpot App Marketplace. You can create a custom CRM card to display tracked bugs directly on contact records, improving support reps' workflow.

## Scope Requirements

To create CRM cards, your app needs the appropriate OAuth scopes to read and write to the relevant CRM objects. For example, displaying cards on contact records requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing these scopes necessitates deleting all existing cards for those object types.  Refer to the [HubSpot OAuth documentation](link-to-oauth-docs-here) for details.


## Creating a CRM Card

CRM cards can be created via the API or through the HubSpot developer account UI.  API details are found in the [Endpoints](link-to-endpoints-here) section.

**Using the HubSpot UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select the app where you want to add the card.
3. Select **CRM cards** in the left sidebar.
4. Click **Create CRM card** in the upper right.


## Data Request

When a user views a CRM record, HubSpot sends a data fetch request to your app's specified URL. This request includes default query parameters and custom parameters based on the card's settings.

**Data Fetch URL:**  Specify the URL (`targetUrl` in the API) where your app fetches data.

**Target Record Types & Properties:** Select the CRM object types (contacts, companies, deals, tickets) and the HubSpot properties to include as query parameters.  These are defined in the `objectTypes` array in the API.

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

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Parameters:**

| Parameter             | Type     | Description                                                                 |
|----------------------|----------|-----------------------------------------------------------------------------|
| `userId`              | Default  | HubSpot user ID.                                                             |
| `userEmail`           | Default  | Email address of the user.                                                   |
| `associatedObjectId`   | Default  | ID of the CRM record.                                                        |
| `associatedObjectType` | Default  | Type of CRM record (e.g., CONTACT, COMPANY).                               |
| `portalId`            | Default  | ID of the HubSpot account.                                                  |
| `firstname`, `email`, `lastname` | Custom   | HubSpot properties specified in the card settings (`propertiesToSend`).       |

**Timeout:** Requests timeout after 5 seconds; a connection must be established within 3 seconds.


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
        // ... actions
      ]
    },
    // ... more results
  ],
  "settingsAction": { /* ... */ },
  "primaryAction": { /* ... */ },
  "secondaryActions": [ /* ... */ ]
}
```

**Response Structure:**

* `results`: Array of objects (up to 5).  Each object represents a card item.
* `objectId`: Unique ID for the object.
* `title`: Title of the object.
* `link`: URL for more details (optional, use `null` if no links).
* `created`, `priority`: Example custom properties defined in card settings.
* `properties`: Array of additional custom properties not defined in card settings.
* `actions`: Array of actions the user can perform.
* `settingsAction`, `primaryAction`, `secondaryActions`:  Actions for settings, primary action and secondary actions.



## Request Signatures

HubSpot includes an `X-HubSpot-Signature` header to verify requests.  This header contains a SHA-256 hash of the app secret, HTTP method, URL, and request body (if any).  Verify this signature on your server to prevent unauthorized access.  See the [HubSpot request validation documentation](link-to-request-validation-here) for details.


## Card Properties

The **Card Properties** tab allows defining custom properties displayed on the card.  These properties are included in your app's response.  Supported data types: CURRENCY, DATE, DATETIME, EMAIL, LINK, NUMERIC, STATUS, STRING.


## Property Types

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:** Displays as a mailto link.
* **LINK:** Displays a hyperlink; use `linkLabel` for custom label.
* **NUMERIC:** Displays a number.
* **STATUS:** Displays as a colored indicator (DEFAULT, SUCCESS, WARNING, DANGER, INFO). Requires `optionType`.
* **STRING:** Displays text.


## Custom Actions

The **Custom actions** tab defines the URLs for action buttons on the card.  Action types include:

* **IFRAME:** Opens a modal with an iframe.  No request signature is sent.  Use `window.postMessage` to close the modal (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH).  Includes `X-HubSpot-Signature`.
* **CONFIRMATION_ACTION_HOOK:** Same as `ACTION_HOOK`, but displays a confirmation dialog.  Includes `X-HubSpot-Signature`.


##  Example Custom Action (JSON)

**IFRAME:**

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

**ACTION_HOOK:**

```json
{
  "type": "ACTION_HOOK",
  "httpMethod": "POST",
  "uri": "https://example.com/action-hook",
  "label": "Example action",
  "associatedObjectProperties": ["some_crm_property"]
}
```

**CONFIRMATION_ACTION_HOOK:**

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

Remember to replace placeholder URLs and property names with your actual values.  Consult the HubSpot API documentation for the most up-to-date information and details on error handling.
