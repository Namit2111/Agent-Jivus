# HubSpot CRM API: Owners

This document describes the HubSpot CRM API endpoints for retrieving owner information.  Owners in HubSpot represent users who can be assigned to records, activities, or marketing tasks.  This API is read-only; you cannot create or modify owners through these endpoints.

## Endpoints

### 1. Retrieve a List of Owners

**Endpoint:** `/crm/v3/owners`

**Method:** `GET`

**Description:** Retrieves a list of all owners in your HubSpot account.  You can filter for archived owners using the `archived` query parameter.

**Query Parameters:**

* `archived`: (boolean)  If `true`, returns archived owners. Defaults to `false`.

**Response:** A JSON object with a `results` array containing owner objects. Each owner object has the following fields:

* `id`: (string) The unique ID of the owner. Use this ID to retrieve individual owner information or assign ownership to records.
* `email`: (string) The owner's email address.
* `type`: (string)  Always "PERSON".
* `firstName`: (string) The owner's first name.
* `lastName`: (string) The owner's last name.
* `userId`: (integer) The HubSpot user ID.  `null` for archived users.
* `userIdIncludingInactive`: (integer) The HubSpot user ID, including inactive users.  This field is populated even for archived users.
* `createdAt`: (string)  ISO 8601 timestamp indicating when the owner was created.
* `updatedAt`: (string) ISO 8601 timestamp indicating when the owner was last updated.  Note: This reflects updates to the Owner object, not the underlying User object.
* `archived`: (boolean)  Indicates whether the owner is archived.
* `teams`: (array of objects) An array of team objects, each with `id` and `name` fields.  The `primary` field indicates if it's the user's primary team.


**Example Request (Active Owners):**

```bash
GET /crm/v3/owners
```

**Example Response (Active Owners):**

```json
{
  "results": [
    {
      "id": "41629779",
      "email": "email@hubspot.com",
      "type": "PERSON",
      "firstName": "HubSpot",
      "lastName": "Test Owner",
      "userId": 9586504,
      "userIdIncludingInactive": 9586504,
      "createdAt": "2019-12-25T13:01:35.228Z",
      "updatedAt": "2023-08-22T13:40:26.790Z",
      "archived": false,
      "teams": [
        {
          "id": "368389",
          "name": "Sales Team",
          "primary": true
        }
      ]
    },
    // ... more owner objects
  ]
}
```

**Example Request (Archived Owners):**

```bash
GET /crm/v3/owners?archived=true
```

**Example Response (Archived Owners):**

```json
{
  "results": [
    {
      "id": "42103462",
      "email": "useremail@hubspot.com",
      "type": "PERSON",
      "firstName": "",
      "lastName": "",
      "userId": null,
      "userIdIncludingInactive": 9685555,
      "createdAt": "2020-01-09T20:28:50.080Z",
      "updatedAt": "2020-01-09T20:28:50.080Z",
      "archived": true
    }
    // ... more archived owner objects
  ]
}
```


### 2. Retrieve Information About an Individual Owner

**Endpoint:** `/crm/v3/owners/{ownerId}`

**Method:** `GET`

**Description:** Retrieves information about a specific owner.

**Path Parameters:**

* `ownerId`: (string) The ID of the owner to retrieve.

**Response:** A JSON object representing the owner, with the same fields as described in the previous endpoint.

**Example Request:**

```bash
GET /crm/v3/owners/41629779
```

**Example Response:** (Similar to a single object from the previous response, omitting the `results` wrapper)


## Important Notes

* The `updatedAt` field only reflects changes to the Owner object itself, not the underlying User object.
* The `userId` field will be `null` for archived owners; use `userIdIncludingInactive` instead.
*  Use the `id` field when assigning ownership to records.  Using `userId` for this purpose will result in an error.


This API provides a way to retrieve owner information for various HubSpot integrations and applications. Remember to consult the HubSpot API documentation for the most up-to-date information and authentication details.
