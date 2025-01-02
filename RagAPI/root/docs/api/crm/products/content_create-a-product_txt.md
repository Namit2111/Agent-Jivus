# HubSpot CRM API: Products

This document details the HubSpot CRM API endpoints for managing products.  Products represent goods or services sold, allowing for quick addition to deals, quote generation, and performance reporting.  This API facilitates data management and synchronization between HubSpot and other systems.

## Understanding HubSpot Products

Products are CRM objects, similar to companies, contacts, deals, etc.  They are distinct from line items, which represent individual instances of products within deals or quotes.  This separation allows for flexible customization of goods and services without altering the core product definition.

## API Endpoints

All endpoints are accessed via the HubSpot API.  Replace `YOUR_API_KEY` with your actual API key.

**Base URL:** `https://api.hubapi.com/crm/v3/`


### 1. Create a Product

**Method:** `POST`

**Endpoint:** `/objects/products`

**Request Body:**

```json
{
  "properties": {
    "name": "Product Name",
    "price": "100.00",
    "hs_sku": "SKU123",
    "description": "Product Description",
    "hs_cost_of_goods_sold": "20.00",
    "hs_recurring_billing_period": "P12M" // Format: P#M (e.g., P12M for 12 months)
  }
}
```

**Response (201 Created):**  The newly created product object, including its ID.

**Example:**

```bash
curl -X POST \
  https://api.hubapi.com/crm/v3/objects/products \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "properties": {
      "name": "Implementation Service",
      "price": "6000.00",
      "hs_sku": "123456",
      "description": "Onboarding service for data product",
      "hs_cost_of_goods_sold": "600.00",
      "hs_recurring_billing_period": "P12M"
    }
  }'
```


### 2. Get Product Properties

**Method:** `GET`

**Endpoint:** `/properties/products`

**Response:** A list of all available product properties.


### 3.  Retrieve Product Properties

Similar to the `GET` request above but for a specific product ID.


### 4. Associate Products (via Line Items)

Products cannot be directly associated with other objects.  Associations are managed through line items.


#### 4.1 Create and Associate a Line Item (Multiple Calls)

**Step 1: Create a Line Item**

**Method:** `POST`

**Endpoint:** `/objects/line_item`

**Request Body:**

```json
{
  "properties": {
    "quantity": 1,
    "hs_object_id": "PRODUCT_ID", // ID of the product
    "name": "Line Item Name"
  }
}
```

**Response (201 Created):** The created line item object, including its ID.


**Step 2: Associate Line Item with Deal (or other object)**

**Method:** `PUT`

**Endpoint:** `/objects/line_items/{line_item_id}/associations/default/deals/{deal_id}`

Replace `{line_item_id}` with the ID from Step 1 and `{deal_id}` with the ID of the deal.

**Response (200 OK):** Confirmation of association.


#### 4.2 Create and Associate a Line Item (Single Call)

**Method:** `POST`

**Endpoint:** `/objects/line_item`

**Request Body:**

```json
{
  "properties": {
    "quantity": 1,
    "hs_object_id": "PRODUCT_ID", // ID of the product
    "name": "Line Item Name"
  },
  "associations": [
    {
      "to": {
        "id": "DEAL_ID" // ID of the deal
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

**Response (201 Created):** The created and associated line item object.

**Note:**  `associationTypeId` might vary depending on the object you're associating with (e.g., quotes). Consult HubSpot's documentation for specific association types.  Always refer to the official HubSpot API documentation for the most up-to-date information on endpoints, request bodies, and response formats.  Error handling and authentication (API keys) are crucial aspects not explicitly detailed here but are essential for successful API interaction.
