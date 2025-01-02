# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK facilitates communication between a HubSpot account and a calling app, providing users with a custom calling experience directly from CRM records.  It comprises three key components:

1. **Calling Extensions SDK (JavaScript):**  Enables communication between the app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure settings for each connected HubSpot account.
3. **Calling iFrame:** The app's user interface within HubSpot, configured via the settings endpoints.


**Note:** Only outgoing calls are currently supported.

## Getting Started

### 1. Install the Demo App (Optional)

Two demo apps are available to test the SDK:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:**  More comprehensive example using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Installation Steps (for either demo):**

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo directory (e.g., `cd demos/demo-minimal-js`).
4. Run `npm i && npm start` (or `yarn add @hubspot/calling-extensions-sdk && yarn start`).  This will open the app at `https://localhost:9025/`.  You might need to bypass a security warning.


### 2. Launch the Demo App from HubSpot

1. Go to your HubSpot contacts or companies.
2. Open your browser's developer console.
3. Run one of the following commands in the console, depending on which demo app and whether you installed it:


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

4. Refresh the page.  The demo app should appear in the call switcher.


### 3. Install the Calling Extensions SDK

Add the SDK as a dependency to your app:

**npm:**

```bash
npm i --save @hubspot/calling-extensions-sdk
```

**yarn:**

```bash
yarn add @hubspot/calling-extensions-sdk
```


## Using the Calling Extensions SDK

The SDK uses events for communication.

### Events

**Sent to HubSpot:**

* `initialized`: Softphone is ready. Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Outgoing call answered. Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`: Error occurred. Payload: `{ message: string }`
* `resizeWidget`: Resize widget. Payload: `{ height: number, width: number }`


**Received from HubSpot:**

* `onReady`: HubSpot is ready.  Payload: `{ engagementId: number, iframeLocation: Enum, ownerId: String or Number, portalId: Number, userId: Number }`
* `onDialNumber`: Outbound call triggered. Payload: `{ phoneNumber: string, ownerId: number, subjectId: number, objectId: number, objectType: CONTACT | COMPANY, portalId: number, countryCode: string, calleeInfo: {calleeId: number, calleeObjectTypeId: string}, startTimestamp: number, toPhoneNumberSrc: string }`
* `onEngagementCreated`: **Deprecated**. Use `onCreateEngagementSucceeded` instead.
* `onNavigateToRecordFailed`: Navigation to record failed. Payload: `{ engagementId: number, objectCoordinates: object }`
* `onPublishToChannelSucceeded`: Publishing to channel succeeded. Payload: `{ engagementId: number, externalCallId: string }`
* `onPublishToChannelFailed`: Publishing to channel failed. Payload: `{ engagementId: number, externalCallId: string }`
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement creation succeeded.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement update succeeded.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed. Payload: `{ isMinimized: boolean, isHidden: boolean }`
* `defaultEventHandler`: Default event handler.


### SDK Initialization

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: log debug messages
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Example: Handling `onDialNumber`

```javascript
extensions.eventHandlers.onDialNumber = (data) => {
  const { phoneNumber, ownerId, ...rest } = data;
  // Make the call using your softphone
  console.log("Dialing:", phoneNumber, "for user:", ownerId);
};
```


## API Endpoints (Calling Settings)

Use the following API endpoints to manage your app's settings:

* **URL:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`
* **Methods:** `POST`, `PATCH`, `GET`, `DELETE`
* **Payload (example):**

```json
{
  "name": "My App",
  "url": "https://my-app.com",
  "height": 600,
  "width": 400,
  "isReady": false // Set to true for production
}
```

**Note:**  The `isReady` flag indicates production readiness.  Set it to `false` during testing.


### Overriding Settings with `localStorage` (for testing)

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production and Publishing

1. Set `isReady` to `true` using the API.
2. Publish your app to the HubSpot marketplace (optional).


## Frequently Asked Questions (FAQ)

Refer to the original text for the FAQ section.


This markdown documentation provides a structured and comprehensive overview of the HubSpot Calling Extensions SDK, including code examples and API details. Remember to consult the HubSpot developer documentation for the most up-to-date information.
