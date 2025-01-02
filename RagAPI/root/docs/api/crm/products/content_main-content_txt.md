# HubSpot CRM API: Products

This document details the HubSpot CRM API endpoints for managing products.  Products represent goods or services sold and are used to add products to deals, generate quotes, and report on performance.  Products are objects within the HubSpot CRM, alongside companies, contacts, deals, tickets, line items, and quotes.


## I.  Creating a Product

To create a product, send a `POST` request to:

`/crm/v3/objects/products`

The request body should include a `properties` object containing the product's attributes.  You can update a product's properties later using a `PATCH` request to the same endpoint.

**Request Body Example:**

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

`hs_recurring_billing_period` uses the format `P#M`, where `#` represents the number of months.

To view all available product properties, send a `GET` request to:

`/crm/v3/properties/products`


## II. Associating Products with Deals or Quotes

Products cannot be directly associated with other CRM objects.  Instead, use *line items*. Line items represent individual instances of products and are associated with deals or quotes.  This allows for flexible tailoring of goods and services without modifying the product itself.

**Important Note:** Line items belong to a single parent object.  Create separate line items for deals and quotes to avoid data loss when deleting one object.


## III. Creating and Associating a Line Item (Multiple Calls)

This method involves two API calls: one to create the line item and another to associate it.

**A. Create a Line Item:**

Send a `POST` request to:

`/crm/v3/objects/line_item`

**Request Body Example:**

```json
{
  "properties": {
    "quantity": 1,
    "hs_object_id": "1234567", // Product ID
    "name": "New line item (product-based)"
  }
}
```

The response will contain the newly created line item's ID.

**B. Associate the Line Item with a Deal:**

Send a `PUT` request to:

`/crm/v4/objects/line_items/{lineItemId}/associations/default/deals/{dealId}`

Replace `{lineItemId}` with the ID from the previous step and `{dealId}` with the deal's ID.

**Example Response:**

```json
{
  "status": "COMPLETE",
  "results": [
    {
      "from": { "id": "14795354663" }, //deal ID
      "to": { "id": "7791176460" }, //line item ID
      "associationSpec": {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 19
      }
    },
    // ... (symmetrical association) ...
  ],
  "startedAt": "...",
  "completedAt": "..."
}
```


## IV. Creating and Associating a Line Item (Single Call)

This method creates and associates a line item in a single API call.

Send a `POST` request to:

`/crm/v3/objects/line_item`

**Request Body Example:**

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

A `200` response indicates success.  The line item will appear in the deal's "Line items" card in HubSpot.


## V.  Getting Line Item Properties

To retrieve all available line item properties, send a `GET` request to:

`/crm/v3/properties/line_items`

This will return a list of all available properties you can use when creating or updating a line item.
