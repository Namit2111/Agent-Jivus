# HubSpot CRM API: Fees

This document describes the HubSpot CRM API endpoint for managing fees. Fees are used in conjunction with discounts and taxes when calculating the final price of a quote.

## Create a Fee

To create a fee, send a POST request to the following endpoint:

```
POST https://api.hubspi.com/crm/v3/objects/fee
```

**Request Body:**

The request body should be a JSON object with a `properties` field.  The `properties` field contains the fee details.  Currently, only percentage-based fees are supported.

```json
{
  "properties": {
    "hs_label": "A percentage-based fee of 10%",
    "hs_type": "PERCENT",
    "hs_value": "10"
  }
}
```

* **hs_label (string):** A human-readable label for the fee.
* **hs_type (string):**  The type of fee. Currently only `"PERCENT"` is supported.
* **hs_value (string):** The value of the fee. For percentage-based fees, this is the percentage (e.g., "10" for 10%).


**Response:**

Upon successful creation, the API will return a JSON object containing the newly created fee's properties, including its unique ID.  The exact structure of the response may vary, but it will include at least the `id` property.  Refer to the HubSpot API documentation for the complete response structure.  Example response (structure may vary):

```json
{
  "id": "12345",
  "properties": {
    "hs_label": "A percentage-based fee of 10%",
    "hs_type": "PERCENT",
    "hs_value": "10"
  }
}
```


## Retrieve Fees

To retrieve a list of fees, send a GET request to the following endpoint:

```
GET https://api.hubspi.com/crm/v3/objects/fee
```

The response will be a JSON array containing the properties of all existing fees.  Use appropriate query parameters (refer to the HubSpot API documentation) for pagination and filtering.


## Associate a Fee with a Quote

After creating a fee, you can associate it with a quote using the quote's API endpoint.  The exact method for association will depend on the quote API's specifics (refer to the HubSpot Quote API documentation).  This typically involves including the fee's ID in the quote's properties or related objects.


## Error Handling

The API will return appropriate HTTP status codes and error messages in case of failures.  Refer to the HubSpot API documentation for details on error handling and response codes.


##  Further Information

For a complete list of endpoints and their required/optional fields, refer to the official HubSpot API documentation for the CRM Fees endpoint.  This documentation provides detailed information about request parameters, response structures, and error handling.  Remember to consult the HubSpot API documentation for the most up-to-date information and details.
