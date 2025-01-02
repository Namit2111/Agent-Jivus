# HubSpot CRM API: Line Items

This document describes the HubSpot CRM API endpoints for managing line items. Line items represent individual instances of products associated with deals, quotes, invoices, payment links, or subscriptions.  This API allows for creating, retrieving, updating, and deleting line items, enabling synchronization with external systems.

## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/objects/line_items`

**Note:**  Requires HubSpot API Key authentication.  See HubSpot's API documentation for details on authentication.

### 1. Create a Line Item (POST)

**Endpoint:** `/crm/v3/objects/line_items`

**Method:** `POST`

**Request Body:**

```json
{
  "properties": {
    "name": "Line Item Name",
    "quantity": 1,
    "price": 10.00,
    "hs_product_id": "product_id" // Optional: ID of an existing HubSpot product
    // Add other properties as needed (see "Line Item Properties" section)
  },
  "associations": [ // Optional: Associate with a Deal, Quote, etc.
    {
      "to": {
        "id": 12345 // ID of the associated object (Deal, Quote, etc.)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 20 // Association type ID (see HubSpot documentation for IDs)
        }
      ]
    }
  ]
}
```

**Response:** (On success)  A JSON object representing the created line item, including its ID.

**Example Request (curl):**

```bash
curl -X POST \
  https://api.hubapi.com/crm/v3/objects/line_items \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "properties": {
      "name": "Example Line Item",
      "quantity": 2,
      "price": 25.50
    }
  }'
```

**Important Notes:**

* Line items belong to a single parent object.  Associating with multiple parent objects of the same type is not allowed.
* The `price` property cannot be negative.
* `hs_recurring_billing_period` accepts ISO-8601 period formats (PnYnMnD and PnW).


### 2. Retrieve a Line Item (GET)

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`

**Method:** `GET`

**Parameters:**

* `lineItemId`: The ID of the line item to retrieve.
* `properties`: Comma-separated list of properties to return (optional).
* `propertiesWithHistory`: Comma-separated list of properties to return with history (optional).


**Response:** A JSON object representing the line item.

**Example Request (curl):**

```bash
curl -X GET \
  https://api.hubapi.com/crm/v3/objects/line_items/123 \
  -H 'Authorization: Bearer YOUR_API_KEY'
```


**Endpoint (all line items):** `/crm/v3/objects/line_items`

**Method:** `GET`

**Parameters:** (Same as above)

**Response:** A JSON object containing a list of line items.


### 3. Update a Line Item (PATCH)

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`

**Method:** `PATCH`

**Request Body:**

```json
{
  "properties": {
    "price": 30.00,
    "quantity": 5
    // Update other properties as needed
  }
}
```

**Response:** (On success) A JSON object representing the updated line item.

**Note:** Associations cannot be updated using this method. Use the Associations API for managing associations.

### 4. Delete a Line Item (DELETE)

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`

**Method:** `DELETE`

**Response:** (On success)  A successful HTTP status code (e.g., 204 No Content).


## Line Item Properties

To retrieve a complete list of available properties, make a `GET` request to: `/crm/v3/properties/line_item`

| Property Name             | Label in UI     | Description                                                                    |
|--------------------------|-----------------|--------------------------------------------------------------------------------|
| `name`                   | Name            | The name of the line item.                                                     |
| `description`            | Description     | Full description of the product.                                                |
| `hs_sku`                 | SKU             | Unique product identifier.                                                      |
| `hs_recurring_billing_start_date` | Billing start date | Recurring billing start date.                                                  |
| `hs_recurring_billing_end_date`  | Billing end date  | Recurring billing end date.                                                   |
| `recurringbillingfrequency` | Billing frequency | How often a recurring billing line item is billed.                            |
| `quantity`               | Quantity        | How many units of a product are included in this line item.                    |
| `price`                  | Unit price      | The cost of a single unit of the product.                                      |
| `amount`                 | Net price       | The total cost of the line item (quantity * price).                            |
| `currency`               | Currency        | Currency code for the line item (e.g., USD, EUR).                              |


This documentation provides a concise overview. Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications, including error codes and handling.
