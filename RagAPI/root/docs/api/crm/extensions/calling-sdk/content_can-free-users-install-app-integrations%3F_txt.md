# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into HubSpot CRM.

## Overview

The Calling Extensions SDK enables communication between a calling application and HubSpot, providing a custom calling experience directly from CRM records.  It consists of three parts:

1. **Calling Extensions SDK (JavaScript):** A JavaScript SDK facilitating communication between the app and HubSpot.
2. **Calling Settings Endpoints (API):**  Used to configure the calling app's settings for each connected HubSpot account.
3. **Calling iFrame:** The iframe where the app appears to HubSpot users, configured via the settings endpoints.


**Note:** Only outgoing calls are currently supported.


## Getting Started

### 1. Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS (see `index.js`).
* **`demo-react-ts`:** A more comprehensive implementation using React, TypeScript, and Styled Components (see `useCti.ts`).

**Note:** These demos use mock data and are not fully functional calling apps.


### 2. Installing the Demo App

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app's directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
4. This will start the app at `https://localhost:9025/`.  You may need to bypass a security warning.


### 3. Launching the Demo App from HubSpot

1. Go to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Run one of the following commands in the console, depending on the demo app and whether you installed it:
   * **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### 4. Installing the SDK

Add the SDK to your project:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends events, and your app responds by handling them and sending messages back.

### API

The core of the SDK is the `CallingExtensions` object. You initialize it with options, including `eventHandlers`:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, //Optional: Logs debug messages to console
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

**HubSpot sends these events:**

* `onReady`: HubSpot is ready for communication.
* `onDialNumber`: A user initiated an outbound call.
* `onEngagementCreated`: An engagement was created (deprecated, use `onCreateEngagementSucceeded`).
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publishing to a channel succeeded/failed.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match succeeded/failed.
* `onUpdateEngagementSucceeded`/`onUpdateEngagementFailed`: Engagement update succeeded/failed.
* `onVisibilityChanged`: Call widget visibility changed.


**Your app sends these messages:**

* `initialized`: Softphone is ready (includes `isLoggedIn` and `engagementId`).
* `userLoggedIn`/`userLoggedOut`: User login/logout status.
* `outgoingCall`: Outgoing call started (includes `toNumber`, `fromNumber`, `createEngagement`, `callStartTime`).
* `callAnswered`: Outgoing call answered (includes `externalCallId`).
* `callEnded`: Outgoing call ended (includes `externalCallId`, `engagementId`, `callEndStatus`).
* `callCompleted`: Outgoing call completed (includes `engagementId`, `hideWidget`, `engagementProperties`, `externalCallId`).
* `sendError`: An error occurred.
* `resizeWidget`: Request to resize the widget.


### Calling Settings Endpoint

Use this API endpoint to configure your app's settings:

```bash
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"My App","url":"https://my-app.com","height":600,"width":400,"isReady":false}'
```

Replace `APP_ID` with your app's ID and `DEVELOPER_ACCOUNT_API_KEY` with your API key.  This endpoint also supports `PATCH`, `GET`, and `DELETE`. The `isReady` flag should be `false` during testing and `true` for production.


### Overriding Settings with localStorage

For testing, you can override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


### Publishing to the Marketplace

Once ready, publish your app to the HubSpot Marketplace.


## Frequently Asked Questions

Refer to the original text for the FAQ section.


This Markdown documentation provides a more structured and easily navigable overview of the HubSpot Calling Extensions SDK.  Remember to consult the original text for complete details and specific examples for each event and API call.
