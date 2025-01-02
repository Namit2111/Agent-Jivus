# HubSpot CRM API: Feedback Submissions (BETA)

This document details the HubSpot CRM API endpoints for retrieving feedback submission data.  **Note:** This API is currently in beta and subject to change.  Use is governed by HubSpot's [Developer Terms](link_to_terms) and [Developer Beta Terms](link_to_beta_terms).

## Overview

The Feedback Submissions API allows you to retrieve data about submissions to feedback surveys within HubSpot.  These surveys include Net Promoter Score (NPS), Customer Satisfaction (CSAT), Customer Effort Score (CES), and custom surveys.  Currently, the API is **read-only**; you cannot create or update submissions via the API.

## API Endpoints

The primary endpoint for retrieving feedback submissions is:

`/crm/v3/objects/feedback_submissions`


### 1. Retrieve Feedback Survey Submissions

#### **GET /crm/v3/objects/feedback_submissions/{feedbackSubmissionId}**

Retrieves a single feedback submission by its ID.

* **Method:** GET
* **Path Parameter:**
    * `feedbackSubmissionId`: The ID of the feedback submission to retrieve.
* **Query Parameters:**
    * `properties`: (Optional) A comma-separated list of properties to include in the response.  If omitted, only `hs_createdate`, `hs_lastmodifieddate`, and `hs_object_id` are returned.  Example: `properties=hs_sentiment,hs_survey_channel`
* **Response:** A JSON object representing the feedback submission.  The structure depends on the specified properties.  See "Feedback Submission Properties" below for details.

**Example Request:**

```bash
GET https://api.hubspot.com/crm/v3/objects/feedback_submissions/12345?properties=hs_sentiment,hs_survey_channel
```

**Example Response (partial, depends on properties):**

```json
{
  "hs_object_id": 12345,
  "hs_createdate": "2024-10-27T10:00:00Z",
  "hs_lastmodifieddate": "2024-10-27T10:00:00Z",
  "hs_sentiment": "Positive",
  "hs_survey_channel": "Email"
}
```


#### **GET /crm/v3/objects/feedback_submissions**

Retrieves multiple feedback submissions.  This allows for bulk retrieval, potentially filtering by criteria (future development may add filtering options).

* **Method:** GET
* **Query Parameters:**
    * `properties`: (Optional) A comma-separated list of properties to include in the response.  See above for details.  Example: `properties=hs_sentiment,hs_survey_channel`
    * *(Future development may include additional query parameters for filtering)*
* **Response:** A JSON object containing a list of feedback submission objects.  The structure of each object depends on the specified properties.

**Example Request:**

```bash
GET https://api.hubspot.com/crm/v3/objects/feedback_submissions?properties=hs_sentiment,hs_survey_channel
```

**Example Response (partial):**

```json
{
  "results": [
    {
      "hs_object_id": 12345,
      "hs_createdate": "2024-10-27T10:00:00Z",
      "hs_lastmodifieddate": "2024-10-27T10:00:00Z",
      "hs_sentiment": "Positive",
      "hs_survey_channel": "Email"
    },
    {
      "hs_object_id": 67890,
      "hs_createdate": "2024-10-26T15:30:00Z",
      "hs_lastmodifieddate": "2024-10-26T15:30:00Z",
      "hs_sentiment": "Neutral",
      "hs_survey_channel": "Website"
    }
  ]
}
```


## Feedback Submission Properties

Feedback submissions have default properties (e.g., `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`) and allow for custom properties.  These custom properties **cannot be created or modified via the API**.  They must be created within the HubSpot feedback surveys tool.

## Associations

Feedback submissions can be associated with Contacts and Tickets.  Use the HubSpot [Associations API](link_to_associations_api) to manage these associations.


## Authentication

To use the API, you'll need a HubSpot API key.  Include this key in the `Authorization` header of your requests:

`Authorization: Bearer YOUR_API_KEY`


This documentation provides a basic overview.  Refer to the HubSpot developer portal for the most up-to-date information and complete API specifications.  Remember that this API is in beta, so expect changes.
