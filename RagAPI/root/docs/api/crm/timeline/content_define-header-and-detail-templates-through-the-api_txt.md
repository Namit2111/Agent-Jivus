# HubSpot CRM API: Timeline Events

This document details the HubSpot CRM API's functionality for creating and managing timeline events.  Timeline events allow you to add custom information from your app to the timelines of HubSpot contacts, companies, or deals.

## I.  Creating an Event Template

Before creating events, you must create an event template.  This defines the structure and appearance of events your app will add.  An app can have up to 750 event templates.

### A. Creating Event Templates through the API

**Endpoint:** `POST https://api.hubapi.com/crm/v3/timeline/{{appId}}/event-templates?hapikey={{developerAPIkey}}`

**Request Body (JSON):**

```json
{
  "name": "Example Webinar Registration",
  "objectType": "contacts"  // or "companies", "deals"
  "headerTemplate": "Registered for {{webinarName}}", //Optional, Handlebars template
  "detailTemplate": "Registration at {{#formatDate timestamp}}{{/formatDate}}", //Optional, Handlebars template
  "tokens": [ //Optional, define tokens here instead of separately
    {
      "name": "webinarName",
      "label": "Webinar Name",
      "type": "string"
    },
    // ... more tokens
  ]
}
```

**Response (JSON):**  The full event template definition, including the newly assigned `id`.

**Example using cURL:**

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Example Webinar Registration",
        "objectType": "contacts"
       }' \
  'https://api.hubapi.com/crm/v3/timeline/{{appId}}/event-templates?hapikey={{developerAPIkey}}'
```

**Retrieve all event templates:**

**Endpoint:** `GET https://api.hubapi.com/crm/v3/timeline/{{appId}}/event-templates?hapikey={{developerAPIkey}}`


### B. Creating Event Templates in HubSpot

You can also create and manage event templates within your HubSpot developer account under your app's settings, navigating to the Timeline events section.

### C. Defining Event Tokens

Tokens allow you to attach custom data to events.  A template can have up to 500 tokens.  Company and deal events cannot be used in list segmentation or automation.  Reserved token names: `log`, `lookup`.

**Endpoint (Create Token):** `POST https://api.hubapi.com/crm/v3/timeline/{{appId}}/event-templates/{{eventTemplateId}}/tokens?hapikey={{developerAPIkey}}`

**Request Body (JSON):**

```json
{
  "name": "webinarName",
  "label": "Webinar Name",
  "type": "string" // "number", "enumeration", "date" (milliseconds since epoch)
  "options":[ {"value":"regular","label":"Regular"}, {"value":"ama","label":"Ask me anything"}] //For type: enumeration
}
```

**Endpoint (Retrieve Tokens):** `GET https://api.hubapi.com/crm/v3/timeline/{{appId}}/event-templates/{{eventTemplateId}}/tokens?hapikey={{developerAPIkey}}`


### D. Defining Header and Detail Templates (Handlebars)

These templates control how events are displayed in the HubSpot timeline.  `extraData` can only be referenced in the `detailTemplate`.

**Endpoint (Update Template):** `PUT https://api.hubapi.com/crm/v3/timeline/{{appId}}/event-templates/{{eventTemplateId}}?hapikey={{developerAPIkey}}`


**Request Body (JSON):**

```json
{
  "id": "{{eventTemplateId}}",
  "name": "Example Webinar Registration",
  "headerTemplate": "Registered for [{{webinarName}}](https://mywebinarsystem/webinar/{{webinarId}})",
  "detailTemplate": "Registration occurred at {{#formatDate timestamp}}{{/formatDate}}"
}
```

## II. Creating an Event

To create an event, you need an OAuth 2.0 access token (developer API keys are not allowed).

### A. Creating an Event through the API

**Endpoint:** `POST https://api.hubapi.com/crm/v3/timeline/events`

**Request Headers:**

* `Content-Type: application/json`
* `Authorization: Bearer {{OAuth2AccessToken}}`

**Request Body (JSON):**

```json
{
  "eventTemplateId": "{{eventTemplateId}}",
  "email": "a.test.contact@email.com", // Or objectId, utk (or combination)
  "timestamp": "2024-10-27T10:00:00Z", //Optional, ISO 8601 or epoch milliseconds
  "tokens": {
    "webinarName": "A Test Webinar",
    "webinarId": "001001",
    "webinarType": "regular"
  },
  "extraData": {
    // ...optional extra data
  },
    "timelineIFrame":{ //optional
        "linkLabel":"View external data",
        "headerLabel":"Example iframe",
        "url":"https://www.example.com",
        "width":800,
        "height":300
    }
}
```

**Response:**  The created event details.


### B.  Associating Events with CRM Objects

* **Contacts:** Use `email` or `objectId` (vid) or `utk` (usertoken) – or a combination. `objectId` has highest priority.
* **Companies:** Use `objectId` (companyId).
* **Deals:** Use `objectId` (dealId).

### C. Stamping Event Data onto CRM Object Properties

Map event tokens to HubSpot properties using the `objectPropertyName` field when updating a token via PUT request.


## III.  `extraData`

Use `extraData` to add complex, unstructured JSON data to an event.  It can only be accessed within the `detailTemplate`.

## IV. Setting up a Custom Icon

Upload a square image with a transparent background (max 5MB) through your HubSpot developer account's Timeline Events settings.


This documentation provides a comprehensive overview of HubSpot's CRM Timeline Events API. Remember to replace placeholders like `{{appId}}`, `{{developerAPIkey}}`, `{{eventTemplateId}}`, and `{{OAuth2AccessToken}}` with your actual values.  Consult the official HubSpot API documentation for the most up-to-date information and details.
