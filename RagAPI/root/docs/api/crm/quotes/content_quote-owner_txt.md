# HubSpot CRM API: Quotes

This document details the HubSpot CRM API endpoints for managing sales quotes.  It covers creating, updating, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows developers to create, manage, and retrieve sales quotes within HubSpot.  Quotes can be shared with buyers via URL or PDF.  Integration with HubSpot Payments or Stripe enables online payment processing.

The quote creation process involves these steps:

1. **Create a Quote:**  Define basic details (name, expiration date). Optionally enable e-signatures and payments.
2. **Set up Associations:** Link the quote to other CRM objects (line items, quote template, deal, etc.).  This inheritance property values from associated records and account settings.
3. **Set the Quote State:**  Transition the quote through different stages (draft, pending approval, approved, rejected) affecting its accessibility and properties.
4. **Share the Quote:**  Once published, share the quote with buyers.


## API Endpoints

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

* `hs_title` (string, required): Quote name.
* `hs_expiration_date` (string, required): Quote expiration date (YYYY-MM-DD).

**Other Properties:**  A complete list of properties is available via a `GET` request to `/crm/v3/properties/quotes`.  See [Properties API](#properties-api) for details.  Additional properties are required for publishing a quote (e.g., associating with a deal and quote template).

**Response (200 OK):**  Includes the newly created quote's `id`.

```json
{
  "id": "123456"
  // ... other properties ...
}
```

### 2. Update Quote Properties

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body:**  Similar structure to the create request, but only includes properties to update.

```json
{
  "properties": {
    "hs_title": "Updated Quote Name"
  }
}
```

**Response (200 OK):** Updated quote details.


### 3. Retrieve Quotes

**Endpoint (individual):** `/crm/v3/objects/quotes/{quoteId}`

**Endpoint (all):** `/crm/v3/objects/quotes`

**Endpoint (batch):** `/crm/v3/objects/quotes/batch/read`  (Method: `POST`)


**Method:** `GET` (for individual and all)

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties including history.
* `associations`: Comma-separated list of associated objects to retrieve.

**Batch Read Request Body:**

```json
{
  "inputs": [
    {"id": "quoteId1"},
    {"id": "quoteId2"}
  ],
  "properties": ["property1", "property2"]
}
```

**Response (200 OK):**  Quote details (individual) or array of quote details (all).


### 4.  Enable E-signatures

Include the `hs_esign_enabled` property with value `true` in your POST or PATCH request.  Countersigners must be added in HubSpot UI.


### 5. Enable Payments

Include `hs_payment_enabled: true`, `hs_payment_type` (HUBSPOT or BYO_STRIPE), and `hs_allowed_payment_methods` (e.g., "CREDIT_OR_DEBIT_CARD;ACH").  Requires HubSpot Payments or Stripe integration.

**Parameters:**

| Parameter                  | Type      | Description                                                                                             |
|---------------------------|-----------|---------------------------------------------------------------------------------------------------------|
| `hs_payment_enabled`       | Boolean   | Enables payment collection.                                                                               |
| `hs_payment_type`         | Enumeration | Payment processor (HUBSPOT or BYO_STRIPE).                                                              |
| `hs_allowed_payment_methods` | Enumeration | Allowed payment methods (e.g., CREDIT_OR_DEBIT_CARD, ACH).                                               |
| `hs_collect_billing_address` | Boolean | Allows buyer to enter billing address.                                                                    |
| `hs_collect_shipping_address` | Boolean | Allows buyer to enter shipping address.                                                                    |


**Automatic Updates:** `hs_payment_status` (PENDING, PROCESSING, PAID) and `hs_payment_date` are updated automatically by HubSpot.


### 6. Adding Associations

Use the Associations API (`/crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`) with `PUT` requests to link the quote with other objects.

**Required Associations:**

* Line items
* Quote template
* Deal

**Optional Associations:** Contact, Company, Discounts, Fees, Taxes


### 7.  Create Quote with Associations (Single Request)

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

Each association object includes:  `to` (ID of the object), `types` (array of association type objects with `associationCategory` and `associationTypeId`).


### 8. Update Quote State

**Endpoint:** `/crm/v3/objects/quote/{quoteId}`

**Method:** `PATCH`

Update the `hs_status` property:

* `DRAFT`: Editable in HubSpot.
* `APPROVAL_NOT_NEEDED`: Published without approval.
* `PENDING_APPROVAL`: Awaiting approval.
* `APPROVED`: Published.
* `REJECTED`: Rejected.

### 9. Properties Set by Quote State

Several properties are automatically updated when the quote's state changes (e.g., `hs_quote_amount`, `hs_domain`, `hs_quote_link`, `hs_payment_status`).


### 10. Scopes

The necessary OAuth scopes are:

`crm.objects.quotes.write`, `crm.objects.quotes.read`, `crm.objects.line_items.write`, `crm.objects.line_items.read`, `crm.objects.owners.read`, `crm.objects.contacts.write`, `crm.objects.contacts.read`, `crm.objects.deals.write`, `crm.objects.deals.read`, `crm.objects.companies.write`, `crm.objects.companies.read`, `crm.schemas.quote.read`, `crm.schemas.line_items.read`, `crm.schemas.contacts.read`, `crm.schemas.deals.read`, `crm.schemas.companies.read`


## Example Use Case: Creating a Quote

1.  **Create a quote:** Use a `POST` request to `/crm/v3/objects/quotes` with `hs_title` and `hs_expiration_date`.
2.  **Get IDs:** Use `GET` requests to retrieve IDs for the deal, quote template, and line items.
3.  **Associate objects:** Use `PUT` requests to `/crm/v4/objects/quotes/{quoteId}/associations/default/{toObjectType}/{toObjectId}` to associate the quote with the deal, template, and line items.
4.  **Update state:** Use a `PATCH` request to `/crm/v3/objects/quote/{quoteId}` to set `hs_status` to `APPROVAL_NOT_NEEDED` or `PENDING_APPROVAL`.


This detailed outline provides a comprehensive understanding of the HubSpot CRM Quotes API. Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
