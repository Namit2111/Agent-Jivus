# HubSpot CRM API: Setting up Third-Party Calling in Help Desk (BETA)

This document details the HubSpot CRM API for setting up third-party calling in the help desk.  This is a beta feature.  Developers must have completed the SDK setup and inbound calling API steps before proceeding.

## Overview

This API allows third-party applications to integrate their phone number provisioning into the HubSpot help desk.  When a HubSpot user wants to connect a phone number, HubSpot sends a request to your registered webhook to retrieve a list of available numbers.

## Webhook Details

### Request

HubSpot sends a `POST` request to your registered webhook with the following parameters:

| Parameter   | Type    | Description                                      |
|-------------|---------|--------------------------------------------------|
| `appId`     | Integer | The ID of the app making the request.            |
| `portalId`  | Integer | The ID of the HubSpot portal.                    |
| `userId`    | Integer | The ID of the HubSpot user making the request.   |

The request includes HubSpot signature headers for request validation.  See [validating requests](link-to-validation-docs-if-available) for details.


### Response Schema

Your webhook must return a JSON response containing a list of available phone numbers:

```json
{
  "phoneNumbers": [
    {
      "e164PhoneNumber": "+18001231234",
      "extension": "1",  //Extensions are currently not connected to the helpdesk.
      "friendlyName": "My cell phone number"
    }
  ]
}
```

* **`e164PhoneNumber`**: Phone number in E.164 format (e.g., +18001231234).
* **`extension`**:  (Optional) Phone number extension.  Currently not used for help desk connection.
* **`friendlyName`**:  (Max 24 characters) User-friendly name for the phone number.  Longer names will be truncated.


## Managing Channel Connection Settings

These endpoints manage your webhook's registration and readiness status.  See `/channel-connection` endpoints in the calling SDK reference documentation for full details.


### Create Channel Connection Settings

`POST /crm/v3/extensions/calling/{appId}/settings/channel-connection`

Request Body:

```json
{
  "url": "https://example.com/my-help-desk-service",
  "isReady": true
}
```

* **`url`**: Your webhook URL.
* **`isReady`**: `true` to make the webhook available to users, `false` for testing.


### Fetch Existing Channel Connection Settings

`GET /crm/v3/extensions/calling/{appId}/settings/channel-connection`

Response (example):

```json
{
  "url": "https://example.com/my-help-desk-service",
  "createdAt": "2024-04-30 12:01",
  "updatedAt": "2024-04-30 12:01",
  "isReady": true
}
```


### Update Channel Connection Settings

`PATCH /crm/v3/extensions/calling/{appId}/settings/channel-connection`

Request Body (can include either or both):

```json
{
  "url": "https://new-url.com/updated-service",
  "isReady": false
}
```


### Delete Existing Channel Connection Settings

`DELETE /crm/v3/extensions/calling/{appId}/settings/channel-connection`

A successful deletion returns a `204 No Content` status code.


## `isReady` Flag

The `isReady` flag controls whether your webhook is available to users.

* `isReady: true`:  Your webhook is enabled and visible to users.
* `isReady: false`: Your webhook is registered but hidden from users; useful for testing.

You can temporarily override `isReady` for in-browser testing by setting the local storage flag:

```javascript
window.localStorage.setItem('LocalSettings:Calling:supportsChannelConnection', true);
```

## User Experience

* `isReady: false` and local storage flag is `false`: The app is greyed out for users.
* `isReady: true` or local storage flag is `true`: The app is selectable for users.


This documentation provides a concise overview. Refer to the full HubSpot API documentation for comprehensive details, including error handling and rate limits.
