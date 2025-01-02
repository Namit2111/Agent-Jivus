# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK facilitates communication between a HubSpot account and a calling application.  It enables users to initiate calls directly from HubSpot CRM records through a custom calling interface within the HubSpot UI.  The SDK handles much of the engagement creation and update process, simplifying development.

A calling extension comprises three key components:

1. **Calling Extensions SDK (JavaScript):**  The core SDK enabling communication between the app and HubSpot.  Available via npm or yarn.
2. **Calling Settings Endpoints (API):** Used to configure the calling app's settings for each connected HubSpot account.
3. **Calling iFrame:**  The visual interface displayed to the HubSpot user, configured via the settings endpoints.

**Note:** Only outgoing calls are currently supported.


## Getting Started

### 1.  Demo Apps

Two demo apps are provided to illustrate SDK usage:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js`).
* **`demo-react-ts`:**  More comprehensive implementation using React, TypeScript, and Styled Components (`useCti.ts`).

These demos use mock data and are not fully functional calling apps.

**Installation (for demos):**

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo directory: `cd demos/demo-minimal-js` (or `demos/demo-react-ts`).
4. Install dependencies: `npm i`
5. Start the app: `npm start` (opens `https://localhost:9025/`).  You may need to bypass a security warning.

**Launching the Demo from HubSpot:**

1. Go to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Set the appropriate localStorage item:

   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page. Select the demo app from the "Call from" dropdown in the call switcher.

### 2. Installing the SDK

Add the SDK to your project using npm or yarn:

**npm:** `npm i --save @hubspot/calling-extensions-sdk`

**yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends events to the app, and the app responds using methods provided by the SDK.

### API

The `CallingExtensions` object is the core of the SDK.  It's initialized with options, including `eventHandlers` to handle HubSpot events.

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Dial number event received */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

### Events

**Sent to HubSpot:**

* `initialized(payload)`: Signals readiness; includes `isLoggedIn` and `engagementId`.
* `userLoggedIn()`: User login event.
* `userLoggedOut()`: User logout event.
* `outgoingCall(callInfo)`: Outgoing call started; includes `toNumber`, `fromNumber`, `callStartTime`, `createEngagement`.
* `callAnswered(payload)`: Call answered; includes `externalCallId`.
* `callEnded(payload)`: Call ended; includes `externalCallID`, `engagementId`, `callEndStatus`.
* `callCompleted(data)`: Call completed; includes `engagementId`, `hideWidget`, `engagementProperties`, `externalCallId`.
* `sendError(data)`: Error occurred; includes `message`.
* `resizeWidget(data)`: Resize request; includes `height` and `width`.


**Received from HubSpot:**

* `onReady(data)`: HubSpot is ready. Provides `engagementId`, `iframeLocation`, `ownerId`, `portalId`, `userId`.
* `onDialNumber(data)`: Outbound call initiated. Contains extensive call details.
* `onEngagementCreated(data)`: **Deprecated**. Use `onCreateEngagementSucceeded` instead. Provides `engagementId`.
* `onNavigateToRecordFailed(data)`: Navigation to a record failed.  Includes `engagementId` and `objectCoordinates`.
* `onPublishToChannelSucceeded(data)`: Publishing to a channel succeeded. Includes `engagementId` and `externalCallId`.
* `onPublishToChannelFailed(data)`: Publishing to a channel failed. Includes `engagementId` and `externalCallId`.
* `onCallerIdMatchSucceeded(event)`: Caller ID match successful.
* `onCallerIdMatchFailed(event)`: Caller ID match failed.
* `onCreateEngagementSucceeded(event)`: Engagement creation successful.
* `onCreateEngagementFailed(event)`: Engagement creation failed.
* `onUpdateEngagementSucceeded(event)`: Engagement update successful.
* `onUpdateEngagementFailed(event)`: Engagement update failed.
* `onVisibilityChanged(data)`: Widget visibility changed. Includes `isMinimized` and `isHidden`.
* `defaultEventHandler(event)`:  Handles any unhandled events.


### Calling Settings Endpoint (API)

Use this API endpoint to configure your app's settings in HubSpot:

`POST/PATCH/GET/DELETE https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`

**Request Body (example):**

```json
{
  "name": "My Calling App",
  "url": "https://myapp.com/widget",
  "height": 600,
  "width": 400,
  "isReady": false, // Set to true for production
  "supportsCustomObjects": true
}
```

**Note:**  `isReady: false` during testing; set to `true` for production.


### Local Storage Override (for testing)

For testing, you can override settings using localStorage:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'my-local-url',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production Deployment

1. Set `isReady` to `true` using the settings API.
2. Publish your app to the HubSpot marketplace (optional).


## FAQ

Refer to the original document for the frequently asked questions.


This Markdown documentation provides a structured overview of the HubSpot Calling Extensions SDK.  Remember to consult the official HubSpot documentation for the most up-to-date information and detailed examples.
