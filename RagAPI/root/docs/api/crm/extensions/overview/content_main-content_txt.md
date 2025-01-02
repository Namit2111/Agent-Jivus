# HubSpot Extensions Overview

This document provides an overview of HubSpot extensions, their functionality, and how they integrate with HubSpot apps.

## What are HubSpot Extensions?

HubSpot extensions allow customization of the HubSpot CRM functionality. They enable features like creating custom events for CRM record timelines, integrating custom calling options, and building custom UI elements.  There are several types of extensions, each with different capabilities.

## Types of HubSpot Extensions

| Extension Type             | Description                                                                                                        | Supported App Types                                                                  |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| **Calling extensions SDK** | Enables users to make calls using custom calling options.                                                         | Public Apps                                                                         |
| **Custom timeline events**  | Creates custom events displaying information from other systems on CRM record timelines.                           | Public Apps                                                                         |
| **Classic CRM cards**      | Creates cards to pull external data into CRM records. Offers less customization than UI extensions.              | Public Apps                                                                         |
| **UI extensions (BETA)**   | Customizes CRM record pages with custom cards; sends and receives HubSpot and external data using customizable components.| Private Apps (created with Projects Beta) and Public Apps (created with Projects Beta) |
| **Video conference extension** | Integrates video conferencing into the meetings tool.                                                           | Public Apps                                                                         |


## Extension Support in Apps

Extensions are powered by HubSpot apps.  You must first create a public app or a private app (using the Projects Beta) before adding an extension.  The type of app determines which extensions are supported:

| App Type     | Supported Extensions                                                                                                |
|--------------|---------------------------------------------------------------------------------------------------------------------|
| Private App  | UI extensions (supported in private apps created with Projects (BETA))                                             |
| Public App   | Calling SDK, Classic CRM cards, Timeline events, Video conference extension, UI extensions (using Projects (BETA)) |

**Note:** Classic CRM cards differ from UI extensions (created with Projects Beta). UI extensions offer more advanced functionality and customization.


##  Example (Conceptual): Adding a Custom Timeline Event

This example illustrates adding a custom timeline event (requires a public app):

1. **Create a Public App:** Follow the HubSpot documentation to create a public app.
2. **Develop the Extension:**  Use the HubSpot API to create the logic for your custom event. This involves defining the event data, how it's fetched, and how it's displayed on the timeline.
3. **Integrate with App:**  Integrate your extension into your public app.
4. **Deploy and Install:** Deploy your app to the HubSpot marketplace or install it privately.


## API and Endpoint Reference

The specific API endpoints and methods for interacting with each extension type are not fully detailed in the provided text.  Refer to the official HubSpot Developer Documentation for comprehensive API reference material related to each extension type.


## Further Information

For more detailed information on building apps and the differences between private and public apps, refer to the HubSpot documentation on building apps overview.  The beta nature of some features implies that documentation and capabilities may change. Always refer to the official HubSpot Developer portal for the most up-to-date information.
