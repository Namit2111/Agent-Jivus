# HubSpot Video Conference Extension API Documentation

This document details the HubSpot Video Conference Extension API, allowing developers to integrate video conferencing capabilities into their HubSpot public apps.

## Prerequisites

* A HubSpot developer account.
* A HubSpot public app.

## Authentication

All requests to the Video Conferencing API require authentication using your developer API key. Include the key as a `hapikey` query parameter in the request URL (e.g., `...?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY`).  Find your API key in your HubSpot developer account settings.


## API Endpoints

All endpoints are under the base URL `/crm/v3/extensions/videoconferencing/settings/{appId}` where `{appId}` is your public app ID.

### 1. Configure Webhook URLs (PUT)

**Endpoint:** `/crm/v3/extensions/videoconferencing/settings/{appId}?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY`

**Method:** `PUT`

**Request Body:**

| Field             | Type    | Description                                                                                                 | Required |
|----------------------|---------|-------------------------------------------------------------------------------------------------------------|----------|
| `createMeetingUrl` | String  | URL to receive meeting creation webhook payloads. Must use `https` protocol.                               | Yes       |
| `updateMeetingUrl` | String  | URL to receive meeting update webhook payloads. Must use `https` protocol.                                 | No        |
| `deleteMeetingUrl` | String  | URL to receive meeting deletion webhook payloads. Must use `https` protocol.                               | No        |
| `userVerifyUrl`    | String  | URL for user identity verification (optional).                                                             | No        |

**Example Request:**

```json
{
  "createMeetingUrl": "https://example.com/create-meeting",
  "updateMeetingUrl": "https://example.com/update-meeting",
  "deleteMeetingUrl": "https://example.com/delete-meeting"
}
```

**Example Response (200 OK):**

```json
{
  "createMeetingUrl": "https://example.com/create-meeting",
  "updateMeetingUrl": "https://example.com/update-meeting",
  "deleteMeetingUrl": "https://example.com/delete-meeting"
}
```


### 2. Retrieve Webhook URLs (GET)

**Endpoint:** `/crm/v3/extensions/videoconferencing/settings/{appId}?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY`

**Method:** `GET`

**Example Response (200 OK):**

```json
{
  "createMeetingUrl": "https://example.com/create-meeting",
  "updateMeetingUrl": "https://example.com/update-meeting",
  "deleteMeetingUrl": "https://example.com/delete-meeting",
  "userVerifyUrl": "https://example.com/user-verify"
}
```

### 3. Webhook Payloads

HubSpot sends HMAC-signed payloads to the configured URLs for meeting creation, updates, and deletions.  See the Webhooks Security documentation for details on HMAC signing (note that the rest of that page does not apply to these webhooks).


#### 3.1 Create Meeting Webhook

**Request Payload:**

| Field      | Type    | Description                                                                         |
|-------------|---------|-------------------------------------------------------------------------------------|
| `portalId` | Number  | HubSpot account ID.                                                                  |
| `userId`    | Number  | HubSpot user ID assigned to the meeting.                                             |
| `userEmail` | String  | Email address of the HubSpot user.                                                  |
| `topic`     | String  | Meeting title.                                                                     |
| `source`    | String  | `MEETINGS` (meeting scheduling page) or `MANUAL` (manually created from CRM record). |
| `startTime` | Number  | Meeting start time in epoch milliseconds.                                          |
| `endTime`   | Number  | Meeting end time in epoch milliseconds.                                            |

**Example Payload:**

```json
{
  "portalId": 123123,
  "userId": 123,
  "userEmail": "test.user@example.com",
  "topic": "A Test Meeting",
  "source": "MEETINGS",
  "startTime": 1534197600000,
  "endTime": 1534201200000
}
```

**Required Response:**

```json
{
  "conferenceId": "some-unique-id",
  "conferenceUrl": "https://example.com/join",
  "conferenceDetails": "Click here to join: https://example.com/join"
}
```


#### 3.2 Update Meeting Webhook

**Request Payload:**

| Field          | Type    | Description                                                                                             |
|-----------------|---------|---------------------------------------------------------------------------------------------------------|
| `conferenceId` | String  | Unique conference ID (provided in the create meeting webhook response).                               |
| `userId`        | Number  | HubSpot user ID.                                                                                     |
| `userEmail`     | String  | HubSpot user email address.                                                                          |
| `portalId`      | Number  | HubSpot account ID.                                                                                  |
| `topic`         | String  | Meeting title.                                                                                     |
| `startTime`     | Number  | Meeting start time in epoch milliseconds.                                                          |
| `endTime`       | Number  | Meeting end time in epoch milliseconds.                                                            |

**Example Payload:**

```json
{
  "conferenceId": "some-unique-id",
  "userId": 123,
  "userEmail": "test.user@example.com",
  "portalId": 123123,
  "topic": "A Test Meeting (updated)",
  "startTime": 1534197600000,
  "endTime": 1534201200000
}
```

**Required Response:** 200 OK or 204 No Content


#### 3.3 Delete Meeting Webhook

**Request Payload:**

```json
{
  "conferenceId": "some-unique-id"
}
```

**Required Response:** 200 OK or 204 No Content


#### 3.4 User Verification Webhook (Optional)

**Endpoint:**  Specified in `userVerifyUrl` setting.

**Request Payload:**

```json
{
  "portalId": 123123,
  "userEmail": "test.user@example.com"
}
```

**Response (200 OK):**  If successful, return your internal user ID:

```json
{
  "id": "any-string-id"
}
```

A 404 response indicates the user doesn't exist in your system.  Other error codes are also acceptable.

This concludes the documentation for the HubSpot Video Conference Extension API. Remember to consult the HubSpot developer documentation for further assistance and updates.
