# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, enabling custom calling options within the HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between your calling application and HubSpot. It consists of three key components:

1. **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure settings for your app on a per-HubSpot account basis.
3. **Calling iFrame:** Your app's user interface, displayed within HubSpot.

**Note:** Currently, only outgoing calls are supported.

## Getting Started

### 1. Install the Demo App (Optional):

Two demo apps are available: `demo-minimal-js` (JavaScript, HTML, CSS) and `demo-react-ts` (React, TypeScript, Styled Components).

* **Prerequisites:** Node.js and npm (or yarn).
* **Installation:**
    * Clone the repository.
    * Navigate to the demo app's directory (`demos/demo-minimal-js` or `demos/demo-react-ts`).
    * Run `npm i && npm start` (or `yarn install && yarn start`).
    * Access the app at `https://localhost:9025/`.  You might need to bypass a security warning.

### 2. Launch the Demo App from HubSpot:

1. Go to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Run one of the following commands in the console, depending on the demo app and whether you installed it locally:
    * **Installed `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **Installed `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.  The demo app should appear in the call switcher.

### 3. Install the Calling Extensions SDK:

Add the SDK as a dependency to your project:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses events for communication.  See the "Events" section for a complete list.

### Creating an SDK Instance:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* HubSpot sends dial number */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    // ...other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

### Calling Settings Endpoint (API)

Use this API to configure your app's settings in HubSpot.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values.

**Endpoint:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Methods:** POST, PATCH, GET, DELETE

**Example (POST):**

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"My App","url":"https://myapp.com","height":600,"width":400,"isReady":false}'
```

**Payload Parameters:**

* `name`: (string) App name.
* `url`: (string) App URL.
* `width`: (number) iFrame width.
* `height`: (number) iFrame height.
* `isReady`: (boolean)  `true` for production, `false` for testing.
* `supportsCustomObjects`: (boolean) Whether the app supports calls from custom objects (true/false).


### Overriding Settings with localStorage (for testing):

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

## Events

### Sending Messages to HubSpot:

* `initialized(payload)`: Softphone ready.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn()`: User logged in.
* `userLoggedOut()`: User logged out.
* `outgoingCall(callInfo)`: Outgoing call started.  `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered(payload)`: Call answered. `payload`: `{ externalCallId: string }`
* `callEnded(payload)`: Call ended. `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted(data)`: Call completed. `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: object, externalCallId: number }`
* `sendError(data)`: Error occurred. `data`: `{ message: string }`
* `resizeWidget(data)`: Resize widget. `data`: `{ height: number, width: number }`


### Receiving Messages from HubSpot:

* `onReady(data)`: HubSpot ready. `data`: `{ engagementId: number, iframeLocation: Enum, ownerId: string|number, portalId: number, userId: number }`
* `onDialNumber(data)`: Outbound call initiated.  (See detailed payload parameters in the original document)
* `onEngagementCreated(data)`: (Deprecated) Engagement created. `data`: `{ engagementId: number }`
* `onNavigateToRecordFailed(data)`: Navigation to record failed. `data`: `{ engagementId: number, objectCoordinates: object }`
* `onPublishToChannelSucceeded(data)`: Publishing to channel succeeded. `data`: `{ engagementId: number, externalCallId: string }`
* `onPublishToChannelFailed(data)`: Publishing to channel failed. `data`: `{ engagementId: number, externalCallId: string }`
* `onCallerIdMatchSucceeded(event)`: Caller ID match succeeded.
* `onCallerIdMatchFailed(event)`: Caller ID match failed.
* `onCreateEngagementSucceeded(event)`: Engagement creation succeeded.
* `onCreateEngagementFailed(event)`: Engagement creation failed.
* `onUpdateEngagementSucceeded(event)`: Engagement update succeeded.
* `onUpdateEngagementFailed(event)`: Engagement update failed.
* `onVisibilityChanged(data)`: Widget visibility changed. `data`: `{ isMinimized: boolean, isHidden: boolean }`
* `defaultEventHandler(event)`: Default event handler.


## Frequently Asked Questions (FAQ)

The original document contains a FAQ section which is too extensive to fully reproduce here, but key points are covered in other sections of this Markdown document.  Consult the original document for complete FAQ answers.


## Publishing to the Marketplace

Once your app is ready, publish it to the HubSpot marketplace (details in the original document).


This Markdown documentation provides a structured and comprehensive overview of the HubSpot Calling Extensions SDK.  Remember to consult the original document for complete details and edge cases.
