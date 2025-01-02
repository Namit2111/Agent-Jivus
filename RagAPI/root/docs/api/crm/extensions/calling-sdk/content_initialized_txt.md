# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling options into their HubSpot apps.

## Overview

The HubSpot Calling Extensions SDK facilitates communication between your app and HubSpot, allowing users to make calls directly from CRM records.  It comprises three key components:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:**  The visual interface of your app within HubSpot, configured via the settings endpoints.

**Note:** Currently, only outgoing calls are supported.


## Getting Started

### 1. Install the Demo App (Optional):

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  (See `index.js` for SDK instantiation).
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components. (See `useCti.ts` for SDK instantiation).

These demos use mock data.  To install:

1. Install Node.js.
2. Clone the repository (or download the ZIP).
3. Navigate to the demo directory (e.g., `cd demos/demo-minimal-js`).
4. Run `npm i && npm start` (or `yarn add @hubspot/calling-extensions-sdk` then `yarn start`). This will launch the app at `https://localhost:9025/`. You may need to bypass a security warning.


### 2. Launch the Demo App from HubSpot:

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following `localStorage` commands, depending on the demo app and whether you installed it:

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
4. Refresh the page.  Select the demo app from the "Call from" dropdown in the call switcher.


### 3. Install the Calling Extensions SDK:

Add the SDK to your project using npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends events, and your app responds via event handlers.

### Creating an SDK Instance:

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
  }
};

const extensions = new CallingExtensions(options);
```

### Events

#### Sending Messages to HubSpot (Methods of `extensions` object):

| Method             | Description                                                                   | Payload                                                                     |
|----------------------|-------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| `initialized`      | Notifies HubSpot that the app is ready.                                      | `{ isLoggedIn: boolean, engagementId: number }`                            |
| `userLoggedIn`      | Notifies HubSpot that the user has logged in.                               | None                                                                       |
| `userLoggedOut`     | Notifies HubSpot that the user has logged out.                               | None                                                                       |
| `outgoingCall`      | Notifies HubSpot of an outgoing call.                                        | `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }` |
| `callAnswered`      | Notifies HubSpot that a call has been answered.                              | `{ externalCallId: string }`                                               |
| `callEnded`         | Notifies HubSpot that a call has ended.                                      | `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }` |
| `callCompleted`    | Notifies HubSpot that a call is completed.                                   | `{ engagementId: number, hideWidget: boolean, engagementProperties: object, externalCallId: number }` |
| `sendError`         | Notifies HubSpot of an error.                                                | `{ message: string }`                                                      |
| `resizeWidget`      | Requests a widget resize.                                                    | `{ height: number, width: number }`                                        |


#### Receiving Messages from HubSpot (Event Handlers):

| Event Handler        | Description                                                              | Payload (example)                                                                                                          |
|-----------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| `onReady`            | HubSpot is ready to receive messages.                                   | `{ engagementId: number, iframeLocation: string, ownerId: string|number, portalId: number, userId: number }`                  |
| `onDialNumber`       | Outbound call initiated by user in HubSpot.                            | `{ phoneNumber: string, ownerId: number, subjectId: number, objectId: number, objectType: string, portalId: number, countryCode: string, calleeInfo: object, startTimestamp: number, toPhoneNumberSrc: string }` |
| `onCreateEngagementSucceeded` | Engagement successfully created by HubSpot.                            | `{ engagementId: number }`                                                                                                    |
| `onCreateEngagementFailed`  | Engagement creation failed.                                            | `{ error: string }`                                                                                                         |
| `onUpdateEngagementSucceeded` | Engagement successfully updated.                                        | `{ engagementId: number }`                                                                                                    |
| `onUpdateEngagementFailed`  | Engagement update failed.                                               | `{ error: string }`                                                                                                         |
| `onNavigateToRecordFailed` | Navigating to a record failed.                                         | `{ engagementId: number, objectCoordinates: object }`                                                                          |
| `onPublishToChannelSucceeded` | Publishing to a channel succeeded.                                     | `{ engagementId: number, externalCallId: string }`                                                                          |
| `onPublishToChannelFailed`  | Publishing to a channel failed.                                        | `{ engagementId: number, externalCallId: string }`                                                                          |
| `onCallerIdMatchSucceeded` | Caller ID match successful.                                         | `{}`                                                                                                                          |
| `onCallerIdMatchFailed`  | Caller ID match failed.                                              | `{}`                                                                                                                          |
| `onVisibilityChanged` | Widget visibility changed (minimized/hidden).                            | `{ isMinimized: boolean, isHidden: boolean }`                                                                                  |
| `defaultEventHandler` | Default handler for unhandled events.                                | `{ event: object }`                                                                                                             |


### Calling Settings Endpoint (API)

Use this API endpoint to configure your app's settings for each HubSpot account.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values.

* **Endpoint:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`
* **Methods:** `POST`, `PATCH`, `GET`, `DELETE`
* **Payload Example (POST/PATCH):**
  ```json
  {
    "name": "My Calling App",
    "url": "https://my-calling-app.com",
    "height": 600,
    "width": 400,
    "isReady": true, // Set to false during testing
    "supportsCustomObjects": true
  }
  ```

### Overriding Settings with localStorage (for testing):

You can override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'My URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production Deployment

1. Set `isReady` to `true` in your calling settings using the API's PATCH method.
2. Publish your app to the HubSpot Marketplace.


## Frequently Asked Questions (FAQ)

Refer to the original text for the FAQ section.


This markdown documentation provides a structured and easily understandable overview of the HubSpot Calling Extensions SDK.  Remember to consult the original text for any details not covered here.
