# HubSpot CRM API: Quotes

This document details the HubSpot CRM API for managing sales quotes.  It covers creating, updating, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows you to create, manage, and retrieve sales quotes within HubSpot.  Quotes can be shared via URL or PDF.  Integration with HubSpot payments or Stripe allows for online payments.

The quote creation process involves these steps:

1. **Create a quote:** Define basic details (name, expiration date). Optionally enable e-signatures and payments.
2. **Set up associations:** Link the quote to line items, a quote template, a deal, contacts, and companies.
3. **Set the quote state:**  Transition the quote through states like `DRAFT`, `APPROVAL_NOT_NEEDED`, `APPROVED`, etc., to reflect its progress.
4. **Share the quote:** Once published, share the quote's URL or PDF with the buyer.


## API Endpoints

### 1. Create a Quote

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/quotes`

**Request Body (minimum):**

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

**Response:** A `200` response with the created quote's `id`.

### 2. Update Quote Properties

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Request Body:**  A JSON object containing the properties to update.

**Example:**

```json
{
  "properties": {
    "hs_note": "Added a new discount."
  }
}
```

**Response:** A `200` response confirming the update.


### 3.  Enable E-signatures

Include `hs_esign_enabled: true` in the request body (POST or PATCH).  Countersigners must be added in HubSpot.  Publishing is blocked if the monthly e-signature limit is exceeded.


### 4. Enable Payments

Include the following properties in the request body (POST or PATCH):

* `hs_payment_enabled`: `true`
* `hs_payment_type`: `"HUBSPOT"` or `"BYO_STRIPE"`
* `hs_allowed_payment_methods`:  e.g., `"CREDIT_OR_DEBIT_CARD;ACH"`
* `hs_collect_billing_address`: `true` / `false`
* `hs_collect_shipping_address`: `true` / `false`


HubSpot automatically updates `hs_payment_status` and `hs_payment_date`.


### 5. Adding Associations

Use the Associations API (`/crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`) to link the quote with other objects.  `PUT` requests are used to create associations.

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


**Retrieving IDs:** Use `GET` requests to the relevant object endpoints (e.g., `/crm/v3/objects/line_items?properties=name`) to obtain the IDs needed for associations.


### 6. Create a Quote with Associations (Single Request)

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/quote`

**Request Body:**

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-09-30"
  },
  "associations": [
    // Association objects for quote template, deal, line items, etc.
  ]
}
```

See the original text for the detailed structure of the `associations` array.


### 7. Update Quote State

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/quote/{quoteId}`

**Request Body:**

```json
{
  "properties": {
    "hs_status": "APPROVAL_NOT_NEEDED" // or DRAFT, APPROVED, etc.
  }
}
```

This updates the `hs_status` property, changing the quote's state and potentially updating other properties automatically.


### 8. Retrieve Quotes

**Individual Quote:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/quotes/{quoteID}`

**List of Quotes:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/quotes`

**Batch Retrieval:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/quotes/batch/read`

Query parameters (`properties`, `propertiesWithHistory`, `associations`) can be used for filtering and specifying returned data.


## Properties Set by Quote State

Several properties are automatically updated when the quote's state changes.  See the original text for a complete list, including those automatically set upon publication.


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

This comprehensive documentation provides a detailed overview of the HubSpot CRM Quotes API, enabling developers to effectively integrate quote management into their applications. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
