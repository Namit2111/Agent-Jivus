# HubSpot CRM API: Products

This document details the HubSpot CRM API endpoints for managing products. Products represent goods or services sold and are crucial for adding products to deals, generating quotes, and reporting on performance.  This API allows syncing product data between HubSpot and other systems.

## Understanding HubSpot Products

Products, alongside companies, contacts, deals, tickets, line items, and quotes, are objects within the HubSpot CRM.  For details on object properties, associations, and relationships, refer to the [Understanding the CRM Objects](hypothetical_link_to_crm_objects_guide) guide.

**Example Use Case:**  Import your product catalog into HubSpot via the Products API to enable sales reps to easily add goods and services to deals, quotes, etc.

## API Endpoints

### 1. Create a Product

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/products`

**Request Body:**  Includes a `properties` object with product properties.  Use a `PATCH` request to the same endpoint for updates.  Retrieve available product properties using a `GET` request to the `/crm/v3/properties/products` endpoint.

**Example Request:**

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

**`hs_recurring_billing_period` Format:** `P#M` (where # represents the number of months).


### 2. Associate Products (via Line Items)

Products cannot be directly associated with other CRM objects.  Instead, use **line items**. Line items represent individual instances of products and allow tailoring goods/services on a deal or quote without modifying the product itself.

**Important Note:** Line items belong to a single parent object.  Create separate line items for deals and quotes to prevent data loss.  Deleting a parent object (e.g., a quote) deletes its associated line items.

#### 2.1 Create and Associate a Line Item (Multiple Calls)

This approach involves two separate API calls:

**Step 1: Create a Line Item**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/line_item`

**Request Body:**

```json
{
  "properties": {
    "quantity": 1,
    "hs_object_id": "1234567", // Product ID
    "name": "New line item (product-based)"
  }
}
```

**Response:**  The response contains the newly created line item ID.

**Step 2: Associate the Line Item with a Deal**

**Method:** `PUT`

**Endpoint:** `/crm/v4/objects/line_items/{line_item_id}/associations/default/deals/{deal_id}`

(Replace `{line_item_id}` and `{deal_id}` with the appropriate IDs)

**Example Response (200 OK):**

```json
{
  "status": "COMPLETE",
  "results": [
    {
      "from": { "id": "14795354663" }, // Deal ID
      "to": { "id": "7791176460" },     // Line Item ID
      "associationSpec": {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 19
      }
    },
    // ...symmetrical association...
  ],
  "startedAt": "...",
  "completedAt": "..."
}
```


#### 2.2 Create and Associate a Line Item (Single Call)

This method creates and associates a line item in a single API call.

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/line_item`

**Request Body:**

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

**Response:** Details about the newly created line item.


##  Further Information

* **Line Item Properties:** Use a `GET` request to `/crm/v3/properties/line_items` to retrieve available line item properties.
* **Association Types:**  Learn more about association types between different CRM records at [hypothetical_link_to_association_types].
* **Associations API:**  Consult the HubSpot documentation for details on the Associations API.


This documentation provides a concise overview. Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications. Remember to replace placeholder IDs with your actual IDs.
