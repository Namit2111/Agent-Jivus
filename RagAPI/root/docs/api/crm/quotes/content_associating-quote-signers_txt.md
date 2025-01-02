# HubSpot CRM API: Quotes

This document details the HubSpot CRM API endpoints for managing sales quotes.  It covers creating, updating, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows you to create, manage, and retrieve sales quotes within HubSpot.  Quotes can be shared via URL or PDF.  Integration with HubSpot Payments or Stripe allows for online payments.

The quote creation process involves these steps:

1. **Create a Quote:**  Create a basic quote with details like name and expiration date.  You can also enable e-signatures and payments.
2. **Set Up Associations:** Associate the quote with line items, a quote template, a deal, and other CRM objects.
3. **Set the Quote State:** Update the quote's state (e.g., `DRAFT`, `APPROVED`, `PENDING_APPROVAL`) to reflect its progress.
4. **Share the Quote:** Once published, share the quote with buyers.


## API Endpoints

### 1. Create a Quote

**Endpoint:** `/crm/v3/objects/quotes`

**Method:** `POST`

**Request Body:**

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-12-10"
  }
}
```

**Required Properties:**

* `hs_title` (string): Quote name.
* `hs_expiration_date` (string): Quote expiration date (YYYY-MM-DD).

**Optional Properties:**  See `/crm/v3/properties/quotes` (GET request) for a complete list.  Key optional properties include:

* `hs_esign_enabled` (boolean): Enable e-signatures (requires associating quote signers).
* `hs_payment_enabled` (boolean): Enable payments (requires HubSpot Payments or Stripe setup).
    * `hs_payment_type` (enum):  `HUBSPOT` or `BYO_STRIPE`.
    * `hs_allowed_payment_methods` (enum):  e.g., `CREDIT_OR_DEBIT_CARD;ACH`.
    * `hs_collect_billing_address` (boolean): Collect billing address.
    * `hs_collect_shipping_address` (boolean): Collect shipping address.

**Response:**  A `200` response with the created quote's `id`.

### 2. Update Quote Properties

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body:**

```json
{
  "properties": {
    "hs_title": "Updated Quote Name",
    // ... other properties to update
  }
}
```

**Response:** A `200` response confirming the update.


### 3. Retrieve Quotes

**Endpoint (single quote):** `/crm/v3/objects/quotes/{quoteID}`

**Endpoint (all quotes):** `/crm/v3/objects/quotes`

**Endpoint (batch read):** `/crm/v3/objects/quotes/batch/read` (Method: `POST`)

**Method:** `GET` (for single and all quotes), `POST` (for batch)

**Query Parameters (single & all quotes):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties with history to return.
* `associations`: Comma-separated list of associated objects to retrieve.

**Request Body (batch read):**

```json
{
  "inputs": [
    {"id": "quoteId1"},
    {"id": "quoteId2"}
  ],
  "properties": ["property1", "property2"]
}
```

**Response:** A `200` response with the requested quote(s) data.


### 4.  Associations API

**Creating Associations:**

**Endpoint:** `/crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`

**Method:** `PUT`

This endpoint associates a quote with other CRM objects (line items, deals, quote templates, etc.).  You need to retrieve the `id` of the object you want to associate first using a GET request to the relevant object's endpoint (e.g., `/crm/v3/objects/line_items`).

**Example:**

```
PUT /crm/v4/objects/quotes/12345/associations/default/line_items/67890
```


**Associating Quote Signers (e-signatures):**

**Endpoint:** `/crm/v4/objects/quote/{quoteId}/associations/contact/{contactId}`

**Method:** `PUT`

**Request Body:**

```json
[
  {
    "associationCategory": "HUBSPOT_DEFINED",
    "associationTypeId": 702
  }
]
```

### 5. Update Quote State

**Endpoint:** `/crm/v3/objects/quote/{quoteId}`

**Method:** `PATCH`

**Request Body:**

```json
{
  "properties": {
    "hs_status": "APPROVAL_NOT_NEEDED" // or DRAFT, APPROVED, PENDING_APPROVAL, REJECTED
  }
}
```

**Response:** A `200` response confirming the state update.  Note that updating the state may automatically populate other properties (e.g., `hs_quote_amount`, `hs_quote_link`).

## Scopes

The following scopes are required for full functionality:

* `crm.objects.quotes.write`
* `crm.objects.quotes.read`
* `crm.objects.line_items.write`
* `crm.objects.line_items.read`
* `crm.objects.owners.read`
* `crm.objects.contacts.write`
* `crm.objects.contacts.read`
* `crm.objects.deals.write`
* `crm.objects.deals.read`
* `crm.objects.companies.write`
* `crm.objects.companies.read`
* `crm.schemas.quote.read`
* `crm.schemas.line_items.read`
* `crm.schemas.contacts.read`
* `crm.schemas.deals.read`
* `crm.schemas.companies.read`


This documentation provides a comprehensive overview. Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
