# HubSpot CRM API: Deal Splits

This document describes the HubSpot CRM API endpoints for managing deal splits.  Deal splits allow distributing credit for deal amounts among multiple users. This functionality requires a Sales Hub Enterprise subscription.

## 1. Create or Update Deal Splits

This endpoint allows creating new deal splits or updating existing ones.

**API Call:** `POST /crm/v3/objects/deals/splits/batch/upsert`

**Request Body:**

The request body is a JSON object with an `inputs` array. Each element in the array represents a deal and its associated splits.

```json
{
  "inputs": [
    {
      "id": 5315919905, // Deal ID (obtainable via the Deals API)
      "splits": [
        {
          "ownerId": 41629779, // HubSpot User ID
          "percentage": 0.5 // Percentage of deal amount (0.0 - 1.0)
        },
        {
          "ownerId": 60158084, // HubSpot User ID
          "percentage": 0.5 // Percentage of deal amount (0.0 - 1.0)
        }
      ]
    }
  ]
}
```

**Request Requirements:**

* The deal's owner must be included as a split owner.
* The sum of split percentages must equal 1.0.
*  You must adhere to the minimum split percentage and maximum split users limits defined in your deal split settings.  Failure to meet these requirements will result in an error.

**Example Request (cURL):**

```bash
curl -X POST \
  https://api.hubapi.com/crm/v3/objects/deals/splits/batch/upsert \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
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
  }'
```

**Response:**  A successful request will return a 200 OK status code.  Error responses will provide details on validation failures.


## 2. Retrieve Deal Splits

This endpoint retrieves split information for specified deals.

**API Call:** `POST /crm/v3/objects/deals/splits/batch/read`

**Request Body:**

The request body is a JSON object with an `inputs` array containing the IDs of the deals.

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

**Example Request (cURL):**

```bash
curl -X POST \
  https://api.hubapi.com/crm/v3/objects/deals/splits/batch/read \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "inputs": [
      {"id": "5315919905"},
      {"id": "17137567105"}
    ]
  }'
```

**Response:**

The response includes the `status` ("COMPLETE"), `results` (an array of deals with their splits), `startedAt`, and `completedAt` timestamps.  Each deal's split information contains:

* `id`: Deal ID
* `splits`: An array of split objects, each with:
    * `id`: Split ID
    * `properties`: Object with `hs_deal_split_percentage` and `hubspot_owner_id`
    * `createdAt`: Timestamp
    * `updatedAt`: Timestamp
    * `archived`: Boolean indicating if the split is archived


```json
{
  "status": "COMPLETE",
  "results": [
    {
      "id": "17137567105",
      "splits": [
        // ... split objects ...
      ]
    },
    {
      "id": "5315919905",
      "splits": [
        // ... split objects ...
      ]
    }
  ],
  "startedAt": "2024-03-11T19:56:42.555Z",
  "completedAt": "2024-03-11T19:56:42.596Z"
}
```

Remember to replace `YOUR_API_KEY` with your actual HubSpot API key.  Error handling should be implemented in your application to manage potential API errors.
