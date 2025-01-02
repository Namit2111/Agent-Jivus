# HubSpot CRM API: Owners

This document describes the HubSpot CRM API endpoints for retrieving owner information.  Owners in HubSpot represent users who can be assigned to records, activities, or marketing tasks.

## API Endpoints

The Owners API provides two main endpoints:

### 1. Retrieve a List of Owners

**Endpoint:** `/crm/v3/owners`

**Method:** `GET`

**Description:** Retrieves a list of all current owners in your HubSpot account.  Includes details like name, email, ID, creation/update dates, and team information.  The response includes two ID values:

* `id`: The owner's ID.  Use this when retrieving individual owner information or assigning ownership to records.
* `userId`: The user's ID.  Use this only with the HubSpot settings API; using it for ownership assignment will result in an error.


**Request Parameters:**

* `archived`: (boolean) If `true`, includes archived owners (deactivated users).  Defaults to `false`.

**Response:**

A JSON object with a `results` array containing owner objects. Each owner object has the following fields:

* `id` (string): Owner ID.
* `email` (string): Owner's email address.
* `type` (string):  Always "PERSON".
* `firstName` (string): Owner's first name.
* `lastName` (string): Owner's last name.
* `userId` (integer): User ID (null for archived owners).
* `userIdIncludingInactive` (integer): User ID, including inactive users.  This is populated even for archived owners.
* `createdAt` (string): Date and time the owner was created (ISO 8601 format).
* `updatedAt` (string): Date and time the owner was last updated (ISO 8601 format). Note: This reflects updates to the Owner object, not the User object.
* `archived` (boolean):  Indicates whether the owner is archived.
* `teams` (array): An array of objects, each representing a team the owner belongs to.  Each team object has `id` (string), `name` (string), and `primary` (boolean) fields.


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
    }
    // ... more owners
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
    // ... more archived owners
  ]
}
```


### 2. Retrieve Information About an Individual Owner

**Endpoint:** `/crm/v3/owners/{ownerId}`

**Method:** `GET`

**Description:** Retrieves detailed information about a specific owner using their `id`.

**Path Parameters:**

* `{ownerId}` (string): The ID of the owner to retrieve.

**Response:**  Returns a JSON object representing the owner, with the same fields as described in the previous endpoint.

**Example Request:**

```bash
GET /crm/v3/owners/41629779
```

**Example Response (will be similar to a single owner object from the previous example response).**


## Note on `updatedAt`

The `updatedAt` field reflects changes to the Owner object itself, not the underlying User object.  For instance, changing a user's permissions will *not* update the `updatedAt` value.
