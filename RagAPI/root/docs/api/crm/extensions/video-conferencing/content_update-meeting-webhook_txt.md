# HubSpot Video Conference Extension API Documentation

This document details the HubSpot Video Conference Extension API, allowing developers to integrate video conferencing capabilities into HubSpot meetings.  The API uses webhooks for notifications and requires authentication with a HubSpot developer API key.

## Prerequisites

* A HubSpot developer account.
* A public HubSpot app created within your developer account.

## API Authentication

All requests must include your developer API key as a `hapikey` query parameter in the URL (e.g., `.../{appId}?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY`).  You can find your API key in your HubSpot developer account settings.


## Webhook Configuration

Use the following endpoints to manage webhook URLs for your app:

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

* **`createMeetingUrl` (Required):**  The URL to receive meeting creation notifications.  Must use `https`.
* **`updateMeetingUrl` (Optional):** The URL to receive meeting update notifications. Must use `https`.
* **`deleteMeetingUrl` (Optional):** The URL to receive meeting deletion notifications. Must use `https`.
* **`userVerifyUrl` (Optional):** The URL for user identity verification. Must use `https`.


**Example Request:**

```bash
PUT /crm/v3/extensions/videoconferencing/settings/YOUR_APP_ID?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY
```

**Example Response (200 OK):**

```json
{
  "createMeetingUrl": "https://example.com/create-meeting",
  "updateMeetingUrl": "https://example.com/update-meeting",
  "deleteMeetingUrl": "https://example.com/delete-meeting",
  "userVerifyUrl": "https://example.com/user-verify"
}
```


### 2. Retrieve Webhook URLs (GET)

**Endpoint:** `/crm/v3/extensions/videoconferencing/settings/{appId}`

**Method:** `GET`

**Example Request:**

```bash
GET /crm/v3/extensions/videoconferencing/settings/YOUR_APP_ID?hapikey=YOUR_HUBSPOT_DEVELOPER_API_KEY
```

**Example Response (200 OK):**

```json
{
  "createMeetingUrl": "https://example.com/create-meeting",
  "updateMeetingUrl": "https://example.com/update-meeting",
  "deleteMeetingUrl": "https://example.com/delete-meeting",
  "userVerifyUrl": "https://example.com/user-verify"
}
```

## Webhook Payloads and Responses

HubSpot sends HMAC-signed payloads to the configured webhook URLs.  You must verify the signature using your app's secret.  (Refer to HubSpot's webhook security documentation for details - note that the provided documentation does not describe this specific video conference extension webhook signing process).

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

**Required Response:**

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

**Required Response:**  `200 OK` or `204 No Content`


### 3. Delete Meeting Webhook

**Payload:**

```json
{
  "conferenceId": "some-unique-id"
}
```

**Required Response:** `200 OK` or `204 No Content`


### 4. User Verification Webhook (Optional)

**Request Payload:**

```json
{
  "portalId": 123123,
  "userEmail": "test.user@example.com"
}
```

**Response (200 OK - if successful):**

```json
{
  "id": "any-string-id" // Your system's user ID
}
```

A `404 Not Found` response indicates the user is not found in your system.


## Error Handling

The API may return various HTTP status codes to indicate success or failure.  Always check the response status code and handle any errors appropriately.  For the user verification webhook, a non-200 response will be handled accordingly by HubSpot.


This documentation provides a comprehensive overview of the HubSpot Video Conference Extension API. Remember to consult the official HubSpot developer documentation for the most up-to-date information and detailed specifications.
