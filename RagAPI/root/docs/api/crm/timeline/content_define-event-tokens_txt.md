# HubSpot CRM API: Timeline Events Documentation

This document details the HubSpot CRM API endpoints for creating and managing timeline events. Timeline events allow you to add custom information from your app to the timeline of HubSpot contacts, companies, or deals.

## 1. Creating an Event Template

Before creating events, you must create an event template.  An event template defines the structure and display of your custom events.  A single app can have up to 750 event templates.

**1.1 Creating Event Templates via API:**

Use a `POST` request to `/crm/v3/timeline/{appId}/event-templates`.

**Request:**

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Example Webinar Registration",
    "objectType": "contacts"
  }' \
  'https://api.hubapi.com/crm/v3/timeline/{appId}/event-templates?hapikey={developerAPIkey}'
```

* Replace `{appId}` with your app ID.
* Replace `{developerAPIkey}` with your developer API key.
* `objectType` can be "contacts", "companies", or "deals".
* `headerTemplate` and `detailTemplate` (see section 3) can be included in this request.

**Response:**  A JSON object representing the created event template, including its `id`.  This ID is crucial for subsequent operations.

**1.2 Getting all Event Templates:**

Use a `GET` request to `/crm/v3/timeline/{appId}/event-templates`.

```bash
curl -X GET 'https://api.hubapi.com/crm/v3/timeline/{appId}/event-templates?hapikey={developerAPIkey}'
```

**Response:** A JSON array containing all event templates for the app.

**1.3 Creating Event Templates in HubSpot UI:**

You can also create and manage event templates through your HubSpot developer account under "Timeline events".


## 2. Defining Event Tokens

Event tokens allow you to attach custom data to events.  You can create up to 500 tokens per event template.  Company and deal events cannot be used in list segmentation or automation.

**2.1 Creating Event Tokens via API:**

Use a `POST` request to `/crm/v3/timeline/{appId}/event-templates/{eventTemplateId}/tokens`.

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "name": "webinarName",
    "label": "Webinar Name",
    "type": "string"
  }' \
  'https://api.hubapi.com/crm/v3/timeline/{appId}/event-templates/{eventTemplateId}/tokens?hapikey={developerAPIkey}'
```

* Replace `{eventTemplateId}` with the ID of the event template.
* Supported types: `"string"`, `"number"`, `"enumeration"`, `"date"` (milliseconds since Unix epoch).

**2.2 Getting Event Tokens:**

Use a `GET` request to `/crm/v3/timeline/{appId}/event-templates/{eventTemplateId}/tokens`.

```bash
curl -X GET -H "Content-Type: application/json" 'https://api.hubapi.com/crm/v3/timeline/{appId}/event-templates/{eventTemplateId}?hapikey={developerHapikey}'
```


## 3. Defining Header and Detail Templates

These templates control how events are displayed in the HubSpot timeline.  They use Markdown with Handlebars templating.

**3.1 Defining Templates via API:**

Use a `PUT` request to `/crm/v3/timeline/{appId}/event-templates/{eventTemplateId}`.

```bash
curl -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "id": "{eventTemplateId}",
    "name": "Example Name Change",
    "headerTemplate": "Registered for [{{webinarName}}](https://mywebinarsystem/webinar/{{webinarId}})",
    "detailTemplate": "Registration occurred at {{#formatDate timestamp}}{{/formatDate}}"
  }' \
  'https://api.hubapi.com/crm/v3/timeline/{appId}/event-templates/{eventTemplateId}?hapikey={developerAPIkey}'
```

* Use Handlebars expressions like `{{tokenName}}` to insert token values.  `#formatDate` is a custom helper for date formatting.


## 4. Creating an Event

To create an event, you need an OAuth 2.0 access token. Developer API keys and private app access tokens are **not** sufficient.

**4.1 Creating Events via API:**

Use a `POST` request to `/crm/v3/timeline/events`.

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {OAuth2AccessToken}" \
  -d '{
    "eventTemplateId": "{eventTemplateId}",
    "email": "a.test.contact@email.com",
    "tokens": {
      "webinarName": "A Test Webinar",
      "webinarId": "001001",
      "webinarType": "regular"
    }
  }' \
  'https://api.hubapi.com/crm/v3/timeline/events'
```

* Replace `{OAuth2AccessToken}` with your OAuth access token.
* You can use `email`, `objectId` (for existing contacts, companies, or deals), or `utk` (user token) to identify the CRM object.  `objectId` has highest priority, followed by `utk`, then `email`.
* The `timestamp` property can specify the event time (milliseconds since Unix epoch or ISO 8601 format).  Defaults to the request time.
* `extraData` allows for adding arbitrary JSON data (see Section 7).

## 5.  Associating Events with CRM Objects

Use `email`, `objectId`, or `utk` to associate an event with a contact, company, or deal.  Prioritize `objectId` (vid), then `utk`, then `email`. Using `email` might create a new contact if one doesn't exist.


## 6. Stamping Event Data onto CRM Object Properties

You can map event tokens to CRM object properties to automatically update object properties when an event is created.  This is done by setting the `objectPropertyName` field when defining or updating a token.


## 7. Understanding `extraData`

The `extraData` field allows adding structured JSON data to an event. This data can only be accessed within the `detailTemplate` using Handlebars.


## 8. Setting up a Custom Icon

Upload a custom icon (square dimensions, transparent background, 5MB max size) via the HubSpot UI under Timeline events.  This icon will appear next to your events in the CRM timeline.


## 9. Timeline Extensions (iFrames)

You can include an iFrame within an event using the `timelineIFrame` field, which includes `linkLabel`, `headerLabel`, `url`, `width`, and `height` properties.  This allows displaying external data in a modal window.


This documentation provides a comprehensive overview of the HubSpot CRM Timeline Events API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
