# HubSpot CRM API: Quotes Documentation

This document details the HubSpot CRM API endpoints for managing sales quotes.  It covers creating, updating, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows you to create, manage, and retrieve sales quotes for sharing pricing information with potential buyers.  Quotes can be shared via a URL or PDF.  Integration with HubSpot payments or Stripe allows for online payments.

The quote creation process generally involves these steps:

1. **Create a quote:**  Establish basic details like name and expiration date.  Enable e-signatures and payments as needed.
2. **Set up associations:** Link the quote to other CRM objects (line items, quote template, deal, etc.).  This inheritance of properties from associated records is crucial.
3. **Set the quote state:** Define the quote's readiness (draft, published, pending approval, etc.).  This impacts accessibility and properties inherited from associated records.
4. **Share the quote:** Once published, share the quote with the buyer.


## API Endpoints and Calls

### 1. Create a Quote

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/quotes`

**Request Body (Minimum):**

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-12-10"
  }
}
```

* **`hs_title` (string, required):** Quote name.
* **`hs_expiration_date` (string, required):** Quote expiration date (YYYY-MM-DD).

**Response:**  A `200` response with the created quote's `id` and other properties.  Additional properties are needed for a publishable quote (see below).  Use a `GET` request to `/crm/v3/properties/quotes` to see all available properties.

**Example with e-signatures and payments:**

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-12-10",
    "hs_esign_enabled": true,
    "hs_payment_enabled": true,
    "hs_payment_type": "HUBSPOT",
    "hs_allowed_payment_methods": "CREDIT_OR_DEBIT_CARD;ACH"
  }
}
```

### 2. Update Quote Properties

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Request Body:**  A JSON object with the properties to update.

**Example:**

```json
{
  "properties": {
    "hs_title": "Updated Quote Name"
  }
}
```

### 3. Retrieve Quotes

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}` (individual quote) or `/crm/v3/objects/quotes` (all quotes)

**Query Parameters:**

* **`properties`:** Comma-separated list of properties to return.
* **`propertiesWithHistory`:** Comma-separated list of current and historical properties.
* **`associations`:** Comma-separated list of associated objects to retrieve.

**Batch Retrieval (POST):**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/quotes/batch/read`

**Request Body:**

```json
{
  "inputs": [
    {"id": "quoteId1"},
    {"id": "quoteId2"}
  ],
  "properties": ["property1", "property2"]
}
```


### 4. Quote Owner

The `hubspot_owner_id` property is calculated.  It reflects the owner of the associated deal (`hs_associated_deal_owner_id`) if one exists; otherwise, it uses `hs_quote_owner_id`.

### 5. Adding Associations

The Associations API (`/crm/v4/objects/quotes/{quoteId}/associations/default/{toObjectType}/{toObjectId}`) is used to link the quote with other objects.  A `PUT` request is used for each association.

**Required Associations:**

* Line items
* Quote template
* Deal

**Optional Associations:**

* Contact
* Company
* Discounts
* Fees
* Taxes

**Before associating, retrieve the IDs of the objects using `GET` requests to the respective object endpoints (e.g., `/crm/v3/objects/line_items?properties=name`).**

**Example Association (Line Item):**

`PUT /crm/v4/objects/quotes/{quoteId}/associations/default/line_items/{lineItemId}`

### 6.  Associating Quote Signers (E-signatures)

For e-signatures, use a specific association label:

**Method:** `PUT`

**Endpoint:** `/crm/v4/objects/quote/{quoteId}/associations/contact/{contactId}`

**Request Body:**

```json
[
  {
    "associationCategory": "HUBSPOT_DEFINED",
    "associationTypeId": 702
  }
]
```


### 7. Create a Quote with Associations (Single Request)

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/quote`

**Request Body:**

```json
{
  "properties": {
    "hs_title": "Quote Title",
    "hs_expiration_date": "2024-03-15"
  },
  "associations": [
    // Association objects for quote template, deal, line items, etc.
  ]
}
```

### 8. Update Quote State

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/quote/{quoteId}`

**Request Body:**

```json
{
  "properties": {
    "hs_status": "APPROVAL_NOT_NEEDED" // or DRAFT, PENDING_APPROVAL, APPROVED, REJECTED
  }
}
```

### 9. Properties Set by Quote State

Several properties are automatically updated when the quote state changes (e.g., `hs_quote_amount`, `hs_domain`, `hs_quote_link`, `hs_payment_status`).


## Scopes

The following scopes are required:

`crm.objects.quotes.write`, `crm.objects.quotes.read`, `crm.objects.line_items.write`, `crm.objects.line_items.read`, `crm.objects.owners.read`, `crm.objects.contacts.write`, `crm.objects.contacts.read`, `crm.objects.deals.write`, `crm.objects.deals.read`, `crm.objects.companies.write`, `crm.objects.companies.read`, `crm.schemas.quote.read`, `crm.schemas.line_items.read`, `crm.schemas.contacts.read`, `crm.schemas.deals.read`, `crm.schemas.companies.read`


This documentation provides a comprehensive overview.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
