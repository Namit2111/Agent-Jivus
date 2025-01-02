# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot's CRM.

## Overview

The Calling Extensions SDK facilitates communication between a calling app and HubSpot, providing users with a custom calling experience directly from CRM records.  It consists of three core components:

1. **Calling Extensions SDK (JavaScript):**  Enables communication between your app and HubSpot.  This is the primary component you'll interact with.
2. **Calling Settings Endpoints (API):** Used to configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:**  The visual interface displayed to HubSpot users, customized via the calling settings endpoints.

**Note:** Only outgoing calls are currently supported.

## Getting Started

### 1. Install the Demo App (Optional):

You can test the SDK using two demo apps: `demo-minimal-js` (JavaScript, HTML, CSS) and `demo-react-ts` (React, TypeScript, Styled Components).

**Prerequisites:** Node.js

**Installation:**

1. Clone the repository (link to repository needed here).
2. Navigate to the demo app's directory:
   - `cd demos/demo-minimal-js` (for `demo-minimal-js`)
   - `cd demos/demo-react-ts` (for `demo-react-ts`)
3. Install dependencies: `npm i`
4. Start the app: `npm start` (opens at `https://localhost:9025/`)

**Note:** You might need to bypass a security warning to access the application.

### 2. Launch the Demo App from HubSpot:

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Set the `localStorage` item:

   - **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   - **`demo-minimal-js` (no installation):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   - **`demo-react-ts` (no installation):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.
5. Select the demo app from the "Call from" dropdown in the call switcher.

### 3. Install the Calling Extensions SDK:

Add the SDK to your project using npm or yarn:

**npm:** `npm i --save @hubspot/calling-extensions-sdk`
**yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends events to your app, and your app sends events back to HubSpot.

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
    // ... other event handlers
    defaultEventHandler: (event) => { /* Handle any unhandled events */ }
  }
};

const extensions = new CallingExtensions(options);
```

### Events

**Outbound Events (Sent from your app to HubSpot):**

* `initialized`: Notifies HubSpot that your app is ready.  Requires a payload with `isLoggedIn` (boolean) and `engagementId` (number).
* `userLoggedIn`: Notifies HubSpot that the user has logged in.
* `userLoggedOut`: Notifies HubSpot that the user has logged out.
* `outgoingCall`: Notifies HubSpot of an outgoing call.  Requires a payload with `toNumber`, `fromNumber`, `callStartTime`, and `createEngagement` (boolean).  `phoneNumber` is deprecated in favor of `toNumber`.
* `callAnswered`: Notifies HubSpot that the call has been answered. Requires an `externalCallId`.
* `callEnded`: Notifies HubSpot that the call has ended. Requires `externalCallID`, `engagementId`, and `callEndStatus` (enum).
* `callCompleted`: Notifies HubSpot that the call is complete. Requires `engagementId`, `hideWidget` (boolean), `engagementProperties` (object), and `externalCallId`.
* `sendError`: Notifies HubSpot of an error. Requires an error `message`.
* `resizeWidget`: Requests a resize of the call widget. Requires `height` and `width`.


**Inbound Events (Sent from HubSpot to your app):**

* `onReady`: HubSpot is ready to receive messages. Provides `engagementId`, `iframeLocation`, `ownerId`, `portalId`, and `userId`.
* `onDialNumber`: A user initiated an outbound call. Provides `phoneNumber`, `ownerId`, `subjectId`, `objectId`, `objectType`, `portalId`, `countryCode`, `calleeInfo`, `startTimestamp`, and `toPhoneNumberSrc`.
* `onEngagementCreated`: (Deprecated)  Use `onCreateEngagementSucceeded` instead.
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publishing to a channel succeeded/failed.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match succeeded/failed.
* `onCreateEngagementSucceeded`/`onCreateEngagementFailed`: Engagement creation succeeded/failed.
* `onUpdateEngagementSucceeded`/`onUpdateEngagementFailed`: Engagement update succeeded/failed.
* `onVisibilityChanged`: Widget visibility changed (minimized/hidden). Provides `isMinimized` and `isHidden`.
* `defaultEventHandler`: Catches any unhandled events.

### Calling Settings Endpoint (API)

This API allows you to configure your app's settings.  Use `APP_ID` and your `DEVELOPER_ACCOUNT_API_KEY`.

**Endpoint:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`

**Methods:** POST, PATCH, GET, DELETE

**Example Payload (POST):**

```json
{
  "name": "My App",
  "url": "https://myapp.com",
  "height": 600,
  "width": 400,
  "isReady": false, // Set to true for production
  "supportsCustomObjects": true
}
```

### Overriding Settings with localStorage (For Testing):

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production Deployment

1. Set `isReady` to `true` in the calling settings API.
2. Publish your app to the HubSpot marketplace (link to marketplace instructions needed here).


## Frequently Asked Questions

**(Refer to the original document for FAQ answers.)**


This markdown documentation provides a more structured and readable format compared to the original text, including clear section headings, code blocks, and tables where applicable. Remember to replace placeholder links with actual links to relevant resources.
