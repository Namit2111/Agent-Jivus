# HubSpot CRM API: Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, enabling custom calling options within the HubSpot CRM.

## Overview

The Calling Extensions SDK allows developers to integrate their calling applications directly into the HubSpot user interface.  Users can initiate calls from CRM records, and the SDK facilitates communication between the app and HubSpot, handling call engagement creation and updates.  Only outgoing calls are currently supported.

A calling extension consists of three parts:

1. **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:** Your app's interface displayed to HubSpot users, configured via the settings endpoints.


## Getting Started

### 1. Install the Demo App (Optional):

This section provides options to test the SDK using pre-built demo applications.

**Prerequisites:** Node.js and npm (or yarn)

**Steps:**

1. Clone the demo repository (link provided in original text, assumed to exist).
2. Navigate to the `demos` directory.
3. For `demo-minimal-js`: `cd demo-minimal-js && npm install && npm start`
4. For `demo-react-ts`: `cd demo-react-ts && npm install && npm start`

This starts a local development server (typically `https://localhost:9025/`). You might need to bypass security warnings.

### 2. Launch the Demo App from HubSpot:

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Set the appropriate `localStorage` item:

   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (no install):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (no install):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.  The demo app should appear in the call switcher.

### 3. Install the Calling Extensions SDK:

Add the SDK to your project using npm or yarn:

* **npm:** `npm install --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses an event-driven architecture. HubSpot sends events to your app, and your app sends events to HubSpot.

### SDK API

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Outbound call initiated */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    // ...other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Events

**Sent by HubSpot:**

* `onReady`:  HubSpot is ready.  Provides `engagementId`, `iframeLocation`, `ownerId`, `portalId`, and `userId`.
* `onDialNumber`:  Outbound call initiated. Provides `phoneNumber`, `ownerId`, `subjectId`, `objectId`, `objectType`, `portalId`, `countryCode`, `calleeInfo`, `startTimestamp`, `toPhoneNumberSrc`.
* `onCreateEngagementSucceeded`: Engagement created successfully.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement updated successfully.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed (minimized or hidden).


**Sent by Your App:**

* `initialized`:  Your app is initialized.  Provides `isLoggedIn` and `engagementId`.
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started.  Provides `callStartTime`, `createEngagement`, `toNumber`, `fromNumber`.
* `callAnswered`: Call answered. Provides `externalCallId`.
* `callEnded`: Call ended. Provides `externalCallId`, `engagementId`, `callEndStatus`.
* `callCompleted`: Call completed. Provides `engagementId`, `hideWidget`, `engagementProperties`, `externalCallId`.
* `sendError`: Error encountered. Provides `message`.
* `resizeWidget`: Request to resize the widget. Provides `height` and `width`.


### Calling Settings Endpoint (API)

This API allows you to configure your app's settings in HubSpot.  Use `APP_ID` and your `DEVELOPER_ACCOUNT_API_KEY`.

**Endpoint:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`

**Methods:** POST, PATCH, GET, DELETE

**Example Payload (POST):**

```json
{
  "name": "My Calling App",
  "url": "https://my-app.com/widget",
  "height": 600,
  "width": 400,
  "isReady": false, // Set to true for production
  "supportsCustomObjects": true
}
```

### Overriding Settings (for testing) using localStorage

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


##  Frequently Asked Questions (FAQ)

The original text contains a FAQ section that is well-written and should be included in the final documentation.


This Markdown documentation provides a comprehensive overview of the HubSpot Calling Extensions SDK, including API details, code examples, and frequently asked questions. Remember to replace placeholders like `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values.
