# HubSpot Extensions Overview

This document provides an overview of HubSpot extensions, their functionalities, and how they integrate with HubSpot apps.

## What are HubSpot Extensions?

HubSpot extensions allow customization of the HubSpot CRM functionality.  They enable developers to integrate external systems and data, enhancing the CRM's capabilities.  Examples include adding custom events to timelines, integrating custom calling options, and creating custom UI elements.

## Types of HubSpot Extensions

HubSpot offers several types of extensions:

* **Calling Extensions SDK:** Enables users to make calls using custom calling options.

* **Custom Timeline Events:** Creates custom events displaying information from other systems on CRM record timelines.

* **Classic CRM Cards:** Creates cards to pull external data into CRM records. These offer less customization than UI extensions.

* **UI Extensions (BETA):**  Allows customization of CRM record pages with custom cards capable of sending and receiving HubSpot and external data using various customizable components.  This is a beta feature.

* **Video Conference Extension:** Integrates video conferencing into the meetings tool.


## Extension Support in Apps

Extensions are powered by apps.  You must first create a public app or a private app before adding an extension.  The type of app determines which extensions are supported:

| App Type        | Supported Extensions                                                                     | Notes                                                                                                  |
|-----------------|-----------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Private App     | UI Extensions (Supported in private apps created with projects (BETA))                     |                                                                                                          |
| Public App      | Calling SDK, Classic CRM Cards, Timeline Events, Video Conference Extension, UI Extensions (Supported in public apps created with projects (BETA)) | UI Extensions offer more advanced functionality and customizable components than Classic CRM Cards. |


**Note:** Classic CRM cards differ from UI extension app cards created with projects (BETA). UI extensions provide more advanced functionality and customization.


##  Example (Conceptual):  Adding a Custom Timeline Event

While specific API calls are not provided in the source text, a conceptual example of adding a custom timeline event might involve:

1. **API Call:**  Making an API request to the HubSpot API (endpoint unspecified in source text) to create a new timeline event.  The request would include data such as the CRM record ID, event type, and event details.

2. **Response:** The API would return a response indicating success or failure, possibly including an ID for the newly created event.

3. **UI Update:** The HubSpot CRM UI would automatically update to display the new custom event on the relevant record timeline.


## Further Information

For detailed API documentation and specifics on creating and using extensions, refer to the HubSpot Developer Documentation.  The provided text does not contain this level of detail.
