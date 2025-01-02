# HubSpot CRM API: Setting up Third-Party Calling in Help Desk (BETA)

This document details the HubSpot CRM API for setting up third-party calling within the help desk.  This is a beta feature.  Developers must have completed the SDK setup and inbound calling API steps before proceeding.

## Overview

This API allows third-party applications to integrate their phone number provisioning into the HubSpot help desk.  When a HubSpot user wants to connect a phone number, HubSpot sends a request to your registered webhook to retrieve a list of available numbers.

## Webhook Details

### Request

HubSpot sends a `POST` request to your registered webhook with the following parameters:

| Parameter   | Type    | Description                                         |
|-------------|---------|-----------------------------------------------------|
| `appId`     | Integer | ID of the app making the request.                 |
| `portalId`  | Integer | ID of the HubSpot portal.                          |
| `userId`    | Integer | ID of the HubSpot user making the request.           |

HubSpot signature headers are included for request validation.  See [Validating Requests](LINK_TO_VALIDATION_DOCUMENTATION -  replace with actual link if available) for details.

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

* **`e164PhoneNumber` (String):** Phone number in E.164 format (e.g., +18001231234).
* **`extension` (String):** Phone number extension (currently not used for help desk connection).
* **`friendlyName` (String):**  User-friendly name for the phone number (truncated to 24 characters by HubSpot).


## Managing Webhook Settings

These endpoints use the `/crm/v3/extensions/calling/{appId}/settings/channel-connection` path, replacing `{appId}` with your app's ID.


### Create Channel Connection Settings

**Method:** `POST`

**Request Body:**

```json
{
  "url": "https://example.com/my-help-desk-service",
  "isReady": true
}
```

* **`url` (String):** Your webhook URL.
* **`isReady` (Boolean):**  Indicates whether the webhook is ready for user access (`true`) or not (`false`).


### Fetch Existing Channel Connection Settings

**Method:** `GET`

**Response (example):**

```json
{
  "url": "https://example.com/my-help-desk-service",
  "createdAt": "2024-04-30 12:01",
  "updatedAt": "2024-04-30 12:01",
  "isReady": true
}
```


### Update Channel Connection Settings

**Method:** `PATCH`

**Request Body:**  Use one or both of the following:

* **`url` (String):** Updated webhook URL.
* **`isReady` (Boolean):** Updated `isReady` status.


### Delete Existing Channel Connection Settings

**Method:** `DELETE`

A successful deletion returns a `204 No Content` status code.


## `isReady` Flag

The `isReady` flag controls whether your webhook is available to HubSpot users.

* `isReady=true`:  Your webhook is accessible to users.
* `isReady=false`: Your webhook is registered but not yet accessible to users.  You can test it using the in-browser override:

```javascript
window.localStorage.setItem('LocalSettings:Calling:supportsChannelConnection', true);
```

This command should be run in your browser's developer console.


## User Experience

* **`isReady=false` and local storage flag `false`:** The app appears grayed out for users.
* **`isReady=true` or local storage flag `true`:** Users can select the app.


## Error Handling

(Add details on error responses and their codes here.  This section is missing from the provided text)


This documentation provides a comprehensive overview.  Refer to the [HubSpot Calling SDK reference documentation](LINK_TO_SDK_DOCS - replace with actual link if available) for additional details and examples.
