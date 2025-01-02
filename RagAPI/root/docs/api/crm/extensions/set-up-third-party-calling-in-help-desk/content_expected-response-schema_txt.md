# HubSpot CRM API: Third-Party Calling in Help Desk (BETA)

This document details the HubSpot CRM API for setting up third-party calling in the help desk.  This is a beta feature.

**Prerequisites:** Developers must have completed the SDK setup and inbound calling API steps before proceeding.

**Overview:** This API allows third-party calling applications to integrate with the HubSpot help desk, providing users with a selection of phone numbers managed by the third-party app.  This is achieved through webhooks that provide HubSpot with a list of available phone numbers.

## Webhook Integration

HubSpot uses a webhook to fetch available phone numbers from your application.

### Webhook Request

HubSpot sends a `POST` request to your registered webhook with the following parameters:

| Parameter   | Type    | Description                                         |
|-------------|---------|-----------------------------------------------------|
| `appId`     | Integer | ID of the app making the request.                   |
| `portalId`  | Integer | ID of the HubSpot portal.                           |
| `userId`    | Integer | ID of the HubSpot user making the request.          |

HubSpot includes signature headers for request validation.  See [Validate Requests](link_to_validation_doc_if_available) for details.


### Webhook Response

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

* **`e164PhoneNumber`**: Phone number in E.164 format (e.g., +18001231234).
* **`extension`**:  Phone number extension (currently not used for connection).
* **`friendlyName`**:  Descriptive name (HubSpot truncates to 24 characters).


## Managing Webhook Settings

These endpoints manage the webhook URL and its availability (`isReady` flag).  See `/channel-connection` endpoints in the calling SDK reference documentation for detailed parameter information.


### Create Channel Connection Settings

`POST` request to: `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

Request Body:

```json
{
  "url": "https://example.com/my-help-desk-service",
  "isReady": true
}
```

* **`url`**: Your webhook URL.
* **`isReady`**:  `true` to make the webhook available to users; `false` for testing.


### Fetch Existing Channel Connection Settings

`GET` request to: `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

Example Response:

```json
{
  "url": "https://example.com/my-help-desk-service",
  "createdAt": "2024-04-30 12:01",
  "updatedAt": "2024-04-30 12:01",
  "isReady": true
}
```


### Update Channel Connection Settings

`PATCH` request to: `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

Request Body (can include `url` and/or `isReady`):

```json
{
  "isReady": false 
}
```


### Delete Existing Channel Connection Settings

`DELETE` request to: `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

Response: `204 No Content` on success.


## `isReady` Flag

* `isReady=true`: The app appears as selectable for users connecting a number to their help desk.
* `isReady=false`: The app is greyed out unless the browser's local storage flag `LocalSettings:Calling:supportsChannelConnection` is set to `true` (for testing).

To enable testing in the browser console:

```javascript
window.localStorage.setItem('LocalSettings:Calling:supportsChannelConnection', true);
```


## User Experience

* `isReady=false` and local storage flag is `false`: App appears greyed out.
* `isReady=true` or local storage flag is `true`: App is selectable.


This documentation provides a concise overview. Refer to the full HubSpot Calling SDK reference documentation for detailed API specifications and error handling.
