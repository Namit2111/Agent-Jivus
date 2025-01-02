# HubSpot Video Conference Extension API Documentation

This document details the API for integrating video conferencing functionality into HubSpot meetings using a public app.  All requests require authentication using your HubSpot developer API key via the `hapikey` query parameter.

## Prerequisites

* A HubSpot developer account.
* A created public app within your developer account.

## 1. Configure Webhook URLs (PUT)

Configure the URLs where HubSpot will send notifications for meeting creation, updates, and deletions.

**API Endpoint:**

`/crm/v3/extensions/videoconferencing/settings/{appId}?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY`

**Request Method:** `PUT`

**Request Body:**

```json
{
  "createMeetingUrl": "https://example.com/create-meeting",
  "updateMeetingUrl": "https://example.com/update-meeting",
  "deleteMeetingUrl": "https://example.com/delete-meeting",
  "userVerifyUrl": "https://example.com/user-verify" // Optional
}
```

**Request Fields:**

| Field             | Type    | Description                                                                                                  | Required |
|----------------------|---------|--------------------------------------------------------------------------------------------------------------|----------|
| `createMeetingUrl` | String  | URL to receive meeting creation webhook payloads. Must use `https` protocol.                               | Yes       |
| `updateMeetingUrl` | String  | URL to receive meeting update webhook payloads. Must use `https` protocol.                                 | No        |
| `deleteMeetingUrl` | String  | URL to receive meeting deletion webhook payloads. Must use `https` protocol.                               | No        |
| `userVerifyUrl`    | String  | URL for user identity verification (optional).                                                              | No        |


**Example Response (200 OK):**

```json
{
  "createMeetingUrl": "https://example.com/create-meeting",
  "updateMeetingUrl": "https://example.com/update-meeting",
  "deleteMeetingUrl": "https://example.com/delete-meeting",
  "userVerifyUrl": "https://example.com/user-verify"
}
```

## 2. Retrieve Webhook URLs (GET)

Retrieve the currently configured webhook URLs for your app.

**API Endpoint:**

`/crm/v3/extensions/videoconferencing/settings/{appId}`

**Request Method:** `GET`

**Example Response (200 OK):**  (Same format as the PUT response above)


## 3. Webhook Payloads

HubSpot sends HMAC-signed payloads to the configured URLs upon meeting events.  See the Webhooks Security documentation for details on HMAC verification. (Note: The provided text mentions this but doesn't link to the security documentation).


## 4. Create Meeting Webhook

Triggered when a meeting is created in HubSpot.

**Request Payload:**

```json
{
  "portalId": 123123,
  "userId": 123,
  "userEmail": "test.user@example.com",
  "topic": "A Test Meeting",
  "source": "MEETINGS", // or "MANUAL"
  "startTime": 1534197600000,
  "endTime": 1534201200000
}
```

**Payload Fields:**

| Field       | Type    | Description                                                                   |
|-------------|---------|-------------------------------------------------------------------------------|
| `portalId`  | Number  | HubSpot account ID.                                                           |
| `userId`    | Number  | HubSpot user ID associated with the meeting.                                   |
| `userEmail` | String  | Email address of the HubSpot user.                                           |
| `topic`     | String  | Meeting title.                                                              |
| `source`    | String  | Meeting creation source ("MEETINGS" or "MANUAL").                           |
| `startTime` | Number  | Meeting start time in epoch milliseconds.                                    |
| `endTime`   | Number  | Meeting end time in epoch milliseconds.                                      |


**Required Response:**

```json
{
  "conferenceId": "some-unique-id",
  "conferenceUrl": "https://example.com/join",
  "conferenceDetails": "Click here to join: https://example.com/join"
}
```

**Response Fields:**

| Field             | Type    | Description                                                                            |
|----------------------|---------|----------------------------------------------------------------------------------------|
| `conferenceId`     | String  | Unique ID for the video conference (globally unique within your system).             |
| `conferenceUrl`     | String  | URL to join the video conference.                                                    |
| `conferenceDetails` | String  | Plain text invitation details (newlines are preserved).                               |


## 5. Update Meeting Webhook

Triggered when a meeting's details are updated.

**Request Payload:** (Includes `conferenceId` from the create meeting response)

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

**Required Response:**  `200 OK` or `204 No Content`


## 6. Deleted Meeting Webhook

Triggered when a meeting is deleted.

**Request Payload:**

```json
{
  "conferenceId": "some-unique-id"
}
```

**Required Response:** `200 OK` or `204 No Content`


## 7. User Verification Webhook (Optional)

Used to verify user identity before creating, updating, or deleting a video conference link.

**Request Payload:**

```json
{
  "portalId": 123123,
  "userEmail": "test.user@example.com"
}
```

**Response (200 OK):**  (If you need to map HubSpot user IDs to your system)

```json
{
  "id": "any-string-id"
}
```

**Response (Error Codes):**  Return appropriate error codes (e.g., `404 Not Found`) if the user is not found.


This comprehensive documentation provides a clear overview of the HubSpot Video Conference Extension API, enabling developers to seamlessly integrate video conferencing capabilities into their HubSpot applications.  Remember to replace placeholder URLs and API keys with your actual values.
