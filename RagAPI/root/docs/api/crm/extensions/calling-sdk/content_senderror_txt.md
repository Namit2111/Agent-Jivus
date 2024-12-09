# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling options into their HubSpot apps.

## Overview

The Calling Extensions SDK facilitates communication between a calling app and HubSpot, allowing users to make calls directly from CRM records.  It consists of three core components:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK for communication between your app and HubSpot.
2. **Calling Settings Endpoints:** APIs for configuring your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:** The interface displayed to HubSpot users, configured via the calling settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](link_to_knowledge_base_article_here).  After integration, your app will appear in the HubSpot call switcher.  If you don't have a HubSpot app, you can [create one here](link_to_hubspot_developer_account_creation).

**Note:** Currently, only outgoing calls are supported.


## Getting Started

### Run the Demo Calling App

Two demo apps illustrate the SDK's usage:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more realistic implementation using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.


### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](link_to_zip_download) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * For `demo-minimal-js`:  `cd demos/demo-minimal-js && npm i && npm start`
   * For `demo-react-ts`:  `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Run one of the following commands (depending on whether you installed the demo app):
    * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page and select the demo app from the "Call from" dropdown in the call switcher.


### Install the Calling Extensions SDK

Add the SDK as a dependency to your app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses events for communication.  See the [Events](#events) section for a full list.

### SDK Initialization

Create a `CallingExtensions` instance, defining event handlers:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* HubSpot sends dial number */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created */ },
    onEngagementCreatedFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

###  iFrame Parameters

HubSpot requires these iFrame parameters:

```json
{
  "name": "My App Name",
  "url": "My App URL",
  "width": 400,
  "height": 600,
  "isReady": true, // Set to false during testing
  "supportsCustomObjects": true
}
```

### Calling Settings Endpoint

Use the following API endpoint to manage app settings (replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`):

```bash
curl --request POST \
     --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '{"name":"My App","url":"https://myapp.com","height":600,"width":400,"isReady":false}'
```
This endpoint also supports `PATCH`, `GET`, and `DELETE` methods.


### Overriding Settings with localStorage

For testing, override settings using the browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'My App URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production Readiness

Set `isReady` to `true` using the `PATCH` endpoint once testing is complete.


### Publishing to the Marketplace

[Learn how to publish your app to the HubSpot marketplace here](link_to_marketplace_publishing_guide).


## Events

### Sending Messages to HubSpot

* **`initialized`:**  Indicates softphone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn`:** User logged in.
* **`userLoggedOut`:** User logged out.
* **`outgoingCall`:** Outgoing call started.  Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered`:** Outgoing call answered. Payload: `{ externalCallId: string }`
* **`callEnded`:** Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted`:** Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: object, externalCallId: number }`
* **`sendError`:**  Error encountered. Payload: `{ message: string }`
* **`resizeWidget`:** Resize the widget. Payload: `{ height: number, width: number }`


### Receiving Messages from HubSpot

* **`onReady`:** HubSpot is ready.
* **`onDialNumber`:** Outbound call triggered.
* **`onEngagementCreated`:** (Deprecated) Engagement created.
* **`onNavigateToRecordFailed`:** Navigation to record failed.
* **`onPublishToChannelSucceeded`:** Publishing to channel succeeded.
* **`onPublishToChannelFailed`:** Publishing to channel failed.
* **`onCallerIdMatchSucceeded`:** Caller ID match succeeded.
* **`onCallerIdMatchFailed`:** Caller ID match failed.
* **`onCreateEngagementSucceeded`:** Engagement creation succeeded.
* **`onCreateEngagementFailed`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded`:** Engagement update succeeded.
* **`onUpdateEngagementFailed`:** Engagement update failed.
* **`onVisibilityChanged`:** Widget visibility changed.
* **`defaultEventHandler`:** Default event handler.


## Frequently Asked Questions (FAQ)

* **User Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver.
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; apps should create engagements for calls initiated externally.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Marketplace Apps:** Functionality can be added to existing apps.
* **Existing Softphone Integration:** Easily integrable.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Integration Appearance:** Yes, for updates to existing apps.
* **User Installation/Uninstallation:** Controlled by user permissions.
* **Custom Calling Property:** Creatable via the properties API.
* **Calls from Custom Objects:** Supported if using the SDK to create calls and setting `createEngagement: true` in the `outgoingCall` event.


Remember to replace placeholders like `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values.  This documentation provides a solid foundation for integrating the HubSpot Calling Extensions SDK into your applications.  Consult the HubSpot developer portal for the most up-to-date information and API references.
