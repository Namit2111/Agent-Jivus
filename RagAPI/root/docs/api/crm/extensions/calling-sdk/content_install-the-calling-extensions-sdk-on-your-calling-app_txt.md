# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling custom calling options within the HubSpot CRM.

## Overview

The HubSpot Calling Extensions SDK facilitates communication between your calling application and HubSpot.  It allows you to integrate your custom calling functionality directly into the HubSpot user interface, appearing as an option in the call switcher.  Currently, only outgoing calls are supported.  The SDK consists of three key parts:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication between your app and HubSpot.  Installed via npm or yarn.
2. **Calling Settings Endpoints (API):** Used to configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:** The iframe where your calling app is displayed to HubSpot users; configured via the calling settings endpoints.

## Getting Started

### 1. Create a HubSpot Developer Account (if needed)

If you don't have a HubSpot developer account, create one [here](link_to_hubspot_developer_signup).  You'll need this to create and manage your calling app.

### 2. Create a HubSpot App (if needed)

If you don't already have a HubSpot app, create one from your HubSpot developer account.  This will provide you with an `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`, necessary for API calls.

### 3. Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:**  More realistic implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Installation (for demo apps):**

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo app directory (e.g., `cd demos/demo-minimal-js`).
4. Run `npm i && npm start` (or `yarn install && yarn start` for `yarn`).

**Launching Demo Apps from HubSpot:**

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Set the appropriate `localStorage` item:
    * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page and select the demo app from the call switcher.

### 4. Install the SDK

Add the SDK to your app as a dependency:

**npm:** `npm i --save @hubspot/calling-extensions-sdk`

**yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends events; your app responds via event handlers.

### Creating an SDK Instance

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Enable debug logging
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


### Events

**HubSpot sends these events:**

* `onReady`: HubSpot is ready.
* `onDialNumber`: User initiates an outbound call.  Provides phone number, owner ID, object ID, object type, portal ID, country code, callee info, timestamp, and phone number source.
* `onCreateEngagementSucceeded`/`onCreateEngagementFailed`:  Result of engagement creation (HubSpot handles this automatically unless manually overridden).
* `onUpdateEngagementSucceeded`/`onUpdateEngagementFailed`: Result of engagement update (usually after the call).
* `onVisibilityChanged`: Widget visibility changes.
* `onNavigateToRecordFailed` (Deprecated): Failed to navigate to a record.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Result of publishing to a channel.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Result of caller ID matching.

**Your app sends these events:**

* `initialized`:  App is initialized (include `isLoggedIn` and `engagementId`).
* `userLoggedIn`/`userLoggedOut`: User login/logout status.
* `outgoingCall`: Outgoing call started (include `callStartTime`, `createEngagement`, `toNumber`, and `fromNumber`).
* `callAnswered`: Outgoing call answered (include `externalCallId`).
* `callEnded`: Outgoing call ended (include `externalCallID`, `engagementId`, and `callEndStatus`).
* `callCompleted`: Outgoing call completed (include `engagementId`, `hideWidget`, `engagementProperties`, `externalCallId`).
* `sendError`: Error occurred.
* `resizeWidget`: Request to resize the widget.


### Calling Settings Endpoint (API)

Use this API endpoint to configure your app's settings:

`POST/PATCH/GET/DELETE https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Payload Example (POST/PATCH):**

```json
{
  "name": "My Calling App",
  "url": "https://my-calling-app.com",
  "width": 400,
  "height": 600,
  "isReady": true, // Set to false during development
  "supportsCustomObjects": true
}
```

### LocalStorage Override (for testing)

You can override settings using localStorage:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'my-local-url'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

## Production

Set `isReady` to `true` in your API settings to make your app available in production.  Publish your app to the HubSpot marketplace if desired.

## Frequently Asked Questions (FAQ)

See the original document for the FAQ section.


This markdown documentation provides a structured and more easily navigable version of the provided text.  Remember to replace placeholder links (like `link_to_hubspot_developer_signup`) with actual URLs.
