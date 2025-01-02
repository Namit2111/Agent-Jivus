# HubSpot CRM API: Quotes

This document details the HubSpot CRM API for managing sales quotes.  It covers quote creation, association with other CRM objects, state management, and retrieval.

## Overview

The Quotes API allows you to create, manage, and retrieve sales quotes.  Quotes can be shared via URL or PDF.  Integration with HubSpot Payments or Stripe allows for payment processing directly through the API.

The quote creation process involves these steps:

1. **Create a quote:** Define basic details (name, expiration date).  Optional features include e-signatures and payments.
2. **Set up associations:** Link the quote to other CRM objects (line items, quote template, deal, etc.).
3. **Set the quote state:** Define the quote's status (draft, published, pending approval, etc.).  This affects its accessibility and properties.
4. **Share the quote:** Once published, share the quote with buyers.

## API Endpoints

### 1. Create a Quote

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/quotes`

**Request Body:**

The request body requires `hs_title` (quote name) and `hs_expiration_date`.  Other properties are optional but necessary for a fully functional quote (see below for details).

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-12-10"
  }
}
```

**Response:**  A `200 OK` response containing the newly created quote's `id`.

### 2.  Retrieve Quote Properties

**Method:** `GET`

**Endpoint:** `/crm/v3/properties/quotes`

**Response:** A list of all available quote properties.

### 3. Update Quote Properties

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Request Body:**  A JSON object containing the properties to update.

```json
{
  "properties": {
    "hs_title": "Updated Quote Name",
    "hs_expiration_date": "2024-01-15"
  }
}
```

**Response:** A `200 OK` response.


### 4.  Enable E-Signatures

Include the `hs_esign_enabled` property with a value of `true` in the POST or PATCH request.  Note: Countersigners must be added in HubSpot;  publishing is blocked if the monthly e-signature limit is exceeded.

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-12-10",
    "hs_esign_enabled": true
  }
}
```

### 5. Enable Payments

Include `hs_payment_enabled: true`, `hs_payment_type` (HUBSPOT or BYO_STRIPE), and `hs_allowed_payment_methods` (e.g., "CREDIT_OR_DEBIT_CARD;ACH").  HubSpot Payments or Stripe integration is required.

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-12-10",
    "hs_payment_enabled": true,
    "hs_payment_type": "HUBSPOT",
    "hs_allowed_payment_methods": "CREDIT_OR_DEBIT_CARD;ACH"
  }
}
```

**Response:** A `200 OK` response.  `hs_payment_status` and `hs_payment_date` are automatically updated by HubSpot.


### 6. Adding Associations

Use the Associations API (`/crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`) to associate the quote with other objects.  Required associations: line items, quote template, deal.

**Method:** `PUT`

**Endpoint:**  `/crm/v4/objects/quotes/{quoteId}/associations/default/{toObjectType}/{toObjectId}`

Example: Associate with a line item (replace placeholders):

`/crm/v4/objects/quotes/{quoteId}/associations/default/line_items/{lineItemId}`

**Response:** A `200 OK` response confirming the association.


### 7. Retrieving IDs for Associations

Use `GET` requests to retrieve IDs of associated objects:

* Line items: `/crm/v3/objects/line_items?properties=name`
* Quote templates: `/crm/v3/objects/quote_template?properties=hs_name`
* Deals: `/crm/v3/objects/deals?properties=dealname`
* ...and others.


### 8.  Associating Quote Signers (E-Signatures)

Use a specific endpoint for associating quote signers:

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


### 9. Create a Quote with Associations (Single Request)

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/quote`

This allows creating a quote and its associations in a single request.  See the original text for the complex request body structure.


### 10. Update Quote State

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/quote/{quoteId}`

Update the `hs_status` property to change the quote's state (DRAFT, APPROVAL_NOT_NEEDED, PENDING_APPROVAL, APPROVED, REJECTED).

```json
{
  "properties": {
    "hs_status": "APPROVAL_NOT_NEEDED"
  }
}
```

**Response:** A `200 OK` response.  Several properties are automatically updated based on the new state.


### 11. Retrieve Quotes

* **Individual quote:** `GET /crm/v3/objects/quotes/{quoteID}`
* **List of quotes:** `GET /crm/v3/objects/quotes`
* **Batch retrieval:** `POST /crm/v3/objects/quotes/batch/read` (IDs in request body).


## Properties Set by Quote State

Several quote properties are automatically updated when the quote's state changes.  See the original text for a complete list.


## Scopes

The following scopes are required:

* `crm.objects.quotes.write`, `crm.objects.quotes.read`
* `crm.objects.line_items.write`, `crm.objects.line_items.read`
* `crm.objects.owners.read`
* `crm.objects.contacts.write`, `crm.objects.contacts.read`
* `crm.objects.deals.write`, `crm.objects.deals.read`
* `crm.objects.companies.write`, `crm.objects.companies.read`
* `crm.schemas.quote.read`, `crm.schemas.line_items.read`, `crm.schemas.contacts.read`, `crm.schemas.deals.read`, `crm.schemas.companies.read`


This markdown provides a structured and more concise representation of the provided text.  Remember to replace placeholders like `{quoteId}`, `{lineItemId}`, etc., with actual values.  Consult the HubSpot API documentation for the most up-to-date information and details.
