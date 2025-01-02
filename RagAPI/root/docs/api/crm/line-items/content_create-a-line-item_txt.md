# HubSpot CRM API: Line Items

This document details the HubSpot CRM API endpoints for managing line items. Line items represent individual instances of products associated with deals, quotes, invoices, payment links, or subscriptions.  This API allows for creating, retrieving, updating, and deleting line items, enabling synchronization between HubSpot and external systems.

## API Endpoints

All endpoints are located under the `/crm/v3/objects/line_items` base path.  Replace `{lineItemId}` with the actual ID of the line item.

**Base URL:** `https://api.hubapi.com/crm/v3/objects/line_items`

### 1. Create a Line Item (POST)

* **Endpoint:** `/crm/v3/objects/line_items`
* **Method:** `POST`
* **Request Body:** JSON object with the following structure:

```json
{
  "properties": {
    "name": "Line Item Name",
    "price": 10.00,
    "quantity": 1,
    "hs_product_id": 123  // Optional: ID of an existing product
    // ... other properties (see "Line Item Properties" section)
  },
  "associations": [ // Optional: Associate with Deals, Quotes, etc.
    {
      "to": {
        "id": 12345  // ID of the associated object (Deal, Quote, etc.)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 20 // Association type ID (e.g., 20 for Deals)
        }
      ]
    }
  ]
}
```

* **Response:**  A JSON object representing the newly created line item, including its ID.  Example:

```json
{
  "id": "new_line_item_id",
  "properties": {
    "name": "Line Item Name",
    "price": 10.00,
    "quantity": 1,
    // ... other properties
  }
}
```

* **Note:**  Line items can only belong to one parent object.  Creating multiple associations to different parent objects within a single line item is not supported.  The `price` property cannot be negative. The `hs_recurring_billing_period` property accepts ISO-8601 period formats (PnYnMnD and PnW).


### 2. Retrieve a Line Item (GET)

* **Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`  or `/crm/v3/objects/line_items` (for all line items)
* **Method:** `GET`
* **Query Parameters:**
    * `properties`: Comma-separated list of properties to return.
    * `propertiesWithHistory`: Comma-separated list of properties to return with their history.
* **Response:** A JSON object (single line item) or a JSON array (multiple line items) representing the retrieved line item(s).


### 3. Update a Line Item (PATCH)

* **Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`
* **Method:** `PATCH`
* **Request Body:** JSON object containing only the properties to be updated.  Associations cannot be updated using this method; use the Associations API instead.

```json
{
  "properties": {
    "price": 25.00,
    "quantity": 3,
    "name": "Updated Line Item Name"
  }
}
```

* **Response:** A JSON object representing the updated line item.


### 4. Delete a Line Item (DELETE)

* **Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`
* **Method:** `DELETE`
* **Response:**  A successful deletion typically returns a 204 No Content status code.


## Line Item Properties

The following table lists common line item properties.  A complete list can be retrieved via a GET request to `/crm/v3/properties/line_item`.

| Property Name             | Label in UI    | Description                                                                    |
|--------------------------|----------------|--------------------------------------------------------------------------------|
| `name`                    | Name           | The name of the line item.                                                     |
| `description`             | Description    | Full description of the product.                                                |
| `hs_sku`                  | SKU            | Unique product identifier.                                                    |
| `hs_recurring_billing_start_date` | Billing start date | Recurring billing start date for a line item.                               |
| `hs_recurring_billing_end_date`  | Billing end date  | Recurring billing end date for a line item.                                 |
| `recurringbillingfrequency` | Billing frequency | How often a recurring line item is billed.                                     |
| `quantity`                | Quantity       | How many units of a product are included.                                     |
| `price`                   | Unit price     | The cost of a single unit of the product.                                     |
| `amount`                  | Net price      | The total cost of the line item (quantity * unit price).                     |
| `currency`                | Currency       | Currency code for the line item (e.g., USD, EUR).                             |


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Error responses will typically include a JSON object with details about the error.  Refer to the HubSpot API documentation for a complete list of error codes and their meanings.


This documentation provides a comprehensive overview of the HubSpot CRM Line Items API.  For more detailed information and specific examples, refer to the official HubSpot API documentation.
