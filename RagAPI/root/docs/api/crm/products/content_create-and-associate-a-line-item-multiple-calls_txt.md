# HubSpot CRM API: Products

This document details the HubSpot CRM API endpoints for managing products.  Products in HubSpot represent goods or services you sell, allowing for easy addition to deals, quote generation, and performance reporting.  This API allows management and synchronization of product data between HubSpot and external systems.

## I. Product Management

### A. Creating a Product

To create a product, send a `POST` request to:

`/crm/v3/objects/products`

The request body should include a `properties` object containing the product's attributes.  You can subsequently update these properties via a `PATCH` request to the same endpoint.

**Request:**

```json
{
  "properties": {
    "name": "Implementation Service",
    "price": "6000.00",
    "hs_sku": "123456",
    "description": "Onboarding service for data product",
    "hs_cost_of_goods_sold": "600.00",
    "hs_recurring_billing_period": "P12M"
  }
}
```

`hs_recurring_billing_period` follows the format `P#M`, where `#` is the number of months.

**To retrieve all available product properties:** Send a `GET` request to `/crm/v3/properties/products`.


### B. Associating Products

Products cannot be directly associated with other CRM objects.  Instead, use **line items**. Line items represent individual instances of products and are associated with deals or quotes.  This allows tailoring goods/services without modifying the product itself.  Line items belong to a single parent object.


## II. Line Item Management

### A. Creating and Associating a Line Item (Multiple Calls)

This method involves two separate API calls:

1. **Create Line Item:** Send a `POST` request to `/crm/v3/objects/line_item`.  Include `hs_object_id` (product ID) and other relevant properties.

**Request:**

```json
{
  "properties": {
    "quantity": 1,
    "hs_object_id": "1234567", // Product ID
    "name": "New line item (product-based)"
  }
}
```

The response contains the newly created line item's ID.

2. **Associate Line Item:** Send a `PUT` request to associate the line item with a deal. Replace placeholders with actual IDs.

`/crm/v4/objects/line_items/{lineItemId}/associations/default/deals/{dealId}`

**Request (example):**

```
PUT /crm/v4/objects/line_items/7791176460/associations/default/deals/14795354663
```

**Response (example):**

```json
{
  "status": "COMPLETE",
  "results": [
    {
      "from": { "id": "14795354663" },
      "to": { "id": "7791176460" },
      "associationSpec": {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 19
      }
    },
    // ...
  ],
  "startedAt": "2023-12-21T20:06:52.083Z",
  "completedAt": "2023-12-21T20:06:52.192Z"
}
```

**To retrieve all available line item properties:** Send a `GET` request to `/crm/v3/properties/line_items`.


### B. Creating and Associating a Line Item (Single Call)

This method creates and associates a line item in a single call.

**Request:**

```json
{
  "properties": {
    "quantity": 1,
    "hs_object_id": "1234567", // Product ID
    "name": "New line item (product-based)"
  },
  "associations": [
    {
      "to": { "id": "14795354663" }, // Deal ID
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 20
        }
      ]
    }
  ]
}
```

The `associationTypeId` (20 in this example) defines the association type between line items and deals.  Consult HubSpot's documentation for other association types.


## III. Error Handling

The API responses include standard HTTP status codes to indicate success or failure.  Refer to the HubSpot API documentation for details on specific error codes and their meanings.


## IV.  Authentication

You need a HubSpot API key for authentication.  Include the key in the request header as `Authorization: Bearer YOUR_API_KEY`.  Refer to HubSpot's API documentation for detailed authentication instructions.
