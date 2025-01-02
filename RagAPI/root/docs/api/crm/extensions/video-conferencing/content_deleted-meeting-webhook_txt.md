# HubSpot Video Conference Extension API Documentation

This document describes the HubSpot Video Conference Extension API, allowing developers to integrate video conferencing capabilities into their HubSpot public apps.

## Prerequisites

* A HubSpot developer account.
* A created public app within your developer account.

## Authentication

All requests to the Video Conferencing API must be authenticated using your developer API key.  Include the key as a `hapikey` query parameter in the request URL (e.g., `...?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY`).

## API Endpoints

All endpoints are under the `/crm/v3/extensions/videoconferencing/settings/{appId}` base path, where `{appId}` is your public app's ID.

### 1. Configure Webhook URLs (PUT)

**Endpoint:** `/crm/v3/extensions/videoconferencing/settings/{appId}`

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

* **`createMeetingUrl` (Required):**  The URL to receive meeting creation webhook payloads (HTTPS required).
* **`updateMeetingUrl` (Optional):** The URL to receive meeting update webhook payloads (HTTPS required).
* **`deleteMeetingUrl` (Optional):** The URL to receive meeting deletion webhook payloads (HTTPS required).
* **`userVerifyUrl` (Optional):** The URL to verify user existence in your video conferencing system.


**Response (200 OK):**

```json
{
  "createMeetingUrl": "https://example.com/create-meeting",
  "updateMeetingUrl": "https://example.com/update-meeting",
  "deleteMeetingUrl": "https://example.com/delete-meeting",
  "userVerifyUrl": "https://example.com/user-verify" // May be included if provided in request
}
```


### 2. Retrieve Webhook URLs (GET)

**Endpoint:** `/crm/v3/extensions/videoconferencing/settings/{appId}`

**Method:** `GET`

**Response (200 OK):**

```json
{
  "createMeetingUrl": "https://example.com/create-meeting",
  "updateMeetingUrl": "https://example.com/update-meeting",
  "deleteMeetingUrl": "https://example.com/delete-meeting",
  "userVerifyUrl": "https://example.com/user-verify" // May not be included if not configured
}
```


## Webhook Payloads and Responses

All webhooks are HMAC signed using your app's secret (see HubSpot's webhook security documentation for details).  Responses should include appropriate HTTP status codes (200 OK or 204 No Content for create/update/delete; 200 OK or error code for user verification).

### 1. Create Meeting Webhook

**Payload:**

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

**Response:**

```json
{
  "conferenceId": "some-unique-id",
  "conferenceUrl": "https://example.com/join",
  "conferenceDetails": "Click here to join: https://example.com/join"
}
```


### 2. Update Meeting Webhook

**Payload:**

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

**Response:** 200 OK or 204 No Content


### 3. Delete Meeting Webhook

**Payload:**

```json
{
  "conferenceId": "some-unique-id"
}
```

**Response:** 200 OK or 204 No Content


### 4. User Verification Webhook

**Request Payload:**

```json
{
  "portalId": 123123,
  "userEmail": "test.user@example.com"
}
```

**Response (200 OK):**  If successful, return your system's user ID.

```json
{
  "id": "any-string-id"
}
```

**Response (Error):** Return an appropriate HTTP error code (e.g., 404 Not Found).


## Error Handling

The API may return standard HTTP status codes to indicate success or failure.  Refer to the HubSpot API documentation for detailed error codes and messages.


This documentation provides a comprehensive overview of the HubSpot Video Conference Extension API.  Remember to consult the official HubSpot developer documentation for the most up-to-date information and detailed specifications.
