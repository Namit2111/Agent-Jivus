# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling custom calling options within the HubSpot CRM.

## Overview

The Calling Extensions SDK allows developers to integrate their calling applications directly into the HubSpot user interface.  This provides users with a seamless calling experience from within HubSpot records (Contacts, Companies, etc.).  The integration consists of three key components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:** The visual representation of your app within HubSpot, controlled via the settings endpoints.

**Note:** Currently, only outgoing calls are supported.


## Getting Started

### 1. Choose a Demo App (Optional):

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** Demo apps use mock data and are not fully functional calling applications.


### 2. Install the Demo App (Optional):

Requires Node.js.  Clone the repository and navigate to the demo app directory:

**`demo-minimal-js`:**

```bash
cd demos/demo-minimal-js && npm i && npm start
```

**`demo-react-ts`:**

```bash
cd demos/demo-react-ts && npm i && npm start
```

This installs dependencies and starts the app at `https://localhost:9025/`.  You may need to bypass a security warning.


### 3. Launch the Demo App from HubSpot:

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Set the appropriate `localStorage` item:

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### 4. Install the Calling Extensions SDK:

Add the SDK to your project using npm or yarn:

**npm:**

```bash
npm i --save @hubspot/calling-extensions-sdk
```

**yarn:**

```bash
yarn add @hubspot/calling-extensions-sdk
```


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends events, and your app responds using event handlers.

### API:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Enables debug logging
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Outbound call initiated */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    defaultEventHandler: (event) => { /* Default event handler */ }
  }
};

const extensions = new CallingExtensions(options);
```

### Events:

**Sent to HubSpot:**

* `initialized`:  Indicates app readiness (includes `isLoggedIn` and `engagementId`).
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started (includes `callStartTime`, `createEngagement`, `toNumber`, `fromNumber`).
* `callAnswered`: Call answered (includes `externalCallId`).
* `callEnded`: Call ended (includes `externalCallId`, `engagementId`, `callEndStatus`).
* `callCompleted`: Call completed (includes `engagementId`, `hideWidget`, `engagementProperties`, `externalCallId`).
* `sendError`: Error occurred (includes `message`).
* `resizeWidget`: Request to resize the widget (includes `height`, `width`).

**Received from HubSpot:**

* `onReady`: HubSpot is ready.
* `onDialNumber`:  Outbound call initiated (includes phone number, contact/company details, etc.).
* `onEngagementCreated`: (Deprecated)  Engagement created. Use `onCreateEngagementSucceeded` instead.
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publishing to a channel succeeded/failed.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match succeeded/failed.
* `onUpdateEngagementSucceeded`/`onUpdateEngagementFailed`: Engagement update succeeded/failed.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Catches unhandled events.

Each event has a corresponding data payload (refer to the original text for details on each payload's properties).


## Calling Settings Endpoint (API)

Use this API to configure your app's settings:

**URL:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Methods:** `POST`, `PATCH`, `GET`, `DELETE`

**Payload Example (POST/PATCH):**

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

`isReady` indicates production readiness. Set to `false` during testing.


## Local Storage Overrides (for testing)

You can override settings using localStorage:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production and Publishing

1. Set `isReady` to `true` using the API's PATCH method.
2. Publish your app to the HubSpot marketplace (details in the original text).


## Frequently Asked Questions (FAQ)

Refer to the original text for answers to frequently asked questions regarding authentication, CDN hosting, engagement creation/updates, required scopes, integration with existing apps, multi-integration support, free user access, automatic updates, user permissions, custom properties, and custom object calling.


This markdown documentation provides a structured and easily readable overview of the HubSpot Calling Extensions SDK. Remember to consult the original text for detailed information on specific events, API calls and error handling.
