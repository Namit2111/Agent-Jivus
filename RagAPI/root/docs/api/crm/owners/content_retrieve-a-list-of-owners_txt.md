# HubSpot CRM API: Owners

This document describes the HubSpot CRM API endpoints for retrieving information about owners.  Owners in HubSpot represent users who can be assigned to records, activities, or marketing tasks.  They are automatically created and updated when users are added or synced from Salesforce.  These API endpoints are read-only.

## API Endpoints

The Owners API provides two main endpoints:

### 1. Retrieve a list of owners

**Endpoint:** `/crm/v3/owners`

**Method:** `GET`

**Request Parameters:**

* `archived`: (optional) Boolean.  If `true`, returns archived owners (deactivated users). Defaults to `false`.

**Response:**

A JSON object with a `results` array containing owner objects.  Each owner object has the following fields:

* `id`: (string) The owner's ID.  Use this to retrieve information about a specific owner or to assign ownership to a record.
* `email`: (string) The owner's email address.
* `type`: (string) Always "PERSON".
* `firstName`: (string) The owner's first name.
* `lastName`: (string) The owner's last name.
* `userId`: (integer) The user's ID.  Use this for the settings API, but not for assigning ownership. Will be `null` for archived owners.
* `userIdIncludingInactive`: (integer) The user's ID, including inactive users.  Useful for archived owners.
* `createdAt`: (string)  ISO 8601 timestamp indicating when the owner was created.
* `updatedAt`: (string) ISO 8601 timestamp indicating when the owner was last updated. Note: This updates only when the Owner object itself is modified, not when the associated User object changes.
* `archived`: (boolean) Indicates whether the owner is archived.
* `teams`: (array of objects)  An array of team objects, each with `id`, `name`, and `primary` (boolean) fields.


**Example Response (non-archived owners):**

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

**Example Response (archived owners):**

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


### 2. Retrieve information about an individual owner

**Endpoint:** `/crm/v3/owners/{ownerId}`

**Method:** `GET`

**Path Parameters:**

* `{ownerId}`: (string) The ID of the owner to retrieve.

**Response:**

A JSON object representing a single owner with the same fields as described in the previous endpoint.


##  Notes

* The `updatedAt` field reflects changes to the Owner object, not the associated User object.  Changes to user permissions will not update this field.
*  The `id` field is crucial for assigning ownership to records or activities.  Use the `userId` field only with the HubSpot settings API.


This documentation provides a comprehensive overview of the HubSpot CRM Owners API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
