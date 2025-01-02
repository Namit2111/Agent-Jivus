# HubSpot CRM API: Deal Splits

This document describes the HubSpot CRM API endpoints for managing deal splits.  Deal splits allow assigning credit for a deal's amount across multiple users. This functionality requires a Sales Hub Enterprise subscription.

## API Endpoints

The API uses two main endpoints: one for creating or updating deal splits and another for retrieving them.  Both endpoints use a batch approach, allowing for multiple deal operations in a single request.

**1. Create or Update Deal Splits:**

* **Endpoint:** `POST /crm/v3/objects/deals/splits/batch/upsert`
* **Method:** `POST`
* **Request Body:**  A JSON object with an `inputs` array. Each element in the array represents a deal and its splits.

    ```json
    {
      "inputs": [
        {
          "id": 5315919905, // Deal ID (obtained via the Deals API)
          "splits": [
            {
              "ownerId": 41629779, // HubSpot User ID
              "percentage": 0.5
            },
            {
              "ownerId": 60158084, // HubSpot User ID
              "percentage": 0.5
            }
          ]
        }
      ]
    }
    ```

* **Request Fields:**
    * `id`: The ID of the deal.  Required.
    * `splits`: An array of split objects.  Required.  Each split object must contain:
        * `ownerId`: The ID of the HubSpot user receiving a portion of the deal credit. Required.
        * `percentage`: The percentage of the deal amount assigned to the owner (e.g., 0.5 for 50%). Must be a number between 0 and 1. Required.

* **Constraints:**
    * The deal's owner must be included as a split owner.
    * The sum of `percentage` values for a deal must equal 1.0.
    * You must adhere to the minimum split percentage and maximum split users limits defined in your HubSpot deal split settings.  Failure to meet these requirements will result in an error response.

* **Response:**  Success indicates the deal splits were updated or created successfully.  Error responses provide details about validation failures.


**2. Retrieve Deal Splits:**

* **Endpoint:** `POST /crm/v3/objects/deals/splits/batch/read`
* **Method:** `POST`
* **Request Body:** A JSON object with an `inputs` array containing the IDs of the deals for which you want to retrieve splits.

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

* **Request Fields:**
    * `id`: The ID of the deal. Required.

* **Response:** A JSON object with a `results` array.  Each element in the array contains the split information for a deal.

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
            }
            // ... more splits for this deal
          ]
        },
        // ... more deals
      ],
      "startedAt": "2024-03-11T19:56:42.555Z",
      "completedAt": "2024-03-11T19:56:42.596Z"
    }
    ```

* **Response Fields:**
    * `status`: Indicates the success or failure of the request (e.g., "COMPLETE").
    * `results`: An array of deal objects, each containing an `id` and a `splits` array.  Each split object includes:
        * `id`: The ID of the split.
        * `properties`:  Properties of the split, including `hs_deal_split_percentage` and `hubspot_owner_id`.
        * `createdAt`: Timestamp of the split's creation.
        * `updatedAt`: Timestamp of the split's last update.
        * `archived`: Boolean indicating whether the split is archived.


## Error Handling

Both endpoints return standard HubSpot API error responses in case of failures, including HTTP status codes and error details.  Refer to the HubSpot API documentation for detailed error handling.


## Authentication

You'll need a valid HubSpot API key to authenticate your requests.  Include your API key in the `Authorization` header as `Bearer <your_api_key>`.


This documentation provides a concise overview.  For complete details and additional information, refer to the official HubSpot API documentation.
