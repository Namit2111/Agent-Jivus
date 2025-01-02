# HubSpot CRM API: Feedback Submissions (BETA)

This document describes the HubSpot CRM API endpoints for retrieving feedback survey submissions.  **Note:** This API is currently in beta and subject to change.  Use at your own risk.  Refer to HubSpot's [Developer Terms](link_to_developer_terms) and [Developer Beta Terms](link_to_developer_beta_terms).

## Overview

HubSpot's feedback submissions store data from various surveys including Net Promoter Score (NPS), Customer Satisfaction (CSAT), Customer Effort Score (CES), and custom surveys. This API allows retrieval of this submission data.  Currently, the API is **read-only**:  submissions cannot be created or modified via the API.

## API Endpoints

The primary endpoint for retrieving feedback submissions is:

`/crm/v3/objects/feedback_submissions`

This endpoint supports both retrieving a single submission and multiple submissions.


### 1. Retrieve Feedback Survey Submissions

**Method:** `GET`

**URL:**

* **Single Submission:** `/crm/v3/objects/feedback_submissions/{feedbackSubmissionId}`  (Replace `{feedbackSubmissionId}` with the ID of the submission)
* **Multiple Submissions:** `/crm/v3/objects/feedback_submissions` (with query parameters)


**Query Parameters (for multiple submissions):**

* `properties`: (Comma-separated list) Specifies the properties to retrieve.  If omitted, only `hs_createdate`, `hs_lastmodifieddate`, and `hs_object_id` are returned.  Example: `properties=hs_sentiment,hs_survey_channel`


**Request Example (Multiple Submissions):**

```bash
curl -X GET \
  'https://api.hubspot.com/crm/v3/objects/feedback_submissions?properties=hs_sentiment,hs_survey_channel' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response Example (JSON):**

```json
{
  "results": [
    {
      "hs_createdate": "2024-10-27T10:00:00",
      "hs_lastmodifieddate": "2024-10-27T10:00:00",
      "hs_object_id": 12345,
      "hs_sentiment": "Positive",
      "hs_survey_channel": "Email"
    },
    {
      "hs_createdate": "2024-10-26T14:30:00",
      "hs_lastmodifieddate": "2024-10-26T14:30:00",
      "hs_object_id": 67890,
      "hs_sentiment": "Neutral",
      "hs_survey_channel": "Website"
    }
  ],
  "hasMore": false,
  "vidOffset": 0
}
```

**Request Example (Single Submission):**

```bash
curl -X GET \
  'https://api.hubspot.com/crm/v3/objects/feedback_submissions/12345' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```


### 2. Feedback Submission Properties

Feedback submissions have default properties (e.g., `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`) and allow for custom properties.  However, **properties cannot be created or modified via the API**.  They must be created and managed within the HubSpot feedback surveys tool.


### 3. Associations

Feedback submissions can be associated with Contacts and Tickets using the HubSpot [Associations API](link_to_associations_api).


##  Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Error responses will include JSON with details about the error.


## Authentication

Requests must include a valid HubSpot API key in the `Authorization` header using Bearer token authentication.


Remember to replace `YOUR_API_KEY` with your actual API key.  Refer to the HubSpot developer documentation for details on obtaining an API key.  The provided links (`link_to_developer_terms`, `link_to_developer_beta_terms`, `link_to_associations_api`) should be replaced with the actual URLs from the HubSpot developer portal.
