# HubSpot CRM API: Set up Third-party Calling in Help Desk (BETA)

This document describes how to integrate third-party calling into the HubSpot help desk using the CRM API.  This is a beta feature.

**Prerequisites:**

* Completion of the HubSpot SDK setup and inbound calling API steps.

**Overview:**

This integration allows users to connect their phone numbers from your third-party calling extension to their HubSpot help desk.  Your extension will register a webhook with HubSpot. When a user wants to connect a number, HubSpot will send a request to this webhook to retrieve a list of available phone numbers.

## Webhook Details

### Request

HubSpot sends a `POST` request to your registered webhook with the following parameters:

| Parameter  | Type    | Description                                          |
|------------|---------|------------------------------------------------------|
| `appId`    | Integer | The ID of your app.                                  |
| `portalId` | Integer | The ID of the HubSpot portal.                        |
| `userId`   | Integer | The ID of the HubSpot user making the request.       |

The request includes HubSpot signature headers for request validation.  See [validating requests](link-to-validation-docs-if-available) for details.

### Response

Your webhook must return a JSON response containing a list of available phone numbers:

```json
{
  "phoneNumbers": [
    {
      "e164PhoneNumber": "+18001231234",
      "extension": "1",  // Extensions are currently not connected to the help desk.
      "friendlyName": "My cell phone number"
    }
  ]
}
```

* **`e164PhoneNumber`**: Phone number in E.164 format (e.g., +18001231234).
* **`extension`**:  While accepted, extensions are not currently used for help desk connections.
* **`friendlyName`**:  Limited to 24 characters; longer names will be truncated.


## Managing Webhook Settings (/channel-connection Endpoints)

These endpoints manage your webhook's URL and `isReady` status.  See the `/channel-connection` endpoints in the [calling SDK reference documentation](link-to-calling-sdk-reference) for details on parameters and responses.

### Create Channel Connection Settings

Use a `POST` request to:  `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

Request Body:

```json
{
  "url": "https://example.com/my-help-desk-service",
  "isReady": true // Set to true to make the webhook available to users.
}
```

### Fetch Existing Channel Connection Settings

Use a `GET` request to: `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

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

Use a `PATCH` request to: `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

Request Body (update `url` and/or `isReady` as needed):

```json
{
  "url": "https://updated.example.com/my-help-desk-service",
  "isReady": false
}
```

### Delete Existing Channel Connection Settings

Use a `DELETE` request to: `/crm/v3/extensions/calling/{appId}/settings/channel-connection`

A successful deletion returns a `204 No Content` status code.


## `isReady` Flag

* `isReady=true`: Your app's phone number connection will be available to users.
* `isReady=false`: Your app will appear greyed out to users.  Useful for testing.

**In-browser testing:**  To test your webhook before setting `isReady=true`, you can override the `isReady` flag using local storage:

```javascript
window.localStorage.setItem('LocalSettings:Calling:supportsChannelConnection', true);
```


## User Experience

* **`isReady=false` and local storage flag is `false`**: App is greyed out.
* **`isReady=true` or local storage flag is `true`**: App is selectable.


**(Remember to replace placeholders like  `link-to-validation-docs-if-available` and `link-to-calling-sdk-reference` with actual links.)**
