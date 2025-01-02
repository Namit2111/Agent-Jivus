# HubSpot CRM API: Line Items

This document describes the HubSpot CRM API endpoints for managing line items. Line items represent individual instances of products associated with deals, quotes, invoices, payment links, or subscriptions.  This API allows you to create, retrieve, update, and delete line items, synchronizing data between HubSpot and external systems.

## API Endpoints

All endpoints are located under the `/crm/v3/objects/line_items` base path.  Replace `{lineItemId}` with the actual ID of the line item.  All requests require proper API key authentication.


### 1. Create a Line Item (POST)

**Endpoint:** `/crm/v3/objects/line_items`

**Method:** `POST`

**Request Body:**

The request body must include a `properties` object containing line item details.  You can optionally include an `associations` array to link the line item to other HubSpot objects (deals, quotes, etc.).

**Example Request (JSON):**

```json
{
  "properties": {
    "price": 10,
    "quantity": 1,
    "name": "New standalone line item",
    "hs_product_id": 123 // Optional: ID of an existing HubSpot product
  },
  "associations": [
    {
      "to": {
        "id": 12345 // ID of the associated object (e.g., deal ID)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 20 // Association type ID (check HubSpot documentation for available types)
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created line item, including its ID.


**Important Considerations:**

* Line items belong to a single parent object.  Creating multiple associations is not supported.
* The `price` property cannot be negative.
* The `hs_recurring_billing_period` property (Term) accepts ISO-8601 period formats (PnYnMnD and PnW).


### 2. Retrieve a Line Item (GET)

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}` (for a single line item) or `/crm/v3/objects/line_items` (for multiple line items)

**Method:** `GET`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.  If a property is not found, it's ignored.
* `propertiesWithHistory`: Comma-separated list of properties to return with their history.

**Example Request (GET single line item):**

`/crm/v3/objects/line_items/1234?properties=name,price,quantity`

**Response:**  A JSON object (single line item) or a JSON array (multiple line items) containing the requested line item data.


### 3. Update a Line Item (PATCH)

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`

**Method:** `PATCH`

**Request Body:**

Only the properties to be updated need to be included.  Associations cannot be updated via this method; use the associations API instead.

**Example Request (JSON):**

```json
{
  "properties": {
    "price": 25,
    "quantity": 3,
    "name": "Updated line item"
  }
}
```

**Response:** A JSON object representing the updated line item.


### 4. Delete a Line Item (DELETE)

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`

**Method:** `DELETE`

**Response:** A successful deletion returns a 204 No Content status code.


## Line Item Properties

The following are common line item properties:  A complete list can be retrieved via a `GET` request to `/crm/v3/properties/line_item`.

| Property Name             | Label in UI    | Description                                         |
|--------------------------|----------------|-----------------------------------------------------|
| `name`                    | Name           | Name of the line item                               |
| `description`            | Description    | Full description of the product                     |
| `hs_sku`                  | SKU            | Unique product identifier                           |
| `hs_recurring_billing_start_date` | Billing start date | Recurring billing start date                         |
| `hs_recurring_billing_end_date`  | Billing end date  | Recurring billing end date                          |
| `recurringbillingfrequency` | Billing frequency | How often a recurring line item is billed           |
| `quantity`                | Quantity       | Number of units                                     |
| `price`                   | Unit price     | Cost per unit                                       |
| `amount`                  | Net price      | Total cost (quantity * unit price)                  |
| `currency`                | Currency       | Currency code (e.g., USD)                          |


## Error Handling

Refer to the HubSpot API documentation for detailed information on error codes and responses.


This documentation provides a comprehensive overview.  Always refer to the official HubSpot API documentation for the most up-to-date information and details.
