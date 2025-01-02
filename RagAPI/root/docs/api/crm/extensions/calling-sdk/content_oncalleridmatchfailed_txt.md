# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling options into HubSpot CRM records.

## Overview

The HubSpot Calling Extensions SDK allows apps to offer custom calling functionalities directly from CRM records.  It comprises three core components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure calling settings for each connected HubSpot account.
3. **Calling iFrame:** Displays your app to HubSpot users; configured via the settings endpoints.


**Note:** Currently, only outgoing calls are supported.


## Getting Started

### 1. Run the Demo App

Two demo apps are available for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:**  A more comprehensive example using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** Demo apps use mock data and aren't fully functional calling applications.

### 2. Install the Demo App (Optional)

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo app directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
   This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### 3. Launch the Demo App from HubSpot

1. Go to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Set the `localStorage` item:
   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### 4. Install the SDK

Add the SDK to your app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses an event-driven architecture. HubSpot sends events, and your app responds via event handlers.

### API

The `CallingExtensions` object provides methods for sending messages to HubSpot and handling incoming events.


```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, //Optional: Logs debug messages to the console.
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

### Events

**Sending Messages (to HubSpot):**

* `initialized(payload)`: Notifies HubSpot that the app is ready.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn()`: User logged in.
* `userLoggedOut()`: User logged out.
* `outgoingCall(callInfo)`: Outgoing call started. `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered(payload)`: Call answered. `payload`: `{ externalCallId: string }`
* `callEnded(payload)`: Call ended. `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`  `EndStatus` is an enumeration (e.g., `INTERNAL_COMPLETED`, `INTERNAL_FAILED`).
* `callCompleted(data)`: Call completed.  `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError(data)`: Error occurred. `data`: `{ message: string }`
* `resizeWidget(data)`: Resize the widget. `data`: `{ height: number, width: number }`


**Receiving Messages (from HubSpot):**

* `onReady(data)`: HubSpot is ready.  `data`: `{ engagementId: number, iframeLocation: Enum, ownerId: String|Number, portalId: Number, userId: Number }`
* `onDialNumber(data)`: Outbound call initiated (details about the call).
* `onEngagementCreated(data)`: (Deprecated) Engagement created.
* `onNavigateToRecordFailed(data)`: Navigation to record failed.
* `onPublishToChannelSucceeded(data)`: Publishing to channel succeeded.
* `onPublishToChannelFailed(data)`: Publishing to channel failed.
* `onCallerIdMatchSucceeded(event)`: Caller ID match succeeded.
* `onCallerIdMatchFailed(event)`: Caller ID match failed.
* `onCreateEngagementSucceeded(event)`: Engagement creation succeeded.
* `onCreateEngagementFailed(event)`: Engagement creation failed.
* `onUpdateEngagementSucceeded(event)`: Engagement update succeeded.
* `onUpdateEngagementFailed(event)`: Engagement update failed.
* `onVisibilityChanged(data)`: Widget visibility changed. `data`: `{ isMinimized: boolean, isHidden: boolean }`
* `defaultEventHandler(event)`: Default event handler.


### Calling Settings Endpoint (API)

Use this API endpoint to configure your app's settings:

`POST/PATCH/GET/DELETE https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Request Body (JSON):**

```json
{
  "name": "App Name",
  "url": "App URL",
  "width": 400,
  "height": 600,
  "isReady": false // Set to true for production
}
```

### Local Storage Override (for testing)

You can override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'My App URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production Deployment

Set `isReady` to `true` in the settings endpoint to deploy to production.  Then, publish your app to the HubSpot marketplace.


## Frequently Asked Questions (FAQ)

Refer to the original document for the complete FAQ section.


This markdown documentation provides a structured and detailed overview of the HubSpot Calling Extensions SDK, covering installation, usage, API calls, event handling, and troubleshooting.  Remember to consult the original document for the most up-to-date information and complete details.
