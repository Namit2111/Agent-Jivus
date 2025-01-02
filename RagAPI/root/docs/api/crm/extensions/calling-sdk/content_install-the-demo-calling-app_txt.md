# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, enabling custom calling options within the HubSpot CRM.  It covers installation, usage, API calls, event handling, and frequently asked questions.

## Overview

The Calling Extensions SDK allows developers to integrate their calling applications directly into the HubSpot CRM user interface. This integration provides users with a seamless calling experience from within contact and company records.  The SDK facilitates communication between the calling app and HubSpot via events and API calls.  Currently, only outgoing calls are supported.

The calling extension consists of three parts:

1. **Calling Extensions SDK (JavaScript):**  Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:** The interface displayed to HubSpot users, configured via the settings endpoints.


## Getting Started

### 1. Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:**  More realistic implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:**  Demo apps use mock data and aren't fully functional calling apps.

### 2. Installing the Demo App

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
4. Access the app at `https://localhost:9025/` (you might need to bypass a security warning).

### 3. Launching the Demo App from HubSpot

1. Navigate to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Run one of the following commands in the console, depending on which demo app and installation method you used:

   * **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.  The demo app should appear in the call switcher.

### 4. Installing the Calling Extensions SDK

Use npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

### API

The SDK uses events to handle communication:

**Events Sent to HubSpot:**

* `initialized`: Softphone ready (payload: `{ isLoggedIn: boolean, engagementId: number }`).
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started (payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`).
* `callAnswered`: Call answered (payload: `{ externalCallId: string }`).
* `callEnded`: Call ended (payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`).
* `callCompleted`: Call completed (payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`).
* `sendError`: Error encountered (payload: `{ message: string }`).
* `resizeWidget`: Resize widget (payload: `{ height: number, width: number }`).

**Events Received from HubSpot:**

* `onReady`: HubSpot ready (payload includes `engagementId`, `iframeLocation`, `ownerId`, `portalId`, `userId`).
* `onDialNumber`: Outbound call triggered (payload includes phone number, contact/company info, timestamps).
* `onCreateEngagementSucceeded`: Engagement successfully created.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement successfully updated.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed (payload: `{ isMinimized: boolean, isHidden: boolean }`).
* `onNavigateToRecordFailed`: Navigation to record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publishing to channel succeeded/failed.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match succeeded/failed.
* `defaultEventHandler`: Default event handler.


**Example SDK Initialization:**

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true,
  eventHandlers: {
    onReady: (data) => { console.log('HubSpot ready:', data); },
    onDialNumber: (data) => { console.log('Dial number:', data); },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Calling Settings Endpoint (API)

Use this endpoint to configure your app's settings:

`POST/PATCH/GET/DELETE https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Payload Example (POST/PATCH):**

```json
{
  "name": "My Calling App",
  "url": "https://my-calling-app.com",
  "height": 600,
  "width": 400,
  "isReady": false, // Set to true for production
  "supportsCustomObjects": true
}
```

### Overriding Settings with localStorage

For testing, you can override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'http://localhost:3000'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


##  Production and Deployment

1. Set `isReady` to `true` in the API settings.
2. Publish your app to the HubSpot Marketplace (optional).


## Frequently Asked Questions (FAQs)

Refer to the original document for the FAQs section.


This markdown documentation provides a more structured and concise overview of the HubSpot CRM API Calling Extensions SDK, making it easier to understand and use.  Remember to consult the original documentation for complete details and the most up-to-date information.
