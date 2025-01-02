# HubSpot CRM API: Line Items

This document details the HubSpot CRM API endpoints for managing line items. Line items represent individual instances of products associated with deals, quotes, invoices, payment links, or subscriptions.  This API allows for creation, retrieval, update, and deletion of line items, enabling synchronization with external systems.

## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/objects/line_items`

**Note:**  Replace `{lineItemId}` with the actual ID of the line item.  API keys are required for authentication; refer to the HubSpot API documentation for details.

### 1. Create a Line Item

**Method:** `POST`
**Endpoint:** `/crm/v3/objects/line_items`

**Request Body:**

The request body should be a JSON object with `properties` and optionally `associations`.

* **`properties` (required):**  An object containing line item properties.  See "Line Item Properties" section for details.  At minimum, `name`, `quantity`, and `price` are required. To base the line item on an existing product, include `hs_product_id`.

* **`associations` (optional):** An array of objects associating the line item with other HubSpot objects (e.g., deals, quotes). Each object requires a `to` field (containing the associated object's ID) and a `types` array (specifying the association type).

**Example Request (Associating with Deal ID 12345):**

```json
{
  "properties": {
    "price": 10,
    "quantity": 1,
    "name": "New standalone line item",
    "hs_product_id": "product_id_123" // Optional: ID of an existing product
  },
  "associations": [
    {
      "to": {
        "id": 12345
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 20 // Association type for deals
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the created line item, including its ID.

### 2. Retrieve a Line Item

**Method:** `GET`

* **Specific Line Item:**
    * **Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`
    * **Response:** A JSON object representing the specified line item.

* **All Line Items:**
    * **Endpoint:** `/crm/v3/objects/line_items`
    * **Query Parameters:**
        * `properties`: Comma-separated list of properties to return.
        * `propertiesWithHistory`: Comma-separated list of properties to return with history.
    * **Response:** A JSON object containing a list of line items.


### 3. Update a Line Item

**Method:** `PATCH`
**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`

**Request Body:**

A JSON object containing the `properties` to update.  You cannot update associations using this method; use the associations API instead.

**Example Request:**

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

### 4. Delete a Line Item

**Method:** `DELETE`
**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`

**Response:**  A success message (usually a 204 No Content status code).


## Line Item Properties

The following table lists common line item properties.  A complete list can be obtained via a `GET` request to `/crm/v3/properties/line_item`.

| Property Name             | UI Label     | Description                                                                   |
|--------------------------|---------------|-------------------------------------------------------------------------------|
| `name`                    | Name          | The name of the line item.                                                     |
| `description`            | Description   | Full description of the product.                                               |
| `hs_sku`                  | SKU           | Unique product identifier.                                                    |
| `hs_recurring_billing_start_date` | Billing start date | Recurring billing start date (ISO-8601 format: PnYnMnD or PnW).             |
| `hs_recurring_billing_end_date`  | Billing end date  | Recurring billing end date (ISO-8601 format: PnYnMnD or PnW).              |
| `recurringbillingfrequency` | Billing frequency | How often a recurring line item is billed.                                      |
| `quantity`                | Quantity      | Number of units.                                                              |
| `price`                   | Unit price    | Cost per unit. **Cannot be negative.**                                     |
| `amount`                  | Net price     | Total cost (quantity * unit price).                                          |
| `currency`                | Currency      | Currency code (e.g., USD).                                                   |
| `hs_product_id`           | Product ID    | ID of an existing HubSpot product.  If provided, the line item will use the product's data.|


**Important Considerations:**

* Line items belong to a single parent object.  Avoid associating the same line item with multiple parent objects.
* The `price` property cannot be negative.
* The `hs_recurring_billing_period` property accepts ISO-8601 period formats (PnYnMnD and PnW).


This documentation provides a comprehensive overview of the HubSpot CRM API for managing line items.  Consult the official HubSpot API documentation for the most up-to-date information and details on error handling and rate limits.
