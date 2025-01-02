# HubSpot CRM API: Feedback Submissions (BETA)

This document describes the HubSpot CRM API endpoints for retrieving feedback submission data.  This API is currently in beta and subject to change.  Use at your own risk.  Refer to HubSpot's [Developer Terms](link_to_developer_terms) and [Developer Beta Terms](link_to_developer_beta_terms).

**Important Notes:**

* This API is read-only.  You cannot create, update, or delete feedback submissions through the API.
* Feedback submission properties can only be created within the HubSpot feedback surveys tool and cannot be modified via the API after creation.


## Retrieving Feedback Survey Submissions

The API provides two methods for retrieving feedback submissions:

1. **Retrieving a single submission:** Use this to fetch a specific submission by its ID.

   * **Endpoint:** `/crm/v3/objects/feedback_submissions/{feedbackSubmissionId}`
   * **Method:** `GET`
   * **Parameters:**
     * `{feedbackSubmissionId}`: The ID of the feedback submission to retrieve.
   * **Example Request:**
     ```
     GET https://api.hubspot.com/crm/v3/objects/feedback_submissions/12345
     ```
   * **Example Response (partial):**  (The exact response will depend on the properties included)
     ```json
     {
       "hs_createdate": "2024-10-27T12:00:00",
       "hs_lastmodifieddate": "2024-10-27T12:00:00",
       "hs_object_id": 12345,
       "hs_sentiment": "positive",
       "hs_survey_channel": "email"
     }
     ```


2. **Retrieving multiple submissions:** Use this to fetch submissions based on specified properties.

   * **Endpoint:** `/crm/v3/objects/feedback_submissions`
   * **Method:** `GET`
   * **Parameters:**
     * `properties`: (Optional) Comma-separated list of properties to include in the response.  Defaults to `hs_createdate`, `hs_lastmodifieddate`, and `hs_object_id`.
   * **Example Request:** To retrieve submissions with the source and sentiment:
     ```
     GET https://api.hubspot.com/crm/v3/objects/feedback_submissions?properties=hs_sentiment,hs_survey_channel
     ```
   * **Example Response (partial):** (The exact response will be an array of submissions, each with the specified properties)
     ```json
     [
       {
         "hs_createdate": "2024-10-27T12:00:00",
         "hs_lastmodifieddate": "2024-10-27T12:00:00",
         "hs_object_id": 12345,
         "hs_sentiment": "positive",
         "hs_survey_channel": "email"
       },
       {
         "hs_createdate": "2024-10-27T13:00:00",
         "hs_lastmodifieddate": "2024-10-27T13:00:00",
         "hs_object_id": 67890,
         "hs_sentiment": "negative",
         "hs_survey_channel": "in-app"
       }
     ]
     ```


## Feedback Submission Properties

Feedback submissions include default properties such as `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`, and others relating to survey answers.  You can also create custom properties within the HubSpot interface, but these cannot be managed via the API.


## Associations

Feedback submissions can be associated with Contacts and Tickets.  See HubSpot's documentation on the [associations API](link_to_associations_api) for details on how to access these associations.


## Authentication

To use this API, you will need a HubSpot API key.  Include this key in the `Authorization` header of your requests:

```
Authorization: Bearer YOUR_API_KEY
```


This documentation provides a concise overview. For complete details and the most up-to-date information, refer to the official HubSpot API documentation.  Remember to replace placeholders like `YOUR_API_KEY` and `12345` with your actual values.  Remember to add the actual links for developer terms, beta terms and association API.
