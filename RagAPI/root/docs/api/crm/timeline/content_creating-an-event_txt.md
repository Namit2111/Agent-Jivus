# HubSpot CRM API: Timeline Events

This document details the HubSpot CRM API for creating and managing timeline events.  Timeline events allow you to add custom information from your app to the timelines of HubSpot contacts, companies, or deals.

## I. Creating an Event Template

Before creating events, you must create an event template.  This template defines the structure and appearance of the events your app will add.  An app can have up to 750 event templates.

### A. API Call (Create Event Template)

```bash
curl -X POST \
-H "Content-Type: application/json" \
-d '{
  "name": "Example Webinar Registration",
  "objectType": "contacts"
}' \
"https://api.hubapi.com/crm/v3/timeline/<<appId>>/event-templates?hapikey=<<developerAPIkey>>"
```

* **`<<appId>>`**: Your HubSpot App ID.
* **`<<developerAPIkey>>`**: Your HubSpot developer API key.
* **`objectType`**:  Specifies the object type (contacts, companies, or deals).
* **Response**:  Returns the full event template definition, including the `id` (required for subsequent operations).


### B.  API Call (Get All Event Templates)

```bash
curl -X GET \
"https://api.hubapi.com/crm/v3/timeline/<<appId>>/event-templates?hapikey=<<developerAPIkey>>"
```

* **Response**: Returns a list of all event templates for your app, including their IDs.


### C. HubSpot UI (Create Event Template)

You can also create event templates through the HubSpot developer account UI. Navigate to your app settings, then to "Timeline events," and use the "Create event type" button.

## II. Defining Event Tokens

Event tokens allow you to attach custom data to events.  You can create up to 500 tokens per template.  Note: Company and deal events cannot be used in list segmentation or automation.

### A. API Call (Create Event Token)

```bash
curl -X POST \
-H "Content-Type: application/json" \
-d '{
  "name": "webinarName",
  "label": "Webinar Name",
  "type": "string"
}' \
"https://api.hubapi.com/crm/v3/timeline/<<appId>>/event-templates/<<eventTemplateId>>/tokens?hapikey=<<developerHapikey>>"
```

* **`<<eventTemplateId>>`**: The ID of the event template.
* **`name`**: The token name (e.g., `webinarName`).
* **`label`**:  The user-friendly label for the token.
* **`type`**:  The data type (`string`, `number`, `enumeration`, `date`).  `enumeration` requires an `options` array.
* **Response**: Returns the created token.


### B. API Call (Get Event Tokens)

```bash
curl -X GET \
-H "Content-Type: application/json" \
"https://api.hubapi.com/crm/v3/timeline/<<appId>>/event-templates/<<eventTemplateId>>/tokens?hapikey=<<developerHapikey>>"
```

* **Response**: Returns a list of all tokens for the specified event template.

## III. Defining Header and Detail Templates

These templates control how the event is displayed in the HubSpot timeline.  Use Handlebars.js templates with Markdown.

### A. API Call (Update Event Template with Templates)

```bash
curl -X PUT \
-H "Content-Type: application/json" \
-d '{
  "id": "<<eventTemplateId>>",
  "name": "Example Name Change",
  "headerTemplate": "Registered for [{{webinarName}}](https://mywebinarsystem/webinar/{{webinarId}})",
  "detailTemplate": "Registration occurred at {{#formatDate timestamp}}{{/formatDate}}"
}' \
"https://api.hubapi.com/crm/v3/timeline/<<appId>>/event-templates/<<eventTemplateId>>?hapikey=<<developerHapikey>>"
```

*  Handlebars variables (e.g., `{{webinarName}}`) are replaced with token values.
*  `#formatDate` is a custom Handlebars helper (you'll need to implement this).


## IV. Creating an Event

This section shows how to create a timeline event using the created template and tokens.  **OAuth 2.0 access token is required, not developer API keys.**

### A. API Call (Create Event)

```bash
curl -X POST \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <<OAuth2AccessToken>>" \
-d '{
  "eventTemplateId": "<<eventTemplateId>>",
  "email": "a.test.contact@email.com",
  "tokens": {
    "webinarName": "A Test Webinar",
    "webinarId": "001001",
    "webinarType": "regular"
  }
}' \
"https://api.hubapi.com/crm/v3/timeline/events"
```

* **`<<OAuth2AccessToken>>`**: Your OAuth 2.0 access token.
* **`email`**: The email address of the contact (or `objectId` for companies/deals).  You can also use `utk` (usertoken).
* **`tokens`**:  An object containing the token values.
* **Response**: Returns the created event.


### B. Timestamp

You can set a custom timestamp:

```bash
"timestamp": "2020-03-18T15:30:32Z"  // ISO 8601 format
```
or using milliseconds since the epoch.


### C. `extraData`

Use `extraData` to add additional, structured data to the event:

```json
"extraData": {
  "pollData": [ /* ... */ ],
  "coWorkers": [ /* ... */ ]
}
```

This data can be accessed in the `detailTemplate` using Handlebars.


## V. Stamping Event Data onto CRM Object Properties

You can map event tokens to CRM object properties using the `objectPropertyName` field when defining or updating tokens.  This automatically updates the object properties when the event is created.

## VI. Timeline Extensions (iFrame)

Add a link to an external iFrame using the `timelineIFrame` field when creating the event:

```json
"timelineIFrame": {
  "linkLabel": "View external data",
  "headerLabel": "Example iframe",
  "url": "https://www.example.com",
  "width": 800,
  "height": 300
}
```

## VII. Custom Icon

Upload a custom icon for your events through the HubSpot UI.  Specifications for the icon are detailed in the original documentation.


This comprehensive guide provides a clear understanding of the HubSpot CRM API's timeline events functionality, including API calls, examples, and best practices. Remember to replace placeholder values like `<<appId>>`, `<<developerAPIkey>>`, `<<eventTemplateId>>`, and `<<OAuth2AccessToken>>` with your actual values.
