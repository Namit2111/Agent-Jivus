# HubSpot CRM API: Deal Splits

This document describes the HubSpot CRM API endpoints for managing deal splits.  Deal splits allow distributing credit for deal amounts among multiple users. This functionality requires a Sales Hub Enterprise subscription.

## Endpoints

### 1. Create or Update Deal Splits

**Endpoint:** `POST /crm/v3/objects/deals/splits/batch/upsert`

This endpoint allows creating new deal splits or updating existing ones.  The request body is a JSON array of deal objects, each containing an `id` and a `splits` array.

**Request Body:**

```json
{
  "inputs": [
    {
      "id": 5315919905, // Deal ID
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

**Request Headers:**  (Standard HubSpot API authentication headers are required)

**Validation Rules:**

* The deal's owner must be included as a split owner.
* The sum of `percentage` values in the `splits` array must equal 1.0.
*  You must adhere to the split user maximum and split percentage minimum limits defined in your deal split settings.  Failure to meet these requirements will result in an error.


**Response:**  A success response indicates that the deal splits were successfully updated or created. An error response will include details about any validation failures.


### 2. Retrieve Deal Splits

**Endpoint:** `POST /crm/v3/objects/deals/splits/batch/read`

This endpoint retrieves split information for specified deals.  The request body is a JSON array of deal IDs.

**Request Body:**

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

**Request Headers:** (Standard HubSpot API authentication headers are required)

**Response:**

```json
{
  "status": "COMPLETE",
  "results": [
    {
      "id": "17137567105",
      "splits": [
        {
          "id": "311226010924",
          "properties": {
            "hs_deal_split_percentage": "0.5",
            "hubspot_owner_id": "41629779"
          },
          "createdAt": "2024-03-11T19:55:26.219Z",
          "updatedAt": "2024-03-11T19:55:26.219Z",
          "archived": false
        },
        // ... more splits for this deal
      ]
    },
    {
      "id": "5315919905",
      "splits": [
        // ... splits for this deal
      ]
    }
  ],
  "startedAt": "2024-03-11T19:56:42.555Z",
  "completedAt": "2024-03-11T19:56:42.596Z"
}
```

The response includes the `status`,  `results` (an array of deals with their splits), and timestamps indicating when the request started and completed.  Each split includes its ID, properties (percentage and owner ID), creation and update timestamps, and an `archived` flag.


##  Error Handling

The API will return appropriate HTTP status codes and error messages to indicate failures, such as invalid input data or API authentication issues.  Check the response for detailed error information.

##  Rate Limits

Be mindful of HubSpot's API rate limits to avoid exceeding allowed requests per minute.


This documentation provides a comprehensive overview of the HubSpot CRM Deal Splits API. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
