# HubSpot Video Conference Extension API Documentation

This document details the API for integrating a video conferencing system with HubSpot meetings.  It allows developers to add video conferencing links to meetings created within HubSpot.

## Prerequisites

* A HubSpot developer account.
* A public HubSpot app created within your developer account.

## Authentication

All requests to the video conferencing API require authentication using your developer API key.  Include the key as a `hapikey` query parameter in the request URL (e.g., `.../{appId}?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY`).  You can find your API key in your HubSpot developer account settings.


## API Endpoints

All endpoints are under the `/crm/v3/extensions/videoconferencing/settings` base path.  Replace `{appId}` with your public app's ID.

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

* **`createMeetingUrl` (Required):**  The URL HubSpot will use to notify your app when a new meeting is created.  Must use `https`.
* **`updateMeetingUrl` (Optional):** The URL HubSpot will use to notify your app when an existing meeting is updated. Must use `https`.
* **`deleteMeetingUrl` (Optional):** The URL HubSpot will use to notify your app when a meeting is deleted. Must use `https`.
* **`userVerifyUrl` (Optional):** The URL HubSpot will use to verify a user's existence in your video conferencing system.


**Example Request:**

```bash
PUT /crm/v3/extensions/videoconferencing/settings/YOUR_APP_ID?hapikey=YOUR_API_KEY
```

with the request body above.


**Response (200 OK):**

```json
{
  "createMeetingUrl": "https://example.com/create-meeting",
  "updateMeetingUrl": "https://example.com/update-meeting",
  "deleteMeetingUrl": "https://example.com/delete-meeting",
  "userVerifyUrl": "https://example.com/user-verify" //If included in request
}
```


### 2. Retrieve Webhook URLs (GET)

**Endpoint:** `/crm/v3/extensions/videoconferencing/settings/{appId}`

**Method:** `GET`

**Response (200 OK):** Returns the currently configured webhook URLs (same format as the PUT response).


### 3. Webhook Payloads

HubSpot sends payloads to the configured URLs upon meeting creation, updates, and deletions.  All webhooks are HMAC-signed using your app's secret.


#### 3.1 Create Meeting Webhook

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

**Response:**  `200 OK` or `204 No Content`


#### 3.3 Delete Meeting Webhook

**Payload:**

```json
{
  "conferenceId": "some-unique-id"
}
```

**Response:** `200 OK` or `204 No Content`


#### 3.4 User Verification Webhook

**Request (to `userVerifyUrl`)**

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

A `404 Not Found` response indicates the user doesn't exist in your system.  Other error codes are also acceptable.



## Error Handling

Appropriate HTTP status codes should be used to indicate success or failure.  Error responses should include detailed error messages.


This documentation provides a comprehensive overview of the HubSpot Video Conference Extension API.  Remember to consult the HubSpot developer documentation for the most up-to-date information and details.
