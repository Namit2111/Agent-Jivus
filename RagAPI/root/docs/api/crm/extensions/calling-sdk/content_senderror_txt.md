# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into HubSpot CRM.

## Overview

The Calling Extensions SDK enables apps to provide a custom calling experience directly from CRM records. It consists of three components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:**  Displays your app to HubSpot users. Configured via the settings endpoints.

**Note:** Only outgoing calls are currently supported.


## Getting Started

### 1. Run the Demo App

Two demo apps are available:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:** More realistic implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** Demo apps use mock data.

**Installation (optional):**

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo's directory:
   - `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   - `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
   This starts the app at `https://localhost:9025/`. You might need to bypass a security warning.


### 2. Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Run one of the following commands, depending on whether you installed the demo or not:

   **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`

   **Not Installed:**
     - `demo-minimal-js`: `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
     - `demo-react-ts`: `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.  Select the demo app from the "Call from" dropdown in the call switcher.


### 3. Install the SDK

Add the SDK as a dependency to your app:

**npm:** `npm i --save @hubspot/calling-extensions-sdk`

**yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends events; your app responds using `eventHandlers`.


###  API

The `CallingExtensions` object is the core of the SDK.  It's initialized with options, including `eventHandlers`:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Outbound call initiated */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    // ...other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

### Events

**Sent to HubSpot:**

* `initialized`:  Softphone ready.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Call answered. Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: object, externalCallId: number }`
* `sendError`: Error occurred. Payload: `{ message: string }`
* `resizeWidget`: Resize the widget. Payload: `{ height: number, width: number }`


**Received from HubSpot:**

* `onReady`: HubSpot is ready.  Payload includes `engagementId`, `iframeLocation`, `ownerId`, `portalId`, `userId`.
* `onDialNumber`: Outbound call initiated. Payload includes phone number, owner ID, subject ID, object ID, object type, portal ID, country code, callee info, start timestamp, and `toPhoneNumberSrc`.
* `onEngagementCreated` (Deprecated - use `onCreateEngagementSucceeded`): Engagement created.
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`: Publishing to a channel succeeded.
* `onPublishToChannelFailed`: Publishing to a channel failed.
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement creation succeeded.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement update succeeded.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`:  Handles any unhandled events.


## Calling Settings Endpoint (API)

Use this API to configure your app's settings for each HubSpot account.  The API supports `POST`, `PATCH`, `GET`, and `DELETE`.

**Endpoint:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Example Payload (POST):**

```json
{
  "name": "Demo Widget",
  "url": "https://mywidget.com/widget",
  "height": 600,
  "width": 400,
  "isReady": false,
  "supportsCustomObjects": true
}
```


## Overriding Settings (Local Storage)

For testing, override settings using localStorage:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production Readiness

Set `isReady` to `true` via the PATCH endpoint to make your app available in production.


## Publishing to the Marketplace

Once ready, publish your app to the HubSpot marketplace.


## Frequently Asked Questions (FAQ)

Refer to the original document for the FAQ section.


This markdown documentation provides a more structured and concise overview of the HubSpot Calling Extensions SDK.  Remember to consult the original document for complete details and edge cases.
