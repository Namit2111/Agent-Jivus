# HubSpot CRM API: Goals

This document describes the HubSpot CRM API endpoints for interacting with Goals.  Goals in HubSpot allow creating user-specific quotas for sales and service teams based on provided templates. This API allows retrieving goal data from your HubSpot account.


## Retrieving Goals

The Goals API offers several methods for retrieving goal data:

**1. Retrieving All Goals:**

* **Method:** `GET`
* **Endpoint:** `/crm/v3/objects/goal_targets`
* **Example Request:**  `https://api.hubapi.com/crm/v3/objects/goal_targets`
* **Response:** A JSON array containing all goals in your account. Each goal is represented as a JSON object with the following properties (at minimum):

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

**2. Retrieving a Single Goal:**

* **Method:** `GET`
* **Endpoint:** `/crm/v3/objects/goal_targets/{goalTargetId}`
* **Parameters:** `{goalTargetId}`: The ID of the goal to retrieve.
* **Example Request:** `https://api.hubapi.com/crm/v3/objects/goal_targets/44027423340`
* **Response:** A JSON object representing the specified goal.  See the example response below.

**3. Searching Goals (Filtering):**

The documentation mentions using a POST request to a search endpoint for filtering goals based on specific criteria.  Details on this search endpoint are not provided in this excerpt, but it's implied to be a standard HubSpot CRM search functionality.


## Goals Properties

The following properties can be retrieved for each goal:

* `hs_goal_name` (string): The name of the goal.
* `hs_target_amount` (number): The target value of the goal.
* `hs_start_datetime` (UTC timestamp): The goal's start date.
* `hs_end_datetime` (UTC timestamp): The goal's end date.
* `hs_created_by_user_id` (string): The HubSpot User ID of the goal's creator.
* `hs_createdate` (UTC timestamp): The goal's creation date.
* `hs_lastmodifieddate` (UTC timestamp): The goal's last modification date.
* `hs_object_id` (string): The HubSpot object ID of the goal.
* `id` (string): The goal's ID.
* `createdAt` (UTC timestamp):  The goal's creation date (likely equivalent to `hs_createdate`).
* `updatedAt` (UTC timestamp): The goal's last update date (likely equivalent to `hs_lastmodifieddate`).
* `archived` (boolean): Indicates whether the goal is archived.


**Specifying Properties:**

To retrieve only specific properties, include the `properties` query parameter in your GET request with a comma-separated list of desired property names.

* **Example Request (retrieving specific properties):**

```
https://api.hubapi.com/crm/v3/objects/goal_targets/44027423340?properties=hs_goal_name,hs_target_amount,hs_start_datetime,hs_end_datetime,hs_created_by_user_id
```

* **Example Response (with specified properties):**

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

Remember to replace placeholders like `{goalTargetId}` with actual values.  Authentication is required to access the HubSpot API; consult the HubSpot API documentation for details on authentication methods.
