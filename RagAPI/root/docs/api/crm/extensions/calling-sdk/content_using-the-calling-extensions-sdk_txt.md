# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK facilitates communication between a calling app and HubSpot, enabling users to make calls directly from CRM records.  It consists of three main parts:

1. **JavaScript SDK:** Enables communication between the app and HubSpot.
2. **Calling Settings Endpoints:** Configure the calling app's settings for each connected HubSpot account.
3. **Calling iFrame:** Displays the app to HubSpot users; configured via the settings endpoints.

**Note:** Only outgoing calls are currently supported.


## Getting Started

### 1. Demo Apps

Two demo apps are available to test the SDK:

* `demo-minimal-js`: Minimal implementation using JavaScript, HTML, and CSS (`index.js`).
* `demo-react-ts`:  More realistic implementation using React, TypeScript, and Styled Components (`useCti.ts`).

**Note:** Demo apps use mock data.


### 2. Installing the Demo App

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
4.  The app will launch at `https://localhost:9025/`. You might need to bypass a security warning.

### 3. Launching the Demo App from HubSpot

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Run one of the following commands in the console, depending on the demo app and whether it was installed locally:
    * **Installed `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **Installed `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page and select the demo app from the call switcher.


### 4. Installing the SDK

Add the SDK to your project using npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends events, and the app responds via event handlers.

### API

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Outbound call initiated */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

### Events

**Sent to HubSpot:**

* `initialized`:  Notifies HubSpot the app is ready.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Call answered. Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`: Error encountered. Payload: `{ message: string }`
* `resizeWidget`: Resize the widget. Payload: `{ height: number, width: number }`

**Received from HubSpot:**

* `onReady`: HubSpot is ready.
* `onDialNumber`: Outbound call initiated.  Includes phone number, owner ID, object ID, object type, portal ID, country code, callee info, start timestamp, and phone number source.
* `onEngagementCreated`: (Deprecated, use `onCreateEngagementSucceeded`) Engagement created.
* `onNavigateToRecordFailed`: Navigation to record failed.
* `onPublishToChannelSucceeded`: Publishing to channel succeeded.
* `onPublishToChannelFailed`: Publishing to channel failed.
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement created successfully.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement updated successfully.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Handles any unhandled events.


### Calling Settings Endpoint

Use this API endpoint to configure your app's settings:

* **URL:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`
* **Methods:** POST, PATCH, GET, DELETE
* **Payload (example):** `{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}`
* `isReady`: Set to `true` for production.


### Local Storage Override

For testing, you can override settings using localStorage:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


##  Production Deployment

1. Set `isReady` to `true` using the settings endpoint.
2. Publish your app to the HubSpot marketplace (optional).


## FAQ

Refer to the original document for the detailed FAQ section.


This Markdown documentation provides a structured overview of the HubSpot Calling Extensions SDK, covering installation, API usage, event handling, and deployment.  Remember to consult the original source for the most up-to-date information.
