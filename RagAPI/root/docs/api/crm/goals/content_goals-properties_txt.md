# HubSpot CRM API: Goals

This document details the HubSpot CRM API endpoints for interacting with Goals.  Goals in HubSpot allow you to create user-specific quotas for sales and services teams based on provided templates.  This API allows retrieval of goal data.


## Retrieving Goals

The HubSpot CRM API provides several ways to retrieve goal data:

**1. Retrieve All Goals:**

* **Method:** `GET`
* **Endpoint:** `/crm/v3/objects/goal_targets`
* **Example Request:**  `https://api.hubapi.com/crm/v3/objects/goal_targets`
* **Response:** A JSON array containing all goals in the account.  Each goal object includes properties like `id`, `createdAt`, `updatedAt`, `archived`, and various goal-specific properties (see "Goals Properties" section).

**Example Response:**

```json
[
  {
    "id": "87504620389",
    "properties": {
      "hs_createdate": "2021-11-30T22:18:49.923Z",
      "hs_lastmodifieddate": "2023-12-11T19:21:32.851Z",
      "hs_object_id": "87504620389"
    },
    "createdAt": "2021-11-30T22:18:49.923Z",
    "updatedAt": "2023-12-11T19:21:32.851Z",
    "archived": false
  },
  // ... more goals
]
```

**2. Retrieve a Single Goal:**

* **Method:** `GET`
* **Endpoint:** `/crm/v3/objects/goal_targets/{goalTargetId}`
* **Example Request:** `https://api.hubapi.com/crm/v3/objects/goal_targets/44027423340` (replace `44027423340` with the actual goal ID)
* **Response:** A JSON object representing the specified goal.


**3. Search Goals (using CRM search endpoint):**

To retrieve goals based on specific criteria, use the HubSpot CRM search endpoint (details not provided in the source text, but documentation should be available in HubSpot's API documentation).  This would involve a `POST` request with filter parameters in the request body.


## Goals Properties

The following properties are available for goals.  You can specify which properties to retrieve using the `properties` query parameter in your GET request (comma-separated list of property names).

* **`hs_goal_name`:** (string) The name of the goal.
* **`hs_target_amount`:** (number) The target value for the goal.
* **`hs_start_datetime`:** (UTC timestamp) The goal's start date.
* **`hs_end_datetime`:** (UTC timestamp) The goal's end date.
* **`hs_created_by_user_id`:** (number) The HubSpot user ID of the person who created the goal.
* **`hs_createdate`:** (UTC timestamp) The goal's creation date.
* **`hs_lastmodifieddate`:** (UTC timestamp) The goal's last modification date.
* **`hs_object_id`:** (number) The HubSpot object ID of the goal.
* **`id`:** (string) Unique identifier for the goal.
* **`createdAt`:** (UTC timestamp) Creation timestamp.
* **`updatedAt`:** (UTC timestamp) Last update timestamp.
* **`archived`:** (boolean) Indicates whether the goal is archived.



**Example Request with Specific Properties:**

```
https://api.hubapi.com/crm/v3/objects/goal_targets/44027423340?properties=hs_goal_name,hs_target_amount,hs_start_datetime,hs_end_datetime
```

**Example Response:**

```json
{
  "id": "44027423340",
  "properties": {
    "hs_goal_name": "Revenue Goal 2023",
    "hs_target_amount": "2000.00",
    "hs_start_datetime": "2023-12-01T00:00:00Z",
    "hs_end_datetime": "2024-01-01T00:00:00Z"
  },
  "createdAt": "2023-02-15T15:53:07.080Z",
  "updatedAt": "2023-02-16T10:02:21.131Z",
  "archived": false
}
```


**Note:**  Remember to replace placeholder values like `44027423340` with actual IDs and use your HubSpot API key for authentication.  Consult the official HubSpot API documentation for complete details, including authentication methods, rate limits, and error handling.
