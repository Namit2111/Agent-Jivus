# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot directly from CRM records.

## Overview

The Calling Extensions SDK facilitates communication between a calling app and HubSpot.  It consists of three main parts:

1. **The SDK (JavaScript):** Enables message exchange between the app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure the app's calling settings for each connected HubSpot account.
3. **Calling iFrame:** The app's user interface within HubSpot, configured via the settings endpoints.

**Note:** Only outgoing calls are currently supported.


## Getting Started

### 1. Install the Demo App (Optional):

This section helps you test the SDK with provided demo applications.

**Prerequisites:** Node.js installed.

**Steps:**

1. Clone the repository (link needed here, replace `xxxxxxxxxx`): `git clone <repository_url>`
2. Navigate to the demo app directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
3. Access the app at `https://localhost:9025/` (may require bypassing a security warning).


### 2. Launch the Demo App from HubSpot:

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Set `localStorage` based on your installation method:
   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **demo-minimal-js (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **demo-react-ts (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page and select the demo app from the call switcher.


### 3. Install the Calling Extensions SDK:

Add the SDK to your project using npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses events for communication:

### Events

**Outbound (App to HubSpot):**

* `initialized`: Notifies HubSpot the app is ready (payload: `{ isLoggedIn: boolean, engagementId: number }`).
* `userLoggedIn`:  User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call initiated (payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`).
* `callAnswered`: Call answered (payload: `{ externalCallId: string }`).
* `callEnded`: Call ended (payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`).
* `callCompleted`: Call completed (payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`).
* `sendError`: Error occurred (payload: `{ message: string }`).
* `resizeWidget`: Resize the widget (payload: `{ height: number, width: number }`).

**Inbound (HubSpot to App):**

* `onReady`: HubSpot is ready (payload: `{ engagementId: number, iframeLocation: Enum, ownerId: String | Number, portalId: Number, userId: Number }`).
* `onDialNumber`: Outbound call initiated by HubSpot (payload: `{ phoneNumber: string, ownerId: number, subjectId: number, objectId: number, objectType: CONTACT | COMPANY, portalId: number, countryCode: string, calleeInfo: {calleeId: number, calleeObjectTypeId: string}, startTimestamp: number, toPhoneNumberSrc: string }`).
* `onEngagementCreated`: *(Deprecated)* Engagement created by HubSpot. Use `onCreateEngagementSucceeded` instead.
* `onNavigateToRecordFailed`: Navigation to record failed.
* `onPublishToChannelSucceeded`: Publishing to channel succeeded.
* `onPublishToChannelFailed`: Publishing to channel failed.
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement creation succeeded.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement update succeeded.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Default event handler.


### Example Code (SDK Initialization):

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true,
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

## API Endpoints

### Calling Settings Endpoint

Use this API to manage your app's settings.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values.

* **URL:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`
* **Methods:** `POST`, `PATCH`, `GET`, `DELETE`
* **Payload (example):**
  ```json
  {
    "name": "demo widget",
    "url": "https://mywidget.com/widget",
    "height": 600,
    "width": 400,
    "isReady": false,
    "supportsCustomObjects": true
  }
  ```
  The `isReady` flag indicates production readiness (set to `false` during testing).


## LocalStorage Overrides (for testing)

You can override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

## Production & Publishing

Set `isReady` to `true` via the API endpoint before publishing to the HubSpot marketplace.  Refer to the provided link for marketplace publishing details.


## Frequently Asked Questions

Refer to the original text for the FAQ section.


This markdown documentation provides a comprehensive overview of the HubSpot Calling Extensions SDK. Remember to replace placeholder values (URLs, IDs, etc.) with your actual data.
