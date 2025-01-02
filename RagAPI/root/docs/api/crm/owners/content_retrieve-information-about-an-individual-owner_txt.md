# HubSpot CRM API: Owners

This document describes the HubSpot CRM API endpoints for retrieving information about owners.  Owners in HubSpot represent users who can be assigned to records, activities, or marketing tasks.  These endpoints are read-only.

## API Endpoints

### 1. Retrieve a List of Owners

**Endpoint:** `/crm/v3/owners`

**Method:** `GET`

**Parameters:**

* `archived`: (Optional) Boolean.  If `true`, returns archived owners. Defaults to `false`.

**Response:**

A JSON object with a `results` array containing owner objects. Each owner object has the following fields:

* `id`: (String) The owner's ID.  Use this ID to retrieve information about a specific owner or to assign ownership to a record.
* `email`: (String) The owner's email address.
* `type`: (String)  Always "PERSON".
* `firstName`: (String) The owner's first name.
* `lastName`: (String) The owner's last name.
* `userId`: (Integer) The user's ID.  Use this ID for the settings API; using it for assigning ownership will result in an error.  Will be `null` for archived owners.
* `userIdIncludingInactive`: (Integer) The user's ID, including inactive users. This is used for archived owners.
* `createdAt`: (String) ISO 8601 timestamp indicating when the owner was created.
* `updatedAt`: (String) ISO 8601 timestamp indicating when the owner was last updated.  Note: This updates only when the Owner object itself is modified, not when the associated User object changes.
* `archived`: (Boolean) Indicates whether the owner is archived.
* `teams`: (Array of Objects) An array of team objects, each with:
    * `id`: (String) The team's ID.
    * `name`: (String) The team's name.
    * `primary`: (Boolean) Indicates if this is the owner's primary team.


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

**Example Response (Archived Owners - `archived=true`):**

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

**Parameters:**

* `{ownerId}`: (String) The ID of the owner to retrieve.

**Response:**

A JSON object representing a single owner with the same fields as described in the previous section.


**Example Call (using `curl`):**

```bash
curl -X GET "https://api.hubapi.com/crm/v3/owners/41629779" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Replace `YOUR_API_KEY` with your actual HubSpot API key.  This will return the details for the owner with ID `41629779`.


**Note:**  The `updatedAt` field reflects changes to the Owner object itself, not changes to the associated User object (e.g., permission changes).
