# HubSpot CRM API: Set up Third-Party Calling in Help Desk (BETA)

This document describes how to integrate third-party calling into the HubSpot Help Desk using the HubSpot CRM API.  This is a beta feature.

## Prerequisites

Developers must have completed the SDK setup and inbound calling API steps before proceeding.

## Overview

This integration allows users to connect their phone numbers from your third-party calling extension to their HubSpot help desk.  To achieve this, you'll register a webhook with HubSpot.  HubSpot will then make requests to this webhook to retrieve a list of available phone numbers for the user to choose from.

## Webhook Details

### Request

HubSpot sends a `POST` request to your registered webhook with the following parameters:

| Parameter   | Type    | Description                                      |
|-------------|---------|--------------------------------------------------|
| `appId`     | Integer | ID of the app making the request.                |
| `portalId`  | Integer | ID of the HubSpot portal.                        |
| `userId`    | Integer | ID of the HubSpot user making the request.       |

HubSpot will also include signature headers for request validation.  See the [request validation documentation](LINK_TO_VALIDATION_DOCS -  This needs to be added if available) for details.

### Response

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

* **`e164PhoneNumber` (String):** Phone number in E.164 format (e.g., +18001231234).
* **`extension` (String):**  While accepted, extensions are not currently connected to the help desk. Numbers with extensions will not be selectable.
* **`friendlyName` (String):**  HubSpot truncates names longer than 24 characters.


## Managing Webhook Settings

The following endpoints manage your webhook URL and `isReady` status:  `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

### Create Channel Connection Settings (`POST`)

Create webhook settings using a `POST` request to: `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

Request Body:

```json
{
  "url": "https://example.com/my-help-desk-service",
  "isReady": true
}
```

* **`url` (String):** Your webhook URL.
* **`isReady` (Boolean):**  `true` to make the webhook available to users, `false` for testing.


### Fetch Existing Channel Connection Settings (`GET`)

Retrieve existing settings with a `GET` request to: `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

Example Response:

```json
{
  "url": "https://example.com/my-help-desk-service",
  "createdAt": "2024-04-30 12:01",
  "updatedAt": "2024-04-30 12:01",
  "isReady": true
}
```

### Update Channel Connection Settings (`PATCH`)

Update settings using a `PATCH` request to: `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

You can update either or both `url` and `isReady`.

### Delete Existing Channel Connection Settings (`DELETE`)

Delete settings with a `DELETE` request to: `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

A successful deletion returns a `204 No Content` status code.

## `isReady` Flag

* `isReady=true`: The app is available for users to select when connecting a number to their help desk.
* `isReady=false`: The webhook is registered but not yet available to users.  You can test it by setting the browser's local storage flag: `LocalSettings:Calling:supportsChannelConnection=true`

## User Experience

* `isReady=false` and local storage flag is `false`: The app appears greyed out.
* `isReady=true` or local storage flag is `true`: The app is selectable.


This documentation provides a comprehensive guide for integrating third-party calling into HubSpot Help Desk. Remember to replace placeholders like `{appId}` and URLs with your actual values.  Refer to the full HubSpot API documentation for complete details and error handling.
