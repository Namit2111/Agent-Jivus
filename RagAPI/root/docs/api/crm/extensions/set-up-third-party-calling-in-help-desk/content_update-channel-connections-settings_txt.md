# HubSpot CRM API: Set up Third-party Calling in Help Desk (BETA)

This document details the API integration for setting up third-party calling in the HubSpot Help Desk.  This is a beta feature.  Developers must have completed the SDK setup and inbound calling API steps before proceeding.

## Overview

This integration allows third-party calling applications to provide phone numbers to HubSpot users for connection to their help desk.  It involves registering a webhook that HubSpot will call to retrieve a list of available phone numbers.

## Webhook Details

### Request

HubSpot sends a `POST` request to your registered webhook with the following parameters:

| Parameter | Type    | Description                                                              |
|-----------|---------|--------------------------------------------------------------------------|
| `appId`   | Integer | The ID of the app making the request.                                     |
| `portalId`| Integer | The ID of the HubSpot portal.                                           |
| `userId`  | Integer | The ID of the HubSpot user making the request.                            |

The request includes HubSpot signature headers for request validation.  See [Validating Requests](link-to-validation-doc-if-available) for details.

### Response Schema

Your webhook should return a JSON response containing a list of available phone numbers:

```json
{
  "phoneNumbers": [
    {
      "e164PhoneNumber": "+18001231234",
      "extension": "1",
      "friendlyName": "My cell phone number"
    }
  ]
}
```

* **`e164PhoneNumber`**:  The phone number in E.164 format (e.g., +18001231234).
* **`extension`**: The phone number extension (currently not used for help desk connection).
* **`friendlyName`**: A user-friendly name for the phone number (maximum 24 characters).


## Managing Webhook Settings

These endpoints use the `/crm/v3/extensions/calling/{appId}/settings/channel-connection` path, replacing `{appId}` with your app's ID.

### Create Channel Connection Settings (`POST`)

Creates the webhook settings.

**Request Body:**

```json
{
  "url": "https://example.com/my-help-desk-service",
  "isReady": true
}
```

* **`url`**: The webhook URL.
* **`isReady`**:  A boolean indicating whether the webhook is ready for user access (`true`) or not (`false`).


### Fetch Existing Channel Connection Settings (`GET`)

Retrieves the current webhook settings.

**Example Response:**

```json
{
  "url": "https://example.com/my-help-desk-service",
  "createdAt": "2024-04-30 12:01",
  "updatedAt": "2024-04-30 12:01",
  "isReady": true
}
```


### Update Channel Connection Settings (`PATCH`)

Updates existing webhook settings.  You can update `url` and/or `isReady`.

### Delete Existing Channel Connection Settings (`DELETE`)

Deletes the webhook settings.  A successful deletion returns a `204 No Content` status code.


## `isReady` Flag

The `isReady` flag controls whether your webhook is available to users.

* `isReady: true`: The app will be selectable by users.
* `isReady: false`: The app will be greyed out (unless overridden in the browser using local storage).

For testing purposes, you can temporarily enable the webhook in the browser using this local storage setting:

```javascript
window.localStorage.setItem('LocalSettings:Calling:supportsChannelConnection', true);
```

## User Experience

* **`isReady: false` and local storage flag: false:** The app appears greyed out.
* **`isReady: true` or local storage flag: true:** The app is selectable.


## API Reference

A more comprehensive API reference with detailed parameter descriptions and error handling is available at [link-to-api-reference-if-available].
