# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, enabling custom calling options within the HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between your calling application and HubSpot.  It consists of three core components:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication.
2. **Calling Settings Endpoints (API):**  Used to configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:** Your app's interface displayed to HubSpot users, configured via the settings endpoints.

**Note:** Only outgoing calls are currently supported.


## Getting Started

### 1.  Demo Apps

Two demo apps are available for testing:

*   `demo-minimal-js`: Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
*   `demo-react-ts`:  More realistic implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** Demo apps use mock data and are not fully functional calling apps.

### 2. Installing Demo Apps

1.  Install Node.js.
2.  Clone/download the repository.
3.  Navigate to the demo app's directory:
    *   `cd demos/demo-minimal-js && npm i && npm start` (for `demo-minimal-js`)
    *   `cd demos/demo-react-ts && npm i && npm start` (for `demo-react-ts`)

This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### 3. Launching Demo App from HubSpot

1.  Navigate to HubSpot Contacts or Companies.
2.  Open your browser's developer console.
3.  Run one of the following commands based on your installation method:

    * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4.  Refresh the page.  Select the demo app from the "Call from" dropdown in the call switcher.

### 4. Installing the SDK

Add the SDK as a dependency:

*   **npm:** `npm i --save @hubspot/calling-extensions-sdk`
*   **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends events; your app responds via event handlers.

### API

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Dial number received */ },
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

**Outbound Events (Sent from your app to HubSpot):**

*   `initialized`:  Indicates app readiness (payload: `{ isLoggedIn: boolean, engagementId: number }`).
*   `userLoggedIn`: User logged in.
*   `userLoggedOut`: User logged out.
*   `outgoingCall`: Outgoing call started (payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`).
*   `callAnswered`: Call answered (payload: `{ externalCallId: string }`).
*   `callEnded`: Call ended (payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`).
*   `callCompleted`: Call completed (payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: object, externalCallId: number }`).
*   `sendError`: Error occurred (payload: `{ message: string }`).
*   `resizeWidget`: Resize the widget (payload: `{ height: number, width: number }`).

**Inbound Events (Sent from HubSpot to your app):**

*   `onReady`: HubSpot is ready (payload: `{ engagementId: number, iframeLocation: Enum, ownerId: String | Number, portalId: Number, userId: Number }`).
*   `onDialNumber`: Outbound call initiated from HubSpot (payload includes phone number, contact/company info, etc.).
*   `onCreateEngagementSucceeded`: Engagement created successfully.
*   `onCreateEngagementFailed`: Engagement creation failed.
*   `onUpdateEngagementSucceeded`: Engagement updated successfully.
*   `onUpdateEngagementFailed`: Engagement update failed.
*   `onVisibilityChanged`: Widget visibility changed.
*   `defaultEventHandler`: Default event handler.


## Calling Settings Endpoint (API)

Use this API endpoint to configure your app's settings:

`POST/PATCH/GET/DELETE https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Payload Example:**

```json
{
  "name": "My App",
  "url": "https://myapp.com",
  "height": 600,
  "width": 400,
  "isReady": false // Set to true for production
}
```

`isReady` flag indicates production readiness. Set to `false` during testing.

## Local Storage Override

For testing, override settings using local storage:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

## Production & Publishing

Set `isReady` to `true` via the API to prepare for production.  Finally, publish your app to the HubSpot marketplace.


## FAQ

Refer to the original text for the frequently asked questions and answers.


This markdown documentation provides a structured and comprehensive overview of the HubSpot Calling Extensions SDK.  Remember to consult the original text and HubSpot's official documentation for the most up-to-date information and details.
