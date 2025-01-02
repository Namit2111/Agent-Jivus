# HubSpot CRM API: Set up Third-Party Calling in Help Desk (BETA)

This document details the API and workflow for setting up third-party calling in the HubSpot Help Desk.  This is a beta feature.

**Prerequisites:**  Developers must have completed the SDK setup and inbound calling API steps before proceeding.

**Overview:**

This API allows third-party calling applications to integrate with the HubSpot Help Desk, providing users with a selection of phone numbers managed by the third-party app.  The integration uses webhooks to fetch available phone numbers.

## Webhook Details

HubSpot will send a `POST` request to your registered webhook to retrieve a list of available phone numbers for a user.

### Request

**Method:** `POST`

**Request Body:**

| Parameter    | Type    | Description                                       |
|--------------|---------|---------------------------------------------------|
| `appId`      | Integer | ID of the app making the request.                 |
| `portalId`   | Integer | ID of the HubSpot portal.                        |
| `userId`     | Integer | ID of the HubSpot user making the request.       |

**Headers:** HubSpot signature headers will be included for request validation.  See [validation instructions](link_to_validation_instructions_if_available) for details.


### Response Schema

Your webhook should return a JSON response with a list of available phone numbers:

**Example Response:**

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

**Response Parameters:**

| Parameter         | Type    | Description                                                              |
|----------------------|---------|--------------------------------------------------------------------------|
| `e164PhoneNumber` | String  | Phone number in E.164 format (e.g., +18001231234).                     |
| `extension`        | String  | Phone number extension (currently not used for help desk connections). |
| `friendlyName`     | String  | User-friendly name for the phone number (truncated to 24 characters).    |


## Managing Webhook Settings

These endpoints manage the webhook URL and its availability (`isReady` flag).  See `/channel-connection` endpoints in the calling SDK reference documentation for full details.


### Create Channel Connection Settings

**Method:** `POST`

**Endpoint:** `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

**Request Body:**

| Parameter | Type    | Description                                                                  |
|-----------|---------|------------------------------------------------------------------------------|
| `url`     | String  | Webhook URL.                                                              |
| `isReady` | Boolean | `true` to make the webhook available to users; `false` for testing.          |

**Example Request:**

```json
{
  "url": "https://example.com/my-help-desk-service",
  "isReady": true
}
```


### Fetch Existing Channel Connection Settings

**Method:** `GET`

**Endpoint:** `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

**Example Response:**

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

**Endpoint:** `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

**Request Body:** (One or both of the following)

| Parameter | Type    | Description                                                                  |
|-----------|---------|------------------------------------------------------------------------------|
| `url`     | String  | Updated webhook URL.                                                        |
| `isReady` | Boolean | Updated `isReady` status.                                                   |


### Delete Existing Channel Connection Settings

**Method:** `DELETE`

**Endpoint:** `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

**Response:** 204 No Content (on success)


## `isReady` Flag

The `isReady` flag determines if the webhook is available to users.  `isReady=false` allows testing without immediate user access.  In-browser testing can be enabled by setting the local storage flag: `LocalSettings:Calling:supportsChannelConnection=true`.


## User Experience

* `isReady=false` and local storage flag is `false`: App appears greyed out for users.
* `isReady=true` or local storage flag is `true`: Users can select the app.


This documentation provides a concise overview. Refer to the HubSpot Calling SDK reference documentation for detailed parameter descriptions and comprehensive examples.
