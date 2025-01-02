# HubSpot CRM API: Setting up Third-Party Calling in Help Desk (BETA)

This document details the API and process for integrating third-party calling into the HubSpot Help Desk.  This is a beta feature.

**Prerequisites:**  Developers must have completed the SDK setup and inbound calling API steps before proceeding.

**Overview:**

This integration allows users to connect phone numbers from your third-party calling application to their HubSpot Help Desk.  This is achieved by registering a webhook with HubSpot.  HubSpot will then make requests to this webhook to retrieve a list of available phone numbers for the user to choose from.

## Webhook Details

**Request:**

HubSpot sends a `POST` request to your registered webhook containing the following parameters:

| Parameter | Type    | Description                                                              |
|-----------|---------|--------------------------------------------------------------------------|
| `appId`   | Integer | The ID of your app.                                                      |
| `portalId`| Integer | The ID of the HubSpot portal making the request.                         |
| `userId`  | Integer | The ID of the HubSpot user making the request.                           |

HubSpot signature headers will also be included for request validation.  Refer to HubSpot's documentation on request validation for details.


**Response:**

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

* **`e164PhoneNumber` (String):** The phone number in E.164 format (e.g., +18001231234).
* **`extension` (String):**  While accepted, extensions are not currently supported for Help Desk connections.  Numbers with extensions will not be selectable by the user.
* **`friendlyName` (String):**  A user-friendly name for the number (maximum 24 characters; longer names will be truncated).


## Managing Webhook Settings

These endpoints use the `/crm/v3/extensions/calling/{appId}/settings/channel-connection` path, replacing `{appId}` with your app's ID.

**1. Create Channel Connection Settings:**

* **Method:** `POST`
* **Request Body:**
  ```json
  {
    "url": "https://example.com/my-help-desk-service",
    "isReady": true
  }
  ```
  * `url` (String):  The URL of your webhook.
  * `isReady` (Boolean):  Indicates whether the webhook is ready for use. `true` makes the integration available to users; `false` allows testing without immediate user access.

**2. Fetch Existing Channel Connection Settings:**

* **Method:** `GET`
* **Response (Example):**
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
* **Request Body:**  Use this to update either the `url` or `isReady` fields.

**4. Delete Existing Channel Connection Settings:**

* **Method:** `DELETE`
* **Response:** A `204 No Content` status code indicates successful deletion.


## `isReady` Flag

The `isReady` flag controls whether your integration is visible to HubSpot users.

* `isReady: true`:  The integration is available to users.
* `isReady: false`: The integration is not available to users (but can be tested using the browser's local storage override described below).

**In-Browser Testing (isReady=false):** To test your webhook while `isReady` is false, use the following JavaScript command in your browser's developer console:

```javascript
window.localStorage.setItem('LocalSettings:Calling:supportsChannelConnection', true);
```

## User Experience

* **`isReady: false` and local storage flag: false:** The app will appear greyed out for users.
* **`isReady: true` or local storage flag: true:** Users can select the app when connecting a number.


This documentation provides a comprehensive overview of integrating third-party calling into the HubSpot Help Desk using their API.  Remember to consult HubSpot's official API documentation for the most up-to-date information and details.
