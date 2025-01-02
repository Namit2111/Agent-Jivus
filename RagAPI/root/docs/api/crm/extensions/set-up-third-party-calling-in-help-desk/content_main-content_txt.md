# HubSpot CRM API: Third-Party Calling in Help Desk (BETA)

This document details the HubSpot CRM API for setting up third-party calling in the help desk.  This is a beta feature.  Developers must have completed the SDK setup and inbound calling API steps before proceeding.

## Overview

This API allows third-party applications to integrate their phone number selection into the HubSpot help desk.  When a HubSpot user wants to connect a phone number, HubSpot sends a request to your registered webhook to retrieve a list of available numbers.

## Webhook Details

### Request

HubSpot sends a `POST` request to your registered webhook with the following parameters:

| Parameter  | Type    | Description                                      |
|------------|---------|--------------------------------------------------|
| `appId`    | Integer | The ID of the app.                             |
| `portalId` | Integer | The ID of the HubSpot portal.                   |
| `userId`   | Integer | The ID of the HubSpot user making the request.   |

HubSpot signature headers are included for request validation.  See the [request validation documentation](link_to_validation_docs_here - replace with actual link if available) for details.


### Response

Your webhook *must* return a JSON response with the following schema:

```json
{
  "phoneNumbers": [
    {
      "e164PhoneNumber": "+18001231234",  // E.164 format required
      "extension": "1",                    // Optional, but currently ignored
      "friendlyName": "My cell phone number" // Max 24 characters
    }
  ]
}
```

**Example Response:**

```json
{
  "phoneNumbers": [
    {
      "e164PhoneNumber": "+15551234567",
      "extension": "",
      "friendlyName": "Sales Line"
    },
    {
      "e164PhoneNumber": "+15559876543",
      "extension": null,
      "friendlyName": "Support Line"
    }
  ]
}
```

## Channel Connection Settings API Endpoints

These endpoints manage your webhook's registration and readiness status.  All endpoints use the following base URL: `/crm/v3/extensions/calling/{appId}/settings/channel-connection`  Replace `{appId}` with your application's ID.

### Create Channel Connection Settings (`POST`)

Creates the channel connection settings.

**Request Body:**

```json
{
  "url": "https://example.com/my-help-desk-service",
  "isReady": true  // Set to false for testing, then PATCH to true when ready
}
```

### Fetch Existing Channel Connection Settings (`GET`)

Retrieves the current channel connection settings.

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

Updates the channel connection settings.  You can update `url` and/or `isReady`.

**Request Body (example):**

```json
{
  "isReady": true
}
```

### Delete Existing Channel Connection Settings (`DELETE`)

Deletes the channel connection settings.  Returns a `204 No Content` status code on success.


## `isReady` Flag

The `isReady` flag determines whether your webhook is available to HubSpot users.

* `isReady: false`:  Your webhook is registered but not visible to users. Useful for testing.  You can enable it temporarily in-browser for testing using local storage:

```javascript
window.localStorage.setItem('LocalSettings:Calling:supportsChannelConnection', true);
```

* `isReady: true`: Your webhook is visible and selectable by users.

## User Experience

* **`isReady: false` and local storage flag: `false`**: The app appears greyed out for users.
* **`isReady: true` or local storage flag: `true`**: The app is selectable by users.


This documentation provides a comprehensive overview. Refer to the full HubSpot API documentation for detailed specifications and error handling.
