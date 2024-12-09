# HubSpot CRM API: Calling Extensions SDK

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK allows apps to offer custom calling options directly from CRM records within HubSpot.  It consists of three core parts:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Configure settings for your app on a per-HubSpot account basis.
3. **Calling iFrame:**  The interface presented to HubSpot users, controlled via the settings endpoints.


For a detailed understanding of the in-app calling experience, refer to [this knowledge base article](link-to-knowledge-base-article).  After integration, your app will appear in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.


## Getting Started

### Prerequisites

* A HubSpot developer account ([sign up here](link-to-signup)).
* If you don't have an app, [create one from your HubSpot developer account](link-to-create-app).
* Node.js installed on your environment.

### Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:** A more advanced implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** These demos use mock data and are not fully functional calling apps.

### Installing Demo Apps

1. Clone, fork, or [download the ZIP](link-to-zip) of the repository.
2. Navigate to the project's root directory.
3. Run the appropriate command:

   * **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### Launching Demo Apps from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console.
3. Run the appropriate `localStorage` command:

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page, click the "Call" icon, select the demo app, and click "Call."


## Integrating the Calling Extensions SDK

### Installation

Use npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


### Using the SDK

The SDK uses an event-driven architecture.  Here's how to create an instance and define event handlers:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Set to true for debugging
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Dial number received */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
  },
};

const extensions = new CallingExtensions(options);
```


### Events

#### Sending Messages to HubSpot

* **`initialized`:**  Signals softphone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn`:** User login notification (only needed if not logged in during initialization).
* **`userLoggedOut`:** User logout notification.
* **`outgoingCall`:** Notifies HubSpot of an outgoing call. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered`:**  Call answered notification. Payload: `{ externalCallId: string }`
* **`callEnded`:** Call ended notification. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted`:** Call completed notification. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError`:** Reports an error. Payload: `{ message: string }`
* **`resizeWidget`:** Requests widget resizing. Payload: `{ height: number, width: number }`

#### Receiving Messages from HubSpot

* **`onReady`:** HubSpot is ready for communication.
* **`onDialNumber`:** Outbound call initiated.
* **`onEngagementCreated`:** (Deprecated; use `onCreateEngagementSucceeded`) Engagement created.
* **`onNavigateToRecordFailed`:** Record navigation failed.
* **`onPublishToChannelSucceeded`:** Publish to channel succeeded.
* **`onPublishToChannelFailed`:** Publish to channel failed.
* **`onCallerIdMatchSucceeded`:** Caller ID match successful.
* **`onCallerIdMatchFailed`:** Caller ID match failed.
* **`onCreateEngagementSucceeded`:** Engagement creation successful.
* **`onCreateEngagementFailed`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded`:** Engagement update successful.
* **`onUpdateEngagementFailed`:** Engagement update failed.
* **`onVisibilityChanged`:** Widget visibility changed.
* **`defaultEventHandler`:** Handles all other events.

### Calling Settings Endpoint

Use this endpoint (e.g., with `curl` or Postman) to manage app settings:  `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

* **`POST`:** Add settings.
* **`PATCH`:** Update settings.
* **`GET`:** Retrieve settings.
* **`DELETE`:** Delete settings.

Payload example:  `{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}`

The `isReady` flag should be `false` during testing and `true` for production.

### Overriding Settings with `localStorage`

For testing, you can override settings using:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production Readiness

Once testing is complete, set `isReady` to `true` using the `PATCH` endpoint.  Then publish your app to the HubSpot marketplace ([details here](link-to-marketplace-details)).

## Frequently Asked Questions

* **Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, using jsDeliver (example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:**  HubSpot creates engagements for calls initiated within the HubSpot UI; apps update them afterward. Apps create engagements for calls initiated outside the HubSpot UI.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:**  Functionality can be added to existing apps.
* **Softphone Integration:** Easily integrates with existing softphones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free User Access:** Yes, all users can install.
* **Automatic Appearance:** Yes, for updated apps.
* **User Permissions:**  Only users with the necessary permissions can install/uninstall.
* **Custom Calling Properties:** Creatable via the properties API.
* **Custom Object Calls:** Possible if using the SDK to create calls and setting `createEngagement: true` in the `outgoingCall` event.


This Markdown documentation provides a structured and detailed guide to the HubSpot Calling Extensions SDK, enhancing readability and ease of use for developers.  Remember to replace placeholder links with the actual links.
