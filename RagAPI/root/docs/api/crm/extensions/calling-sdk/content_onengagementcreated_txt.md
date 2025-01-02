# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between your calling application and HubSpot.  It enables users to initiate calls directly from HubSpot records (Contacts, Companies, and potentially custom objects).  The integration comprises three key parts:

1. **Calling Extensions SDK (JavaScript):**  The core SDK enabling message exchange between your app and HubSpot.
2. **Calling Settings Endpoints (API):**  Used to configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:**  The user interface displayed within HubSpot, configured via the settings endpoints.


**Note:** Currently, only outgoing calls are supported.


## Getting Started

### 1. Install the Demo App (Optional):

This section describes how to install and run the provided demo apps to test the SDK.  These are not fully functional calling apps but provide examples.

**Prerequisites:** Node.js and npm (or yarn)

**Installation:**

1. Clone the repository (or download the ZIP).
2. Navigate to the demo app directory:
    * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
    * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
3. The app will launch in your browser at `https://localhost:9025/`.  You may need to bypass a security warning.


### 2. Launch the Demo App from HubSpot:

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Set the `localStorage` item to indicate which demo app to load:
    * **Installed Demo (demo-minimal-js or demo-react-ts):**  `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **Uninstalled demo-minimal-js:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **Uninstalled demo-react-ts:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and initiate a call.  The console will display events.

### 3. Install the Calling Extensions SDK:

Add the SDK to your project using npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the SDK

The SDK uses events for communication.  Your app sends messages to HubSpot using methods provided by the `CallingExtensions` object, and receives messages via event handlers.

### API: `CallingExtensions` Object

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

#### Sending Messages to HubSpot

* `initialized(payload)`:  Signals the app's readiness.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn()`: User logged in.
* `userLoggedOut()`: User logged out.
* `outgoingCall(callInfo)`: Outgoing call initiated. `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered(payload)`: Call answered. `payload`: `{ externalCallId: string }`
* `callEnded(payload)`: Call ended. `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`  `EndStatus` is an enum (see documentation).
* `callCompleted(data)`: Call completed. `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError(data)`: Error encountered. `data`: `{ message: string }`
* `resizeWidget(data)`: Resize the widget. `data`: `{ height: number, width: number }`

#### Receiving Messages from HubSpot

* `onReady(data)`: HubSpot is ready.  `data` includes `engagementId`, `iframeLocation`, `ownerId`, `portalId`, and `userId`.
* `onDialNumber(data)`: Outbound call initiated by HubSpot.  `data` includes phone number, owner ID, object details, etc.
* `onCreateEngagementSucceeded(event)`: Engagement created successfully.
* `onCreateEngagementFailed(event)`: Engagement creation failed.
* `onUpdateEngagementSucceeded(event)`: Engagement updated successfully.
* `onUpdateEngagementFailed(event)`: Engagement update failed.
* `onNavigateToRecordFailed(data)`: Navigation to a record failed. `data`: `{ engagementId: number, objectCoordinates: object }`
* `onPublishToChannelSucceeded(data)`: Publishing to a channel succeeded.  `data`: `{ engagementId: number, externalCallId: string }`
* `onPublishToChannelFailed(data)`: Publishing to a channel failed.  `data`: `{ engagementId: number, externalCallId: string }`
* `onCallerIdMatchSucceeded(event)`: Caller ID match succeeded.
* `onCallerIdMatchFailed(event)`: Caller ID match failed.
* `onVisibilityChanged(data)`: Widget visibility changed. `data`: `{ isMinimized: boolean, isHidden: boolean }`
* `defaultEventHandler(event)`: Default handler for unhandled events.


### Calling Settings Endpoint (API)

Use this API endpoint to configure your app's settings:

```bash
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"My App","url":"https://my-app.com","height":600,"width":400,"isReady":false}'
```

Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your app's ID and API key.  The `isReady` flag should be `false` during development and `true` for production.  The endpoint also supports `PATCH`, `GET`, and `DELETE` methods.


### LocalStorage Override (for testing)

You can override settings during testing using localStorage:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production Deployment

1. Set `isReady` to `true` via the API.
2. Publish your app to the HubSpot Marketplace (optional).


## Frequently Asked Questions (FAQ)

Refer to the original document for the FAQ section.


This markdown documentation provides a more structured and easier-to-read version of the provided text, emphasizing clarity and ease of use for developers.  Remember to always refer to the official HubSpot documentation for the most up-to-date information.
