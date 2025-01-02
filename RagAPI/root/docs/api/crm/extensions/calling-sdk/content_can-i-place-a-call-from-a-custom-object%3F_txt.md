# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between a calling application and HubSpot.  It consists of three main components:

1. **Calling Extensions SDK (JavaScript):**  Enables communication through events and methods.
2. **Calling Settings Endpoints (API):** Configure settings for each connected HubSpot account.
3. **Calling iFrame:** Displays the app to HubSpot users.

**Note:** Only outgoing calls are currently supported.

## Getting Started

### 1. Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:** More comprehensive implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** Demo apps use mock data.

### 2. Installing Demo Apps

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`

This starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### 3. Launching Demo Apps from HubSpot

1. Go to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Run one of the following commands based on your installation method:

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call."

### 4. Installing the SDK

Add the SDK to your project:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses events and methods for communication.

### Events

**From HubSpot:**

* `onReady`: HubSpot is ready.
* `onDialNumber`:  User initiates an outbound call (see details below).
* `onEngagementCreated`: (Deprecated; use `onCreateEngagementSucceeded`) HubSpot created a call engagement.
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publishing to a channel succeeded/failed.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match succeeded/failed.
* `onCreateEngagementSucceeded`/`onCreateEngagementFailed`: Engagement creation succeeded/failed.
* `onUpdateEngagementSucceeded`/`onUpdateEngagementFailed`: Engagement update succeeded/failed.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Default event handler.

**To HubSpot:**

* `initialized`: Softphone ready.
* `userLoggedIn`/`userLoggedOut`: User login/logout status.
* `outgoingCall`: Outgoing call started (see details below).
* `callAnswered`: Outgoing call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`: An error occurred.
* `resizeWidget`: Resize the widget.

### Methods

The `CallingExtensions` object provides methods for sending events to HubSpot.  Refer to the detailed event descriptions in the original text for payload structures.

### Example: SDK Instantiation

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, //Optional, set to true for debugging messages in the console
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

## API Endpoints

The calling settings are managed through the following API endpoint:

`https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`

This endpoint supports `POST`, `PATCH`, `GET`, and `DELETE` methods.  The payload includes: `name`, `url`, `height`, `width`, and `isReady` (boolean, indicating production readiness).


## Testing and Production

During testing, set `isReady` to `false`. Once ready, use the `PATCH` method to set it to `true`.

## Publishing to the Marketplace

After testing, publish your app to the HubSpot marketplace.


## Frequently Asked Questions (FAQ)

The original text contains a comprehensive FAQ section.  Refer to it for answers to common questions about authentication, CDN hosting, engagement management, required scopes, and more.


This markdown documentation provides a structured overview and detailed information based on the provided text.  Remember to consult the original text for complete details and nuanced explanations.
