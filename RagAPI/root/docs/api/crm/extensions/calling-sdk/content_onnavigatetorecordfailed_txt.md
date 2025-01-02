# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot CRM.  The SDK facilitates communication between a calling app and HubSpot, enabling features like initiating calls directly from CRM records.

## Overview

The Calling Extensions SDK consists of three main components:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication between your app and HubSpot.  This is installed as a Node.js dependency (`@hubspot/calling-extensions-sdk`).
2. **Calling Settings Endpoints (API):** Used to configure your app's settings for each connected HubSpot account.  These are accessed via the HubSpot API.
3. **Calling iFrame:** The iFrame where your app is displayed to HubSpot users; configured using the calling settings endpoints.


## Getting Started

### 1. Run the Demo Apps

Two demo apps are provided:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  View the SDK instantiation in `index.js`.
* **`demo-react-ts`:** A more complete example using React, TypeScript, and Styled Components.  View the SDK instantiation in `useCti.ts`.

**Installation (for both demo apps):**

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app's directory: `cd demos/demo-minimal-js` or `cd demos/demo-react-ts`.
4. Run `npm i && npm start`.  This will open the app at `https://localhost:9025/`.  You may need to bypass a security warning.


### 2. Launch Demo App from HubSpot

1. Navigate to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Run one of the following `localStorage` commands, depending on the demo app and whether it was installed locally:

    * **Installed `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **Installed `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page. The demo app should appear in the call switcher.


### 3. Install the SDK in Your App

Use npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the SDK

The SDK uses events to communicate between your app and HubSpot.

### Events

**Sent to HubSpot:**

* `initialized`:  Signals app readiness (payload: `{ isLoggedIn: boolean, engagementId: number }`).
* `userLoggedIn`:  User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started (payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`).
* `callAnswered`: Call answered (payload: `{ externalCallId: string }`).
* `callEnded`: Call ended (payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`).
* `callCompleted`: Call completed (payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`).
* `sendError`: Error occurred (payload: `{ message: string }`).
* `resizeWidget`: Resize the widget (payload: `{ height: number, width: number }`).

**Received from HubSpot:**

* `onReady`: HubSpot is ready (payload includes `engagementId`, `iframeLocation`, `ownerId`, `portalId`, `userId`).
* `onDialNumber`:  Outbound call initiated (payload includes contact/company details, phone number, etc.).
* `onCreateEngagementSucceeded`: Engagement successfully created.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement successfully updated.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed (payload: `{ isMinimized: boolean, isHidden: boolean }`).
* `defaultEventHandler`: Catches all other events.


### Example Code (JavaScript)

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true,
  eventHandlers: {
    onReady: (data) => { console.log('HubSpot ready:', data); },
    onDialNumber: (data) => {
      console.log('Dial number:', data);
      // Initiate call using your softphone
    },
    onCreateEngagementSucceeded: (data) => { console.log('Engagement created:', data); },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

## API Endpoints (Calling Settings)

Use the HubSpot API to manage your app's settings:

* **URL:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`
* **Methods:** `POST`, `PATCH`, `GET`, `DELETE`
* **Payload (example):**

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


### Overriding Settings with localStorage (for testing)

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

## Production Deployment

1. Set `isReady` to `true` in your app settings via the API.
2. Publish your app to the HubSpot Marketplace (optional).


## Frequently Asked Questions

Refer to the original document for a comprehensive FAQ section.

This markdown documentation provides a structured overview of the HubSpot Calling Extensions SDK.  Remember to consult the original document and HubSpot's developer resources for the most up-to-date information.
