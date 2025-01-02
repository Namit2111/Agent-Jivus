# HubSpot CRM API: Quotes

This document details the HubSpot CRM API for managing sales quotes.  It covers creating, updating, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows you to create, manage, and retrieve sales quotes.  Quotes can be shared with buyers via URL or PDF.  You can also manage quote details, associations, and states within HubSpot.  Integration with HubSpot payments or Stripe allows for payable quotes.

The quote creation process involves these steps:

1. **Create a quote:** Create a quote with basic details (name, expiration date).  You can also enable e-signatures and payments.
2. **Set up associations:** Associate the quote with other CRM objects (line items, quote template, deal, etc.).
3. **Set the quote state:** Set the quote's state (draft, published, etc.). This impacts accessibility and properties.
4. **Share the quote:** Share the published quote with buyers.

## API Endpoints and Calls

### 1. Create a Quote

**Endpoint:** `/crm/v3/objects/quotes`

**Method:** `POST`

**Request Body (minimum):**

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

**Response:** A `200 OK` response including the `id` of the newly created quote.  Additional properties can be set using the `properties` field (see `/crm/v3/properties/quotes` for all available properties).


### 2. Update Quote Properties

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body:**

```json
{
  "properties": {
    "hs_property": "new_value"
  }
}
```

Replace `{quoteId}` with the quote's ID and update desired properties.


### 3. Enable E-Signatures

Include the `hs_esign_enabled` property in the request body (POST or PATCH) with a value of `true`.  Countersigners must be added in HubSpot.  Publishing is prevented if the e-signature limit is exceeded.

**Example:**

```json
{
  "properties": {
    "hs_title": "...",
    "hs_expiration_date": "...",
    "hs_esign_enabled": true
  }
}
```

### 4. Enable Payments

Include `hs_payment_enabled`, `hs_payment_type`, and `hs_allowed_payment_methods` properties.  HubSpot payments or Stripe must be configured.

**Request Body Example (HubSpot Payments):**

```json
{
  "properties": {
    "hs_title": "...",
    "hs_expiration_date": "...",
    "hs_payment_enabled": true,
    "hs_payment_type": "HUBSPOT",
    "hs_allowed_payment_methods": "CREDIT_OR_DEBIT_CARD;ACH"
  }
}
```

* **`hs_payment_enabled` (boolean):** Enables payments (true/false).
* **`hs_payment_type` (enum):**  `HUBSPOT` or `BYO_STRIPE`.
* **`hs_allowed_payment_methods` (enum):**  e.g., `CREDIT_OR_DEBIT_CARD;ACH`.
* **`hs_collect_billing_address` (boolean):** Collect billing address (true/false).
* **`hs_collect_shipping_address` (boolean):** Collect shipping address (true/false).

**Payment Status Properties (automatically updated):**

* `hs_payment_status`: `PENDING`, `PROCESSING`, `PAID`.
* `hs_payment_date`: Date and time of payment confirmation.

### 5. Adding Associations

Required associations: Line items, Quote template, Deal. Optional: Contact, Company, Discounts, Fees, Taxes.

**a) Retrieving IDs:** Use GET requests to relevant object endpoints to retrieve IDs:

* Line items: `/crm/v3/objects/line_items?properties=name`
* Quote templates: `/crm/v3/objects/quote_template?properties=hs_name`
* Deals: `/crm/v3/objects/deals?properties=dealname`
* etc.

**b) Creating Associations:** Use `PUT` requests to the associations API:

`/crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`

Replace placeholders with appropriate IDs and object types.


### 6. Associating Quote Signers (E-Signatures)

Use a `PUT` request:

`/crm/v4/objects/quote/{quoteId}/associations/contact/{contactId}`

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

**Endpoint:** `/crm/v3/objects/quote`

**Method:** `POST`

**Request Body:**  Combines quote properties and associations in a single request (see example in the original text).


### 8. Update Quote State

**Endpoint:** `/crm/v3/objects/quote/{quoteId}`

**Method:** `PATCH`

**Request Body:** Update `hs_status` property:

```json
{
  "properties": {
    "hs_status": "APPROVAL_NOT_NEEDED" // or DRAFT, PENDING_APPROVAL, APPROVED, REJECTED
  }
}
```

### 9. Retrieve Quotes

* **Individual quote:** `GET /crm/v3/objects/quotes/{quoteID}`
* **All quotes:** `GET /crm/v3/objects/quotes`
* **Batch read:** `POST /crm/v3/objects/quotes/batch/read` (IDs in request body)


## Properties Set by Quote State

Various properties are automatically populated based on the quote's state and associations (see details in the original text).


## Scopes

Required scopes for app access:

`crm.objects.quotes.write`, `crm.objects.quotes.read`, `crm.objects.line_items.write`, `crm.objects.line_items.read`, `crm.objects.owners.read`, `crm.objects.contacts.write`, `crm.objects.contacts.read`, `crm.objects.deals.write`, `crm.objects.deals.read`, `crm.objects.companies.write`, `crm.objects.companies.read`, `crm.schemas.quote.read`, `crm.schemas.line_items.read`, `crm.schemas.contacts.read`, `crm.schemas.deals.read`, `crm.schemas.companies.read`


This markdown documentation provides a more structured and easily navigable overview of the HubSpot CRM Quotes API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
