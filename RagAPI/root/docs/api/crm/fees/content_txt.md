# HubSpot CRM API: Fees

This document describes the HubSpot CRM API endpoint for managing fees. Fees are used in conjunction with discounts and taxes when calculating the final price of a quote.

## Creating a Fee

To create a fee, send a POST request to the following endpoint:

```
POST https://api.hubapi.com/crm/v3/objects/fee
```

The request body should be a JSON object with the following properties:

* `"properties"`: An object containing the fee properties.  The following properties are required:

    * `"hs_label"` (string): A human-readable label for the fee (e.g., "A percentage-based fee of 10%").
    * `"hs_type"` (string): The type of fee.  Currently, only `"PERCENT"` is supported.
    * `"hs_value"` (string or number): The value of the fee.  For `"PERCENT"` type, this is a numerical percentage (e.g., "10" for 10%).


**Example Request (Percentage Fee):**

```json
{
  "properties": {
    "hs_label": "A percentage-based fee of 10%",
    "hs_type": "PERCENT",
    "hs_value": "10"
  }
}
```

**Example Response (Successful Creation):**

A successful response will return a JSON object containing the newly created fee's details, including its ID.  The exact structure of the response may vary, but it will include a `id` property.  Example:

```json
{
  "id": "1234567890",
  // ... other properties ...
}
```

**Error Handling:** The API will return an appropriate HTTP error code and a JSON error response in case of failure (e.g., 400 Bad Request for invalid input).


## Retrieving Fees

To retrieve a list of fees, send a GET request to the following endpoint:

```
GET https://api.hubapi.com/crm/v3/objects/fee
```

You can add query parameters to filter and paginate the results. Refer to the HubSpot API documentation for details on available query parameters.


## Associating Fees with Quotes

After creating a fee, you can associate it with a quote using the quote's API endpoint.  The exact method for associating will depend on the quote API's specifications.  Consult the HubSpot API documentation for quotes for details.

##  Endpoint Summary

| Method | Endpoint                  | Description                                      | Request Body       | Response                     |
|--------|---------------------------|--------------------------------------------------|----------------------|------------------------------|
| POST    | `/crm/v3/objects/fee`    | Create a new fee                               | JSON (see example) | JSON (fee details including ID) |
| GET     | `/crm/v3/objects/fee`    | Retrieve a list of fees                         | None                 | JSON (array of fee details)    |


**Note:** This documentation is based on the provided text.  Always refer to the official HubSpot API documentation for the most up-to-date information and details on error handling, rate limits, and other important considerations.  The provided `https://api.hubspi.com` URL in the example is likely a typo and should be `https://api.hubapi.com`.
