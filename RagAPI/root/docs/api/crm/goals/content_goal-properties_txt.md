# HubSpot CRM API: Goals

This document describes the HubSpot CRM API endpoints for interacting with Goals.  Goals in HubSpot allow you to create user-specific quotas for sales and services teams based on templates. This API allows retrieval of goal data.


## Retrieving Goals

The HubSpot CRM API provides several methods for retrieving goal data:

### 1. Retrieving All Goals

To retrieve all goals in your HubSpot account, make a `GET` request to:

`/crm/v3/objects/goal_targets`

**Example Request:**

```bash
GET https://api.hubapi.com/crm/v3/objects/goal_targets
```

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


### 2. Retrieving a Single Goal

To retrieve a specific goal, make a `GET` request to:

`/crm/v3/objects/goal_targets/{goalTargetId}/`

Replace `{goalTargetId}` with the ID of the goal you want to retrieve.

**Example Request:**

```bash
GET https://api.hubapi.com/crm/v3/objects/goal_targets/44027423340/
```

**Example Response:**

```json
{
  "id": "44027423340",
  "properties": {
    "hs_createdate": "2023-02-15T15:53:07.080Z",
    "hs_lastmodifieddate": "2023-02-16T10:02:21.131Z",
    "hs_object_id": "44027423340"
  },
  "createdAt": "2023-02-15T15:53:07.080Z",
  "updatedAt": "2023-02-16T10:02:21.131Z",
  "archived": false
}
```

### 3.  Filtering Goals (using Search API)

For retrieving goals based on specific criteria, use the HubSpot CRM search API.  This is not detailed here, but involves a `POST` request and defining filter parameters in the request body.  Refer to the HubSpot documentation on searching the CRM for more information.


### 4. Specifying Returned Properties

You can specify which properties to return in the response by using the `properties` query parameter.  Provide a comma-separated list of property names.

**Example Request (retrieving specific properties):**

```bash
GET https://api.hubapi.com/crm/v3/objects/goal_targets/44027423340/?properties=hs_goal_name,hs_target_amount,hs_start_datetime,hs_end_datetime
```


## Goals Properties

The following properties are available for goals:

* `hs_goal_name` (string): The name of the goal.
* `hs_target_amount` (number): The target value for the goal.
* `hs_start_datetime` (UTC timestamp): The start date and time of the goal.
* `hs_end_datetime` (UTC timestamp): The end date and time of the goal.
* `hs_created_by_user_id` (number): The HubSpot user ID of the person who created the goal.
* `hs_createdate` (UTC timestamp):  The date and time the goal was created.
* `hs_lastmodifieddate` (UTC timestamp): The date and time the goal was last modified.
* `hs_object_id` (number): The HubSpot object ID of the goal.
* `createdAt` (UTC timestamp):  The date and time the goal was created.
* `updatedAt` (UTC timestamp): The date and time the goal was last modified.
* `archived` (boolean): Indicates if the goal is archived.


**Example Response including specified properties:**

```json
{
  "id": "44027423340",
  "properties": {
    "hs_created_by_user_id": "885536",
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

Remember to replace placeholders like `{goalTargetId}` with actual values and consult the official HubSpot API documentation for the most up-to-date information, including authentication details and rate limits.
