# HubSpot Extensions Overview

This document provides an overview of HubSpot extensions, their functionalities, and how they integrate with HubSpot apps.

## What are HubSpot Extensions?

HubSpot extensions allow customization of the HubSpot CRM functionality.  They enable developers to integrate external systems and data, enhancing the CRM's capabilities. Examples include adding custom calling options, displaying information from other systems on CRM timelines, and creating custom CRM record pages.

## Types of HubSpot Extensions

HubSpot offers several types of extensions:

* **Calling Extensions SDK:** Enables users to make calls using custom calling options.

* **Custom Timeline Events:** Creates custom events that display information from other systems on CRM record timelines.

* **Classic CRM Cards:** Creates cards to pull external data into CRM records.  These offer less customization than UI extensions.

* **UI Extensions (BETA):**  Allows customization of CRM record pages with custom cards. These cards can send and receive HubSpot and external data using a wide variety of customizable components. This is a beta feature.

* **Video Conference Extension:** Integrates video conferencing into the meetings tool.


## Extension Support in Apps

Extensions are powered by HubSpot apps. You must first create either a public app or a private app before adding an extension.  The type of app determines which extensions are supported:

| App Type        | Supported Extensions                                                                         | Notes                                                                                                |
|-----------------|---------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| Private App     | UI Extensions (supported in private apps created with projects (BETA))                       |                                                                                                       |
| Public App      | Calling SDK, Classic CRM Cards, Timeline Events, Video Conference Extension, UI Extensions (supported in public apps created with projects (BETA)) | UI Extensions offer more advanced functionality and customizable components than Classic CRM Cards. |


**Note:**  Classic CRM cards are distinct from the app cards created as UI extensions using Projects (BETA). UI extensions provide more advanced functionality and customizable components.


## Getting Started with Extensions

1. **Create an App:** Decide whether to create a public or private app based on the extensions you need (see table above).  Refer to the HubSpot documentation on building apps for more details.

2. **Choose an Extension:** Select the extension(s) that best suit your needs from the list above.

3. **Develop and Implement:** Follow HubSpot's developer documentation for the specific extension you've chosen to integrate it into your app.


## Example (Conceptual): Custom Timeline Event

Let's say you want to create a custom timeline event that displays order updates from your e-commerce platform.  You would:

1. **Create a Public App:**  Because timeline events are supported by public apps.
2. **Develop the Extension:**  Use the HubSpot API to fetch order update data from your e-commerce platform.  Then, use the Custom Timeline Events extension to display this data on the relevant CRM record timeline.
3. **Deploy the App:**  Make your app available to your HubSpot account.


This example illustrates a high-level workflow. Specific API calls and implementation details will depend on the chosen extension and its documentation.  Refer to HubSpot's API documentation for detailed information on specific API calls and responses.


##  Further Information

For detailed information and API references, consult the official HubSpot Developer Documentation.  Specifically, look for sections on:

* **Apps:**  For creating and managing apps.
* **API Endpoints:**  For making API calls to interact with HubSpot.
* **Specific Extension Documentation:** Each extension will have its own documentation with API details and implementation guides.


This markdown provides a concise overview.  Always refer to the official HubSpot documentation for the most accurate and up-to-date information.
