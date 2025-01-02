# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot's CRM.

## Overview

The Calling Extensions SDK facilitates communication between a calling app and HubSpot, providing a custom calling experience directly from CRM records.  It consists of three parts:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling app-HubSpot communication via events and methods.
2. **Calling Settings Endpoints (API):**  Used to configure the calling app's settings for each connected HubSpot account.
3. **Calling iFrame:** The interface displayed to HubSpot users, configured via the settings endpoints.


**Note:** Only outgoing calls are currently supported.


## Getting Started

### 1. Install the Demo App (Optional):

This section provides instructions to test the SDK using provided demo applications.  You can skip this section and proceed to installing the SDK directly into your application.

**Prerequisites:** Node.js installed.

**Installation:**

1. Clone the demo repository (link provided in original text, omitted here for brevity).
2. Navigate to the demo app directory:
   - For `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   - For `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
3. The app will launch at `https://localhost:9025/`.  You might need to bypass a security warning.

### 2. Launch the Demo App from HubSpot:

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Set the `localStorage` item:
   - **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   - **`demo-minimal-js` (no install):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   - **`demo-react-ts` (no install):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.  Select the demo app from the "Call from" dropdown in the call switcher.

### 3. Install the Calling Extensions SDK:

Add the SDK to your project using npm or yarn:

**npm:** `npm i --save @hubspot/calling-extensions-sdk`

**yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends events, and your app responds.


### SDK API:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Outbound call initiated */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    // ... other event handlers
    defaultEventHandler: (event) => { /* Handle unhandled events */}
  }
};

const extensions = new CallingExtensions(options);
```

### Events:

**HubSpot Sends:**

* `onReady`: HubSpot is ready for communication.
* `onDialNumber`: User initiates an outbound call.  Provides details like `phoneNumber`, `ownerId`, `objectId`, `objectType`, etc.
* `onVisibilityChanged`: Widget visibility changes (minimized/hidden).


**App Sends (using `extensions` object):**

* `initialized`: Softphone ready.  Includes `isLoggedIn` and `engagementId`.
* `userLoggedIn`/`userLoggedOut`: User login/logout status.
* `outgoingCall`: Outbound call started. Requires `toNumber`, `fromNumber`, `callStartTime`, and `createEngagement` (boolean, indicating if HubSpot should create the engagement).
* `callAnswered`: Call answered.
* `callEnded`: Call ended.  Includes `externalCallID`, `engagementId`, and `callEndStatus`.
* `callCompleted`: Call completed.  Includes `engagementId`, `hideWidget` (boolean), `engagementProperties`, and `externalCallId`.
* `sendError`: Error occurred.
* `resizeWidget`: Request to resize the widget.


### Calling Settings Endpoint (API):

This API endpoint manages your app's settings in HubSpot.  Use `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`.

**Endpoint:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Methods:** POST (create), PATCH (update), GET (retrieve), DELETE (delete).

**Example Payload (POST/PATCH):**

```json
{
  "name": "My App",
  "url": "https://myapp.com",
  "height": 600,
  "width": 400,
  "isReady": true, // Set to false during testing
  "supportsCustomObjects": true
}
```

### Overriding Settings with localStorage:

For testing, you can override settings in the browser's developer console:

```javascript
const mySettings = {
  isReady: true,
  name: "My App (Local)",
  url: "http://localhost:3000"
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(mySettings));
```


## Production Deployment

1. Set `isReady` to `true` in the settings endpoint.
2. Publish your app to the HubSpot Marketplace (optional).


## FAQ (Frequently Asked Questions)

The original text includes a comprehensive FAQ section, which is omitted here for brevity, but was included in the original response.  Refer to the original response for this section.


This Markdown documentation provides a structured and concise overview of the HubSpot Calling Extensions SDK. Remember to replace placeholder values like `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values.  Consult the original text for details on specific event parameters and error handling.
