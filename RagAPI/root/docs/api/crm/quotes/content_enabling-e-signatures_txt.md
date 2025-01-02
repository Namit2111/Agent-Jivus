# HubSpot CRM API: Quotes

This document details the HubSpot CRM API endpoints for managing sales quotes.  It covers creating, updating, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows you to create, manage, and retrieve sales quotes for sharing pricing information with potential buyers. Quotes can be shared via URL or PDF.  The API supports enabling e-signatures and payments.

### Workflow Steps

1. **Create a Quote:** Create a basic quote with name and expiration date. Optionally, enable e-signatures and payments.
2. **Set up Associations:** Associate the quote with other CRM objects (line items, quote template, deal, etc.).  The quote inherits properties from these associations.
3. **Set Quote State:** Update the quote's state (e.g., `DRAFT`, `APPROVAL_NOT_NEEDED`, `APPROVED`) to reflect its progress.  This triggers property updates.
4. **Share the Quote:** Once published, share the quote with buyers.


## API Endpoints

### 1. Create a Quote

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/quotes`

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

**Other Properties:** See `/crm/v3/properties/quotes` (GET request) for a complete list.

**Response:**  A `200 OK` response with the created quote's `id`.

### 2. Update Quote Properties

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Request Body:**

```json
{
  "properties": {
    "hs_title": "Updated Quote Name",
    "hs_expiration_date": "2024-01-15"
  }
}
```

**Response:** A `200 OK` response.

### 3. Quote Owner

The `hubspot_owner_id` property is calculated:

* If a deal is associated:  Reflects `hs_associated_deal_owner_id`.
* If no deal is associated: Reflects `hs_quote_owner_id`.

You cannot manually set `hubspot_owner_id`.

### 4. Enable E-signatures

Include `hs_esign_enabled: true` in the request body (POST or PATCH).  Countersigners must be added in HubSpot, not via API.  Publishing is blocked if the e-signature limit is exceeded.


### 5. Enable Payments

Include `hs_payment_enabled: true` and specify payment details:

* `hs_payment_type`: `HUBSPOT` or `BYO_STRIPE`
* `hs_allowed_payment_methods`:  e.g., `"CREDIT_OR_DEBIT_CARD;ACH"`
* `hs_collect_billing_address`: Boolean
* `hs_collect_shipping_address`: Boolean

**Example Request Body:**

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

HubSpot automatically updates `hs_payment_status` and `hs_payment_date`.


### 6. Adding Associations

Required Associations: Line items, Quote Template, Deal.

Optional Associations: Contact, Company, Discounts, Fees, Taxes.

#### 6.1 Retrieving IDs for Associations

Use `GET` requests to the relevant object endpoints:

* Line items: `/crm/v3/objects/line_items?properties=name`
* Quote templates: `/crm/v3/objects/quote_template?properties=hs_name`
* Deals: `/crm/v3/objects/deals?properties=dealname`
* Contacts: `/crm/v3/objects/contacts?properties=email`
* Companies: `/crm/v3/objects/companies?properties=name`
* Discounts, Fees, Taxes: Similar pattern, use `properties` parameter.

#### 6.2 Creating Associations

**Method:** `PUT`

**Endpoint:** `/crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`

* `fromObjectId`: Quote ID
* `toObjectType`:  e.g., `line_items`, `deals`, `quote_template`
* `toObjectId`: ID of the object to associate.

**Example:** `/crm/v4/objects/quotes/123456/associations/default/line_items/55555`


### 7. Associating Quote Signers (E-signatures)

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

### 8. Create Quote with Associations (Single Request)

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/quote`

**Request Body:** Combines quote properties and associations.  See documentation for detailed structure.


### 9. Update Quote State

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/quote/{quoteId}`

Update the `hs_status` property:

* `DRAFT`: Editable in HubSpot.
* `APPROVAL_NOT_NEEDED`: Publicly accessible URL.
* `PENDING_APPROVAL`: Awaiting approval.
* `APPROVED`: Published and accessible.
* `REJECTED`: Rejected, needs edits.

### 10. Retrieve Quotes

* **Individual Quote:** `GET /crm/v3/objects/quotes/{quoteID}`
* **All Quotes:** `GET /crm/v3/objects/quotes`
* **Batch Read:** `POST /crm/v3/objects/quotes/batch/read` (IDs in request body).


### 11. Properties Set by Quote State

Several properties are automatically updated when the quote state changes.  See documentation for a list.


## Scopes

Required scopes for full functionality:  `crm.objects.quotes.write`, `crm.objects.quotes.read`, `crm.objects.line_items.write`, `crm.objects.line_items.read`, `crm.objects.owners.read`, `crm.objects.contacts.write`, `crm.objects.contacts.read`, `crm.objects.deals.write`, `crm.objects.deals.read`, `crm.objects.companies.write`, `crm.objects.companies.read`, `crm.schemas.quote.read`, `crm.schemas.line_items.read`, `crm.schemas.contacts.read`, `crm.schemas.deals.read`, `crm.schemas.companies.read`

This markdown provides a comprehensive overview of the HubSpot CRM Quotes API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
