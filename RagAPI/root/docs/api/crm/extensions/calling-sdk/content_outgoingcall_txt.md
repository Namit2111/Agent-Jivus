# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot directly from CRM records.

## Overview

The Calling Extensions SDK facilitates communication between a calling app and HubSpot.  It consists of three main parts:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication.
2. **Calling Settings Endpoints (API):** Used to configure calling settings for each connected HubSpot account.
3. **Calling iFrame:** The app's user interface within HubSpot, configured via the settings endpoints.

**Note:** Currently, only outgoing calls are supported.


## Getting Started

### 1. Run the Demo App

Two demo apps are available:

* **`demo-minimal-js`:** Minimal implementation (JavaScript, HTML, CSS). SDK instantiation in `index.js`.
* **`demo-react-ts`:**  More realistic implementation (React, TypeScript, Styled Components). SDK instantiation in `useCti.ts`.

**Note:** Demo apps use mock data and are not fully functional calling apps.

### 2. Install the Demo App (Optional)

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo app directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.


### 3. Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Set the `localStorage` item:
   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.  Select the demo app from the "Call from" dropdown in the call switcher.

### 4. Install the SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses an event-driven architecture.

### API

The `CallingExtensions` object provides methods for sending and receiving messages.

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
    onVisibilityChanged: (event) => { /* Widget visibility changed */ }
  }
};

const extensions = new CallingExtensions(options);
```

### Events

**Sending Messages to HubSpot:**

* `initialized(payload)`:  Signals app readiness.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`.
* `userLoggedIn()`: User logged in.
* `userLoggedOut()`: User logged out.
* `outgoingCall(callInfo)`: Outgoing call started. `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`.  `phoneNumber` is deprecated, use `toNumber`.
* `callAnswered(payload)`: Call answered. `payload`: `{ externalCallId: string }`.
* `callEnded(payload)`: Call ended. `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`.
* `callCompleted(data)`: Call completed. `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`.
* `sendError(data)`: Error occurred. `data`: `{ message: string }`.
* `resizeWidget(data)`: Resize the widget. `data`: `{ height: number, width: number }`.

**Receiving Messages from HubSpot:**

* `onReady(data)`:  HubSpot is ready.  `data`: `{ engagementId: number, iframeLocation: Enum, ownerId: String | Number, portalId: Number, userId: Number }`
* `onDialNumber(data)`:  Outbound call triggered.  See detailed data properties in the original text.
* `onEngagementCreated(data)`:  (Deprecated) Engagement created. `data`: `{ engagementId: number }`. Use `onCreateEngagementSucceeded` instead.
* `onNavigateToRecordFailed(data)`: Navigation to a record failed. `data`: `{ engagementId: number, objectCoordinates: object }`.
* `onPublishToChannelSucceeded(data)`: Publishing to a channel succeeded. `data`: `{ engagementId: number, externalCallId: string }`.
* `onPublishToChannelFailed(data)`: Publishing to a channel failed. `data`: `{ engagementId: number, externalCallId: string }`.
* `onCallerIdMatchSucceeded(event)`: Caller ID match succeeded.
* `onCallerIdMatchFailed(event)`: Caller ID match failed.
* `onCreateEngagementSucceeded(event)`: Engagement creation succeeded.
* `onCreateEngagementFailed(event)`: Engagement creation failed.
* `onUpdateEngagementSucceeded(event)`: Engagement update succeeded.
* `onUpdateEngagementFailed(event)`: Engagement update failed.
* `onVisibilityChanged(data)`: Widget visibility changed. `data`: `{ isMinimized: boolean, isHidden: boolean }`.
* `defaultEventHandler(event)`: Default event handler.


## Calling Settings Endpoint (API)

Use this API endpoint to configure your app's settings:

`POST/PATCH/GET/DELETE https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Request Body:**

```json
{
  "name": "App Name",
  "url": "App URL",
  "width": 400,
  "height": 600,
  "isReady": true, // Set to false during testing
  "supportsCustomObjects": true //Optional, defaults to false.
}
```

## Overriding Settings (Local Storage)

For testing, override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'My App URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production Deployment

1. Set `isReady` to `true` using the API.
2. Publish your app to the HubSpot marketplace (optional).


## Frequently Asked Questions (FAQ)

Refer to the original text for the FAQ section.  It covers authentication, CDN hosting, engagement creation/updates, required scopes, integration with existing apps, multiple integrations, free user access, automatic updates, user permissions, custom properties, and calls from custom objects.


This markdown documentation provides a more structured and readable format of the provided text, enhancing clarity and ease of use.  Remember to consult the HubSpot developer documentation for the most up-to-date information.
