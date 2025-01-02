# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot CRM records.

## Overview

The Calling Extensions SDK facilitates communication between a calling app and HubSpot, providing users a custom calling experience directly from CRM records.  The integration consists of three parts:

1. **Calling Extensions SDK (JavaScript):**  Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:**  Your app's interface within HubSpot, configured via the settings endpoints.

**Note:** Currently, only outgoing calls are supported.


## Getting Started

### 1.  Install the Demo App (Optional):

The repository provides demo apps (minimal JS and React/TypeScript) for testing.  Install Node.js, clone the repo, and navigate to the demo directory:

* **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
* **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This will start the app at `https://localhost:9025/`. You may need to bypass a security warning.


### 2. Launch the Demo App from HubSpot:

1. Go to your HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Run one of the following commands in the console, depending on which demo app you're using:

    * **`demo-minimal-js` (installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **`demo-react-ts` (installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
    * **`demo-minimal-js` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **`demo-react-ts` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page. The demo app should appear in the call switcher.


### 3. Install the Calling Extensions SDK:

Add the SDK to your project using npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends events, and your app responds.

### SDK Initialization:

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
    defaultEventHandler: (event) => { /* Handles any unhandled events */}
  }
};

const extensions = new CallingExtensions(options);
```

### Events

#### Sending Messages to HubSpot:

* **`initialized(payload)`:**  Indicates app readiness.  `payload` includes `isLoggedIn` (boolean) and `engagementId` (number).
* **`userLoggedIn()`:** User logged into the app.
* **`userLoggedOut()`:** User logged out of the app.
* **`outgoingCall(callInfo)`:** Outgoing call started.  `callInfo` includes `callStartTime` (number), `createEngagement` (boolean), `toNumber` (string - recipient's number), and `fromNumber` (string - caller's number).
* **`callAnswered()`:** Call answered.  Includes `externalCallId` (string).
* **`callEnded(payload)`:** Call ended. Includes `externalCallID`, `engagementId`, and `callEndStatus` (enum).
* **`callCompleted(data)`:** Call completed. Includes `engagementId`, `hideWidget` (boolean), `engagementProperties` (object), and `externalCallId`.
* **`sendError(data)`:**  Error occurred.  `data` includes `message` (string).
* **`resizeWidget(data)`:** Resize the widget.  `data` includes `height` and `width` (numbers).


#### Receiving Messages from HubSpot:

* **`onReady()`:** HubSpot is ready for communication. Provides `engagementId`, `iframeLocation` (enum: `widget`, `remote`, `window`), `ownerId`, `portalId`, and `userId`.
* **`onDialNumber(data)`:** Outbound call initiated from HubSpot.  `data` includes detailed call information (phone number, owner ID, object type, etc.).
* **`onCreateEngagementSucceeded(event)`:** Engagement created successfully.
* **`onCreateEngagementFailed(event)`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded(event)`:** Engagement update succeeded.
* **`onUpdateEngagementFailed(event)`:** Engagement update failed.
* **`onVisibilityChanged(data)`:** Widget visibility changed.  `data` includes `isMinimized` and `isHidden` (booleans).
* **`defaultEventHandler(event)`:** Catches any unhandled events.


### Calling Settings Endpoint (API)

Use this API endpoint to manage your app's settings:

`https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`

**Methods:** `POST`, `PATCH`, `GET`, `DELETE`

**Payload (Example):**

```json
{
  "name": "My App",
  "url": "https://myapp.com",
  "height": 600,
  "width": 400,
  "isReady": false // Set to true for production
}
```

**Note:** The `isReady` flag indicates production readiness. Set to `false` during testing.

### LocalStorage Override (for testing):

You can override settings using localStorage:

```javascript
const mySettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(mySettings));
```


## Frequently Asked Questions

Refer to the original document for the FAQ section.


## Publishing to the Marketplace

Follow the instructions in the original document to publish your app to the HubSpot marketplace.
