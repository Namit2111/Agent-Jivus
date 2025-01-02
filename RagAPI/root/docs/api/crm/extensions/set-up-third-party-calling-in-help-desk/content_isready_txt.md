# HubSpot CRM API: Set up Third-Party Calling in Help Desk (BETA)

This document details the HubSpot CRM API for setting up third-party calling in the help desk.  This is a BETA feature.  Developers must have completed the SDK setup and inbound calling API steps before proceeding.

## Overview

This API allows third-party applications to integrate their phone number services into the HubSpot help desk.  HubSpot will make requests to a registered webhook to retrieve a list of available phone numbers for users to connect.

## Webhook Details

### Request

HubSpot sends a `POST` request to your registered webhook with the following parameters:

| Parameter   | Type    | Description                                      |
|-------------|---------|--------------------------------------------------|
| `appId`     | Integer | ID of the app making the request.                 |
| `portalId`  | Integer | ID of the HubSpot portal.                        |
| `userId`    | Integer | ID of the HubSpot user making the request.        |

HubSpot signature headers will be included for request validation.  See [validating requests](link-to-validation-docs-if-available) for details.

### Response Schema

The webhook must return a JSON response containing a list of available phone numbers:

```json
{
  "phoneNumbers": [
    {
      "e164PhoneNumber": "+18001231234",
      "extension": "1",  //While accepted, extensions are not currently connected to help desk.
      "friendlyName": "My cell phone number"
    }
  ]
}
```

* **`e164PhoneNumber`:** Phone number in E.164 format (e.g., +18001231234).
* **`extension`:** Phone number extension (currently not used for help desk connection).
* **`friendlyName`:**  Display name for the phone number (truncated to 24 characters by HubSpot).


## Managing Webhook Settings

The following endpoints use the `/channel-connection` path (see reference documentation for full details):

All endpoints use the following base URL pattern:  `crm/v3/extensions/calling/{appId}/settings/channel-connection`  where `{appId}` is your app's ID.

### Create Channel Connection Settings (`POST`)

Creates the webhook settings.

**Request Body:**

```json
{
  "url": "https://example.com/my-help-desk-service",
  "isReady": true
}
```

* **`url`:** The webhook URL.
* **`isReady`:** Boolean indicating whether the webhook is ready for user access (`true` or `false`).


### Fetch Existing Channel Connection Settings (`GET`)

Retrieves current webhook settings.

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

Updates existing settings.  Use the `url` and/or `isReady` parameters in the request body.


### Delete Existing Channel Connection Settings (`DELETE`)

Deletes the webhook settings.  A successful deletion returns a `204 No Content` status code.


## `isReady` Flag

The `isReady` flag controls whether the integration is visible to users.

* `isReady=true`: The integration is available to users.
* `isReady=false`: The integration is hidden from users, allowing testing.  You can temporarily enable it for testing in-browser using the following JavaScript code in your browser's developer console:

```javascript
window.localStorage.setItem('LocalSettings:Calling:supportsChannelConnection', true);
```

## User Experience

* `isReady=false` and local storage flag is `false`: The app appears greyed out.
* `isReady=true` or local storage flag is `true`: The app is selectable by users.


## Error Handling

(Add details on error codes and responses here if available in the original documentation)


This documentation provides a concise overview. Refer to the HubSpot [Calling SDK reference documentation](link-to-hubspot-docs) for complete details, including error handling and further examples.
