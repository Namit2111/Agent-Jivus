# HubSpot CRM API: Goals

This document describes the HubSpot CRM API endpoints for retrieving goal data.  Goals in HubSpot are used to set user-specific quotas for sales and service teams.

## API Endpoints

The Goals API uses the `/crm/v3/objects/goal_targets` endpoint.

### Retrieving Goals

**1. Retrieve All Goals:**

* **Method:** `GET`
* **Endpoint:** `/crm/v3/objects/goal_targets`
* **Example Request:** `https://api.hubapi.com/crm/v3/objects/goal_targets`

**2. Retrieve a Single Goal:**

* **Method:** `GET`
* **Endpoint:** `/crm/v3/objects/goal_targets/{goalTargetId}`
* **Parameter:** `{goalTargetId}` - The ID of the goal to retrieve.
* **Example Request:** `https://api.hubapi.com/crm/v3/objects/goal_targets/44027423340`

**3. Search for Goals (using CRM search endpoint):**

This requires a `POST` request to the CRM search endpoint (not detailed here, refer to HubSpot's CRM search documentation) with filters specified in the request body to retrieve goals that meet specific criteria.


### Specifying Properties

To retrieve only specific goal properties, use the `properties` query parameter in your `GET` request.  Specify comma-separated property names.

* **Example Request (retrieving specific properties):**  `https://api.hubapi.com/crm/v3/objects/goal_targets/44027423340?properties=hs_goal_name,hs_target_amount,hs_start_datetime,hs_end_datetime`


## Response Structure

The API returns a JSON response.  The structure includes:

* `id`: The unique identifier of the goal.
* `properties`: An object containing the goal's properties.
* `createdAt`: The creation timestamp (UTC).
* `updatedAt`: The last update timestamp (UTC).
* `archived`: A boolean indicating whether the goal is archived.


## Example Responses

**Example 1:  Retrieving a single goal (default properties):**

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

**Example 2: Retrieving a single goal with specific properties:**

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


## Available Goal Properties

* `hs_goal_name`: (string) Name of the goal.
* `hs_target_amount`: (number) Target value for the goal.
* `hs_start_datetime`: (UTC timestamp) Goal start date.
* `hs_end_datetime`: (UTC timestamp) Goal end date.
* `hs_created_by_user_id`: (number) HubSpot User ID of the goal creator.
* `hs_createdate`: (UTC timestamp) Goal creation date.
* `hs_lastmodifieddate`: (UTC timestamp) Goal last modification date.
* `hs_object_id`: (number)  The HubSpot object ID of the goal.


## Authentication

To use the HubSpot CRM API, you will need a HubSpot API key.  Include this key in the request header as `Authorization: Bearer YOUR_API_KEY`.  Refer to the HubSpot API documentation for details on obtaining an API key.
