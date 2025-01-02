# HubSpot CRM API: Fees

This document describes the HubSpot CRM API endpoint for managing fees. Fees are used in conjunction with discounts and taxes when calculating the final price of a quote.

## Create a Fee

To create a fee, send a POST request to the following endpoint:

**API Endpoint:**

`POST https://api.hubspi.com/crm/v3/objects/fee`

**Request Body:**

The request body must be a JSON object with a `properties` field.  The `properties` field contains the fee details.  Here's an example for creating a percentage-based fee:

```json
{
  "properties": {
    "hs_label": "A percentage-based fee of 10%",
    "hs_type": "PERCENT",
    "hs_value": "10"
  }
}
```

* **`hs_label` (string):** A human-readable label for the fee.  (Required)
* **`hs_type` (string):** The type of fee.  Currently, "PERCENT" is supported.  (Required)
* **`hs_value` (string):** The value of the fee. For a percentage-based fee, this is the percentage (e.g., "10" for 10%). (Required)


**Response:**

Upon successful creation, the API returns a JSON object representing the newly created fee, including its ID.  The exact structure of the response may vary, but will include at least the fee's ID.  For example:


```json
{
  "id": "1234567890",
  // ...other fee properties...
}
```

A non-2xx status code indicates an error. Check the response body for details.

## Retrieve Fees

To retrieve a list of created fees, send a GET request to:

**API Endpoint:**

`GET https://api.hubspi.com/crm/v3/objects/fee`

This endpoint will return a list of fees.  The exact format of the response will depend on the parameters used, but it will generally be an array of fee objects.

## Associating Fees with Quotes

After creating a fee, you can associate it with a quote using the quote's API endpoint (not detailed here).  The exact method will depend on the quote API's specifications.  The fee's ID obtained from the `POST` request above is needed for this association.


## Error Handling

The API will return appropriate HTTP status codes to indicate success or failure.  Examine the response body for detailed error messages.


## Note:

The provided API URL `https://api.hubspi.com/crm/v3/objects/fee` appears to have a typo (`hubspi` instead of `hubspot`).  The correct URL is likely `https://api.hubspot.com/crm/v3/objects/fee`.  Always refer to the official HubSpot API documentation for the most up-to-date information.
