# HubSpot CRM API: Quotes Documentation

This document details the HubSpot CRM API endpoints for managing sales quotes.  It covers creating, updating, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows developers to programmatically create, manage, and retrieve sales quotes.  Quotes can be shared with buyers via a URL or PDF.  Integration with HubSpot Payments or Stripe allows for online payment processing.

The quote creation process involves these steps:

1. **Create a quote:** Define basic details (name, expiration date, etc.). Optionally, enable e-signatures and payments.
2. **Set up associations:** Link the quote to other CRM objects (line items, quote template, deal, etc.).  This inheritance property values from associated records and account settings.
3. **Set the quote state:**  Transition the quote through stages (draft, pending approval, published, etc.), impacting its accessibility and properties.
4. **Share the quote:**  Once published, share the quote's URL or PDF with the buyer.


## API Endpoints

### 1. Create a Quote

**Endpoint:** `/crm/v3/objects/quotes`

**Method:** `POST`

**Request Body:**

Requires `hs_title` (string) and `hs_expiration_date` (string, YYYY-MM-DD).  Other properties can be included (see [Properties](#properties)).

**Example Request Body:**

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-12-10"
  }
}
```

**Response:**  A `200 OK` response containing the created quote's ID and other properties.


### 2. Update Quote Properties

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body:**  A JSON object containing the properties to update.

**Example Request Body (Enable E-signatures):**

```json
{
  "properties": {
    "hs_esign_enabled": true
  }
}
```

**Response:** A `200 OK` response.


### 3. Enable E-signatures

Include the `hs_esign_enabled` boolean property (set to `true`) in the request body when creating or updating a quote.  Note: Countersigners must be added in HubSpot;  publishing is blocked if the monthly e-signature limit is exceeded.


### 4. Enable Payments

Include the following properties in the request body:

* `hs_payment_enabled`: Boolean (true to enable)
* `hs_payment_type`: Enumeration (`HUBSPOT` or `BYO_STRIPE`)
* `hs_allowed_payment_methods`: Enumeration (e.g., `CREDIT_OR_DEBIT_CARD;ACH`)
* `hs_collect_billing_address`: Boolean
* `hs_collect_shipping_address`: Boolean

**Example Request Body (HubSpot Payments):**

```json
{
  "properties": {
    "hs_payment_enabled": true,
    "hs_payment_type": "HUBSPOT",
    "hs_allowed_payment_methods": "CREDIT_OR_DEBIT_CARD;ACH"
  }
}
```

HubSpot will update `hs_payment_status` and `hs_payment_date` automatically.


### 5. Adding Associations

Use the Associations API (`/crm/v4/objects/quotes/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`) to link the quote to other objects.  Required associations include line items, quote template, and deal.

**Example PUT Request (Associate Line Item):**

```
PUT /crm/v4/objects/quotes/{quoteId}/associations/default/line_items/{lineItemId}
```

### 6. Retrieving IDs for Associations

Use `GET /crm/v3/objects/{objectType}?properties={propertyList}` to retrieve IDs of associated objects (line items, quote templates, deals, contacts, companies, discounts, fees, taxes).


### 7. Create a Quote with Associations (Single Request)

**Endpoint:** `/crm/v3/objects/quotes`

**Method:** `POST`

**Request Body:**  Includes both `properties` and `associations` arrays.

**Example Request Body:**

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


### 8. Update Quote State

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

Update the `hs_status` property to change the quote's state (DRAFT, APPROVAL_NOT_NEEDED, PENDING_APPROVAL, APPROVED, REJECTED).


### 9. Retrieve Quotes

* **Individual Quote:** `GET /crm/v3/objects/quotes/{quoteID}`
* **List of Quotes:** `GET /crm/v3/objects/quotes`
* **Batch Retrieval:** `POST /crm/v3/objects/quotes/batch/read`


## Properties

Refer to the `GET /crm/v3/properties/quotes` endpoint for a complete list of available quote properties.  Key properties include:

* `hs_title`
* `hs_expiration_date`
* `hs_esign_enabled`
* `hs_payment_enabled`
* `hs_payment_type`
* `hs_allowed_payment_methods`
* `hs_status`
* `hs_quote_amount`
* `hs_quote_link` (read-only, populated upon publishing)
* `hubspot_owner_id` (calculated)


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


This documentation provides a comprehensive overview of the HubSpot CRM Quotes API. Refer to the official HubSpot API documentation for the most up-to-date information and details.
