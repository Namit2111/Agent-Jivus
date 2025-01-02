# HubSpot CRM API: Feedback Submissions (BETA)

This document describes the HubSpot CRM API endpoints for retrieving feedback survey submissions.  This API is currently under development and subject to change.  Use at your own risk.  Refer to HubSpot's [Developer Terms](link-to-terms) and [Developer Beta Terms](link-to-beta-terms).

**Important Note:** This API is currently read-only.  You cannot create, update, or delete feedback submissions through this API.


## Retrieving Feedback Survey Submissions

The API provides two ways to retrieve feedback submission data:

* **By ID:** Retrieve a single submission using its `feedbackSubmissionId`.
* **Bulk Retrieval:** Retrieve multiple submissions, optionally filtering by properties.

### 1. Retrieving a Single Submission by ID

**API Endpoint:**

`/crm/v3/objects/feedback_submissions/{feedbackSubmissionId}`

**Method:** `GET`

**Request:**

```
GET https://api.hubspot.com/crm/v3/objects/feedback_submissions/{feedbackSubmissionId}
```

Replace `{feedbackSubmissionId}` with the ID of the feedback submission.

**Response:**

A JSON object representing the feedback submission.  The response includes at minimum `hs_createdate`, `hs_lastmodifieddate`, and `hs_object_id`.  Additional properties can be included (see below).


**Example:**

```bash
curl -X GET \
  'https://api.hubspot.com/crm/v3/objects/feedback_submissions/12345' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```


### 2. Bulk Retrieval of Submissions

**API Endpoint:**

`/crm/v3/objects/feedback_submissions`

**Method:** `GET`

**Request:**

```
GET https://api.hubspot.com/crm/v3/objects/feedback_submissions?properties=property1,property2,...
```

Use the `properties` query parameter to specify which properties to include in the response.  If omitted, only `hs_createdate`, `hs_lastmodifieddate`, and `hs_object_id` are returned.

**Example:** To retrieve submissions with `hs_sentiment` and `hs_survey_channel`:

```bash
curl -X GET \
  'https://api.hubspot.com/crm/v3/objects/feedback_submissions?properties=hs_sentiment,hs_survey_channel' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response:**

A JSON object containing a list of feedback submissions.  Each submission is represented as a JSON object with the specified properties.


## Feedback Submission Properties

Feedback submissions have default properties including submission date, survey information, and answer data. You can also create custom properties within the HubSpot feedback surveys tool.  **These properties cannot be created or modified via the API.**

**Example Default Properties:**

* `hs_createdate`: Date and time of submission creation.
* `hs_lastmodifieddate`: Date and time of last modification.
* `hs_object_id`: Unique identifier for the submission.
* `hs_sentiment`: Sentiment analysis of the submission (if available).
* `hs_survey_channel`: Channel through which the survey was submitted (e.g., email, website).


## Associations

Feedback submissions can be associated with Contact and Ticket records using the HubSpot Associations API (documentation needed to be provided separately).


## Error Handling

Standard HubSpot API error responses will be returned in case of failures (e.g., invalid API key, submission not found, etc.).  Refer to the HubSpot API documentation for details on error codes and responses.


## Rate Limits

Observe HubSpot's API rate limits to avoid throttling.  Refer to the HubSpot API documentation for details on rate limits and best practices.
