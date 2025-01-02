# HubSpot CRM API: Timeline Events

This document details the HubSpot CRM API for creating and managing timeline events.  Timeline events allow you to add custom information from your application to the timeline of HubSpot contacts, companies, or deals.

## I. Creating an Event Template

Before creating events, you must create an event template.  An event template defines the structure and display of your custom events.  You can create up to 750 event templates per app.

**A. API Call (POST):**

```bash
curl -X POST \
-H "Content-Type: application/json" \
-d '{
"name": "Example Webinar Registration",
"objectType": "contacts"
}' \
'https://api.hubapi.com/crm/v3/timeline/<<appId>>/event-templates?hapikey=<<developerAPIkey>>'
```

* Replace `<<appId>>` with your app ID.
* Replace `<<developerAPIkey>>` with your developer API key.
* `objectType`:  Specifies the object type (contacts, companies, deals).  Defaults to contacts.

**B. Response:**  The API returns the full event template definition, including the `id` property, which is crucial for subsequent operations.

**C. HubSpot UI:**  You can also create event templates through the HubSpot UI in your app settings under "Timeline events".


## II. Defining Event Tokens

Event tokens allow you to attach custom data to your events.  You can create up to 500 tokens per event template.  Company and deal events cannot be used in list segmentation or automation.

**A. API Call (POST):**

```bash
curl -X POST \
-H "Content-Type: application/json" \
-d '{
"name": "webinarName",
"label": "Webinar Name",
"type": "string"
}' \
'https://api.hubapi.com/crm/v3/timeline/<<appId>>/event-templates/<<eventTemplateId>>/tokens?hapikey=<<developerHapikey>>'
```

* Replace `<<eventTemplateId>>` with the ID of the event template.
* Supported token types: `string`, `number`, `enumeration`, `date` (milliseconds since epoch).
* `name`:  The internal name of the token.
* `label`: The user-friendly label.

**B. Response:** The API returns the created token.

**C. HubSpot UI:** Tokens can also be managed in the "Data" tab of the event template in the HubSpot UI.


## III. Defining Header and Detail Templates

Header and detail templates control how events are displayed on the HubSpot timeline.  Use Handlebars.js templates within Markdown.

**A. API Call (PUT):**

```bash
curl -X PUT \
-H "Content-Type: application/json" \
-d '{
"id": "<<eventTemplateId>>",
"name": "Example Name Change",
"headerTemplate": "Registered for [{{webinarName}}](https://mywebinarsystem/webinar/{{webinarId}})",
"detailTemplate": "Registration occurred at {{#formatDate timestamp}}{{/formatDate}}"
}' \
'https://api.hubapi.com/crm/v3/timeline/<<appId>>/event-templates/<<eventTemplateId>>?hapikey=<<developerHapikey>>'
```

* Use `{{tokenName}}` to reference tokens in your templates.
* `headerTemplate`: A concise, one-line summary.
* `detailTemplate`: A more detailed description.

**B. Response:** The updated event template.


## IV. Creating an Event

To create an event, you need an OAuth 2.0 access token, not a developer API key.

**A. API Call (POST):**

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
'https://api.hubapi.com/crm/v3/timeline/events'
```

* Replace `<<OAuth2AccessToken>>` with your OAuth access token.
* `eventTemplateId`: The ID of the event template.
* `email`, `objectId` (vid), or `utk`:  Identify the HubSpot object to associate the event with.  `objectId` has highest priority, then `utk`, then `email`.  Multiple identifiers can be used.
* `tokens`:  An object containing the token values.

**B. Response:** The created event.

**C. Timestamp:** You can specify a custom timestamp using the `timestamp` field (milliseconds since epoch or ISO 8601 format).

**D. `extraData`:** Add arbitrary JSON data using the `extraData` field.  This data can be accessed in the detail template.


## V. Stamping Event Data onto CRM Object Properties

You can map event tokens to HubSpot object properties. This allows you to update object properties when creating an event.

**A. API Call (PUT):**

```bash
curl -X PUT \
-H "Content-Type: application/json" \
-d '{
"label" : "Updated Webinar Name",
"objectPropertyName": "zz_webinar_name"
}' \
'https://api.hubapi.com/crm/v3/timeline/<<appId>>/event-templates/<<eventTemplateId>>/tokens/<<tokenName>>?hapikey=<<developerHapikey>>'
```

* `objectPropertyName`: The name of the HubSpot object property to map the token to.


## VI. Timeline Extensions (iFrame)

You can include an iFrame in your timeline event using the `timelineIFrame` field.

**A.  API Call (POST - included in the event creation):**

```json
{
  "eventTemplateId": "<<eventTemplateId>>",
  "email": "a.test.contact@email.com",
  "timelineIFrame": {
    "linkLabel": "View external data",
    "headerLabel": "Example iframe",
    "url": "https://www.example.com",
    "width": 800,
    "height": 300
  }
}
```

**B. Fields:**

* `linkLabel`: Text for the link to open the iFrame.
* `headerLabel`: Title of the modal containing the iFrame.
* `url`: URL of the iFrame content.
* `width`, `height`: Dimensions of the modal.



## VII. Setting up a Custom Icon

You can set a custom icon for your app's timeline events via the HubSpot UI in your app's Timeline Events settings.  The icon should be roughly square, have a transparent background, and be center-aligned.  It should also be 5MB or less and able to scale down to 30x30 pixels.


This comprehensive guide provides a clear understanding of the HubSpot CRM API for timeline events, including API calls, responses, and best practices. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
