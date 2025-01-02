# HubSpot CRM API: Line Items

This document details the HubSpot CRM API endpoints for managing line items.  Line items represent individual instances of products associated with deals, quotes, invoices, payment links, or subscriptions.

## API Endpoints

All endpoints are located under the `/crm/v3/objects/line_items` base path.  Replace `{lineItemId}` with the actual ID of the line item.  The base URL for all API calls is `https://api.hubapi.com`.

### 1. Create a Line Item (POST)

**Endpoint:** `/crm/v3/objects/line_items`

**Method:** `POST`

**Request Body:**  JSON payload containing line item properties and optional associations.

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
    "name": "New line item associated with deal",
    "hs_product_id": 45678 //Optional: ID of an existing product
  },
  "associations": [
    {
      "to": {
        "id": 12345
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 20 // Association type for Deals
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created line item, including its ID.

**Notes:**

* Line items belong to a single parent object.  Associating with multiple parent objects simultaneously is not supported.
* `price` cannot be negative.
* `hs_recurring_billing_period` accepts ISO-8601 period formats (PnYnMnD and PnW).


### 2. Retrieve a Line Item (GET)

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}` (single) or `/crm/v3/objects/line_items` (multiple)

**Method:** `GET`

**Query Parameters (for multiple line items):**

* `properties`: Comma-separated list of properties to return.  Ignored properties are omitted.
* `propertiesWithHistory`: Comma-separated list of properties to return with history.

**Response:**  A JSON object representing the requested line item(s).


### 3. Update a Line Item (PATCH)

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`

**Method:** `PATCH`

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

**Response:** A JSON object representing the updated line item.


### 4. Delete a Line Item (DELETE)

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`

**Method:** `DELETE`

**Response:**  A success indicator (usually a 204 No Content status code).


## Line Item Properties

This table lists common line item properties.  A complete list can be retrieved via a GET request to `/crm/v3/properties/line_item`.

| Property Name             | UI Label      | Description                                                                  |
|--------------------------|----------------|------------------------------------------------------------------------------|
| `name`                    | Name           | Name of the line item.                                                       |
| `description`            | Description    | Full description of the product.                                             |
| `hs_sku`                  | SKU            | Unique product identifier.                                                   |
| `hs_recurring_billing_start_date` | Billing start date | Recurring billing start date.                                                |
| `hs_recurring_billing_end_date`  | Billing end date  | Recurring billing end date.                                                 |
| `recurringbillingfrequency` | Billing frequency | How often a recurring line item is billed.                                |
| `quantity`                | Quantity       | Number of units.                                                            |
| `price`                   | Unit price     | Cost per unit.                                                              |
| `amount`                  | Net price      | Total cost (quantity * unit price).                                          |
| `currency`                | Currency       | Currency code (e.g., USD).                                                  |
| `hs_product_id`           | Product ID     | ID of an existing HubSpot product (optional, for associating with a product)|


This documentation provides a comprehensive overview of the HubSpot CRM API for managing line items.  Refer to the HubSpot API documentation for further details and authentication information.
