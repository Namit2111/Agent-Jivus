# HubSpot CRM API: CRM Cards

This document details how to create and manage custom CRM cards within HubSpot using the API. CRM cards allow you to display information from external systems directly on HubSpot contact, company, deal, and ticket records within a public app.

**Note:** These CRM cards differ from custom cards created as UI extensions with projects.  CRM cards (described here) are for public apps, while UI extensions offer greater flexibility and are built using a more modern toolset.  If you are not building a public app, consider using React-based UI extensions.

## Key Concepts

* **Public App:**  CRM cards are a feature specifically for public apps listed on the HubSpot App Marketplace.
* **Card Limit:** Each app can have up to 25 CRM cards.
* **Data Fetch:** HubSpot makes outbound requests to your app to retrieve data for display on the card.
* **Custom Actions:**  Cards can include actions (e.g., opening a modal, performing server-side operations).
* **OAuth Scopes:**  Your app requires specific OAuth scopes to read and write to the CRM objects your cards appear on (e.g., `crm.objects.contacts.read`, `crm.objects.contacts.write`).


## Creating a CRM Card

CRM cards can be created via the API or through the HubSpot developer UI:

**Via API:** Refer to the [Endpoints](#endpoints) section for details.

**Via HubSpot UI:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select the app where you want to add a card.
3. In the left sidebar, select **CRM cards**.
4. Click **Create CRM card**.
5. Configure the card using the tabs described below.

## Card Configuration

### Scope Requirements

To create cards for a specific CRM object type (Contacts, Companies, Deals, Tickets), your app must request the necessary read and write scopes for that object.  Removing these scopes requires deleting all existing cards for those object types first. See the HubSpot OAuth documentation for more details on scopes.

### Data Request

When a user views a CRM record, HubSpot sends a data fetch request to your app's specified URL. This request includes default parameters (e.g., `userId`, `userEmail`, `associatedObjectId`, `associatedObjectType`, `portalId`) and custom properties you select.

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
  // ...
}
```

**Example Request:**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Parameters:**

| Parameter           | Type    | Description                                                                        |
|----------------------|---------|------------------------------------------------------------------------------------|
| `userId`             | Default | HubSpot user ID.                                                                   |
| `userEmail`          | Default | Email address of the logged-in user.                                              |
| `associatedObjectId` | Default | ID of the CRM record.                                                             |
| `associatedObjectType` | Default | Type of CRM record (CONTACT, COMPANY, DEAL, TICKET).                              |
| `portalId`           | Default | HubSpot account ID.                                                              |
| Custom Properties    | Custom  | Properties specified in the card's configuration (e.g., `firstname`, `email`). |

**Timeout:** Requests time out after 5 seconds; a connection must be established within 3 seconds.

### Example Response

Your app responds with a JSON payload containing card data.

**Example Response (JSON):**

```json
{
  "results": [
    // ... (array of objects, up to 5) ...
  ],
  "settingsAction": { /* iframe action for settings */ },
  "primaryAction": { /* primary action */ },
  "secondaryActions": [ /* array of actions */ ]
}
```

Each object in the `results` array represents a data item to display on the card.  It can include:

* `objectId`: Unique ID.
* `title`: Title of the object.
* `link`: URL for more details (optional, use `null` if no links).
* `created`, `priority`:  Custom properties defined in the Card Properties tab.
* `properties`: Array of additional custom properties.
* `actions`: Array of actions the user can take.


### Request Signatures

HubSpot uses a signature header (`X-HubSpot-Signature`) to verify requests.  To verify:

1. Concatenate your app secret, HTTP method, URL, and request body (if any).
2. Generate a SHA-256 hash of the concatenated string.
3. Compare the hash to the signature in the header.

### Card Properties Tab

This tab allows you to define custom properties for your card.  You can add properties with specific data types:

* **CURRENCY:** Requires `currencyCode` (ISO 4217).
* **DATE:** `yyyy-mm-dd` format.
* **DATETIME:** Milliseconds since epoch.
* **EMAIL:**  Displayed as a mailto link.
* **LINK:** Displays a hyperlink; `linkLabel` is optional.
* **NUMERIC:** Displays a number.
* **STATUS:** Displays a colored indicator (DEFAULT, SUCCESS, WARNING, DANGER, INFO).
* **STRING:** Displays text.

### Custom Actions Tab

Define action URLs for buttons on your CRM card.  Actions can be:

* **IFRAME:** Opens a modal with an iframe. Uses `window.postMessage` to close ({"action": "DONE"} or {"action": "CANCEL"}).
* **ACTION_HOOK:** Sends a server-side request (GET, POST, PUT, DELETE, PATCH). Includes a signature header.
* **CONFIRMATION_ACTION_HOOK:**  Similar to `ACTION_HOOK`, but shows a confirmation dialog first. Includes a signature header.


## Endpoints

*(This section would list specific API endpoints for creating, updating, and deleting CRM cards.  The provided text does not contain endpoint details.)*


## Further Reading

* [HubSpot OAuth Documentation](link_to_oauth_docs)
* [Validating Requests from HubSpot](link_to_request_validation)
* [Using Extension Property Types](link_to_property_types)


This Markdown documentation provides a comprehensive overview of HubSpot's CRM cards API.  Remember to replace placeholder links with actual HubSpot documentation URLs.
