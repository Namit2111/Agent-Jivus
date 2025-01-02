# HubSpot CRM API: Quotes

This document details the HubSpot CRM API for managing sales quotes.  It covers creating, updating, retrieving, and associating quotes with other CRM objects.

## Overview

The Quotes API allows developers to create, manage, and retrieve sales quotes within HubSpot.  Quotes can be shared with buyers via URL or PDF.  Integration with HubSpot Payments or Stripe allows for payment processing directly through the API.

The quote creation process involves these steps:

1. **Create a Quote:**  Create a basic quote with `hs_title` and `hs_expiration_date`.  Additional properties can be added to enable e-signatures and payments.
2. **Set up Associations:** Associate the quote with line items, a quote template, a deal, and other CRM objects.
3. **Set the Quote State:** Update the quote's `hs_status` to reflect its progress (e.g., `DRAFT`, `APPROVED`, `APPROVAL_NOT_NEEDED`). This action populates additional properties.
4. **Share the Quote:** Once published (`APPROVAL_NOT_NEEDED` or `APPROVED`), the quote can be shared with buyers.


## API Endpoints

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

**Response:**  A `200 OK` response with the newly created quote's `id` and other properties.

**Example Response:**

```json
{
  "id": "12345",
  // ... other properties ...
}
```

**Full Quote Creation (including associations):** See section "Create a quote with associations (single request)".


### 2. Update Quote Properties

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body:**  An object containing the properties to update.

```json
{
  "properties": {
    "hs_title": "Updated Quote Title",
    "hs_expiration_date": "2024-01-15"
  }
}
```

**Response:** A `200 OK` response confirming the update.


### 3. Update Quote State

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body:** Update the `hs_status` property.

```json
{
  "properties": {
    "hs_status": "APPROVAL_NOT_NEEDED"
  }
}
```

**Response:** A `200 OK` response confirming the state change.  Note that this will automatically populate other properties (e.g., `hs_quote_link`, `hs_pdf_download_link`).


### 4. Retrieve Quotes

**Endpoint (single quote):** `/crm/v3/objects/quotes/{quoteId}`

**Endpoint (batch):** `/crm/v3/objects/quotes/batch/read` (Method: `POST`)

**Endpoint (all quotes):** `/crm/v3/objects/quotes`

**Method:** `GET` (for single and all quotes), `POST` (for batch)

**Query Parameters:** `properties`, `propertiesWithHistory`, `associations`

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

**Response:** A `200 OK` response with the requested quote(s) data.


### 5. Get Quote Properties

**Endpoint:** `/crm/v3/properties/quotes`

**Method:** `GET`

**Response:** A list of all available quote properties.


### 6. Associations API

This API is used to associate quotes with other CRM objects (line items, deals, contacts, companies, etc.).  See the detailed sections below for specific endpoints and usage.


##  Key Properties

* **`hs_title`:** (String, Required) The name of the quote.
* **`hs_expiration_date`:** (String, Required) The quote's expiration date (YYYY-MM-DD).
* **`hs_esign_enabled`:** (Boolean) Enables e-signatures.
* **`hs_payment_enabled`:** (Boolean) Enables payments.
* **`hs_payment_type`:** (Enumeration) Payment processor (`HUBSPOT`, `BYO_STRIPE`).
* **`hs_allowed_payment_methods`:** (Enumeration) Allowed payment methods (e.g., `CREDIT_OR_DEBIT_CARD;ACH`).
* **`hs_status`:** (String) The quote's state (`DRAFT`, `APPROVAL_NOT_NEEDED`, `APPROVED`, `REJECTED`, `PENDING_APPROVAL`).
* **`hubspot_owner_id`:** (Calculated Property) The ID of the quote's owner.


##  Associations

### Retrieving IDs for Associations

Use `GET /crm/v3/objects/{objectType}?properties=id` to retrieve IDs for different object types (line items, deals, contacts, etc.).


### Creating Associations

Use `PUT /crm/v4/objects/quotes/{quoteId}/associations/default/{toObjectType}/{toObjectId}` to create associations.  For quote signers, use `/crm/v4/objects/quote/{quoteId}/associations/contact/{contactId}` with a specific `associationTypeId` (702).


##  Create a Quote with Associations (Single Request)

**Endpoint:** `/crm/v3/objects/quotes`

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

Each association object needs `to` (object ID), `associationCategory` (`HUBSPOT_DEFINED`), and `associationTypeId` (286 for quote template, 64 for deal, 67 for line item).


## Scopes

The following scopes are required:

`crm.objects.quotes.write`, `crm.objects.quotes.read`, `crm.objects.line_items.write`, `crm.objects.line_items.read`, `crm.objects.owners.read`, `crm.objects.contacts.write`, `crm.objects.contacts.read`, `crm.objects.deals.write`, `crm.objects.deals.read`, `crm.objects.companies.write`, `crm.objects.companies.read`, `crm.schemas.quote.read`, `crm.schemas.line_items.read`, `crm.schemas.contacts.read`, `crm.schemas.deals.read`, `crm.schemas.companies.read`


This documentation provides a comprehensive overview of the HubSpot CRM Quotes API.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
