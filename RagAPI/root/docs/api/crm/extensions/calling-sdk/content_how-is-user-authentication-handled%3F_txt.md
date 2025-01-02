# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into HubSpot.

## Overview

The Calling Extensions SDK facilitates communication between a calling app and HubSpot, providing a custom calling experience directly from CRM records.  It consists of three main components:

1. **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Used to configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:** Displays your app to HubSpot users; configured via the settings endpoints.

**Note:** Only outgoing calls are currently supported.


## Getting Started

### 1. Install the Demo App (Optional)

Two demo apps are available for testing: `demo-minimal-js` (JavaScript) and `demo-react-ts` (React/TypeScript).  To install:

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app directory:
   - `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   - `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
4. Access the app at `https://localhost:9025/` (you may need to bypass a security warning).

**Note:** Demo apps use mock data and are not fully functional calling apps.

### 2. Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Set the `localStorage` item:
   - **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   - **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   - **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.  The demo app should appear in the call switcher.


### 3. Install the Calling Extensions SDK

Add the SDK as a dependency to your project:

**npm:** `npm i --save @hubspot/calling-extensions-sdk`

**yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends events; your app responds via event handlers.

### API Reference

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Outbound call initiated */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

### Events

#### Sending Messages to HubSpot

* **`initialized(payload)`:** Notifies HubSpot the app is ready.  `payload: { isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn()`:**  User logged into the app.
* **`userLoggedOut()`:** User logged out of the app.
* **`outgoingCall(callInfo)`:** Outgoing call started. `callInfo: { phoneNumber: string (deprecated, use toNumber), callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered()`:** Outgoing call answered. `payload: {externalCallId: string}`
* **`callEnded(payload)`:** Outgoing call ended. `payload: { externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted(data)`:** Outgoing call completed. `data: { engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError(data)`:** Error occurred. `data: { message: string }`
* **`resizeWidget(data)`:** Resize the widget. `data: { height: number, width: number }`

#### Receiving Messages from HubSpot

* **`onReady(data)`:** HubSpot is ready. `data: { engagementId: number, iframeLocation: Enum, ownerId: String | Number, portalId: Number, userId: Number }`
* **`onDialNumber(data)`:** Outbound call initiated from HubSpot.  (See detailed data properties in original text)
* **`onEngagementCreated(data)`:** (Deprecated) Engagement created. `data: { engagementId: number }`
* **`onCreateEngagementSucceeded(event)`:** Engagement created successfully.
* **`onCreateEngagementFailed(event)`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded(event)`:** Engagement updated successfully.
* **`onUpdateEngagementFailed(event)`:** Engagement update failed.
* **`onNavigateToRecordFailed(data)`:** Navigation to record failed. `data: { engagementId: number, objectCoordinates: object }`
* **`onPublishToChannelSucceeded(data)`:** Publishing to channel succeeded. `data: { engagementId: number, externalCallId: string }`
* **`onPublishToChannelFailed(data)`:** Publishing to channel failed. `data: { engagementId: number, externalCallId: string }`
* **`onCallerIdMatchSucceeded(event)`:** Caller ID match succeeded.
* **`onCallerIdMatchFailed(event)`:** Caller ID match failed.
* **`onVisibilityChanged(data)`:** Widget visibility changed. `data: { isMinimized: boolean, isHidden: boolean }`
* **`defaultEventHandler(event)`:** Default event handler.


## Calling Settings Endpoint (API)

Use this API endpoint to configure your app's settings:

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

* `APP_ID`: Your app's ID.
* `DEVELOPER_ACCOUNT_API_KEY`: Your developer API key.
* `isReady`:  `true` for production, `false` for testing.  This endpoint also supports `PATCH`, `GET`, and `DELETE`.


## Overriding Settings with localStorage

For testing, you can override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Frequently Asked Questions (FAQ)

Refer to the original text for the comprehensive FAQ section.


##  Publishing to the HubSpot Marketplace

Once your app is ready, publish it to the HubSpot Marketplace (details in original text).


This markdown documentation provides a structured and comprehensive overview of the HubSpot Calling Extensions SDK, including API calls, event handling, and troubleshooting.  Remember to consult the original text for more detailed information and specific examples.
