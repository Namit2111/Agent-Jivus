# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling functionality within HubSpot.

## Overview

The HubSpot Calling Extensions SDK allows developers to offer custom calling options directly from CRM records.  It comprises three key components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure calling settings for each connected HubSpot account.
3. **Calling iFrame:**  The user interface displayed within HubSpot, configured via the settings endpoints.

**Note:** Currently, only *outgoing* calls are supported.


## Getting Started

### 1. Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:**  More realistic implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** Demo apps use mock data and are not fully functional calling applications.

### 2. Installing the Demo App

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo app directory:
    * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
    * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
4. Access the app at `https://localhost:9025/` (may require bypassing a security warning).

### 3. Launching the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console.
3. Set the `localStorage` item:
    * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **Uninstalled (minimal-js):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **Uninstalled (react-ts):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


## Installing the Calling Extensions SDK

Add the SDK as a dependency to your project:

**npm:** `npm i --save @hubspot/calling-extensions-sdk`
**yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses events for communication.

### Events

**Sent to HubSpot:**

* `initialized`:  Softphone ready (payload: `{ isLoggedIn: boolean, engagementId: number }`).
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started (payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`).
* `callAnswered`: Outgoing call answered (payload: `{ externalCallId: string }`).
* `callEnded`: Call ended (payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`).
* `callCompleted`: Call completed (payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`).
* `sendError`: Error occurred (payload: `{ message: string }`).
* `resizeWidget`: Resize the widget (payload: `{ height: number, width: number }`).

**Received from HubSpot:**

* `onReady`: HubSpot ready (payload includes `engagementId`, `iframeLocation`, `ownerId`, `portalId`, `userId`).
* `onDialNumber`: Outbound call initiated (payload includes phone number, contact/company details, timestamps).
* `onEngagementCreated` (Deprecated, use `onCreateEngagementSucceeded`): Engagement created.
* `onNavigateToRecordFailed`: Navigation to record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publishing to channel result.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match result.
* `onCreateEngagementSucceeded`/`onCreateEngagementFailed`: Engagement creation/update result.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Default event handler.


### SDK API Example

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: enable debug logging
  eventHandlers: {
    onReady: (event) => { /* Handle onReady event */ },
    onDialNumber: (event) => { /* Handle onDialNumber event */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);

// Example of sending an outgoingCall event
extensions.outgoingCall({ toNumber: '+15551234567', fromNumber: '+15559876543', createEngagement: true });
```


## Calling Settings Endpoint (API)

Use this API to manage your app's settings in HubSpot.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values.

**Endpoint:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Methods:** `POST`, `PATCH`, `GET`, `DELETE`

**Example (POST - creating settings):**

```bash
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"My App","url":"https://myapp.com","height":600,"width":400,"isReady":false}'
```

**Example (PATCH - updating settings):**

```bash
curl --request PATCH \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"isReady":true}'
```

The `isReady` flag indicates production readiness (set to `false` during testing).


## LocalStorage Override

For testing, you can override settings using browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'My URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production and Publishing

Set `isReady` to `true` via the API and publish your app to the HubSpot Marketplace.


## Frequently Asked Questions

Refer to the original document for a complete list of FAQs.


This markdown documentation provides a more structured and easily navigable guide to the HubSpot Calling Extensions SDK.  Remember to replace placeholder values with your actual app details.
