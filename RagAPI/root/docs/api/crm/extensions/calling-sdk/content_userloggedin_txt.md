# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, enabling custom calling options within the HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between your calling application and HubSpot.  It consists of three key components:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK for communication between your app and HubSpot.  It handles event exchange and message passing.
2. **Calling Settings Endpoints (API):** Used to configure your calling app's settings for each connected HubSpot account.
3. **Calling iFrame:** The interface displayed to HubSpot users, configured via the calling settings endpoints.

**Note:** Only outgoing calls are currently supported.

## Getting Started

### 1. Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** Minimal implementation (JavaScript, HTML, CSS).  SDK instantiation in `index.js`.
* **`demo-react-ts`:**  More realistic implementation (React, TypeScript, Styled Components). SDK instantiation in `useCti.ts`.

**Note:** Demo apps use mock data.

### 2. Installing Demo Apps

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo app directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`

This starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### 3. Launching Demo Apps from HubSpot

1. Go to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Run one of the following commands in the console, depending on the demo app and whether you installed it locally:

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

The SDK uses events for communication.  See the "Events" section for a complete list.

### Creating an SDK Instance

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* HubSpot sends dial number */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ }
  }
};

const extensions = new CallingExtensions(options);
```

### Testing Your App

To launch the iFrame, HubSpot requires these parameters:

```javascript
{
  name: "My App Name", // String
  url: "My App URL", // String
  width: 400, // Number
  height: 600, // Number
  isReady: false, // Boolean (set to true for production)
  supportsCustomObjects: true // Boolean
}
```

### Calling Settings Endpoint (API)

Use this API endpoint to configure your app's settings:

```bash
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your app's ID and API key.  This endpoint supports `POST`, `PATCH`, `GET`, and `DELETE`.  Set `isReady` to `true` for production.

### Overriding Settings with localStorage

For testing, override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production Readiness

Set `isReady` to `true` using the `PATCH` method on the calling settings endpoint.

### Publishing to Marketplace

Publish your app to the HubSpot marketplace [here](link-to-marketplace).


## Events

### Sending Messages to HubSpot

* **`initialized(payload)`:**  Indicates softphone readiness.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`.
* **`userLoggedIn()`:** User logged in.
* **`userLoggedOut()`:** User logged out.
* **`outgoingCall(callInfo)`:** Outgoing call started.  `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`.
* **`callAnswered(payload)`:** Call answered.  `payload`: `{ externalCallId: string }`.
* **`callEnded(payload)`:** Call ended.  `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`.
* **`callCompleted(data)`:** Call completed.  `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`.
* **`sendError(data)`:** Error occurred.  `data`: `{ message: string }`.
* **`resizeWidget(data)`:** Resize widget.  `data`: `{ height: number, width: number }`.

### Receiving Messages from HubSpot

* **`onReady(data)`:** HubSpot is ready.  `data`: `{ engagementId: number, iframeLocation: Enum, ownerId: String|Number, portalId: Number, userId: Number}`.
* **`onDialNumber(data)`:** Outbound call triggered.  `data` includes phone number, owner ID, subject ID, object ID, object type, portal ID, country code, callee info, start timestamp, and `toPhoneNumberSrc`.
* **`onEngagementCreated(data)`:** (Deprecated) Engagement created.  `data`: `{ engagementId: number }`.  Use `onCreateEngagementSucceeded` instead.
* **`onNavigateToRecordFailed(data)`:** Navigation to record failed. `data`: `{engagementId: number, objectCoordinates: object}`.
* **`onPublishToChannelSucceeded(data)`:** Publishing to channel succeeded. `data`: `{engagementId: number, externalCallId: string}`.
* **`onPublishToChannelFailed(data)`:** Publishing to channel failed. `data`: `{engagementId: number, externalCallId: string}`.
* **`onCallerIdMatchSucceeded(event)`:** Caller ID match succeeded.
* **`onCallerIdMatchFailed(event)`:** Caller ID match failed.
* **`onCreateEngagementSucceeded(event)`:** Engagement creation succeeded.
* **`onCreateEngagementFailed(event)`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded(event)`:** Engagement update succeeded.
* **`onUpdateEngagementFailed(event)`:** Engagement update failed.
* **`onVisibilityChanged(data)`:** Widget visibility changed. `data`: `{isMinimized: boolean, isHidden: boolean}`.
* **`defaultEventHandler(event)`:** Default event handler.


## Frequently Asked Questions (FAQ)

Refer to the original text for the FAQ section.


This markdown documentation provides a structured and comprehensive overview of the HubSpot Calling Extensions SDK, including API calls, event handling, and troubleshooting.  Remember to replace placeholder values like `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual credentials.
