# HubSpot CRM API: Quotes

This document details the HubSpot CRM API endpoints for managing sales quotes.  It covers creating, updating, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows you to create, manage, and retrieve sales quotes within HubSpot. Quotes can be shared via URL or PDF.  You can also manage quote details, associations, and states directly through the API.  Integration with HubSpot Payments or Stripe allows for payment processing.

### Key Concepts

* **Quote Creation:** A multi-step process involving creating the quote, setting up associations, and setting the quote state.
* **Associations:** Linking the quote to other CRM objects like line items, deals, contacts, and companies.
* **Quote State:**  Reflects the quote's progress (draft, pending approval, approved, rejected, etc.).  Changing the state triggers automatic property updates.
* **Payments:** Enabling payment collection via HubSpot Payments or Stripe.
* **E-signatures:** Enabling e-signature capabilities on the quote.

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

**Optional Properties:**  (See `/crm/v3/properties/quotes` for a complete list)

* `hs_esign_enabled` (boolean): Enable e-signatures (`true`/`false`).
* `hs_payment_enabled` (boolean): Enable payments (`true`/`false`).
* `hs_payment_type` (enumeration): Payment processor (`HUBSPOT` or `BYO_STRIPE`).
* `hs_allowed_payment_methods` (enumeration): Allowed payment methods (e.g., `CREDIT_OR_DEBIT_CARD;ACH`).
* `hs_collect_billing_address` (boolean): Collect billing address.
* `hs_collect_shipping_address` (boolean): Collect shipping address.


**Response:**  A `200 OK` response containing the newly created quote's ID and other properties.

### 2. Update Quote Properties

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body:**

```json
{
  "properties": {
    "hs_title": "Updated Quote Name",
    "hs_expiration_date": "2024-01-15"
  }
}
```

**Response:** A `200 OK` response confirming the update.

### 3. Retrieve Quotes

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}` (individual) or `/crm/v3/objects/quotes` (all)

**Method:** `GET`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties with history to return.
* `associations`: Comma-separated list of associated objects to retrieve.

**Response:** A `200 OK` response with the requested quote(s) data.

**Batch Retrieval:**  `/crm/v3/objects/quotes/batch/read` (POST) - Accepts an array of quote IDs.

### 4. Quote Owner

The `hubspot_owner_id` property is calculated:

* If a deal is associated: It reflects `hs_associated_deal_owner_id`.
* Otherwise: It reflects `hs_quote_owner_id`.

You cannot manually set `hubspot_owner_id`.


### 5. Adding Associations

Requires using the Associations API (`/crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`).  `PUT` requests are used to associate a quote with:

* Line items
* Quote template
* Deal
* Contact
* Company
* Discounts
* Fees
* Taxes

**Example (Associate Line Item):**

`PUT /crm/v4/objects/quotes/{quoteId}/associations/default/line_items/{lineItemId}`


### 6. Update Quote State

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body:**

```json
{
  "properties": {
    "hs_status": "APPROVAL_NOT_NEEDED"  // or DRAFT, PENDING_APPROVAL, APPROVED, REJECTED
  }
}
```

**Response:** A `200 OK` response indicating the state update.  Changing the state automatically updates several properties (e.g., `hs_quote_amount`, `hs_quote_link`).


### 7. Create Quote with Associations (Single Request)

**Endpoint:** `/crm/v3/objects/quote`

**Method:** `POST`

**Request Body:** This combines quote creation and association in a single request.  See the original text for the complex structure of this request body, which includes `properties` and `associations` arrays.


## Scopes

The following scopes are required:

`crm.objects.quotes.write`, `crm.objects.quotes.read`, `crm.objects.line_items.write`, `crm.objects.line_items.read`, `crm.objects.owners.read`, `crm.objects.contacts.write`, `crm.objects.contacts.read`, `crm.objects.deals.write`, `crm.objects.deals.read`, `crm.objects.companies.write`, `crm.objects.companies.read`, `crm.schemas.quote.read`, `crm.schemas.line_items.read`, `crm.schemas.contacts.read`, `crm.schemas.deals.read`, `crm.schemas.companies.read`


This markdown documentation provides a comprehensive overview of the HubSpot CRM Quotes API. Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
