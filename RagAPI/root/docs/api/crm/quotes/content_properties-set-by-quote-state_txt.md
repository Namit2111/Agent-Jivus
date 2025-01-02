# HubSpot CRM API: Quotes Documentation

This document details the HubSpot CRM API endpoints for managing sales quotes.  It covers creating, updating, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows developers to create, manage, and retrieve sales quotes within HubSpot. Quotes can be shared with buyers via a URL or PDF.  The API supports e-signatures and payments (requiring HubSpot Payments or Stripe integration).

The quote creation process involves several steps:

1. **Create a quote:**  Define basic details (name, expiration date). Optionally, enable e-signatures and payments.
2. **Set up associations:** Link the quote to other CRM objects (line items, quote template, deal, etc.).
3. **Set the quote state:**  Transition the quote through stages (draft, pending approval, approved, rejected) affecting its accessibility and properties.
4. **Share the quote:** Once published, share the quote's URL or PDF with the buyer.

## API Endpoints

### 1. Create a Quote

**Endpoint:** `/crm/v3/objects/quotes`

**Method:** `POST`

**Request Body:**

Requires `hs_title` (string) and `hs_expiration_date` (string, YYYY-MM-DD).  Other properties are optional but may be needed for publishing.  Use `/crm/v3/properties/quotes` (GET) to see all available properties.

**Example Request Body:**

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-12-10"
  }
}
```

**Response:**  A `200 OK` response with the newly created quote's `id`.

### 2. Update Quote Properties

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body:**  An object containing the properties to update.

**Example Request Body (Enabling E-Signatures):**

```json
{
  "properties": {
    "hs_esign_enabled": true
  }
}
```

**Response:** A `200 OK` response.

### 3. Enable Payments

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body (Enabling HubSpot Payments with Credit/Debit Card and ACH):**

```json
{
  "properties": {
    "hs_payment_enabled": true,
    "hs_payment_type": "HUBSPOT",
    "hs_allowed_payment_methods": "CREDIT_OR_DEBIT_CARD;ACH"
  }
}
```

**Parameters:**

* `hs_payment_enabled` (boolean): Enables payments.
* `hs_payment_type` (enumeration): "HUBSPOT" or "BYO_STRIPE".
* `hs_allowed_payment_methods` (enumeration): e.g., "CREDIT_OR_DEBIT_CARD;ACH".
* `hs_collect_billing_address` (boolean): Collect billing address.
* `hs_collect_shipping_address` (boolean): Collect shipping address.

**Response:** A `200 OK` response.  HubSpot automatically updates `hs_payment_status` and `hs_payment_date`.

### 4. Adding Associations

Requires associating with Line Items, Quote Template, and Deal (minimum).  Other associations are optional.

**a) Retrieving IDs:** Use GET requests on relevant object endpoints (e.g., `/crm/v3/objects/line_items?properties=name`).

**b) Creating Associations:**  Use PUT requests to `/crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`.

**Example PUT Request (Associating a Line Item):**

```
PUT /crm/v4/objects/quotes/{quoteId}/associations/default/line_items/{lineItemId}
```

**Response:** A `200 OK` response confirming the association.


### 5. Create a Quote with Associations (Single Request)

**Endpoint:** `/crm/v3/objects/quote`

**Method:** `POST`

**Request Body:**

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-09-30"
  },
  "associations": [
    // ... association objects ...
  ]
}
```

Each association object needs `to` (object ID), `associationCategory` ("HUBSPOT_DEFINED"), and `associationTypeId` (e.g., 286 for quote-to-quote-template, 64 for quote-to-deal, 67 for quote-to-line-item).

### 6. Update Quote State

**Endpoint:** `/crm/v3/objects/quote/{quoteId}`

**Method:** `PATCH`

**Request Body (Publishing the Quote):**

```json
{
  "properties": {
    "hs_status": "APPROVAL_NOT_NEEDED" 
  }
}
```

Possible `hs_status` values: `DRAFT`, `APPROVAL_NOT_NEEDED`, `PENDING_APPROVAL`, `APPROVED`, `REJECTED`.

### 7. Retrieve Quotes

* **Individual Quote:** `GET /crm/v3/objects/quotes/{quoteID}`
* **All Quotes:** `GET /crm/v3/objects/quotes`
* **Batch Retrieval:** `POST /crm/v3/objects/quotes/batch/read` (IDs in request body)

Query parameters: `properties`, `propertiesWithHistory`, `associations`.


## Scopes

The following scopes are required for full functionality:

`crm.objects.quotes.write`, `crm.objects.quotes.read`, `crm.objects.line_items.write`, `crm.objects.line_items.read`, `crm.objects.owners.read`, `crm.objects.contacts.write`, `crm.objects.contacts.read`, `crm.objects.deals.write`, `crm.objects.deals.read`, `crm.objects.companies.write`, `crm.objects.companies.read`, `crm.schemas.quote.read`, `crm.schemas.line_items.read`, `crm.schemas.contacts.read`, `crm.schemas.deals.read`, `crm.schemas.companies.read`


This documentation provides a comprehensive overview of the HubSpot CRM Quotes API. Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
