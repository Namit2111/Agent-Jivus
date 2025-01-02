# HubSpot CRM API: Quotes Documentation

This document details the HubSpot CRM API endpoints for managing sales quotes.  It covers creating, updating, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows you to create, manage, and retrieve sales quotes.  Quotes can be shared via URL or PDF.  Integration with HubSpot payments or Stripe allows for online payments.

The quote creation process involves these steps:

1. **Create a quote:** Define basic details (name, expiration date). Optionally enable e-signatures and payments.
2. **Set up associations:** Link the quote to line items, a quote template, a deal, and other CRM objects.
3. **Set the quote state:**  Transition the quote through stages like `DRAFT`, `PENDING_APPROVAL`, `APPROVED`, etc., to reflect its progress.
4. **Share the quote:** Once published, share the quote with buyers.


## API Endpoints

### 1. Create a Quote

**Endpoint:** `/crm/v3/objects/quotes`

**Method:** `POST`

**Request Body:**

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",  // Required: Quote name
    "hs_expiration_date": "2023-12-10"          // Required: Expiration date (YYYY-MM-DD)
    // ... other properties (see below)
  }
}
```

**Required Properties:**

* `hs_title` (string): Quote name.
* `hs_expiration_date` (string): Quote expiration date (YYYY-MM-DD).

**Other Properties:** See `/crm/v3/properties/quotes` (GET request) for a complete list.

**Response:**  A `200 OK` response with the created quote's ID and other properties.  Example:

```json
{
  "id": "12345",
  // ... other properties
}
```


### 2. Update Quote Properties

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body:**

```json
{
  "properties": {
    // Properties to update
    "hs_title": "Updated Quote Name"
  }
}
```

**Response:** A `200 OK` response confirming the update.


### 3. Enable E-signatures

Include `hs_esign_enabled: true` in the POST or PATCH request body.  Note: Countersigners must be added in HubSpot;  publishing is blocked if the monthly e-signature limit is exceeded.


### 4. Enable Payments

Include the following properties in the POST or PATCH request body:

* `hs_payment_enabled`: `true`
* `hs_payment_type`: `"HUBSPOT"` or `"BYO_STRIPE"`
* `hs_allowed_payment_methods`:  e.g., `"CREDIT_OR_DEBIT_CARD;ACH"`
* `hs_collect_billing_address`: `true` / `false`
* `hs_collect_shipping_address`: `true` / `false`

**Note:** HubSpot payments or Stripe must be configured in your account.  `hs_payment_status` and `hs_payment_date` are automatically updated.


### 5. Adding Associations

Associate the quote with other CRM objects using the Associations API (`/crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`).

**Required Associations:**

* **Line items:** (Yes)  Use `/crm/v3/objects/line_items` to get IDs.
* **Quote template:** (Yes) Use `/crm/v3/objects/quote_template` to get IDs.
* **Deal:** (Yes) Use `/crm/v3/objects/deals` to get IDs.

**Optional Associations:**

* Contact
* Company
* Discounts
* Fees
* Taxes


**Example Association PUT Request:**

```
PUT /crm/v4/objects/quotes/12345/associations/default/line_items/67890
```

### 6. Create a Quote with Associations (Single Request)

**Endpoint:** `/crm/v3/objects/quote`

**Method:** `POST`

This allows creating a quote and its associations in a single request.  See the original text for the detailed request body structure, including `properties` and `associations` arrays with `associationTypeId`s.


### 7. Update Quote State

**Endpoint:** `/crm/v3/objects/quote/{quoteId}`

**Method:** `PATCH`

Update the `hs_status` property:

* `DRAFT`: Editable in HubSpot.
* `APPROVAL_NOT_NEEDED`: Published without approval.
* `PENDING_APPROVAL`: Awaiting approval.
* `APPROVED`: Published.
* `REJECTED`: Rejected; requires edits.

### 8. Retrieve Quotes

* **Individual Quote:** `GET /crm/v3/objects/quotes/{quoteID}`
* **List of Quotes:** `GET /crm/v3/objects/quotes`
* **Batch Retrieval:** `POST /crm/v3/objects/quotes/batch/read` (IDs in request body)

Use query parameters `properties`, `propertiesWithHistory`, and `associations` to customize the response.


### 9. Properties Set by Quote State

Several properties are automatically populated based on the quote's state and associations (e.g., `hs_quote_amount`, `hs_domain`, `hs_quote_link`, `hs_payment_status`).


## Scopes

The following OAuth scopes are required:

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


This documentation provides a comprehensive overview. Refer to the HubSpot API documentation for the most up-to-date information and detailed specifications.
