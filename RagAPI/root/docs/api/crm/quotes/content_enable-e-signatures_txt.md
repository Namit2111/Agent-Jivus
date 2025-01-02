# HubSpot CRM API: Quotes

This document details the HubSpot CRM API for managing sales quotes.  It covers creating, updating, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows developers to create, manage, and retrieve sales quotes within HubSpot.  Quotes can be shared via URL or PDF.  Integration with HubSpot Payments or Stripe allows for payment processing directly through the API.

The quote creation process involves several steps:

1. **Create a quote:**  Define basic details (name, expiration date, etc.).  Optional features like e-signatures and payments can be enabled.
2. **Set up associations:** Link the quote to other CRM objects (line items, quote template, deal, etc.).  This inheritance property values from associated records and account settings.
3. **Set the quote state:**  Define the quote's status (draft, published, approved, etc.).  This affects accessibility and properties.
4. **Share the quote:** Once published, share the quote with buyers.


## API Endpoints

The API uses standard HTTP methods (POST, GET, PATCH, PUT).  All endpoints begin with `/crm/v3/objects/quotes` or `/crm/v4/objects/quotes`.


### 1. Create a Quote

**Method:** `POST /crm/v3/objects/quotes`

**Request Body:**

Requires `hs_title` (string) and `hs_expiration_date` (string, YYYY-MM-DD format).  Other properties can be included (see [Properties](#properties)).

**Example Request Body:**

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-12-10"
  }
}
```

**Response:** A `200 OK` response with the created quote's `id`.

### 2. Update Quote Properties

**Method:** `PATCH /crm/v3/objects/quotes/{quoteId}`

**Request Body:**  An object containing the properties to update.

**Example Request Body (Enabling E-signatures):**

```json
{
  "properties": {
    "hs_esign_enabled": true
  }
}
```

**Response:** A `200 OK` response.


### 3. Enable E-Signatures

Include the `hs_esign_enabled` boolean property (set to `true`) in the request body (either during creation or update).  Countersigners must be added in HubSpot UI.  Publishing is blocked if the monthly e-signature limit is exceeded.


### 4. Enable Payments

Include the `hs_payment_enabled` boolean property (set to `true`), along with `hs_payment_type` and `hs_allowed_payment_methods`.  HubSpot Payments or Stripe must be configured in the HubSpot account.

**Example Request Body (Enabling HubSpot Payments):**

```json
{
  "properties": {
    "hs_payment_enabled": true,
    "hs_payment_type": "HUBSPOT",
    "hs_allowed_payment_methods": "CREDIT_OR_DEBIT_CARD;ACH"
  }
}
```

**Payment Status Properties:**

* `hs_payment_status`:  Updated automatically (PENDING, PROCESSING, PAID).
* `hs_payment_date`: Set when payment is confirmed.

### 5. Adding Associations

Use the `/crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}` endpoint (PUT method) to associate a quote with other objects.  **Required associations:** Line items, Quote template, Deal.

**Example (Associating a line item):**

```
PUT /crm/v4/objects/quotes/{quoteId}/associations/default/line_items/{lineItemId}
```

**Retrieving IDs:**  Use `GET /crm/v3/objects/{objectType}?properties={propertyList}` to retrieve IDs of associated objects (e.g., line items, deals, etc.).


### 6. Create a Quote with Associations (Single Request)

**Method:** `POST /crm/v3/objects/quote`

This combines quote creation and association in a single request.  See the documentation for the required structure of the `associations` array.

**Example Request Body:** (This example creates a quote with a template, a deal, line items, and a contact)

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


### 7. Update Quote State

**Method:** `PATCH /crm/v3/objects/quote/{quoteId}`

Update the `hs_status` property to change the quote's state (DRAFT, APPROVAL_NOT_NEEDED, PENDING_APPROVAL, APPROVED, REJECTED).  This automatically updates other properties.

**Example Request Body (Publishing):**

```json
{
  "properties": {
    "hs_status": "APPROVAL_NOT_NEEDED"
  }
}
```


### 8. Retrieve Quotes

**Method:** `GET /crm/v3/objects/quotes/{quoteId}` (individual) or `GET /crm/v3/objects/quotes` (list).  Use query parameters `properties`, `propertiesWithHistory`, and `associations` to control the returned data.  Batch retrieval is available via `POST /crm/v3/objects/quotes/batch/read`.


### Properties

The API uses several properties to manage quotes.  A `GET /crm/v3/properties/quotes` request retrieves a complete list of properties.  Key properties include:

* `hs_title`: Quote name.
* `hs_expiration_date`: Expiration date.
* `hs_status`: Quote status (DRAFT, APPROVAL_NOT_NEEDED, etc.).
* `hs_esign_enabled`: E-signature enabled (boolean).
* `hs_payment_enabled`: Payments enabled (boolean).
* `hs_payment_type`: Payment processor type (HUBSPOT, BYO_STRIPE).
* `hs_allowed_payment_methods`: Allowed payment methods.
* `hs_quote_amount`: Calculated total amount.
* `hs_quote_link`: Publicly accessible URL (read-only after publishing).
* `hubspot_owner_id`: Quote owner ID (calculated).


## Scopes

The following scopes are required for full functionality:

`crm.objects.quotes.write`, `crm.objects.quotes.read`, `crm.objects.line_items.write`, `crm.objects.line_items.read`, `crm.objects.owners.read`, `crm.objects.contacts.write`, `crm.objects.contacts.read`, `crm.objects.deals.write`, `crm.objects.deals.read`, `crm.objects.companies.write`, `crm.objects.companies.read`, `crm.schemas.quote.read`, `crm.schemas.line_items.read`, `crm.schemas.contacts.read`, `crm.schemas.deals.read`, `crm.schemas.companies.read`


This documentation provides a comprehensive overview of the HubSpot CRM Quotes API. Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
