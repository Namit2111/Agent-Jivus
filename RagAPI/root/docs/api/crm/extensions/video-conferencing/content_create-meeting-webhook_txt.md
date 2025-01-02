# HubSpot Video Conference Extension API Documentation

This document details the HubSpot Video Conference Extension API, allowing developers to integrate video conferencing capabilities into their HubSpot public apps.

## Prerequisites

* A HubSpot developer account.
* A created public app within your developer account.

## API Authentication

All requests to the Video Conferencing API require authentication using your developer API key. Include the key as a `hapikey` query parameter in the request URL (e.g., `.../{appId}?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY`).  Find your API key in your HubSpot developer account.


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
  "userVerifyUrl": "https://example.com/user-verify" //Optional
}
```

| Field             | Type    | Description                                                                                                    | Required |
|----------------------|---------|----------------------------------------------------------------------------------------------------------------|----------|
| `createMeetingUrl` | String  | URL to receive meeting creation webhook payloads. Must use `https` protocol.                                      | Yes       |
| `updateMeetingUrl` | String  | URL to receive meeting update webhook payloads. Must use `https` protocol.                                        | No        |
| `deleteMeetingUrl` | String  | URL to receive meeting deletion webhook payloads. Must use `https` protocol.                                      | No        |
| `userVerifyUrl`    | String  | URL for user identity verification.  Optional.                                                              | No        |


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

HubSpot sends HMAC-signed payloads to configured URLs.  See HubSpot's webhook security documentation for details on HMAC signing verification (note that the provided documentation does not contain specifics on this for the video conferencing extension).

### Create Meeting Webhook

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

| Field      | Type    | Description                                                              |
|-------------|---------|--------------------------------------------------------------------------|
| `portalId` | Number  | HubSpot account ID.                                                      |
| `userId`   | Number  | HubSpot user ID assigned to the meeting.                               |
| `userEmail`| String  | Email address of the assigned HubSpot user.                             |
| `topic`    | String  | Meeting title.                                                           |
| `source`   | String  | `MEETINGS` (meeting scheduling page) or `MANUAL` (manually created).       |
| `startTime`| Number  | Meeting start time in epoch milliseconds.                             |
| `endTime`  | Number  | Meeting end time in epoch milliseconds.                               |


**Required Response:**

```json
{
  "conferenceId": "some-unique-id",
  "conferenceUrl": "https://example.com/join",
  "conferenceDetails": "Click here to join: https://example.com/join"
}
```

| Field             | Type    | Description                                                                  |
|----------------------|---------|------------------------------------------------------------------------------|
| `conferenceId`     | String  | Unique ID for the conference in your system.                              |
| `conferenceUrl`    | String  | URL to join the conference.                                               |
| `conferenceDetails` | String  | Plain text invitation details (newlines are preserved).                   |


### Update Meeting Webhook

**Request Payload:**

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

(Fields are similar to the `createMeeting` webhook, including the `conferenceId` from the creation response)

**Required Response:**  `200 OK` or `204 No Content`


### Delete Meeting Webhook

**Request Payload:**

```json
{
  "conferenceId": "some-unique-id"
}
```

**Required Response:** `200 OK` or `204 No Content`


### User Verification Webhook (Optional)

**Endpoint:** (Specified in `userVerifyUrl`)

**Request Payload:**

```json
{
  "portalId": 123123,
  "userEmail": "test.user@example.com"
}
```

**Response (200 OK):**

```json
{
  "id": "any-string-id" // Your internal user ID
}
```

A `404 Not Found` response is appropriate if the user is not found.  If no `userVerifyUrl` is set, HubSpot assumes user identity is verified.


This comprehensive documentation should help you effectively integrate the HubSpot Video Conference Extension API into your application. Remember to always handle potential errors and implement appropriate error handling in your code.
