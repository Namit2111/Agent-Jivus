# HubSpot CRM API: Products

This document details the HubSpot CRM API endpoints for managing products.  Products represent goods or services sold, allowing for easy addition to deals, quote generation, and performance reporting.

## I.  Creating a Product

To create a product, send a `POST` request to:

`/crm/v3/objects/products`

**Request Body:**

```json
{
  "properties": {
    "name": "Product Name",
    "price": "100.00",  // Price as a string
    "hs_sku": "SKU123", // HubSpot SKU
    "description": "Product Description",
    "hs_cost_of_goods_sold": "50.00", // Cost of Goods Sold
    "hs_recurring_billing_period": "P12M" // Recurring billing period (e.g., P12M for 12 months)
  }
}
```

**Example Request (cURL):**

```bash
curl -X POST \
  https://api.hubapi.com/crm/v3/objects/products \
  -H 'Content-Type: application/json' \
  -d '{
    "properties": {
      "name": "Implementation Service",
      "price": "6000.00",
      "hs_sku": "123456",
      "description": "Onboarding service for data product",
      "hs_cost_of_goods_sold": "600.00",
      "hs_recurring_billing_period": "P12M"
    }
  }' \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**  A successful request returns a `201 Created` status code and the newly created product's details including its ID.


**Retrieving Product Properties:**

To see all available product properties, make a `GET` request to:

`/crm/v3/properties/products`


## II. Associating Products (Line Items)

Products cannot be directly associated with other CRM objects.  Instead, use *line items*. Line items represent individual instances of products within deals or quotes.

### A. Create and Associate a Line Item (Multiple Calls)

1. **Create a Line Item:** Send a `POST` request to:

   `/crm/v3/objects/line_items`

   **Request Body:**

   ```json
   {
     "properties": {
       "quantity": 1,
       "hs_object_id": "1234567", // Product ID
       "name": "Line Item Name"
     }
   }
   ```

2. **Associate Line Item:** After creating the line item, obtain its ID from the response. Then, use a `PUT` request to associate it with a deal:

   `/crm/v4/objects/line_items/{line_item_id}/associations/default/deals/{deal_id}`

   Replace `{line_item_id}` and `{deal_id}` with the respective IDs.


### B. Create and Associate a Line Item (Single Call)

Create and associate a line item in a single call by including the `associations` array in the line item creation request:

**Request Body:**

```json
{
  "properties": {
    "quantity": 1,
    "hs_object_id": "1234567", // Product ID
    "name": "Line Item Name"
  },
  "associations": [
    {
      "to": {
        "id": "14795354663" // Deal ID
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 20 // Association type ID for line item - deal
        }
      ]
    }
  ]
}
```

**Important Note:** Line items belong to a single parent object.  Creating separate line items for deals and quotes is crucial to prevent data loss.  Deleting a quote, for example, also deletes its associated line items.


## III. Error Handling

The API will return appropriate HTTP status codes (e.g., 400 Bad Request, 404 Not Found, etc.) and error messages in the response body to indicate any issues.  Refer to the HubSpot API documentation for detailed error codes.


## IV. Authentication

All requests require an API key. Include your API key in the `Authorization` header as a Bearer token.  (e.g., `Authorization: Bearer YOUR_API_KEY`).  Replace `YOUR_API_KEY` with your actual API key.


This markdown provides a comprehensive overview of the HubSpot CRM API's product management features.  Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
