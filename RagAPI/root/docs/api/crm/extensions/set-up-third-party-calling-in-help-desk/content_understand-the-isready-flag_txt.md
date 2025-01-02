# HubSpot CRM API: Set up Third-Party Calling in Help Desk (BETA)

This document details the API and process for setting up third-party calling in the HubSpot Help Desk.  This is a beta feature.

**Prerequisites:**  Developers must have completed the SDK setup and inbound calling API steps before proceeding.

**Overview:**

This API allows third-party applications to integrate their phone number services into the HubSpot Help Desk.  When a HubSpot user wants to connect a phone number, HubSpot makes a request to your application's webhook to retrieve a list of available numbers.  The user can then select a number from this list.

## Webhook Details

HubSpot sends a `POST` request to your registered webhook to retrieve available phone numbers.

**Request:**

| Parameter   | Type    | Description                                         |
|-------------|---------|-----------------------------------------------------|
| `appId`     | Integer | The ID of the app making the request.              |
| `portalId`  | Integer | The ID of the HubSpot portal.                       |
| `userId`    | Integer | The ID of the HubSpot user making the request.      |

**Request Validation:**  The request will include HubSpot signature headers.  Refer to the HubSpot documentation on request validation for details.

**Response Schema:**

The response should be a JSON object containing an array of available phone numbers. Each phone number object should include:

| Parameter         | Type    | Description                                                                     |
|--------------------|---------|---------------------------------------------------------------------------------|
| `e164PhoneNumber` | String  | Phone number in E.164 format (e.g., +18001231234).                             |
| `extension`       | String  | Phone number extension (currently not used for connection).                      |
| `friendlyName`    | String  | User-friendly name for the phone number (truncated to 24 characters by HubSpot). |

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

## Managing Webhook Settings

These endpoints manage the webhook URL and its readiness status (`isReady`).  See the `/channel-connection` endpoints in the calling SDK reference documentation for detailed parameter information and responses.

**1. Create Channel Connection Settings:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/extensions/calling/{appId}/settings/channel-connection`
* **Request Body:**
    * `url`: (String) The webhook URL.
    * `isReady`: (Boolean) `true` to make the webhook immediately available to users; `false` for testing.

* **Example Request:**

```json
{
  "url": "https://example.com/my-help-desk-service",
  "isReady": true
}
```

**2. Fetch Existing Channel Connection Settings:**

* **Method:** `GET`
* **Endpoint:** `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

* **Example Response:**

```json
{
  "url": "https://example.com/my-help-desk-service",
  "createdAt": "2024-04-30 12:01",
  "updatedAt": "2024-04-30 12:01",
  "isReady": true
}
```

**3. Update Channel Connection Settings:**

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/extensions/calling/{appId}/settings/channel-connection`
* **Request Body:**  `url` and/or `isReady` fields.

**4. Delete Existing Channel Connection Settings:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v3/extensions/calling/{appId}/settings/channel-connection`
* **Response:** `204 No Content` on success.


## `isReady` Flag

* `isReady = true`: The app appears as selectable for users when connecting a phone number.
* `isReady = false`: The app is greyed out unless the browser's local storage flag `LocalSettings:Calling:supportsChannelConnection` is set to `true` (for testing purposes).


**Enabling testing in browser (for `isReady=false`):**

```javascript
window.localStorage.setItem('LocalSettings:Calling:supportsChannelConnection', true);
```

## User Experience

* `isReady=false` and local storage flag `false`: App appears greyed out.
* `isReady=true` or local storage flag `true`: App is selectable.


This documentation provides a concise overview. Refer to the HubSpot Calling SDK reference documentation for complete details and further examples.
