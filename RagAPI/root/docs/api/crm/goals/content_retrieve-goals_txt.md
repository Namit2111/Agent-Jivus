# HubSpot CRM API: Goals

This document describes the HubSpot CRM API endpoints for managing goals.  Goals in HubSpot are used to set quotas for sales and service teams. This API allows retrieval of goal data.

## Retrieve Goals

The HubSpot CRM API provides endpoints to retrieve goals data.

**1. Retrieve All Goals:**

* **Method:** `GET`
* **Endpoint:** `/crm/v3/objects/goal_targets`
* **Description:** Retrieves all goals in your HubSpot account.

**Example:**

```bash
curl -X GET \
  'https://api.hubapi.com/crm/v3/objects/goal_targets' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response (Example):**

```json
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
}
```

**2. Retrieve a Single Goal:**

* **Method:** `GET`
* **Endpoint:** `/crm/v3/objects/goal_targets/{goalTargetId}`
* **Description:** Retrieves a specific goal by its ID.  Replace `{goalTargetId}` with the actual goal ID.

**Example:**

```bash
curl -X GET \
  'https://api.hubapi.com/crm/v3/objects/goal_targets/44027423340' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response (Example):**  Similar structure to the "Retrieve All Goals" response, but with data for a specific goal.


**3. Retrieve Goals with Specific Criteria (Search):**

* **Method:** `POST`
* **Endpoint:**  (Not explicitly provided in the text, but mentioned as available via the CRM search endpoint). Consult HubSpot's documentation for the search API endpoint and its filtering capabilities.
* **Description:** Use the CRM search endpoint to retrieve goals based on specified criteria. This requires constructing a POST request with the appropriate filters in the request body.


## Goals Properties

The following properties are available when retrieving goal data.  You can specify which properties to retrieve using the `properties` query parameter (comma-separated list).

* `hs_goal_name`: (string) The name of the goal.
* `hs_target_amount`: (number) The target value for the goal.
* `hs_start_datetime`: (UTC timestamp) The goal's start date.
* `hs_end_datetime`: (UTC timestamp) The goal's end date.
* `hs_created_by_user_id`: (string) The HubSpot user ID of the person who created the goal.
* `hs_createdate`: (UTC timestamp)  The goal's creation date.
* `hs_lastmodifieddate`: (UTC timestamp) The goal's last modification date.
* `hs_object_id`: (string) The HubSpot object ID of the goal.
* `createdAt`: (UTC timestamp)  Creation date.
* `updatedAt`: (UTC timestamp) Last update date.
* `archived`: (boolean) Whether the goal is archived.


**Example Request with Specific Properties:**

```bash
curl -X GET \
  'https://api.hubapi.com/crm/v3/objects/goal_targets/44027423340?properties=hs_goal_name,hs_target_amount,hs_start_datetime,hs_end_datetime,hs_created_by_user_id' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Example Response (with specified properties):**

```json
{
  "id": "44027423340",
  "properties": {
    "hs_created_by_user_id": "885536",
    "hs_createdate": "2023-02-15T15:53:07.080Z",
    "hs_end_datetime": "2024-01-01T00:00:00Z",
    "hs_goal_name": "Revenue Goal 2023",
    "hs_lastmodifieddate": "2023-02-16T10:02:21.131Z",
    "hs_object_id": "44027423340",
    "hs_start_datetime": "2023-12-01T00:00:00Z",
    "hs_target_amount": "2000.00"
  },
  "createdAt": "2023-02-15T15:53:07.080Z",
  "updatedAt": "2023-02-16T10:02:21.131Z",
  "archived": false
}
```

**Note:**  Replace `YOUR_API_KEY` with your actual HubSpot API key.  Error handling and rate limiting should be considered in production implementations.  Always refer to the official HubSpot API documentation for the most up-to-date information.
