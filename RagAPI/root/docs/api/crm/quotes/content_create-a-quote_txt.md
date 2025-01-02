# HubSpot CRM API: Quotes

This document details the HubSpot CRM API for managing sales quotes.  It covers creating, managing, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows you to create, manage, and retrieve sales quotes within HubSpot.  Quotes can be shared via URL or PDF.  Integration with HubSpot Payments or Stripe enables payment processing directly through the API.

The quote creation process involves these steps:

1. **Create a Quote:** Create a basic quote with details like name and expiration date.  You can also enable e-signatures and payments.
2. **Set Up Associations:** Associate the quote with other CRM objects (line items, quote template, deal, etc.).
3. **Set the Quote State:** Set the quote's state (draft, published, pending approval, etc.) to reflect its status.
4. **Share the Quote:** Once published, share the quote with buyers.


## API Endpoints

The API uses standard HTTP methods (GET, POST, PATCH, PUT).  All endpoints are under the `/crm/v3/` or `/crm/v4/` base URL.  Remember to replace placeholders like `{quoteId}` with actual IDs.

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

**Optional Properties:**  (See `/crm/v3/properties/quotes` GET request for full list)

* `hs_esign_enabled` (boolean): Enable e-signatures (true/false).
* `hs_payment_enabled` (boolean): Enable payments (true/false).
* `hs_payment_type` (enum): Payment processor ("HUBSPOT" or "BYO_STRIPE").
* `hs_allowed_payment_methods` (enum): Allowed payment methods (e.g., "CREDIT_OR_DEBIT_CARD;ACH").
* `hs_collect_billing_address` (boolean): Collect billing address (true/false).
* `hs_collect_shipping_address` (boolean): Collect shipping address (true/false).


**Response:**  A `200 OK` response with the newly created quote's ID and other properties.


### 2.  Update Quote Properties

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body:** (Example updating status)

```json
{
  "properties": {
    "hs_status": "APPROVAL_NOT_NEEDED"
  }
}
```

**Response:** A `200 OK` response.


### 3. Retrieve Quotes

**Endpoint (single):** `/crm/v3/objects/quotes/{quoteId}`

**Endpoint (batch):** `/crm/v3/objects/quotes/batch/read` (Method: `POST`)

**Method:** `GET` (single), `POST` (batch)

**Query Parameters (single & batch):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties with history to return.
* `associations`: Comma-separated list of associated objects to retrieve.

**Request Body (batch):**

```json
{
  "inputs": [
    {"id": "quoteId1"},
    {"id": "quoteId2"}
  ],
  "properties": ["property1", "property2"]
}
```

**Response:** A `200 OK` response containing the requested quote(s) data.


### 4.  Managing Associations

**a) Retrieving IDs:** Use `GET` requests to retrieve IDs for associated objects (line items, quote templates, deals, contacts, companies, discounts, fees, taxes).  For example: `/crm/v3/objects/line_items?properties=name`


**b) Creating Associations (individual requests):** Use `PUT` requests to the `/crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}` endpoint.


**c) Creating Associations (single request with quote creation):**  Create associations during quote creation via the `associations` array in the POST request to `/crm/v3/objects/quote`. See example in the original text.


**d) Associating Quote Signers:** Use a `PUT` request to `/crm/v4/objects/quote/{quoteId}/associations/contact/{contactId}` with a specific `associationTypeId` (702).


## Quote States

* **No State (Minimal):**  Visible in the quotes tool but not directly editable.
* **DRAFT:** Editable in HubSpot.
* **APPROVAL_NOT_NEEDED:** Published without approval.
* **PENDING_APPROVAL:** Awaiting approval.
* **APPROVED:** Published and accessible.
* **REJECTED:** Needs edits before resubmission.


## Properties Set by Quote State

Several properties are automatically set or updated based on the quote's state and associations (e.g., `hs_quote_amount`, `hs_domain`, `hs_quote_link`, `hs_payment_status`).


## Scopes

The following scopes are required for app access:

* `crm.objects.quotes.write`, `crm.objects.quotes.read`
* `crm.objects.line_items.write`, `crm.objects.line_items.read`
* `crm.objects.owners.read`
* `crm.objects.contacts.write`, `crm.objects.contacts.read`
* `crm.objects.deals.write`, `crm.objects.deals.read`
* `crm.objects.companies.write`, `crm.objects.companies.read`
* `crm.schemas.quote.read`, `crm.schemas.line_items.read`, `crm.schemas.contacts.read`, `crm.schemas.deals.read`, `crm.schemas.companies.read`


This markdown documentation provides a comprehensive overview of the HubSpot CRM Quotes API, including examples and explanations of various endpoints and operations.  Remember to consult the official HubSpot API documentation for the most up-to-date information.
