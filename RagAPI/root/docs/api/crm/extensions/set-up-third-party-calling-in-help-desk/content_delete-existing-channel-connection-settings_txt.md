# HubSpot CRM API: Setting up Third-Party Calling in Help Desk (BETA)

This document details the API and workflow for integrating third-party calling into the HubSpot help desk.  This is a beta feature.

**Prerequisites:**

* Completion of HubSpot's SDK setup and inbound calling API steps.

**Overview:**

This integration allows users to connect phone numbers from your third-party calling application to their HubSpot help desk.  The process involves registering a webhook that HubSpot will call to retrieve a list of available phone numbers.

## Webhook Interaction

HubSpot will send a `POST` request to your registered webhook to fetch available phone numbers.

**Request:**

* **Method:** `POST`
* **Body Parameters:**
    * `appId` (Integer): ID of the requesting app.
    * `portalId` (Integer): ID of the HubSpot portal.
    * `userId` (Integer): ID of the HubSpot user making the request.
* **Headers:** HubSpot signature headers for request validation (see [HubSpot's documentation on request validation](link-to-hubspot-validation-doc-if-available)).


**Response:**

The webhook should return a JSON response with a list of available phone numbers:

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

* **`e164PhoneNumber` (String):** Phone number in E.164 format (e.g., +15551234567).
* **`extension` (String):** Phone number extension (currently not used for help desk connection).
* **`friendlyName` (String):**  User-friendly name for the phone number (truncated to 24 characters by HubSpot).


## Managing Channel Connection Settings

These endpoints manage the webhook URL and its readiness status (`isReady`).  Replace `{appId}` with your app's ID.  All endpoints are located under `/crm/v3/extensions/calling/{appId}/settings/channel-connection`.


**1. Create Channel Connection Settings:**

* **Method:** `POST`
* **Request Body:**
    * `url` (String): Your webhook URL.
    * `isReady` (Boolean): `true` to make the webhook available to users; `false` for testing.

```json
{
  "url": "https://example.com/my-help-desk-service",
  "isReady": true
}
```

**2. Fetch Existing Channel Connection Settings:**

* **Method:** `GET`

**Response (Example):**

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
* **Request Body:**  Use one or both of the following:
    * `url` (String): Updated webhook URL.
    * `isReady` (Boolean): Updated `isReady` status.

**4. Delete Existing Channel Connection Settings:**

* **Method:** `DELETE`
* **Response:** `204 No Content` on success.


## `isReady` Flag

The `isReady` flag controls whether your webhook is visible to users.

* `isReady = false`: The app appears grayed out in the user interface.  Useful for testing.
* `isReady = true`: The app is selectable by users.

**In-Browser Testing:**  For testing before setting `isReady` to `true`, you can temporarily enable the webhook in your browser's developer console:

```javascript
window.localStorage.setItem('LocalSettings:Calling:supportsChannelConnection', true);
```


## User Experience

* **`isReady = false` and local storage flag = `false`:** App is grayed out for users.
* **`isReady = true` or local storage flag = `true`:** App is selectable for users.


This documentation provides a comprehensive guide to integrating third-party calling into the HubSpot help desk using the provided API endpoints.  Remember to consult the full HubSpot documentation for additional details and error handling.
