# HubSpot CRM API: Products

This document details the HubSpot CRM API endpoints for managing products.  Products represent goods or services sold, allowing for easy addition to deals, quote generation, and performance reporting.

## I. Creating a Product

To create a product, send a `POST` request to:

`/crm/v3/objects/products`

**Request Body:**

```json
{
  "properties": {
    "name": "Product Name",
    "price": "100.00",
    "hs_sku": "SKU123",
    "description": "Product Description",
    "hs_cost_of_goods_sold": "50.00",
    "hs_recurring_billing_period": "P12M" // Format: P#M (e.g., P12M for 12 months)
  }
}
```

* **`name`**: (Required) Product name.
* **`price`**: (Required) Product price.
* **`hs_sku`**:  Stock Keeping Unit.
* **`description`**: Product description.
* **`hs_cost_of_goods_sold`**: Cost of goods sold.
* **`hs_recurring_billing_period`**: Recurring billing period in months (P#M format).


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

**Response (201 Created):**  Returns the created product object with its ID.


**Retrieving Product Properties:**

To see all available product properties, make a `GET` request to:

`/crm/v3/properties/products`


## II. Associating Products (Line Items)

Products cannot be directly associated with other CRM objects (deals, quotes).  Instead, use **line items**.  Line items are individual instances of products and allow for tailored goods/services on deals or quotes without modifying the product itself.

**Important Note:** Line items belong to a single parent object.  Create separate line items for deals and quotes to prevent data loss.


### A. Create and Associate a Line Item (Multiple Calls)

1. **Create a Line Item:**  Send a `POST` request to:

   `/crm/v3/objects/line_item`

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

   * **`quantity`**: Quantity of the product.
   * **`hs_object_id`**: ID of the associated product.
   * **`name`**: Line item name.


2. **Associate the Line Item:** After creating the line item, get its ID from the response. Then, use the `PUT` request to associate it with a deal (or quote):

   `PUT /crm/v4/objects/line_items/{line_item_id}/associations/default/deals/{deal_id}`

   Replace `{line_item_id}` and `{deal_id}` with the respective IDs.


### B. Create and Associate a Line Item (Single Call)

Send a `POST` request to `/crm/v3/objects/line_item`:

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
          "associationTypeId": 20 // Association type for line item-deal
        }
      ]
    }
  ]
}
```

## III. Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Examine the response body for detailed error messages.


This documentation provides a comprehensive overview of the HubSpot CRM API for managing products and their associations.  Remember to replace placeholder IDs and API keys with your actual values.  Consult the official HubSpot API documentation for the most up-to-date information and details.
