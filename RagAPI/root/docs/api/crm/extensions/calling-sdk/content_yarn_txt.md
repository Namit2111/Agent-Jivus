# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK facilitates communication between a calling app and HubSpot, enabling users to initiate calls directly from CRM records.  The SDK handles the exchange of messages between the app and HubSpot, primarily through events.  HubSpot now handles call engagement creation and updates, simplifying the development process.  Only outgoing calls are currently supported.


## Core Components

A calling extension comprises three key parts:

1. **Calling Extensions SDK (JavaScript):** Enables communication between the app and HubSpot.  Installed as a Node.js dependency (`@hubspot/calling-extensions-sdk`).
2. **Calling Settings Endpoints (API):** Configure settings for each connected HubSpot account (name, URL, dimensions, etc.).  Accessed via the HubSpot API.
3. **Calling iFrame:** The app's user interface displayed within HubSpot.  Configured using the calling settings endpoints.


## Getting Started

### 1.  Demo Apps

Two demo apps are provided to illustrate SDK usage:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:**  More comprehensive example using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Installation (for either demo app):**

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo app's directory (`cd demos/demo-minimal-js` or `cd demos/demo-react-ts`).
4. Run `npm i && npm start`.  This opens the app at `https://localhost:9025/` (you might need to bypass a security warning).

### 2. Launching Demo Apps from HubSpot

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Set the appropriate `localStorage` item:

   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.  The demo app should appear in the call switcher.


### 3. Installing the SDK

Add the SDK to your project using npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

### API

The SDK provides methods for sending messages to HubSpot and handling events from HubSpot.

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Outbound call initiated */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

### Events

**Outbound Messages (from App to HubSpot):**

| Event             | Description                                                                  | Payload Example                                           |
|----------------------|------------------------------------------------------------------------------|-----------------------------------------------------------|
| `initialized`      | Softphone ready.                                                             | `{ isLoggedIn: true, engagementId: 123 }`                  |
| `userLoggedIn`     | User logged in.                                                              | `{}`                                                     |
| `userLoggedOut`    | User logged out.                                                             | `{}`                                                     |
| `outgoingCall`     | Outgoing call started.                                                       | `{ toNumber: "+15551234567", fromNumber: "+15559876543", callStartTime: Date.now(), createEngagement: true }` |
| `callAnswered`     | Call answered.                                                              | `{ externalCallId: "my-call-id" }`                      |
| `callEnded`        | Call ended.                                                                 | `{ externalCallID: "my-call-id", engagementId: 123, callEndStatus: "INTERNAL_COMPLETED" }` |
| `callCompleted`    | Call completed.                                                             | `{ engagementId: 123, hideWidget: true, engagementProperties: { myProp: "myVal" } }` |
| `sendError`        | Error occurred.                                                             | `{ message: "An error occurred" }`                       |
| `resizeWidget`     | Resize the widget.                                                          | `{ height: 600, width: 400 }`                           |


**Inbound Messages (from HubSpot to App):**

| Event                        | Description                                                                        | Payload Example                                                                 |
|--------------------------------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| `onReady`                      | HubSpot is ready to receive messages.                                              | `{ engagementId: 123, iframeLocation: "widget", ownerId: 1, portalId: 1234, userId: 5678 }` |
| `onDialNumber`                 | Outbound call initiated by user in HubSpot.                                      |  See detailed payload properties in documentation.                               |
| `onCreateEngagementSucceeded`  | Engagement successfully created by HubSpot.                                       | `{ engagementId: 123 }`                                                        |
| `onCreateEngagementFailed`    | Engagement creation failed.                                                      | `{ error: "Failed to create engagement" }`                                     |
| `onUpdateEngagementSucceeded` | Engagement successfully updated by HubSpot.                                       | `{ engagementId: 123 }`                                                        |
| `onUpdateEngagementFailed`   | Engagement update failed.                                                       | `{ error: "Failed to update engagement" }`                                     |
| `onVisibilityChanged`         | Widget visibility changed (minimized/hidden).                                    | `{ isMinimized: true, isHidden: false }`                                       |
| `defaultEventHandler`         | Handles any unhandled events.                                                    |  The event object.                                                              |


### Calling Settings Endpoint (API)

Use this API endpoint to configure your app's settings for each HubSpot account:

* **URL:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`
* **Methods:** `POST`, `PATCH`, `GET`, `DELETE`
* **Payload (example):**
  ```json
  {
    "name": "My Calling App",
    "url": "https://my-calling-app.com",
    "height": 600,
    "width": 400,
    "isReady": false, // Set to true for production
    "supportsCustomObjects": true
  }
  ```

### LocalStorage Overrides (for testing)

You can override settings using localStorage:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production

1. Set `isReady` to `true` in your API settings.
2. Publish your app to the HubSpot Marketplace.


## Frequently Asked Questions (FAQ)

Refer to the original text for the FAQ section.


This markdown documentation provides a more structured and organized overview of the HubSpot Calling Extensions SDK, including code examples and API details.  Remember to consult the official HubSpot documentation for the most up-to-date information.
