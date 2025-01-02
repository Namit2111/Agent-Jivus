# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot CRM records.

## Overview

The Calling Extensions SDK facilitates communication between a calling application and HubSpot.  It consists of three parts:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication.
2. **Calling Settings Endpoints (API):**  Used to configure calling settings for each connected HubSpot account.
3. **Calling iFrame:** The iframe where the app is displayed to HubSpot users.


**Key Features:**

* **Custom Calling Experience:** Provide a tailored calling interface within HubSpot.
* **Event-Driven Communication:**  Asynchronous messaging between app and HubSpot.
* **Engagement Management:** HubSpot handles engagement creation and updates (no manual management needed).
* **Supports Outgoing Calls:** Currently, only outgoing calls are supported.
* **Integration with Existing Apps:**  Add calling functionality to existing Marketplace apps.
* **Custom Object Support:** Place calls from custom objects.

## Getting Started

### 1. Install Demo App (Optional)

Two demo apps are available for testing:

* `demo-minimal-js`: Minimal implementation (JavaScript, HTML, CSS).  SDK instantiation in `index.js`.
* `demo-react-ts`:  More realistic implementation (React, TypeScript, Styled Components). SDK instantiation in `useCti.ts`.

**Installation:**

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo app directory (`cd demos/demo-minimal-js` or `cd demos/demo-react-ts`).
4. Run `npm i && npm start`.  This opens the app at `https://localhost:9025/`.  You may need to bypass a security warning.

### 2. Launch Demo App from HubSpot

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Run one of the following `localStorage` commands (depending on the demo app and whether you installed it):

   * **Installed `demo-minimal-js` or `demo-react-ts`:**
     ```javascript
     localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');
     ```
   * **Uninstalled `demo-minimal-js`:**
     ```javascript
     localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');
     ```
   * **Uninstalled `demo-react-ts`:**
     ```javascript
     localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');
     ```
4. Refresh the page and select the demo app from the "Call from" dropdown.

### 3. Install Calling Extensions SDK

Add the SDK to your app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

### API

The SDK uses event handlers for communication.  Create a `CallingExtensions` instance:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* HubSpot sends dial number */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created */ },
    // ... other event handlers (see Events section)
  }
};

const extensions = new CallingExtensions(options);
```

### Events

**Sending Messages to HubSpot:**

* `initialized(payload)`: Notifies HubSpot the app is ready.  `payload` includes `isLoggedIn` (boolean) and `engagementId` (number).
* `userLoggedIn()`: User logged in.
* `userLoggedOut()`: User logged out.
* `outgoingCall(callInfo)`: Outgoing call started.  `callInfo` includes `callStartTime` (number), `createEngagement` (boolean), `toNumber` (string), `fromNumber` (string).
* `callAnswered(payload)`: Call answered.  `payload` includes `externalCallId` (string).
* `callEnded(payload)`: Call ended.  `payload` includes `externalCallId` (string), `engagementId` (number), `callEndStatus` (enum).
* `callCompleted(data)`: Call completed. `data` includes `engagementId`, `hideWidget`, `engagementProperties`, `externalCallId`.
* `sendError(data)`: App error.  `data` includes `message` (string).
* `resizeWidget(data)`: Resize the widget. `data` includes `height` and `width`.


**Receiving Messages from HubSpot:**

* `onReady(data)`: HubSpot is ready. `data` includes `engagementId`, `iframeLocation`, `ownerId`, `portalId`, `userId`.
* `onDialNumber(data)`: Outbound call initiated.  `data` includes `phoneNumber`, `ownerId`, `subjectId`, `objectId`, `objectType`, `portalId`, `countryCode`, `calleeInfo`, `startTimestamp`, `toPhoneNumberSrc`.
* `onEngagementCreated(data)`: (Deprecated) Engagement created. Use `onCreateEngagementSucceeded` instead.
* `onNavigateToRecordFailed(data)`: Navigation to record failed.
* `onPublishToChannelSucceeded(data)`: Publishing to channel succeeded.
* `onPublishToChannelFailed(data)`: Publishing to channel failed.
* `onCallerIdMatchSucceeded(event)`: Caller ID match succeeded.
* `onCallerIdMatchFailed(event)`: Caller ID match failed.
* `onCreateEngagementSucceeded(event)`: Engagement creation succeeded.
* `onCreateEngagementFailed(event)`: Engagement creation failed.
* `onUpdateEngagementSucceeded(event)`: Engagement update succeeded.
* `onUpdateEngagementFailed(event)`: Engagement update failed.
* `onVisibilityChanged(data)`: Widget visibility changed. `data` includes `isMinimized` and `isHidden`.
* `defaultEventHandler(event)`: Default event handler.


### Calling Settings Endpoint (API)

Use this API to configure your app's settings:

* **URL:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`
* **Methods:** POST, PATCH, GET, DELETE
* **Payload (example):**
  ```json
  {
    "name": "My App",
    "url": "https://myapp.com",
    "height": 600,
    "width": 400,
    "isReady": false, // Set to true for production
    "supportsCustomObjects": true
  }
  ```

### Overriding Settings with `localStorage`

For testing, override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production Deployment

1. Set `isReady` to `true` in the API settings.
2. Publish your app to the HubSpot Marketplace.

## FAQ

Refer to the original text for the frequently asked questions section.


This markdown documentation provides a structured and more easily readable version of the provided text, improving its clarity and usability.  Remember to replace placeholders like `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values.
