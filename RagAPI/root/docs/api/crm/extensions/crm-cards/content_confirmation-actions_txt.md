# HubSpot CRM API: CRM Cards

This document details how to create and manage custom CRM cards within HubSpot public apps using the HubSpot API.  These cards allow you to display information from external systems directly on HubSpot contact, company, deal, and ticket records.  Note that these CRM cards are distinct from custom cards created as UI extensions with projects.  UI extensions offer greater flexibility and interactivity using a more modern toolset and are recommended for private apps.

## Key Differences from UI Extensions

* **Purpose:** CRM cards are designed for public apps, while UI extensions are better suited for private apps.
* **Flexibility:** UI extensions provide significantly more flexibility and customization options.
* **Interactivity:** UI extensions offer enhanced interactivity.
* **Toolset:** UI extensions utilize a more modern toolset.

If you are not building a public app, consider using React-based UI extensions.


## Scope Requirements

To create custom CRM cards, your app requires specific OAuth scopes:

* `crm.objects.contacts.read` and `crm.objects.contacts.write` (for contact records)
* Similar read and write scopes for company, deal, and ticket records, as needed.

Removing CRM object scopes necessitates deleting all associated cards.  Refer to the HubSpot OAuth documentation for details on scopes and setting up the authorization URL.


## Creating a CRM Card

CRM cards can be created via the API or through the HubSpot developer account UI.  API details are available in the **Endpoints** tab (not shown in provided text).

**Using the HubSpot UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select the app where you want to add a card.
3. Select **CRM cards** from the left sidebar menu.
4. Click **Create CRM card** in the upper right corner.
5. Configure the card using the provided tabs.


## Data Request

When a user views a CRM record, HubSpot sends a data fetch request to your app's specified URL. This request includes:

* **Default Query Parameters:**
    * `userId`: HubSpot user ID.
    * `userEmail`: User's email address.
    * `associatedObjectId`: ID of the CRM record.
    * `associatedObjectType`: Type of CRM record (e.g., `CONTACT`, `COMPANY`).
    * `portalId`: HubSpot account ID.
* **Custom Query Parameters:**  These are HubSpot properties selected in the app's configuration, specified through `propertiesToSend` array in the API.  Example: `firstname`, `email`, `lastname`.

**Example Request URL:**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Timeout:** Requests timeout after 5 seconds; a connection must be established within 3 seconds.


## Example Response

The response should be a JSON object with the following structure:

```json
{
  "results": [ // Array of objects (up to 5)
    {
      "objectId": 245,
      "title": "API-22: APIs working too fast",
      "link": "http://example.com/1",
      "created": "2016-09-15",
      "priority": "HIGH",
      "project": "API",
      "description": "...",
      "actions": [ // Array of actions
        {
          "type": "IFRAME",
          "width": 890,
          "height": 748,
          "uri": "https://example.com/edit-iframe-contents",
          "label": "Edit"
        },
        // ...more actions
      ],
      "properties": [ //Array of custom properties not defined in card settings
          {
              "label": "Resolved by",
              "dataType": "EMAIL",
              "value": "ijones@hubspot.com"
          }
          // ...more custom properties
      ]
    },
    // ...more objects
  ],
  "settingsAction": { // Iframe action for updating app settings
    "type": "IFRAME",
    "uri": "..."
  },
  "primaryAction": { //Primary action for a record type
      "type": "IFRAME",
      "uri": "..."
  },
  "secondaryActions": [ //List of actions displayed on the card
      //...
  ]
}
```


## Request Signatures

HubSpot includes an `X-HubSpot-Signature` header to verify requests.  To validate:

1. Concatenate the app secret, HTTP method, URL, and request body (if any).
2. Generate a SHA-256 hash of the concatenated string.
3. Compare the hash to the signature in the header.


## Card Properties

Define custom properties to display on the card via the **Card Properties** tab.  These properties are included in the response.  Supported data types:

* `CURRENCY`: Requires `currencyCode` (ISO 4217).
* `DATE`: `yyyy-mm-dd` format.
* `DATETIME`: Milliseconds since epoch.
* `EMAIL`: Displays as a mailto link.
* `LINK`: Displays a hyperlink; optionally include `linkLabel`.
* `NUMERIC`: Displays a number.
* `STATUS`: Displays a colored indicator (`DEFAULT`, `SUCCESS`, `WARNING`, `DANGER`, `INFO`). Requires `optionType`.
* `STRING`: Displays text.


## Custom Actions

Define action URLs on the **Custom actions** tab.  These URLs are accessed via the `uri` field in the response's `actions` array.  Action types:

* **IFRAME:** Opens a modal with an iframe.  Uses `window.postMessage` to signal completion (`{"action": "DONE"}` or `{"action": "CANCEL"}`).
* **ACTION_HOOK:** Sends a server-side request (includes `X-HubSpot-Signature`).  `httpMethod` can be `GET`, `POST`, `PUT`, `DELETE`, or `PATCH`.
* **CONFIRMATION_ACTION_HOOK:**  Similar to `ACTION_HOOK`, but includes a confirmation dialog.


This detailed explanation should provide a comprehensive overview of HubSpot's CRM card API. Remember to consult the official HubSpot API documentation for the most up-to-date information and specific endpoint details.
