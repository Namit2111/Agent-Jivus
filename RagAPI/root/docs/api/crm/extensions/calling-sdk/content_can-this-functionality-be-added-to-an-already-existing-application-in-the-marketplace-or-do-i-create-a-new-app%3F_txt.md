# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, enabling custom calling options within the HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between your calling application and HubSpot, providing a seamless calling experience directly from CRM records.  It consists of three core components:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):**  Used to configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:**  Displays your app to HubSpot users; configured via the calling settings endpoints.

**Note:** Currently, only outgoing calls are supported.

## Getting Started

### 1. Run the Demo App

Two demo apps are available:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:**  More realistic implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** Demo apps use mock data and are not fully functional calling applications.

**Installation:**

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
4. Access the app at `https://localhost:9025/` (may require bypassing a security warning).


### 2. Launch the Demo App from HubSpot

1. Go to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Run one of the following commands depending on your demo app and installation method:
    * **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### 3. Install the SDK

Add the SDK as a dependency to your calling app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends events to your app, and your app can send events to HubSpot.

### API

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Dial number received from HubSpot */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    defaultEventHandler: (event) => { /* Handle any other events */ }
  }
};

const extensions = new CallingExtensions(options);
```

### Events

**Sent to HubSpot (using `extensions` object methods):**

* `initialized(payload)`:  Signals app readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn()`:  User logged in.
* `userLoggedOut()`: User logged out.
* `outgoingCall(callInfo)`: Outgoing call started.  Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered(payload)`: Call answered. Payload: `{ externalCallId: string }`
* `callEnded(payload)`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted(data)`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError(data)`: Error occurred. Payload: `{ message: string }`
* `resizeWidget(data)`: Resize widget. Payload: `{ height: number, width: number }`


**Received from HubSpot (handled by `eventHandlers`):**

* `onReady(data)`: HubSpot is ready. Data includes `engagementId`, `iframeLocation`, `ownerId`, `portalId`, and `userId`.
* `onDialNumber(data)`: Outbound call initiated.  Data includes phone number, owner ID, subject ID, object ID, object type, portal ID, country code, callee info, start timestamp, and `toPhoneNumberSrc`.
* `onEngagementCreated(data)`: **Deprecated**. Use `onCreateEngagementSucceeded` instead. Data includes `engagementId`.
* `onNavigateToRecordFailed(data)`: Navigation to record failed. Data includes `engagementId` and `objectCoordinates`.
* `onPublishToChannelSucceeded(data)`: Publishing to channel succeeded. Data includes `engagementId` and `externalCallId`.
* `onPublishToChannelFailed(data)`: Publishing to channel failed. Data includes `engagementId` and `externalCallId`.
* `onCallerIdMatchSucceeded(event)`: Caller ID match succeeded.
* `onCallerIdMatchFailed(event)`: Caller ID match failed.
* `onCreateEngagementSucceeded(event)`: Engagement created successfully.
* `onCreateEngagementFailed(event)`: Engagement creation failed.
* `onUpdateEngagementSucceeded(event)`: Engagement updated successfully.
* `onUpdateEngagementFailed(event)`: Engagement update failed.
* `onVisibilityChanged(data)`: Widget visibility changed. Data includes `isMinimized` and `isHidden`.
* `defaultEventHandler(event)`: Catches any unhandled events.


### Calling Settings Endpoint (API)

Use this endpoint to configure your app's settings:

`POST/PATCH/GET/DELETE https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Payload:**

```json
{
  "name": "Your App Name",
  "url": "Your App URL",
  "width": 400,
  "height": 600,
  "isReady": false, // Set to true for production
  "supportsCustomObjects": true // Optional: Indicates whether your app supports calls from custom objects.
}
```

### LocalStorage Override (for testing)

You can override settings for testing:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'My Local URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


### Production Readiness

Set `isReady` to `true` in the settings API when ready for production.


### Publishing to Marketplace

Publish your app to the HubSpot marketplace once ready.


## Frequently Asked Questions (FAQ)

* **Authentication:** Your app handles authentication.
* **CDN Hosting:** Yes, the SDK is hosted on jsDeliver.
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them.  For calls initiated outside HubSpot, your app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:** You can add this functionality to existing marketplace apps.
* **Softphone Integration:** Easily integrate existing softphone applications.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free Users:** Free users can install the app.
* **Automatic App Appearance:** Yes, for existing app users.
* **Install/Uninstall Permissions:** Only users with appropriate permissions can install/uninstall.
* **Custom Calling Properties:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, if using the SDK and setting `createEngagement: true` in `outgoingCall`.


This documentation provides a comprehensive guide to using the HubSpot Calling Extensions SDK.  Refer to the HubSpot developer portal for further details and support.
