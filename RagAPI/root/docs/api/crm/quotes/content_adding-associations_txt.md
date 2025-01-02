# HubSpot CRM API: Quotes Documentation

This document details the HubSpot CRM API for managing sales quotes.  It covers creating, updating, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows you to create, manage, and retrieve sales quotes.  Quotes can be shared via URL or PDF.  Payment processing (via HubSpot Payments or Stripe) can be integrated.

**Example Use Case:** Creating a contract proposal for a customer interested in an annual SEO auditing service package.

**Quote Creation Process:**

1. **Create a quote:**  Basic details (name, expiration date) are provided via a POST request.  Optional features like e-signatures and payments can also be enabled.
2. **Set up associations:** Associate the quote with other CRM objects (line items, quote template, deal, etc.).  The quote inherits properties from associated records.
3. **Set the quote state:**  Update the quote's status (DRAFT, APPROVAL_NOT_NEEDED, APPROVED, etc.) to reflect its progress. This triggers property updates.
4. **Share the quote:** Once published, the quote can be shared with buyers.


## API Endpoints and Calls

### 1. Create a Quote

**Endpoint:** `/crm/v3/objects/quotes`

**Method:** `POST`

**Request Body (Minimum):**

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

**Other Properties (see `/crm/v3/properties/quotes` for full list):**

* `hs_esign_enabled` (boolean): Enable e-signatures (true/false).
* `hs_payment_enabled` (boolean): Enable payments (true/false).
* `hs_payment_type` (enum): Payment processor (HUBSPOT, BYO_STRIPE).
* `hs_allowed_payment_methods` (enum): Allowed payment methods (CREDIT_OR_DEBIT_CARD, ACH, etc.).  Requires `;` as separator for multiple methods.
* `hs_collect_billing_address` (boolean): Collect billing address (true/false).
* `hs_collect_shipping_address` (boolean): Collect shipping address (true/false).

**Response:**  A `200 OK` response containing the newly created quote's `id`.


### 2. Update Quote Properties

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body:**  Similar to the create request, but only include the properties you want to update.

**Response:** A `200 OK` response.


### 3. Retrieve Quotes

**Endpoint (Single Quote):** `/crm/v3/objects/quotes/{quoteId}`

**Endpoint (All Quotes):** `/crm/v3/objects/quotes`

**Endpoint (Batch):** `/crm/v3/objects/quotes/batch/read` (Method: `POST`)

**Method:** `GET` (single & all), `POST` (batch)

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties with history to return.
* `associations`: Comma-separated list of associated objects to retrieve.

**Batch Request Body:**

```json
{
  "inputs": [
    {"id": "quoteId1"},
    {"id": "quoteId2"}
  ],
  "properties": ["property1", "property2"]
}
```

**Response:**  A `200 OK` response containing the requested quote(s) data.


### 4. Quote Owner

The `hubspot_owner_id` property is calculated:

* If a deal is associated: it reflects `hs_associated_deal_owner_id`.
* If no deal is associated: it reflects `hs_quote_owner_id`.

You cannot set this property manually.


### 5. Adding Associations

**Required Associations:** Line items, Quote Template, Deal.

**Optional Associations:** Contact, Company, Discounts, Fees, Taxes.

**Retrieving IDs:** Use `GET` requests to the relevant object endpoints (e.g., `/crm/v3/objects/line_items?properties=name`).

**Creating Associations:** Use `PUT` requests to the associations API:
`/crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`

Example: Associating a line item:
`/crm/v4/objects/quotes/{quoteId}/associations/default/line_items/{lineItemId}`

**Response:** A `200 OK` response confirming the association.


### 6. Associating Quote Signers (E-signatures)

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


### 7. Create a Quote with Associations (Single Request)

**Endpoint:** `/crm/v3/objects/quote`

**Method:** `POST`

**Request Body:** This combines quote creation and association in a single request.  See the provided example in the original text.


### 8. Update Quote State

**Endpoint:** `/crm/v3/objects/quote/{quoteId}`

**Method:** `PATCH`

**Request Body:** Update the `hs_status` property:

```json
{
  "properties": {
    "hs_status": "APPROVAL_NOT_NEEDED" // or DRAFT, APPROVED, etc.
  }
}
```

**Response:** A `200 OK` response.  The state change updates several other properties automatically (e.g., `hs_quote_amount`, `hs_quote_link`).


## Properties Set by Quote State

Several properties are automatically populated or updated based on the quote's state and associated objects.  See the original text for a complete list.


## Scopes

The required OAuth scopes for accessing the Quotes API are listed in the original text.


This comprehensive markdown documentation provides a detailed overview of the HubSpot CRM Quotes API, including endpoints, request/response examples, and essential considerations for developers.  Remember to consult the official HubSpot API documentation for the most up-to-date information.
