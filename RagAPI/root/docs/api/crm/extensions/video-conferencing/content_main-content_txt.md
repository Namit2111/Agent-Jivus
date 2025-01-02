# HubSpot Video Conference Extension API Documentation

This document details the API for integrating video conferencing into HubSpot meetings.  This allows HubSpot users to add video conference links when creating meetings.

## Prerequisites

* A HubSpot developer account.
* A public app created within your developer account.

## Authentication

All requests to the Video Conferencing API must be authenticated using your developer API key.  Include the key as a `hapikey` query parameter in the request URL (e.g., `...?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY`).  You can find your API key in your HubSpot developer account.


## API Endpoints

All endpoints are under the base URL `/crm/v3/extensions/videoconferencing/settings/{appId}` where `{appId}` is your public app ID.


### 1. Configure Webhook URLs (PUT)

**Endpoint:** `/crm/v3/extensions/videoconferencing/settings/{appId}?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY`

**Method:** `PUT`

**Request Body:**

| Field             | Type    | Description                                                                                                 | Required |
|----------------------|---------|-------------------------------------------------------------------------------------------------------------|----------|
| `createMeetingUrl` | String  | URL HubSpot will notify when a new meeting is created.  Must use `https` protocol.                        | Yes      |
| `updateMeetingUrl` | String  | URL HubSpot will notify when an existing meeting is updated. Must use `https` protocol.                     | No       |
| `deleteMeetingUrl` | String  | URL HubSpot will notify when an existing meeting is deleted. Must use `https` protocol.                     | No       |
| `userVerifyUrl`    | String  | URL HubSpot will use to verify user existence in the external video conferencing system.                  | No       |

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

**Response (200 OK):**  Returns the currently configured webhook URLs.  See the example response in the Configure Webhook URLs section.


### 3. Webhook Payloads

HubSpot sends HMAC-signed payloads to the configured URLs for meeting create, update, and delete events.  See the security documentation for details on HMAC signing.


#### 3.1 Create Meeting Webhook

**Payload:**

| Field      | Type    | Description                                                                              |
|-------------|---------|------------------------------------------------------------------------------------------|
| `portalId`  | Number  | ID of the HubSpot account.                                                              |
| `userId`    | Number  | ID of the HubSpot user assigned to the meeting.                                        |
| `userEmail` | String  | Email address of the HubSpot user.                                                     |
| `topic`     | String  | Title of the meeting.                                                                  |
| `source`    | String  | `MEETINGS` (meeting scheduling page) or `MANUAL` (manually created from a CRM record). |
| `startTime` | Number  | Start time in epoch milliseconds.                                                      |
| `endTime`   | Number  | End time in epoch milliseconds.                                                        |

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

**Payload:**

| Field          | Type    | Description                                                                                                    |
|-----------------|---------|----------------------------------------------------------------------------------------------------------------|
| `conferenceId` | String  | Unique conference ID provided in the create meeting webhook response.                                         |
| `userId`        | Number  | ID of the HubSpot user.                                                                                       |
| `userEmail`     | String  | Email address of the HubSpot user.                                                                            |
| `portalId`      | Number  | ID of the HubSpot account.                                                                                   |
| `topic`         | String  | Title of the meeting.                                                                                      |
| `startTime`     | Number  | Start time in epoch milliseconds.                                                                            |
| `endTime`       | Number  | End time in epoch milliseconds.                                                                              |

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

**Required Response:** 200 or 204 status code.


#### 3.3 Delete Meeting Webhook

**Payload:**

```json
{
  "conferenceId": "some-unique-id"
}
```

**Required Response:** 200 or 204 status code.


#### 3.4 User Verification Webhook

**Endpoint (Optional):**  Specified in `userVerifyUrl` setting.

**Payload:**

```json
{
  "portalId": 123123,
  "userEmail": "test.user@example.com"
}
```

**Response (200 OK):**  If you return a 200 OK, return a payload with the external user ID:

```json
{
  "id": "any-string-id"
}
```


## Error Handling

Refer to the HubSpot API documentation for standard error codes and responses.  A 404 response would be appropriate for a user verification failure.
