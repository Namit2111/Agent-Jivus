# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between your calling application and HubSpot.  It consists of three key components:

1. **Calling Extensions SDK (JavaScript):** Enables message exchange between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:** Your app's user interface displayed within HubSpot.  Configured via the settings endpoints.

**Note:** Currently, only outgoing calls are supported.

## Getting Started

### 1. Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:**  More realistic implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** These demos use mock data.

### 2. Installing Demo Apps

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo app directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
4. Access the app at `https://localhost:9025/` (may require bypassing a security warning).

### 3. Launching Demo Apps from HubSpot

1. Navigate to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Set the `localStorage` item:
   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.
5. Select the demo app from the "Call from" dropdown in the call switcher.

### 4. Installing the SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

### API

The SDK uses an event-driven architecture. Your app sends messages to HubSpot via methods and receives messages through event handlers.

**Creating an instance:**

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Outbound call initiated */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    // ... other event handlers (see below)
  },
};

const extensions = new CallingExtensions(options);
```

### Events

#### Sending Messages to HubSpot

* **`initialized(payload)`:**  Notifies HubSpot that your app is ready.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn()`:** User logged in.
* **`userLoggedOut()`:** User logged out.
* **`outgoingCall(callInfo)`:** Outgoing call started. `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`  `phoneNumber` is deprecated, use `toNumber`.
* **`callAnswered()`:** Outgoing call answered. `payload`: `{ externalCallId: string }`
* **`callEnded(payload)`:** Call ended. `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`  `EndStatus` is an enumeration (see documentation).
* **`callCompleted(data)`:** Call completed. `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError(data)`:** Error occurred. `data`: `{ message: string }`
* **`resizeWidget(data)`:** Resize the widget. `data`: `{ height: number, width: number }`

#### Receiving Messages from HubSpot

* **`onReady(data)`:** HubSpot is ready. `data`: `{ engagementId: number, iframeLocation: Enum, ownerId: string|number, portalId: number, userId: number }`
* **`onDialNumber(data)`:** Outbound call initiated (see detailed data properties in original documentation).
* **`onEngagementCreated(data)`:** (Deprecated) Engagement created.  Use `onCreateEngagementSucceeded` instead.
* **`onNavigateToRecordFailed(data)`:** Navigation to record failed. `data`: `{ engagementId: number, objectCoordinates: object }`
* **`onPublishToChannelSucceeded(data)`:** Publishing to channel succeeded. `data`: `{ engagementId: number, externalCallId: string }`
* **`onPublishToChannelFailed(data)`:** Publishing to channel failed.  `data`: `{ engagementId: number, externalCallId: string }`
* **`onCallerIdMatchSucceeded(event)`:** Caller ID matched successfully.
* **`onCallerIdMatchFailed(event)`:** Caller ID match failed.
* **`onCreateEngagementSucceeded(event)`:** Engagement created successfully.
* **`onCreateEngagementFailed(event)`:** Engagement creation failed.
* **`onVisibilityChanged(data)`:** Widget visibility changed. `data`: `{ isMinimized: boolean, isHidden: boolean }`
* **`defaultEventHandler(event)`:** Default handler for unhandled events.


### Calling Settings Endpoint (API)

Use this API to configure your app's settings:

* **URL:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`
* **Methods:** `POST`, `PATCH`, `GET`, `DELETE`
* **Payload (example):**
  ```json
  {
    "name": "demo widget",
    "url": "https://mywidget.com/widget",
    "height": 600,
    "width": 400,
    "isReady": false, // Set to true for production
    "supportsCustomObjects": true
  }
  ```

### Overriding Settings using localStorage (for testing)

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


### Production Readiness

Set `isReady` to `true` in the settings endpoint to deploy your app to production.


## FAQ (See original document for detailed answers)

* User authentication
* CDN hosting
* Engagement creation vs. update
* Required scopes
* Adding to existing marketplace apps
* Integrating existing softphone applications
* Multiple integrations
* Free user installation
* Automatic appearance for existing users
* User installation/uninstallation permissions
* Custom calling properties
* Calling from custom objects


This documentation provides a comprehensive overview of the HubSpot Calling Extensions SDK.  Refer to the original document for more detailed information and specific examples.
