# HubSpot CRM API: Deal Splits

This document describes the HubSpot CRM API endpoints for managing deal splits.  Deal splits allow distributing credit for deal amounts among multiple users. This functionality requires a Sales Hub Enterprise subscription.

## API Endpoints

The API uses two main endpoints: one for creating or updating splits and another for retrieving them.  Both endpoints use a batch processing approach, allowing multiple deals to be processed in a single request.


### 1. Create or Update Deal Splits

**Endpoint:** `POST crm/v3/objects/deals/splits/batch/upsert`

This endpoint allows creating new deal splits or updating existing ones.  The request body must be a JSON object with an `inputs` array. Each element in the `inputs` array represents a deal and its associated splits.

**Request Body:**

```json
{
  "inputs": [
    {
      "id": <dealId>,
      "splits": [
        {
          "ownerId": <userId1>,
          "percentage": <percentage1>
        },
        {
          "ownerId": <userId2>,
          "percentage": <percentage2>
        }
        // ... more splits
      ]
    },
    {
      "id": <dealId2>,
      "splits": [
        // ... splits for dealId2
      ]
    }
    // ... more deals
  ]
}
```

* **`id` (required):** The ID of the deal.  Obtain this using the HubSpot Deals API.
* **`splits` (required):** An array of split objects.
    * **`ownerId` (required):** The HubSpot user ID to assign the split to.
    * **`percentage` (required):** The percentage of the deal amount assigned to the owner (0.0 to 1.0).

**Important Considerations:**

* The sum of percentages for a deal's splits must equal 1.0.
* The deal's owner must be included as a split owner.
* You must adhere to the minimum split percentage and maximum split users limits configured in your HubSpot deal split settings.  Failure to meet these requirements will result in an error.
* Existing splits for a deal will be *replaced* by the ones provided in the request.


**Example Request:** Assigning 50% credit each to two users on a deal (deal ID: 5315919905, User IDs: 41629779 and 60158084):

```json
{
  "inputs": [
    {
      "id": 5315919905,
      "splits": [
        {
          "ownerId": 41629779,
          "percentage": 0.5
        },
        {
          "ownerId": 60158084,
          "percentage": 0.5
        }
      ]
    }
  ]
}
```

### 2. Retrieve Deal Splits

**Endpoint:** `POST crm/v3/objects/deals/splits/batch/read`

This endpoint retrieves split information for specified deals.

**Request Body:**

```json
{
  "inputs": [
    {
      "id": <dealId1>
    },
    {
      "id": <dealId2>
    }
    // ... more deal IDs
  ]
}
```

* **`id` (required):** The ID of the deal.

**Example Request:** Retrieving splits for two deals (IDs: 5315919905 and 17137567105):

```json
{
  "inputs": [
    {
      "id": "5315919905"
    },
    {
      "id": "17137567105"
    }
  ]
}
```

**Response Body:**

The response includes an array of results, one for each deal. Each result contains the deal ID and an array of its splits. Each split object includes its ID, properties (percentage and owner ID), creation and update timestamps, and an archived flag.


**Example Response:**

```json
{
  "status": "COMPLETE",
  "results": [
    {
      "id": "17137567105",
      "splits": [
        // ... split objects
      ]
    },
    {
      "id": "5315919905",
      "splits": [
        // ... split objects
      ]
    }
  ],
  "startedAt": "...",
  "completedAt": "..."
}
```


This response shows the `status`, `results` (deal splits), and timestamps indicating when the batch processing started and completed.  The `splits` array contains detailed information about each split for the corresponding deal.

Remember to consult the official HubSpot API documentation for the most up-to-date information and authentication details.
