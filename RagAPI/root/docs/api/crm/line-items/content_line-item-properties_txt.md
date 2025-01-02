# HubSpot CRM API: Line Items

This document describes the HubSpot CRM API endpoints for managing line items. Line items represent individual instances of products associated with deals, quotes, invoices, payment links, or subscriptions.  This API allows for creating, retrieving, updating, and deleting line items, synchronizing data between HubSpot and external systems.

## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/objects/line_items`

### 1. Create a Line Item

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/line_items`

**Request Body:**  JSON payload containing line item properties and associations.

**Example Request Body (Standalone Line Item):**

```json
{
  "properties": {
    "price": 10,
    "quantity": 1,
    "name": "New standalone line item"
  }
}
```

**Example Request Body (Line Item associated with Deal ID 12345):**

```json
{
  "properties": {
    "price": 10,
    "quantity": 1,
    "name": "Line item associated with deal",
    "hs_product_id": "product_id_goes_here" //Optional: if based on existing product
  },
  "associations": [
    {
      "to": {
        "id": 12345
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 20 // Association type ID for deals
        }
      ]
    }
  ]
}
```

**Response:**  JSON object representing the created line item, including its ID.

**Note:**  Line items can only belong to one parent object.  Creating duplicate associations will result in data inconsistencies. The `price` property cannot be negative.  The `hs_recurring_billing_period` property accepts ISO-8601 period formats (PnYnMnD and PnW).


### 2. Retrieve a Line Item

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`  (for a single line item)
             `/crm/v3/objects/line_items` (for all line items)

**Parameters:**

* `properties`: Comma-separated list of properties to return.  Ignored if properties don't exist.
* `propertiesWithHistory`: Comma-separated list of properties to return with their history. Ignored if properties don't exist.


**Example Request (Single Line Item):**

`GET /crm/v3/objects/line_items/123`

**Example Request (All Line Items with name and price):**

`GET /crm/v3/objects/line_items?properties=name,price`

**Response:** JSON array (for all line items) or JSON object (for a single line item) representing the requested line item(s).


### 3. Update a Line Item

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`

**Request Body:** JSON payload containing properties to update.  Associations cannot be updated via this method; use the Associations API instead.

**Example Request Body:**

```json
{
  "properties": {
    "price": 25,
    "quantity": 3,
    "name": "Updated line item"
  }
}
```

**Response:** JSON object representing the updated line item.


### 4. Delete a Line Item

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`

**Response:**  A successful deletion typically returns a 204 No Content status code.


## Line Item Properties

The following table lists common line item properties.  A complete list can be retrieved using: `GET /crm/v3/properties/line_item`

| Property Name                | UI Label      | Description                                                                 |
|-----------------------------|----------------|-----------------------------------------------------------------------------|
| `name`                       | Name           | Name of the line item.                                                       |
| `description`                | Description    | Full description of the product.                                              |
| `hs_sku`                     | SKU            | Unique product identifier.                                                   |
| `hs_recurring_billing_start_date` | Billing start date | Recurring billing start date.                                                |
| `hs_recurring_billing_end_date`  | Billing end date  | Recurring billing end date.                                                 |
| `recurringbillingfrequency` | Billing frequency | How often a recurring line item is billed (not applicable for one-time billing). |
| `quantity`                   | Quantity       | Number of units.                                                              |
| `price`                      | Unit price     | Cost per unit.                                                              |
| `amount`                     | Net price      | Total cost (quantity * unit price).                                          |
| `currency`                   | Currency       | Currency code (e.g., USD).                                                  |
| `hs_product_id`             | Product ID    | ID of the associated HubSpot product (optional).                           |


This documentation provides a comprehensive overview of the HubSpot CRM API for managing line items.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details on error handling and authentication.
