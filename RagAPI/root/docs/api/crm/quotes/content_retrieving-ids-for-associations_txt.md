# HubSpot CRM API: Quotes Documentation

This document details the HubSpot CRM API endpoints for managing sales quotes.  It covers quote creation, association with other CRM objects, state management, and retrieval.

## Overview

The HubSpot Quotes API allows developers to create, manage, and retrieve sales quotes programmatically.  Quotes can be shared with buyers via a URL or PDF.  The API supports e-signatures and payment processing integration with HubSpot Payments or Stripe.

The quote creation process generally involves these steps:

1. **Create a quote:** Define basic details (name, expiration date). Optionally enable e-signatures and payments.
2. **Set up associations:** Link the quote to other CRM objects (line items, quote template, deal, etc.).
3. **Set the quote state:**  Transition the quote through stages (draft, pending approval, approved, rejected) to reflect its progress.
4. **Share the quote:**  Once published, share the quote's URL or PDF with the buyer.

## API Endpoints

The primary endpoints are:

* **`/crm/v3/objects/quotes`**:  CRUD operations for quotes (Create, Read, Update, Delete).  Uses `POST` for creation, `GET` for retrieval (single or multiple), `PATCH` for updates.
* **`/crm/v3/objects/quotes/batch/read`**: Batch retrieval of quotes by ID. Uses `POST`.
* **`/crm/v3/properties/quotes`**: Retrieves all available quote properties. Uses `GET`.
* **`/crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`**: Creates associations between a quote and other CRM objects. Uses `PUT`.
* **`/crm/v4/objects/quote/{quoteId}/associations/contact/{contactId}`**: Associates quote signers (contacts) with a quote. Uses `PUT`.


## API Calls and Responses

### 1. Create a Quote

**Request:** `POST /crm/v3/objects/quotes`

**Request Body (minimum):**

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-12-10"
  }
}
```

**Response (example):**

```json
{
  "id": "12345",
  // ... other properties ...
}
```

**Required Properties:**

* `hs_title` (string): Quote name.
* `hs_expiration_date` (string): Quote expiration date (YYYY-MM-DD).

**Additional Properties (for publishing):**  See `/crm/v3/properties/quotes` for a complete list.  Examples include:

* `hs_esign_enabled` (boolean): Enable e-signatures (true/false).
* `hs_payment_enabled` (boolean): Enable payments (true/false).
* `hs_payment_type` (enum): Payment processor (HUBSPOT, BYO_STRIPE).
* `hs_allowed_payment_methods` (enum): Allowed payment methods (CREDIT_OR_DEBIT_CARD, ACH, etc.).


### 2. Update Quote Properties

**Request:** `PATCH /crm/v3/objects/quotes/{quoteId}`

**Request Body (example):**

```json
{
  "properties": {
    "hs_title": "Updated Quote Name",
    "hs_expiration_date": "2024-01-15"
  }
}
```


### 3. Retrieve a Quote

**Request:** `GET /crm/v3/objects/quotes/{quoteId}`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`:  Comma-separated list of properties to return, including historical data.
* `associations`: Comma-separated list of associated objects to retrieve.

### 4. Retrieve Quote Properties

**Request:** `GET /crm/v3/properties/quotes`

This endpoint returns a list of all available properties for quotes.


### 5.  Retrieve Quotes (Batch)

**Request:** `POST /crm/v3/objects/quotes/batch/read`

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

### 6. Create Associations

**Request:** `PUT /crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`

This endpoint associates a quote with other CRM objects (line items, deal, quote template, etc.).  `toObjectType` specifies the type of object (e.g., `line_items`, `deals`, `quote_template`), and `toObjectId` is the ID of that object.

**Example associating a line item:**

```
PUT /crm/v4/objects/quotes/12345/associations/default/line_items/67890
```

### 7. Associate Quote Signers

**Request:** `PUT /crm/v4/objects/quote/{quoteId}/associations/contact/{contactId}`

**Request Body:**

```json
[
  {
    "associationCategory": "HUBSPOT_DEFINED",
    "associationTypeId": 702
  }
]
```


### 8. Update Quote State

**Request:** `PATCH /crm/v3/objects/quote/{quoteId}`

**Request Body (example):**

```json
{
  "properties": {
    "hs_status": "APPROVAL_NOT_NEEDED"
  }
}
```

Possible `hs_status` values: `DRAFT`, `APPROVAL_NOT_NEEDED`, `PENDING_APPROVAL`, `APPROVED`, `REJECTED`.


## Properties Set by Quote State

Certain quote properties are automatically populated when the quote state changes.  These include: `hs_quote_amount`, `hs_domain`, `hs_slug`, `hs_quote_total_preference`, `hs_timezone`, `hs_locale`, `hs_quote_number`, `hs_language`, `hs_currency`, `hs_pdf_download_link`, `hs_locked`, and `hs_quote_link`.

## Scopes

The following OAuth scopes are required:

* `crm.objects.quotes.write`, `crm.objects.quotes.read`
* `crm.objects.line_items.write`, `crm.objects.line_items.read`
* `crm.objects.owners.read`
* `crm.objects.contacts.write`, `crm.objects.contacts.read`
* `crm.objects.deals.write`, `crm.objects.deals.read`
* `crm.objects.companies.write`, `crm.objects.companies.read`
* `crm.schemas.quote.read`, `crm.schemas.line_items.read`, `crm.schemas.contacts.read`, `crm.schemas.deals.read`, `crm.schemas.companies.read`


This documentation provides a comprehensive overview of the HubSpot CRM Quotes API.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
