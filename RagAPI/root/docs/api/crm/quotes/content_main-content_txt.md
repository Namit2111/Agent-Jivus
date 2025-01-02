# HubSpot CRM API: Quotes

This document details the HubSpot CRM API endpoints for managing sales quotes.  Quotes allow sharing pricing information with potential buyers, either via a URL or PDF.  This API enables creation, management, and retrieval of quotes, including features like e-signatures and payments.

## API Endpoints

All endpoints utilize the `/crm/v3/` or `/crm/v4/` base path.  You will need to replace placeholders like `{quoteId}` with actual IDs.

### 1. Create a Quote

**Endpoint:** `/crm/v3/objects/quotes`

**Method:** `POST`

**Request Body:**

The request body must include at minimum `hs_title` and `hs_expiration_date`.  Other properties are available to enhance the quote (see [Properties](#properties)).

```json
{
  "properties": {
    "hs_title": "CustomerName - annual SEO audit",
    "hs_expiration_date": "2023-12-10"
  }
}
```

**Response:** A `200 OK` response containing the newly created quote's `id` and other properties.


### 2. Update Quote Properties

**Endpoint:** `/crm/v3/objects/quotes/{quoteId}`

**Method:** `PATCH`

**Request Body:**

A JSON object containing the properties to update.

```json
{
  "properties": {
    "hs_title": "Updated Quote Title",
    "hs_expiration_date": "2024-01-15"
  }
}
```

**Response:** A `200 OK` response confirming the update.


### 3. Retrieve Quotes

**Endpoint:** `/crm/v3/objects/quotes`  or `/crm/v3/objects/quotes/{quoteId}`

**Method:** `GET`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve (e.g., `line_items`, `deals`).

**Response:**  A `200 OK` response with an array of quotes (for the list endpoint) or a single quote object (for the individual quote endpoint).


### 4. Batch Read Quotes

**Endpoint:** `/crm/v3/objects/quotes/batch/read`

**Method:** `POST`

**Request Body:**

```json
{
  "inputs": [
    {"id": "quoteId1"},
    {"id": "quoteId2"}
  ],
  "properties": ["hs_title", "hs_expiration_date"]
}
```

**Response:** A `200 OK` response containing the requested quotes' properties.  Note: Associations cannot be retrieved via this endpoint.


### 5.  Add Associations

**Endpoint:** `/crm/v4/objects/quotes/{quoteId}/associations/default/{toObjectType}/{toObjectId}`

**Method:** `PUT`

**Parameters:**

* `quoteId`: ID of the quote.
* `toObjectType`: Type of object to associate (e.g., `line_items`, `deals`, `quote_template`).
* `toObjectId`: ID of the object to associate.

**Response:** A `200 OK` response confirming the association.

### 6. Associate Quote Signers (E-Signatures)

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

**Response:** A `200 OK` response confirming the association.


### 7. Create Quote with Associations (Single Request)

**Endpoint:** `/crm/v3/objects/quote`

**Method:** `POST`

**Request Body:**  Combines quote properties and associations in a single request.

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

**Response:** A `200 OK` response containing the newly created quote's ID and other details.


### 8. Update Quote State

**Endpoint:** `/crm/v3/objects/quote/{quoteId}`

**Method:** `PATCH`

**Request Body:** Update `hs_status` property.  Possible values: `DRAFT`, `APPROVAL_NOT_NEEDED`, `PENDING_APPROVAL`, `APPROVED`, `REJECTED`.

```json
{
  "properties": {
    "hs_status": "APPROVAL_NOT_NEEDED"
  }
}
```

**Response:** A `200 OK` response confirming the state update.



## Properties

The following properties are commonly used:

* **`hs_title` (string, required):** Quote name.
* **`hs_expiration_date` (string, required):** Quote expiration date (YYYY-MM-DD).
* **`hs_esign_enabled` (boolean):** Enables e-signatures.
* **`hs_payment_enabled` (boolean):** Enables payments.
* **`hs_payment_type` (enumeration):** Payment processor (`HUBSPOT` or `BYO_STRIPE`).
* **`hs_allowed_payment_methods` (enumeration):** Allowed payment methods (e.g., `CREDIT_OR_DEBIT_CARD;ACH`).
* **`hs_status` (string):** Quote status (see [Update Quote State](#update-quote-state)).
* **`hubspot_owner_id` (calculated):** Quote owner ID (determined by associated deal or `hs_quote_owner_id`).


## Scopes

The following scopes are required for full functionality:

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


This documentation provides a comprehensive overview of the HubSpot CRM API for quotes.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
