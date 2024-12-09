# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot accounts.

## Overview

HubSpot provides standard CRM objects (contacts, companies, deals, tickets).  Custom objects extend this functionality, enabling representation of business-specific data.  This API allows definition of custom objects, their properties, and associations with other CRM objects.  Access requires a Marketing Hub, Sales Hub, Content Hub, Service Hub, or Operations Hub Enterprise subscription.  Account-specific limits on the number of custom objects apply.

**Prerequisites:**

*   One of the following HubSpot products (or higher):
    *   Marketing Hub Enterprise
    *   Sales Hub Enterprise
    *   Content Hub Enterprise
    *   Service Hub Enterprise
    *   Operations Hub Enterprise
*   Authentication via OAuth or private app access tokens (HubSpot API Keys are deprecated).

## Authentication Methods

*   **OAuth:**  Standard OAuth 2.0 flow for secure authentication.
*   **Private App Access Tokens:**  Generate access tokens through a private app for specific permissions.

**Note:** HubSpot API Keys are deprecated as of November 30, 2022.  Migrate existing integrations to OAuth or private app access tokens.


## Create a Custom Object

Creating a custom object involves defining its schema: name, properties, and associations.

**Request:**

*   **Method:** `POST`
*   **Endpoint:** `/crm/v3/schemas`
*   **Body:**  JSON object defining the schema (see details below).

**Schema Definition:**

*   `name`: Object name (alphanumeric and underscores only; must start with a letter).  Cannot be changed after creation.
*   `description`:  (Optional) Description of the object's purpose.
*   `labels`:  Object labels (singular and plural).
*   `primaryDisplayProperty`: Property used to name individual records.
*   `secondaryDisplayProperties`: Properties displayed under the `primaryDisplayProperty` (up to 4, with limitations on property types for the fourth).
*   `searchableProperties`: Properties indexed for searching.
*   `requiredProperties`: Properties required when creating new records.
*   `properties`: Array of property definitions (see details below).
*   `associatedObjects`: Array of associated object IDs (standard objects use names; custom objects use `objectTypeId`).


## Properties

Properties define data fields within custom object records.  Each custom object has a limit of 10 unique value properties.

**Property Definition:**

*   `name`: Property name.
*   `label`: Property label.
*   `type`: Property data type (`string`, `number`, `enumeration`, `date`, `dateTime`, `boolean`).
*   `fieldType`: UI field type (`text`, `textarea`, `number`, `date`, `booleancheckbox`, `checkbox`, `radio`, `select`, `file`).
*   `options` (for `enumeration` type): Array of option labels and values.
*   `hasUniqueValue`: (Optional) Boolean indicating if the property should have unique values.


## Associations

Custom objects automatically associate with emails, meetings, notes, tasks, calls, and conversations.  Additional associations with standard or custom objects can be defined.

**Creating Associations:**

*   **Method:** `POST`
*   **Endpoint:** `/crm/v3/schemas/{objectTypeId}/associations`
*   **Body:** JSON with `fromObjectTypeId`, `toObjectTypeId`, and `name` fields.

## Retrieve Existing Custom Objects

**Retrieve All Custom Objects:**

*   **Method:** `GET`
*   **Endpoint:** `/crm/v3/schemas`

**Retrieve Specific Custom Object:**

*   **Method:** `GET`
*   **Endpoint:**  One of the following:
    *   `/crm/v3/schemas/{objectTypeId}`
    *   `/crm/v3/schemas/p_{object_name}`
    *   `/crm/v3/schemas/{fullyQualifiedName}`

## Retrieve Custom Object Records

**Retrieve Single Record:**

*   **Method:** `GET`
*   **Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`
*   **Query Parameters:** `properties`, `propertiesWithHistory`, `associations`.

**Retrieve Multiple Records (Batch):**

*   **Method:** `POST`
*   **Endpoint:** `/crm/v3/objects/{objectType}/batch/read`
*   **Body:** JSON with `properties`, `idProperty` (optional, for custom unique identifier), and `inputs` (array of IDs).  Associations cannot be retrieved via batch.


## Update Existing Custom Objects

**Update Object Schema:**

*   **Method:** `PATCH`
*   **Endpoint:** `/crm/v3/schemas/{objectTypeId}`
*   **Body:** JSON with updated schema properties (e.g., `requiredProperties`, `searchableProperties`, `secondaryDisplayProperties`).  Object name and labels cannot be changed.


## Update Associations

Add additional object associations.

*   **Method:** `POST`
*   **Endpoint:** `/crm/v3/schemas/{objectTypeId}/associations`

## Delete a Custom Object

Requires deletion of all object instances and associated data.

*   **Method:** `DELETE`
*   **Endpoint:** `/crm/v3/schemas/{objectType}` (soft delete) or `/crm/v3/schemas/{objectType}?archived=true` (hard delete).

## Custom Object Example (Car Dealership Scenario)

A detailed walkthrough demonstrates creating a custom object for car inventory, associating it with contacts and tickets, and adding properties.  The example covers schema creation, record creation, association creation, property definition, and schema updates.


## Error Handling

(Add details about error codes and responses)

## Rate Limits

(Add details about API rate limits)


This markdown provides a comprehensive overview of the HubSpot Custom Objects API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
