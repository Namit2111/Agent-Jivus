# HubSpot Video Conference Extension API Documentation

This document details the API for integrating a video conferencing system with HubSpot meetings.  This integration allows HubSpot users to add video conference links when scheduling meetings.

## Prerequisites

* A HubSpot developer account.
* A public HubSpot app created within your developer account.

## Authentication

All requests to the Video Conferencing API must be authenticated using your developer API key. Include the key as a `hapikey` query parameter in the request URL (e.g., `...?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY`).  Find your API key in your HubSpot developer account settings.

## API Endpoints

All endpoints are under the base URL `/crm/v3/extensions/videoconferencing/settings/{appId}` where `{appId}` is your public app's ID.

### 1. Configure Webhook URLs (PUT)

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

* **`createMeetingUrl` (Required):**  The URL HubSpot uses to notify you of new meeting creation.  Must use `https`.
* **`updateMeetingUrl` (Optional):** The URL HubSpot uses to notify you of existing meeting updates. Must use `https`.
* **`deleteMeetingUrl` (Optional):** The URL HubSpot uses to notify you of meeting deletions. Must use `https`.
* **`userVerifyUrl` (Optional):** The URL HubSpot uses to verify user existence in your video conferencing system. Must use `https`.


**Response (200 OK):**

```json
{
  "createMeetingUrl": "https://example.com/create-meeting",
  "updateMeetingUrl": "https://example.com/update-meeting",
  "deleteMeetingUrl": "https://example.com/delete-meeting",
  "userVerifyUrl": "https://example.com/user-verify" // if provided
}
```


### 2. Retrieve Webhook URLs (GET)

**Endpoint:** `/crm/v3/extensions/videoconferencing/settings/{appId}?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY`

**Method:** `GET`

**Response (200 OK):**  Returns the currently configured webhook URLs (same format as the PUT response).


### 3. Webhook Payloads and Responses

HubSpot sends HMAC-signed payloads to your configured webhook URLs.  You must handle these payloads and respond appropriately.


#### 3.1 Create Meeting Webhook

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

* **`portalId`:** HubSpot account ID.
* **`userId`:** HubSpot user ID.
* **`userEmail`:** HubSpot user email.
* **`topic`:** Meeting title.
* **`source`:**  `MEETINGS` (from scheduling page) or `MANUAL` (manually created).
* **`startTime`:** Meeting start time (epoch milliseconds).
* **`endTime`:** Meeting end time (epoch milliseconds).

**Required Response:**

```json
{
  "conferenceId": "some-unique-id",
  "conferenceUrl": "https://example.com/join",
  "conferenceDetails": "Click here to join: https://example.com/join"
}
```

* **`conferenceId`:** Unique ID for the conference.
* **`conferenceUrl`:** URL to join the conference.
* **`conferenceDetails`:** Plain text instructions for joining.


#### 3.2 Update Meeting Webhook

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

**Required Response:**  `200 OK` or `204 No Content`.


#### 3.3 Delete Meeting Webhook

**Request Payload:**

```json
{
  "conferenceId": "some-unique-id"
}
```

**Required Response:** `200 OK` or `204 No Content`.


#### 3.4 User Verification Webhook (Optional)

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
  "id": "any-string-id" // Your system's user ID
}
```

Response with any other status code indicates failure.



## Error Handling

Refer to HubSpot's API documentation for general error codes.  For webhook responses,  a non-2xx status code generally indicates failure.


This documentation provides a concise overview.  Always refer to the official HubSpot developer documentation for the most up-to-date information and details.
