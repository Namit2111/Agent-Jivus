# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into the HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between a calling app and HubSpot, providing a custom calling experience directly from CRM records.  It consists of three core components:

1. **Calling Extensions SDK (JavaScript):**  Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure calling settings for your app on a per-HubSpot account basis.
3. **Calling iFrame:** Your app's user interface, displayed within HubSpot.  Its configuration is managed via the calling settings endpoints.

**Note:** Only outgoing calls are currently supported.

## Getting Started

### 1. Run the Demo App

Two demo apps are available for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:**  More comprehensive implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** Demo apps use mock data and aren't fully functional calling apps.

**Installation (optional):**

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo's directory:
    * `cd demos/demo-minimal-js` (for `demo-minimal-js`)
    * `cd demos/demo-react-ts` (for `demo-react-ts`)
4. Run `npm i && npm start`.  This opens the app at `https://localhost:9025/` (you might need to bypass a security warning).


### 2. Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console and run one of the following commands, depending on whether you installed the demo app:

    * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

3. Refresh the page. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### 3. Install the SDK

Add the SDK as a dependency to your calling app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends messages (events) to your app, and your app responds using methods provided by the SDK.

### API

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Outbound call initiated */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Events

**Sent from HubSpot:**

* `onReady`: HubSpot is ready.
* `onDialNumber`: User initiates an outbound call.
* `onCreateEngagementSucceeded`/`onCreateEngagementFailed`: Result of engagement creation.
* `onUpdateEngagementSucceeded`/`onUpdateEngagementFailed`: Result of engagement update.
* `onVisibilityChanged`: Widget visibility changes.


**Sent to HubSpot:**

* `initialized`: Softphone ready.
* `userLoggedIn`/`userLoggedOut`: User login/logout status.
* `outgoingCall`: Outbound call started.
* `callAnswered`: Outbound call answered.
* `callEnded`: Outbound call ended.
* `callCompleted`: Outbound call completed.
* `sendError`: Error occurred in the app.
* `resizeWidget`: Request to resize the widget.


Each event has a specific payload (see documentation for details).


### Calling Settings Endpoint (API)

Use this API endpoint to configure your app's settings in HubSpot.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values.

**Endpoint:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Methods:** `POST`, `PATCH`, `GET`, `DELETE`

**Example Payload (POST):**

```json
{
  "name": "My App",
  "url": "https://my-app.com",
  "height": 600,
  "width": 400,
  "isReady": false, // Set to true for production
  "supportsCustomObjects": true
}
```


### Overriding Settings with localStorage

For testing, you can override settings using `localStorage`:

```javascript
const mySettings = {
  isReady: true,
  name: 'My Test App',
  url: 'http://localhost:3000'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(mySettings));
```

### Production Readiness

Set `isReady` to `true` in your settings using the PATCH method on the settings endpoint.


### Publishing to the Marketplace

Once ready, publish your app to the HubSpot marketplace (see HubSpot documentation for details).


## Frequently Asked Questions (FAQ)

Refer to the provided FAQ section in the original text for answers to common questions.


This markdown documentation provides a comprehensive overview and reference for the HubSpot Calling Extensions SDK. Remember to consult the official HubSpot documentation for the most up-to-date information and details.
