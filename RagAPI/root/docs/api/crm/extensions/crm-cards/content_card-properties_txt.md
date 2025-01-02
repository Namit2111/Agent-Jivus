# HubSpot CRM Cards API Documentation

This document details the HubSpot CRM Cards API, allowing developers to create custom cards displaying information from external systems within HubSpot contact, company, deal, and ticket records.

## Overview

HubSpot CRM cards enable public apps to enrich CRM records with data from external integrations.  Each app can have up to 25 CRM cards.  These cards differ from UI extensions created with developer projects; CRM cards are specifically for public apps, offering less flexibility but simpler integration.  If you're not building a public app, consider using React-based UI extensions.

**Example Use Case:**  An app integrates bug tracking software.  A CRM card displays tracked bugs directly on contact records for support representatives.

**Workflow:**  The app defines cards within its settings.  When a user views a relevant CRM record, HubSpot makes an outbound request to the app's specified URL. The app returns data, which HubSpot displays as a card.  Custom actions can be defined for user interaction (e.g., opening a modal for the app's UI).

## Scope Requirements

To create CRM cards, your app needs the appropriate OAuth scopes to read and write to the relevant CRM object. For example, a card on contact records requires `crm.objects.contacts.read` and `crm.objects.contacts.write` scopes.  Removing these scopes requires deleting all existing cards for that object type.  See the HubSpot OAuth documentation for more details.

## Creating a CRM Card

Cards can be created via the API or through the HubSpot developer account UI.

**API Approach:** (See "Endpoints" section below for details).

**UI Approach:**

1. Navigate to **Apps** in your HubSpot developer account.
2. Select your app.
3. Select **CRM cards** in the sidebar.
4. Click **Create CRM card**.

## Data Request

HubSpot makes a data fetch request to your app's specified URL when a user views a CRM record with a relevant card.  The request includes default and custom query parameters.

**Data Fetch URL:**  The URL where HubSpot fetches data (API: `targetUrl`).

**Target Record Types:** Select which CRM record types the card appears on.  Specify the HubSpot properties to include as query parameters (API: `objectTypes` array, containing `name` and `propertiesToSend` arrays).

**Example Configuration (JSON):**

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

**Example Request (GET):**

```
https://www.example.com/demo-fetch?userId=12345&userEmail=loggedinuser@hubspot.com&associatedObjectId=53701&associatedObjectType=CONTACT&portalId=987654&firstname=Tim&email=timrobinson@itysl.com&lastname=Robinson
```

**Request Parameters:**

| Parameter             | Type     | Description                                                                        |
|-----------------------|----------|------------------------------------------------------------------------------------|
| `userId`              | Default  | HubSpot user ID who loaded the CRM record.                                         |
| `userEmail`           | Default  | Email of the user who loaded the CRM record.                                      |
| `associatedObjectId`  | Default  | ID of the loaded CRM record.                                                      |
| `associatedObjectType` | Default  | Type of CRM record (e.g., `CONTACT`, `COMPANY`, `DEAL`).                           |
| `portalId`            | Default  | ID of the HubSpot account.                                                        |
| `firstname`, `email`, `lastname` | Custom   | HubSpot properties specified in `propertiesToSend`.                              |


**Request Timeout:**  Requests timeout after 5 seconds; a connection must be established within 3 seconds.

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
      "actions": [ /* ... actions ... */ ]
    },
    // ... more results ...
  ],
  "settingsAction": { /* ... settings action ... */ },
  "primaryAction": { /* ... primary action ... */ }
}
```

**Response Structure:**

* **`results` (array):**  Up to five card properties.
* **`objectId` (number):** Unique ID for the object.
* **`title` (string):** Object title.
* **`link` (string):**  URL for more details (optional; use `null` if no objects have links).
* **`created`, `priority` etc. (strings/other types):** Custom properties defined in card settings.
* **`properties` (array):** Custom properties not defined in card settings.
* **`actions` (array):** Available actions.
* **`settingsAction`, `primaryAction`, `secondaryActions` (objects):** Actions for settings, primary action and secondary actions respectively.


## Request Signatures

HubSpot includes the `X-HubSpot-Signature` header to verify requests. This header contains a base64 encoded SHA-256 hash. To verify:

1. Concatenate your app secret, HTTP method, URL, and request body.
2. Generate the SHA-256 hash of this string.
3. Compare the hash to the signature in the header.

See the HubSpot documentation on validating requests for more details.

## Card Properties

Define custom properties to display on the card.  The response must include values for these properties.  Supported data types include: `CURRENCY`, `DATE`, `DATETIME`, `EMAIL`, `LINK`, `NUMERIC`, `STATUS`, `STRING`.

**Example Custom Properties:**  See sections below for details on `CURRENCY`, `DATE`, `DATETIME`, `EMAIL`, `LINK`, `NUMERIC`, `STATUS`, and `STRING` properties.

### Currency Properties

Requires `currencyCode` (ISO 4217 code).

```json
{
  "properties": [
    {
      "label": "Resolution impact",
      "dataType": "CURRENCY",
      "value": "94.34",
      "currencyCode": "GBP"
    }
  ]
}
```

### Date Properties

Format: `yyyy-mm-dd`.

```json
{
  "properties": [
    {
      "label": "Date",
      "dataType": "DATE",
      "value": "2023-10-13"
    }
  ]
}
```

### Datetime Properties

Milliseconds since epoch.

```json
{
  "properties": [
    {
      "label": "Timestamp",
      "dataType": "DATETIME",
      "value": "1697233678777"
    }
  ]
}
```

### Email Properties

```json
{
  "properties": [
    {
      "label": "Email address",
      "dataType": "EMAIL",
      "value": "hobbes.baron@gmail.com"
    }
  ]
}
```

### Link Properties

Includes optional `linkLabel`.

```json
{
  "properties": [
    {
      "label": "Link property",
      "dataType": "LINK",
      "value": "https://www.hubspot.com",
      "linkLabel": "Test link"
    }
  ]
}
```

### Numeric Properties

```json
{
  "properties": [
    {
      "label": "Number",
      "dataType": "NUMERIC",
      "value": "123.45"
    }
  ]
}
```

### Status Properties

Requires `optionType`: `DEFAULT`, `SUCCESS`, `WARNING`, `DANGER`, `INFO`.

```json
{
  "properties": [
    {
      "label": "Status",
      "dataType": "STATUS",
      "value": "Errors occurring",
      "optionType": "DANGER"
    }
  ]
}
```

### String Properties

```json
{
  "properties": [
    {
      "label": "First name",
      "dataType": "STRING",
      "value": "Tim Robinson"
    }
  ]
}
```


## Custom Actions

Define URLs for action buttons on the card.  Action hooks and confirmation hooks include `X-HubSpot-Signature`. Iframes do not.

### Action Types

* **`IFRAME`:** Opens a modal with an iframe.  Use `window.postMessage` to close the modal: `{"action": "DONE"}` (success) or `{"action": "CANCEL"}` (cancel).

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

* **`ACTION_HOOK`:** Sends a server-side request.  `httpMethod` can be `GET`, `POST`, `PUT`, `DELETE`, or `PATCH`.

```json
{
  "type": "ACTION_HOOK",
  "httpMethod": "POST",
  "uri": "https://example.com/action-hook",
  "label": "Example action",
  "associatedObjectProperties": ["some_crm_property"]
}
```

* **`CONFIRMATION_ACTION_HOOK`:** Same as `ACTION_HOOK`, but includes a confirmation dialog.

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


## Endpoints

**(This section requires more detail from the provided text.  The original text mentions an "Endpoints" tab but doesn't provide the actual API endpoints.)**  The provided text lacks specific API endpoint details for creating and managing CRM cards.  This section should include HTTP methods, URLs, request parameters, and response structures for all API calls related to CRM card creation and management.  This information is crucial for developers to use the API effectively.
