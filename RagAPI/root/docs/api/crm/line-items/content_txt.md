# HubSpot CRM API: Line Items

This document details the HubSpot CRM API endpoints for managing line items. Line items represent individual instances of products associated with deals, quotes, invoices, payment links, or subscriptions.

## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/objects/line_items`

### 1. Create a Line Item

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/line_items`

**Request Body:**

```json
{
  "properties": {
    "price": 10,
    "quantity": 1,
    "name": "New standalone line item",
    "hs_product_id": 1234 // Optional: ID of an existing product
  },
  "associations": [
    {
      "to": {
        "id": 12345 // ID of associated object (deal, quote, etc.)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 20 // Association type ID (e.g., 20 for deals)
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created line item, including its ID.

**Notes:**

*   `hs_product_id` is optional. If omitted, a standalone line item is created.
*   `associations` array allows linking to multiple objects.  Specify the appropriate `associationTypeId` for each object type.
*   The `price` property cannot be negative.
*   Line items should be individual to each parent object (deal, quote, etc.).  Associating the same line item to multiple objects is not supported.


### 2. Retrieve a Line Item

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`

**Parameters:**

*   `lineItemId`: The ID of the line item to retrieve.

**Optional Query Parameters:**

*   `properties`: Comma-separated list of properties to return.
*   `propertiesWithHistory`: Comma-separated list of properties to return with their history.

**Response:** A JSON object representing the line item.


**Bulk Retrieval:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/line_items`

**Optional Query Parameters:** (Same as above)

**Response:** A JSON array containing multiple line items.


### 3. Update a Line Item

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`

**Request Body:**

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

**Notes:** Associations cannot be updated via this method. Use the associations API for that.


### 4. Delete a Line Item

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/line_items/{lineItemId}`

**Response:**  A success indicator (typically a 204 No Content status code).


## Line Item Properties

The following are common line item properties:

| Property Name             | Label in UI     | Description                                                              |
|--------------------------|-----------------|--------------------------------------------------------------------------|
| `name`                    | Name            | The name of the line item.                                               |
| `description`            | Description     | Full description of the product.                                         |
| `hs_sku`                  | SKU             | Unique product identifier.                                              |
| `hs_recurring_billing_start_date` | Billing start date | Recurring billing start date.                                           |
| `hs_recurring_billing_end_date`  | Billing end date  | Recurring billing end date.                                             |
| `recurringbillingfrequency` | Billing frequency | How often a recurring line item is billed (ISO-8601 PnYnMnD, PnW).       |
| `quantity`                | Quantity        | How many units of a product are included.                               |
| `price`                   | Unit price      | The cost of a single unit of the product.                               |
| `amount`                  | Net price       | The total cost of the line item (quantity * unit price).                |
| `currency`                | Currency        | Currency code for the line item (e.g., USD).                           |


To retrieve all available properties, make a `GET` request to `/crm/v3/properties/line_item`.


##  Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Check the response body for detailed error messages.


## Rate Limits

Be aware of HubSpot's API rate limits to avoid exceeding allowed requests per minute/hour. Refer to the HubSpot API documentation for details.
