# HubSpot Video Conference Extension API Documentation

This document describes the API for integrating a video conferencing service with HubSpot meetings.  It allows developers to add video conference links to HubSpot meetings, similar to existing integrations like Google Meet and Zoom.

## Prerequisites

* A HubSpot developer account.
* A public HubSpot app created within your developer account.

## API Authentication

All requests to the video conferencing API require authentication using your developer API key. Include the key as a `hapikey` query parameter in the request URL (e.g., `...?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY`).  Find your API key in your HubSpot developer account settings.

## Webhook Configuration

To receive notifications about meeting creation, updates, and deletions, configure webhook URLs using the following endpoints:

### 1. Configure Webhook URLs (PUT Request)

**Endpoint:** `/crm/v3/extensions/videoconferencing/settings/{appId}?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY`

**Method:** `PUT`

**Request Body:**

```json
{
  "createMeetingUrl": "https://example.com/create-meeting",
  "updateMeetingUrl": "https://example.com/update-meeting",
  "deleteMeetingUrl": "https://example.com/delete-meeting",
  "userVerifyUrl": "https://example.com/user-verify" // Optional
}
```

**Fields:**

| Field             | Type    | Description                                                                                                  | Required |
|----------------------|---------|--------------------------------------------------------------------------------------------------------------|----------|
| `createMeetingUrl` | String  | URL to receive meeting creation webhook payloads. Must use `https` protocol.                               | Yes      |
| `updateMeetingUrl` | String  | URL to receive meeting update webhook payloads. Must use `https` protocol.                                 | No       |
| `deleteMeetingUrl` | String  | URL to receive meeting deletion webhook payloads. Must use `https` protocol.                               | No       |
| `userVerifyUrl`    | String  | URL for user identity verification.  (Optional, see User Verification Webhook section)                      | No       |


**Example Response (200 OK):**

```json
{
  "createMeetingUrl": "https://example.com/create-meeting",
  "updateMeetingUrl": "https://example.com/update-meeting",
  "deleteMeetingUrl": "https://example.com/delete-meeting",
  "userVerifyUrl": "https://example.com/user-verify"
}
```


### 2. Retrieve Webhook URLs (GET Request)

**Endpoint:** `/crm/v3/extensions/videoconferencing/settings/{appId}`

**Method:** `GET`

**Example Response (200 OK):**  (Same format as the PUT response above)


## Webhook Payloads

HubSpot sends HMAC-signed payloads to the configured URLs.  (See HubSpot's webhook security documentation for details on HMAC signing).

### Create Meeting Webhook

**Triggered when:** A new meeting is created in HubSpot.

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

**Fields:** (Refer to the detailed descriptions in the original text.)


**Required Response:**  Your application must respond with a JSON payload containing:

```json
{
  "conferenceId": "some-unique-id",
  "conferenceUrl": "https://example.com/join",
  "conferenceDetails": "Click here to join: https://example.com/join"
}
```


### Update Meeting Webhook

**Triggered when:**  A meeting's details (topic, start/end times) are updated.

**Request Payload:** Includes `conferenceId` (from the create meeting response), `userId`, `userEmail`, `portalId`, `topic`, `startTime`, and `endTime`.

**Required Response:**  A `200 OK` or `204 No Content` status code.


### Delete Meeting Webhook

**Triggered when:** A meeting is deleted.

**Request Payload:**

```json
{
  "conferenceId": "some-unique-id"
}
```

**Required Response:** A `200 OK` or `204 No Content` status code.


### User Verification Webhook (Optional)

**Triggered when:**  Before creating, updating, or deleting a meeting, HubSpot checks if a `userVerifyUrl` is set. If so, it calls this URL to verify the user's identity.

**Request Payload:**

```json
{
  "portalId": 123123,
  "userEmail": "test.user@example.com"
}
```

**Response (200 OK):**  Return the external user ID (if different from the email address).

```json
{
  "id": "any-string-id"
}
```

A `404 Not Found` response is acceptable if the user is not found.


This comprehensive documentation provides a clear understanding of how to integrate a video conferencing system with HubSpot meetings using their provided API.  Remember to replace placeholder URLs and IDs with your actual values.
