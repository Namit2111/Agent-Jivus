# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling options into their HubSpot apps.

## Overview

The Calling Extensions SDK facilitates communication between a calling app and HubSpot, allowing users to initiate calls directly from CRM records.  The integration consists of three core components:

1. **Calling Extensions SDK (JavaScript):**  Enables message exchange between the app and HubSpot.
2. **Calling Settings Endpoints (API):**  Configure calling settings for each connected HubSpot account.
3. **Calling iFrame:**  The app's user interface within HubSpot, configured via the settings endpoints.

**Note:** Currently, only outgoing calls are supported.


## Getting Started

### 1. Install the Demo App (Optional)

Two demo apps are available to test the SDK: `demo-minimal-js` (JavaScript, HTML, CSS) and `demo-react-ts` (React, TypeScript, Styled Components).

**Prerequisites:** Node.js and npm (or yarn)

**Installation:**

1. Clone the repository: `git clone <repository_url>`
2. Navigate to the demo app directory: `cd demos/demo-minimal-js` (or `cd demos/demo-react-ts`)
3. Install dependencies: `npm install` (or `yarn add`)
4. Start the app: `npm start` (or `yarn start`)  This opens the app at `https://localhost:9025/`.


### 2. Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Set the appropriate `localStorage` item:

   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.  The demo app should appear in the call switcher.


### 3. Install the Calling Extensions SDK

Add the SDK to your project using npm or yarn:

**npm:** `npm install --save @hubspot/calling-extensions-sdk`

**yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture. HubSpot sends messages (events) to the app, and the app responds using SDK methods.


### SDK API

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Outbound call initiated */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

### Events

**HubSpot sends these events:**

* `onReady`:  HubSpot is ready for communication.
* `onDialNumber`: User initiates an outbound call.  Provides phone number, owner ID, object ID, object type, etc.
* `onCreateEngagementSucceeded`: Engagement successfully created by HubSpot.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement successfully updated.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed (minimized/hidden).


**App sends these messages (using `extensions` object methods):**

* `initialized`: App is ready, sends login status and engagement ID.
* `userLoggedIn`: User logs in.
* `userLoggedOut`: User logs out.
* `outgoingCall`: Outbound call started.  Provides call start time, phone number, engagement creation flag, etc.
* `callAnswered`: Outbound call answered.
* `callEnded`: Outbound call ended.
* `callCompleted`: Outbound call completed.  Provides engagement ID, whether to hide the widget, etc.
* `sendError`:  An error occurred in the app.
* `resizeWidget`: Request to resize the widget.



### Example: Handling `onDialNumber` Event

```javascript
extensions.eventHandlers.onDialNumber = (data) => {
  const { phoneNumber, ownerId, objectId, objectType } = data;
  console.log("Dialing:", phoneNumber, "for owner:", ownerId, "object:", objectId, "type:", objectType);
  // Initiate call using your phone system
};
```

### Example: Sending `outgoingCall` Message

```javascript
const callInfo = {
  toNumber: "+15551234567",
  fromNumber: "+15559876543",
  createEngagement: true, // Tells HubSpot to create an engagement
  callStartTime: Date.now(),
};
extensions.outgoingCall(callInfo);
```


## API Endpoints (Calling Settings)

Use these endpoints to configure the calling app's settings:

* **URL:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`
* **Methods:** POST (create/update), PATCH (update), GET (retrieve), DELETE (delete)

**Payload Example (POST/PATCH):**

```json
{
  "name": "My Calling App",
  "url": "https://my-calling-app.com",
  "width": 400,
  "height": 600,
  "isReady": true // Set to false during development
}
```


## LocalStorage Overrides (for Testing)

You can override settings during testing using localStorage:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production Deployment

1. Set `isReady` to `true` in your app settings using the API.
2. Publish your app to the HubSpot marketplace (optional).


## Frequently Asked Questions (FAQ)

Refer to the original text for the FAQ section.


This markdown documentation provides a structured and detailed overview of the HubSpot Calling Extensions SDK, covering installation, usage, API calls, and frequently asked questions.  Remember to consult the official HubSpot documentation for the most up-to-date information.
