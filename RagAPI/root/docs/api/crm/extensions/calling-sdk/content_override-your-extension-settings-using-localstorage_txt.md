# HubSpot Calling Extensions SDK Documentation

This document provides comprehensive information on the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling functionalities within their HubSpot apps.

## Overview

The Calling Extensions SDK facilitates communication between a calling app and HubSpot, allowing users to initiate calls directly from CRM records.  The integration consists of three key parts:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication between your app and HubSpot.  This SDK handles message exchange via methods and event handlers.

2. **Calling Settings Endpoints (API):**  Used to configure the settings for your calling app on a per-HubSpot account basis.

3. **Calling iFrame:**  The iframe where your app is displayed to HubSpot users; its configuration is managed using the calling settings endpoints.

**Note:** Currently, only outgoing calls are supported.


## Getting Started

### 1. Run the Demo Calling App

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS (SDK instantiation in `index.js`).
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components (SDK instantiation in `useCti.ts`).

**Note:**  These demos use mock data and aren't fully functional calling apps.

### 2. Install the Demo App

1. Install Node.js.
2. Clone or download the demo repository.
3. Navigate to the demo directory (`demos/demo-minimal-js` or `demos/demo-react-ts`).
4. Run `npm i && npm start`.  This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.

### 3. Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Set the `localStorage` item based on your chosen demo:

   * **`demo-minimal-js` (installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-react-ts` (installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
   * **`demo-minimal-js` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`

4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".

### 4. Install the Calling Extensions SDK

Use npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses methods to send messages and event handlers to receive them.

###  API Reference

**Creating an instance:**

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Outbound call initiated */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

**Sending Messages to HubSpot:**

| Method             | Description                                                              | Payload Example                                         |
|----------------------|--------------------------------------------------------------------------|---------------------------------------------------------|
| `initialized()`     | Notifies HubSpot that the softphone is ready.                            | `{ isLoggedIn: true, engagementId: 123 }`             |
| `userLoggedIn()`    | Notifies HubSpot that the user has logged in.                             | `{}`                                                    |
| `userLoggedOut()`   | Notifies HubSpot that the user has logged out.                            | `{}`                                                    |
| `outgoingCall()`    | Notifies HubSpot of an outgoing call.                                    | `{ toNumber: "+15551234567", fromNumber: "+15559876543", callStartTime: Date.now(), createEngagement: true }` |
| `callAnswered()`    | Notifies HubSpot that the call has been answered.                        | `{ externalCallId: "uniqueCallId" }`                  |
| `callEnded()`       | Notifies HubSpot that the call has ended.                               | `{ externalCallID: "uniqueCallId", engagementId: 123, callEndStatus: "INTERNAL_COMPLETED" }` |
| `callCompleted()`   | Notifies HubSpot that the call is complete.                              | `{ engagementId: 123, hideWidget: true, engagementProperties: { myProp: "myValue" } }` |
| `sendError()`       | Reports an error to HubSpot.                                             | `{ message: "An error occurred" }`                      |
| `resizeWidget()`    | Requests a resize of the call widget.                                   | `{ height: 600, width: 400 }`                           |


**Receiving Messages from HubSpot:**

| Event                   | Description                                                                        | Payload Example                                           |
|--------------------------|------------------------------------------------------------------------------------|-----------------------------------------------------------|
| `onReady`                | HubSpot is ready to receive messages.                                             | `{ engagementId: 123, iframeLocation: "widget", ownerId: 1234, portalId: 5678, userId: 9012 }` |
| `onDialNumber`           | User initiated an outbound call.                                                  |  See detailed payload structure in the document.         |
| `onCreateEngagementSucceeded` | HubSpot successfully created a call engagement.                                  | `{ engagementId: 123 }`                                 |
| `onCreateEngagementFailed` | HubSpot failed to create a call engagement.                                     | `{ error: "reason for failure" }`                        |
| `onUpdateEngagementSucceeded` | HubSpot successfully updated a call engagement.                                  | `{ engagementId: 123 }`                                 |
| `onUpdateEngagementFailed` | HubSpot failed to update a call engagement.                                     | `{ error: "reason for failure" }`                        |
| `onVisibilityChanged`     | Widget visibility changed (minimized or hidden).                                  | `{ isMinimized: true, isHidden: false }`                   |
| `defaultEventHandler`   | Catches any unhandled events.                                                  |  `{ event: "unhandledEvent", data: {} }`               |


### Calling Settings Endpoint (API)

Use this API endpoint to manage your app's settings in HubSpot:

`https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`

Supported methods: `POST`, `PATCH`, `GET`, `DELETE`.

**Payload Example (POST/PATCH):**

```json
{
  "name": "My Calling App",
  "url": "https://my-app.com/widget",
  "height": 600,
  "width": 400,
  "isReady": true, // Set to false during testing
  "supportsCustomObjects": true
}
```

### Overriding Settings with localStorage

For testing, you can override settings in the browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

##  Frequently Asked Questions (FAQ)

Refer to the original document for a detailed FAQ section.


This markdown documentation provides a structured and concise overview of the HubSpot Calling Extensions SDK.  Remember to consult the original documentation for the most up-to-date information and complete details.
