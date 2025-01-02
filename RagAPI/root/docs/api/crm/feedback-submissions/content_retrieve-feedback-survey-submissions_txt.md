# HubSpot CRM API: Feedback Submissions (BETA)

This document describes the HubSpot CRM API endpoints for retrieving feedback survey submissions.  **Note:** This API is currently in beta and subject to change.  Use at your own risk.  Refer to HubSpot's [Developer Terms](link_to_terms) and [Developer Beta Terms](link_to_beta_terms).

## Overview

HubSpot's feedback submissions store data from various surveys (NPS, CSAT, CES, and custom). This API allows retrieval of submission data, but **currently does not support creating or updating submissions.**

## API Endpoints

All endpoints use the `/crm/v3/objects/feedback_submissions` base path.  Requests should be made to `https://api.hubspot.com/crm/v3/objects/feedback_submissions`.  You will need a valid HubSpot API key for authentication (include in the `Authorization` header as `Bearer <your_api_key>`).

### 1. Retrieve Feedback Survey Submissions

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/feedback_submissions/{feedbackSubmissionId}` (for a single submission) or `/crm/v3/objects/feedback_submissions` (for multiple submissions)


**Parameters:**

* `{feedbackSubmissionId}` (Optional, for single submission): The ID of the feedback submission to retrieve.
* `properties` (Optional, for multiple submissions): A comma-separated list of properties to include in the response.  Defaults to `hs_createdate`, `hs_lastmodifieddate`, and `hs_object_id`.  Example: `properties=hs_sentiment,hs_survey_channel`


**Response:**

A JSON array of feedback submission objects. Each object contains the requested properties.  For example:

```json
[
  {
    "hs_object_id": 123,
    "hs_createdate": "2024-10-27T10:00:00",
    "hs_lastmodifieddate": "2024-10-27T10:00:00",
    "hs_sentiment": "positive",
    "hs_survey_channel": "email"
  },
  {
    "hs_object_id": 456,
    "hs_createdate": "2024-10-26T14:30:00",
    "hs_lastmodifieddate": "2024-10-26T14:30:00",
    "hs_sentiment": "negative",
    "hs_survey_channel": "in-app"
  }
]
```


**Example Request (Multiple Submissions with Specific Properties):**

```bash
curl -X GET \
  'https://api.hubspot.com/crm/v3/objects/feedback_submissions?properties=hs_sentiment,hs_survey_channel' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Example Request (Single Submission):**

```bash
curl -X GET \
  'https://api.hubspot.com/crm/v3/objects/feedback_submissions/123' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```


## Feedback Submission Properties

Feedback submissions have default properties (e.g., `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`) and potentially custom properties defined within the HubSpot feedback surveys tool.  These custom properties **cannot be created or modified via the API.**


## Associations

Feedback submissions can be associated with contacts and tickets.  Refer to HubSpot's [Associations API documentation](link_to_associations_api) for details on how to retrieve these associations.


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Error responses will include a JSON payload with details about the error.


## Rate Limits

Please refer to HubSpot's API documentation for information on rate limits.


This documentation is based on the provided text.  Replace the bracketed placeholders (`link_to_terms`, `link_to_beta_terms`, `link_to_associations_api`) with the actual links from the HubSpot Developer documentation.
