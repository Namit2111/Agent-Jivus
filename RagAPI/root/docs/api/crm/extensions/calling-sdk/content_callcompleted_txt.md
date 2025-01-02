# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling options into HubSpot CRM records.

## Overview

The Calling Extensions SDK facilitates communication between your application and HubSpot, allowing users to initiate calls directly from CRM records.  It consists of three primary components:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication between your app and HubSpot.  It handles event handling and message passing.
2. **Calling Settings Endpoints (API):**  Used to configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:**  The iframe where your app is displayed to HubSpot users; its configuration is managed via the settings endpoints.


**Note:** Currently, only outgoing calls are supported.


## Getting Started

### 1. Demo Apps

Two demo applications are available to test the SDK:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:** A more realistic implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** Demo apps use mock data and are not fully functional calling applications.

### 2. Installing the Demo App

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
4.  The app will open in your browser at `https://localhost:9025/`. You might need to bypass a security warning.

### 3. Launching the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console and run one of the following commands, depending on the demo app and whether you installed it locally:

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
3. Refresh the page.  Select the demo app from the "Call from" dropdown in the call switcher.

### 4. Installing the SDK

Add the SDK as a dependency to your calling app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses event handlers for communication.  Here's a basic example:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* HubSpot sent a dial number */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

### Events

**Outbound Events (Sent to HubSpot):**

* `initialized`:  Notifies HubSpot that the softphone is ready.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`:  User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Initiating an outbound call. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Call answered. Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`: An error occurred. Payload: `{ message: string }`
* `resizeWidget`: Resize the widget. Payload: `{ height: number, width: number }`

**Inbound Events (Received from HubSpot):**

* `onReady`: HubSpot is ready.
* `onDialNumber`: Outbound call initiated from HubSpot.  Provides details like phone number, owner ID, object type, etc.
* `onEngagementCreated`: (Deprecated) Engagement created. Use `onCreateEngagementSucceeded` instead.
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publishing to a channel succeeded/failed.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match succeeded/failed.
* `onUpdateEngagementSucceeded`/`onUpdateEngagementFailed`: Engagement update succeeded/failed.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Handles any unhandled events.


### Calling Settings Endpoint (API)

Use this endpoint to configure your app's settings:

* **URL:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`
* **Methods:** `POST`, `PATCH`, `GET`, `DELETE`
* **Payload (Example):**

```json
{
  "name": "My App",
  "url": "https://myapp.com",
  "height": 600,
  "width": 400,
  "isReady": false // Set to true for production
}
```

### LocalStorage Override (for testing)

You can override settings using localStorage:

```javascript
const settings = { isReady: true, name: 'My App', url: 'mylocalurl' };
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(settings));
```

## Frequently Asked Questions (FAQ)

* **Authentication:** Your app handles authentication.
* **CDN Hosting:** Yes, the SDK is hosted on jsDeliver.
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them with call details. For calls outside the HubSpot UI, your app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:** You can add this functionality to existing marketplace apps.
* **Softphone Integration:** Easily integrate your existing softphone.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free Users:** Free users can install the app.
* **Automatic Appearance:** The integration automatically appears for existing users.
* **App Installation/Uninstallation:**  Only users with appropriate permissions can install/uninstall.
* **Custom Calling Properties:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, if `createEngagement: true` is used in the `outgoingCall` event.



This documentation provides a starting point. Refer to the HubSpot developer portal for the most up-to-date information and detailed API specifications.
