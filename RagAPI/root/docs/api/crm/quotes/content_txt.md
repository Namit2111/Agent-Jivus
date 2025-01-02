# HubSpot CRM API: Quotes

This document details the HubSpot CRM API endpoints for managing sales quotes.  It covers creating, updating, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows developers to create, manage, and retrieve sales quotes. Quotes can be shared with buyers via URL or PDF.  The API supports e-signatures and payments integration (HubSpot Payments or Stripe).

The quote creation process involves these steps:

1. **Create a quote:** Define basic details (name, expiration date, etc.).  Optionally enable e-signatures and payments.
2. **Set up associations:** Link the quote to other CRM objects (line items, quote template, deal, contacts, companies, discounts, fees, taxes).
3. **Set the quote state:**  Transition the quote through stages (draft, pending approval, approved, rejected) to reflect its progress.
4. **Share the quote:** Once published, share the quote's URL or PDF with the buyer.

## API Endpoints

All endpoints are under the `/crm/v3` or `/crm/v4` base URL.  Remember to replace placeholders like `{quoteId}` with actual values.

### 1. Create a Quote

**Endpoint:** `/crm/v3/objects/quotes`

**Method:** `POST`

**Request Body:**

Requires `hs_title` (string) and `hs_expiration_date` (string, YYYY-MM-DD).  Other properties can be included (see [Properties API](#properties-api)).

**Example Request Body:**

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-12-10"
  }
}
```

**Response:** A `200 OK` response with the created quote's `id`.

### 2. Create a Quote with Associations (Single Request)

**Endpoint:** `/crm/v3/objects/quote`

**Method:** `POST`

**Request Body:**

Requires `properties` (object containing at least `hs_title` and `hs_expiration_date`) and `associations` (array of associations).  See details below.


**Example Request Body:**

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-09-30"
  },
  "associations": [
    {
      "to": { "id": 115045534742 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 286 }]
    },
    // ... other associations
  ]
}
```

**Response:** A `200 OK` response with the created quote's `id`.

**Association Type IDs:**

* `286`: quote to quote template
* `64`: quote to deal
* `67`: quote to line item


### 3. Update Quote Properties

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body:**  An object containing the properties to update.

**Example Request Body (Enable E-signatures):**

```json
{
  "properties": {
    "hs_esign_enabled": true
  }
}
```

**Response:** A `200 OK` response.


### 4. Update Quote State

**Endpoint:** `/crm/v3/objects/quote/{quoteId}`

**Method:** `PATCH`

**Request Body:** Update the `hs_status` property.

**Possible `hs_status` values:**

* `DRAFT`: Editable in HubSpot.
* `APPROVAL_NOT_NEEDED`: Published without approval.
* `PENDING_APPROVAL`: Awaiting approval.
* `APPROVED`: Published and approved.
* `REJECTED`: Rejected, requires edits.

**Example Request Body (Publish):**

```json
{
  "properties": {
    "hs_status": "APPROVAL_NOT_NEEDED"
  }
}
```

**Response:** A `200 OK` response.


### 5. Retrieve Quotes

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}` (single quote) or `/crm/v3/objects/quotes` (all quotes) or `/crm/v3/objects/quotes/batch/read` (batch read)

**Method:** `GET` (single/all), `POST` (batch)

**Query Parameters:** `properties`, `propertiesWithHistory`, `associations`

**Example GET Request (single quote with properties):**

`/crm/v3/objects/quotes/123?properties=hs_title,hs_expiration_date`

**Example POST Request (batch):**

```json
{
  "inputs": [
    { "id": "342007287" },
    { "id": "81204505203" }
  ],
  "properties": ["hs_content", "hs_sentiment", "hs_submission_timestamp"]
}
```

**Response:** A `200 OK` response with the requested quote(s) data.


### 6.  Associations API

This API is used to associate quotes with other objects (line items, deals, contacts, etc.).  See the original text for details on endpoints and request methods (`PUT` requests are typically used).


### 7. Properties API

**Endpoint:** `/crm/v3/properties/quotes`

**Method:** `GET`

This endpoint returns all available properties for quotes.

##  Important Properties

* `hs_title`: Quote name.
* `hs_expiration_date`: Quote expiration date.
* `hs_status`: Quote state (DRAFT, APPROVAL_NOT_NEEDED, PENDING_APPROVAL, APPROVED, REJECTED).
* `hs_esign_enabled`: Enables e-signatures (boolean).
* `hs_payment_enabled`: Enables payments (boolean).
* `hs_payment_type`: Payment processor (HUBSPOT or BYO_STRIPE).
* `hs_allowed_payment_methods`: Allowed payment methods.
* `hs_quote_link`: Publicly accessible URL (read-only after publishing).
* `hs_pdf_download_link`: URL to download PDF (read-only after publishing).
* `hubspot_owner_id`: Quote owner ID (calculated).


## Scopes

The following OAuth scopes are required:

`crm.objects.quotes.write`, `crm.objects.quotes.read`, `crm.objects.line_items.write`, `crm.objects.line_items.read`, `crm.objects.owners.read`, `crm.objects.contacts.write`, `crm.objects.contacts.read`, `crm.objects.deals.write`, `crm.objects.deals.read`, `crm.objects.companies.write`, `crm.objects.companies.read`, `crm.schemas.quote.read`, `crm.schemas.line_items.read`, `crm.schemas.contacts.read`, `crm.schemas.deals.read`, `crm.schemas.companies.read`

This comprehensive documentation provides a detailed overview of the HubSpot CRM Quotes API, enabling developers to effectively integrate quote management into their applications.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
