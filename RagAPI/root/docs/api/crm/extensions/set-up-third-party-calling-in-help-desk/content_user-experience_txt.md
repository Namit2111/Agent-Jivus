# HubSpot CRM API: Setting up Third-Party Calling in Help Desk (BETA)

This document describes how to integrate third-party calling into the HubSpot help desk using the CRM API.  This is a beta feature.

**Prerequisites:**

* Completion of the HubSpot SDK setup and inbound calling API steps.

**Overview:**

This integration allows users to connect their phone numbers from a third-party calling extension to their HubSpot help desk.  To achieve this, you must register a webhook with HubSpot.  When a user wants to connect a number, HubSpot will send a request to your webhook to retrieve a list of available numbers.


## Webhook Details

### Request

HubSpot sends a `POST` request to your registered webhook with the following parameters:

| Parameter  | Type    | Description                                      |
|------------|---------|--------------------------------------------------|
| `appId`    | Integer | The ID of your app.                             |
| `portalId` | Integer | The ID of the HubSpot portal.                    |
| `userId`   | Integer | The ID of the HubSpot user making the request.   |

HubSpot will include signature headers to validate the request's authenticity.  Refer to the HubSpot documentation on request validation for details.


### Response Schema

Your webhook must return a JSON response containing a list of available phone numbers:

```json
{
  "phoneNumbers": [
    {
      "e164PhoneNumber": "+18001231234",  // E.164 format required
      "extension": "1",                   // Accepted but currently not used for connection
      "friendlyName": "My cell phone number" // Max 24 characters, truncated if longer
    }
  ]
}
```

**Example:** A response for phone number +18001231234 with extension 1 and friendly name "My cell phone number".


## Managing Webhook Settings

These endpoints manage your webhook URL and availability (`isReady` flag):  `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

### Create Channel Connection Settings (`POST`)

Create the webhook settings using a `POST` request to the above endpoint with the following body:

```json
{
  "url": "https://example.com/my-help-desk-service",
  "isReady": true  // Set to `true` to make it immediately available to users
}
```

### Fetch Existing Channel Connection Settings (`GET`)

Retrieve existing settings using a `GET` request to the same endpoint.  A successful response looks like this:

```json
{
  "url": "https://example.com/my-help-desk-service",
  "createdAt": "2024-04-30 12:01",
  "updatedAt": "2024-04-30 12:01",
  "isReady": true
}
```

### Update Channel Connection Settings (`PATCH`)

Update settings using a `PATCH` request. You can update `url` and/or `isReady`.


### Delete Existing Channel Connection Settings (`DELETE`)

Delete settings using a `DELETE` request.  A successful deletion returns a `204 No Content` status code.


## `isReady` Flag

The `isReady` flag controls whether your webhook is available to users:

* `isReady: true`: The app is selectable by users when connecting a number to the help desk.
* `isReady: false`: The app is greyed out and unavailable (unless the browser's local storage flag `LocalSettings:Calling:supportsChannelConnection` is set to `true` for testing purposes).


**In-browser testing:** To test your webhook without setting `isReady` to `true`, use the following JavaScript code in your browser's developer console:

```javascript
window.localStorage.setItem('LocalSettings:Calling:supportsChannelConnection', true);
```


## User Experience

* **`isReady: false` and local storage flag `false`:** The app appears greyed out.
* **`isReady: true` or local storage flag `true`:** The app is selectable.


This documentation provides a concise overview.  Refer to the HubSpot Developer documentation for complete details and further examples.
