# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The HubSpot Calling Extensions SDK allows developers to provide a custom calling experience directly from CRM records within HubSpot.  It consists of three key components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between the app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure the calling settings for each connected HubSpot account.
3. **Calling iframe:** The interface displayed to HubSpot users, configured via the settings endpoints.


**Note:** Currently, only outgoing calls are supported.

## Getting Started

### 1. Run the Demo Apps

Two demo apps are available to test the SDK:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  SDK instantiation is in `index.js`.
* **`demo-react-ts`:** A more robust example using React, TypeScript, and Styled Components. SDK instantiation is in `useCti.ts`.

**Note:** These demos use mock data.

**Installation:**

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app directory (`demos/demo-minimal-js` or `demos/demo-react-ts`).
4. Run `npm i && npm start`.  This opens the app at `https://localhost:9025/`. You might need to bypass a security warning.


### 2. Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands in the console, depending on which demo app you are using:

    * **`demo-minimal-js` (installed):**  `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **`demo-react-ts` (installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
    * **`demo-minimal-js` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`


4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### 3. Install the SDK

Add the SDK to your project using npm or yarn:

**npm:** `npm i --save @hubspot/calling-extensions-sdk`
**yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends events, and your app responds.


### API

The `CallingExtensions` object provides methods to interact with HubSpot:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Outbound call initiated */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created */ },
    // ... other event handlers (see Events section)
  }
};

const extensions = new CallingExtensions(options);
```

### Events

#### Sending Messages to HubSpot

* **`initialized(payload)`:**  Notifies HubSpot that the softphone is ready.  `payload` includes `isLoggedIn` (boolean) and `engagementId` (number).
* **`userLoggedIn()`:**  Notifies HubSpot of user login.
* **`userLoggedOut()`:** Notifies HubSpot of user logout.
* **`outgoingCall(callInfo)`:** Notifies HubSpot of an outgoing call. `callInfo` includes `callStartTime` (number, milliseconds), `createEngagement` (boolean), `toNumber` (string), and `fromNumber` (string).  `phoneNumber` (string) is deprecated, use `toNumber`.
* **`callAnswered(payload)`:** Notifies HubSpot that a call was answered. `payload` includes `externalCallId` (string).
* **`callEnded(payload)`:** Notifies HubSpot that a call ended. `payload` includes `externalCallID` (string), `engagementId` (number), and `callEndStatus` (enumeration).
* **`callCompleted(data)`:** Notifies HubSpot that the call is completed. `data` includes `engagementId`, `hideWidget` (boolean), `engagementProperties` (object), and `externalCallId`.
* **`sendError(data)`:** Reports an error to HubSpot.  `data` includes `message` (string).
* **`resizeWidget(data)`:** Requests a widget resize. `data` includes `height` and `width` (numbers).


#### Receiving Messages from HubSpot

* **`onReady(data)`:** HubSpot is ready. `data` includes `engagementId`, `iframeLocation`, `ownerId`, `portalId`, and `userId`.
* **`onDialNumber(data)`:** Outbound call initiated.  `data` includes `phoneNumber`, `ownerId`, `subjectId`, `objectId`, `objectType`, `portalId`, `countryCode`, `calleeInfo`, `startTimestamp`, and `toPhoneNumberSrc`.
* **`onEngagementCreated(data)`:** (Deprecated) Engagement created. Use `onCreateEngagementSucceeded` instead. `data` includes `engagementId`.
* **`onNavigateToRecordFailed(data)`:** Navigation to a record failed. `data` includes `engagementId` and `objectCoordinates`.
* **`onPublishToChannelSucceeded(data)`:** Publishing to a channel succeeded. `data` includes `engagementId` and `externalCallId`.
* **`onPublishToChannelFailed(data)`:** Publishing to a channel failed. `data` includes `engagementId` and `externalCallId`.
* **`onCallerIdMatchSucceeded(event)`:** Caller ID match successful.
* **`onCallerIdMatchFailed(event)`:** Caller ID match failed.
* **`onCreateEngagementSucceeded(event)`:** Engagement creation successful.
* **`onCreateEngagementFailed(event)`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded(event)`:** Engagement update successful.
* **`onUpdateEngagementFailed(event)`:** Engagement update failed.
* **`onVisibilityChanged(data)`:** Widget visibility changed.  `data` includes `isMinimized` and `isHidden` (booleans).
* **`defaultEventHandler(event)`:** A catch-all handler for unhandled events.


### Calling Settings Endpoint (API)

Use this API endpoint to configure your app's settings for each HubSpot account.  The endpoint supports POST, PATCH, GET, and DELETE.

**URL:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Payload (Example):**

```json
{
  "name": "My App",
  "url": "https://my-app.com/widget",
  "height": 600,
  "width": 400,
  "isReady": false, // Set to true for production
  "supportsCustomObjects": true
}
```

Replace `APP_ID` with your app's ID and `DEVELOPER_ACCOUNT_API_KEY` with your developer API key.  The `isReady` flag indicates production readiness.


### Overriding Settings with localStorage

For testing, you can override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production

1. Set `isReady` to `true` in your app settings using the API.
2. Publish your app to the HubSpot Marketplace.


## FAQ

Refer to the original document for the frequently asked questions section.


This markdown documentation provides a structured and clearer representation of the provided text, enhancing readability and understanding of the HubSpot Calling Extensions SDK.  Remember to replace placeholder values (like `APP_ID` and API keys) with your actual values.
