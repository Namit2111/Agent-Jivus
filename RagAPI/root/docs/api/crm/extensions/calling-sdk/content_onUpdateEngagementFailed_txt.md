# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling options into HubSpot CRM.

## Overview

The Calling Extensions SDK allows apps to offer custom calling functionality directly from CRM records.  It consists of three key parts:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure calling settings for each connected HubSpot account.
3. **Calling iFrame:**  The user interface of your calling app within HubSpot, configured via the settings endpoints.

**Note:** Only outgoing calls are currently supported.

## Getting Started

### 1. Run the Demo App

Two demo apps are available for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:**  A more realistic implementation using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** Demo apps use mock data and aren't fully functional calling applications.

### 2. Install the Demo App (Optional)

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app's directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.

### 3. Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console.
3. Set `localStorage` based on your installation method:
   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.  Select the demo app from the "Call from" dropdown in the call switcher.

## Integrating the SDK into Your App

### 1. Installation

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

### 2. Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends events, and your app responds via event handlers.

**Creating an SDK instance:**

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* HubSpot sends dial number */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ }
  }
};

const extensions = new CallingExtensions(options);
```

### 3. Events

**Events sent to HubSpot (methods on the `extensions` object):**

* `initialized(payload)`: Notifies HubSpot that the softphone is ready.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn()`: User logged in.
* `userLoggedOut()`: User logged out.
* `outgoingCall(callInfo)`: Outgoing call started.  `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered(payload)`: Call answered. `payload`: `{ externalCallId: string }`
* `callEnded(payload)`: Call ended. `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted(data)`: Call completed. `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError(data)`: Error occurred. `data`: `{ message: string }`
* `resizeWidget(data)`: Resize the widget. `data`: `{ height: number, width: number }`


**Events received from HubSpot (event handlers in the `options.eventHandlers` object):**

* `onReady()`: HubSpot is ready.
* `onDialNumber(data)`: Outbound call initiated.  (See detailed `data` properties in the original document)
* `onEngagementCreated(data)`: (Deprecated) Engagement created.
* `onNavigateToRecordFailed(data)`: Navigation to a record failed.
* `onPublishToChannelSucceeded(data)`: Publishing to a channel succeeded.
* `onPublishToChannelFailed(data)`: Publishing to a channel failed.
* `onCallerIdMatchSucceeded(event)`: Caller ID match succeeded.
* `onCallerIdMatchFailed(event)`: Caller ID match failed.
* `onCreateEngagementSucceeded(event)`: Engagement creation succeeded.
* `onCreateEngagementFailed(event)`: Engagement creation failed.
* `onUpdateEngagementSucceeded(event)`: Engagement update succeeded.
* `onUpdateEngagementFailed(event)`: Engagement update failed.
* `onVisibilityChanged(data)`: Widget visibility changed.  `data`: `{ isMinimized: boolean, isHidden: boolean }`
* `defaultEventHandler(event)`: Default event handler.


### 4. Calling Settings Endpoint (API)

Use this API to configure your app's settings for each HubSpot account.  The endpoint supports POST, PATCH, GET, and DELETE.

**Example (using `curl`):**

```bash
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"My App","url":"https://my-app.com","height":600,"width":400,"isReady":false}'
```

Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your app's ID and your developer API key.  `isReady: false` during testing, `true` for production.

### 5. LocalStorage Override (for testing)

You can override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'my-local-url',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### 6. Production Readiness

Set `isReady` to `true` via the settings API to make your app ready for production.

### 7. Publishing to the Marketplace

Once ready, publish your app to the HubSpot marketplace.  See the HubSpot documentation for details.


## Frequently Asked Questions (FAQ)

Refer to the original document for answers to frequently asked questions about authentication, CDN hosting, engagement creation/updates, required scopes, and more.


This markdown documentation provides a structured and more easily readable version of the original content, focusing on clarity and organization.  Remember to consult the original document for the most up-to-date information.
