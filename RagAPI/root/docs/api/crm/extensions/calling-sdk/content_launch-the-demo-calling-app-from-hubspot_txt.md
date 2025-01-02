# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot CRM records.

## Overview

The Calling Extensions SDK facilitates communication between a calling application and HubSpot.  It consists of three parts:

1. **The SDK (JavaScript):** Enables message exchange between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:** Your app's interface within HubSpot, configured via the settings endpoints.

**Note:** Only outgoing calls are currently supported.


## Getting Started

### 1. Install the Demo App (Optional):

You can test the SDK with two demo apps: `demo-minimal-js` (JavaScript, HTML, CSS) and `demo-react-ts` (React, TypeScript).

**Prerequisites:** Node.js and npm (or yarn)

**Installation:**

1. Clone the repository.
2. Navigate to the demo app directory (`cd demos/demo-minimal-js` or `cd demos/demo-react-ts`).
3. Run `npm install` (or `yarn add`).
4. Run `npm start` (or `yarn start`).  This opens the app at `https://localhost:9025/`.  You may need to bypass a security warning.


### 2. Launch the Demo App from HubSpot:

1. Go to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Set the appropriate `localStorage` item:

   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.  The demo app should appear in the call switcher.


### 3. Install the SDK in your App:

Use npm or yarn:

```bash
# npm
npm i --save @hubspot/calling-extensions-sdk

# yarn
yarn add @hubspot/calling-extensions-sdk
```

## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends events to your app, and your app sends events to HubSpot.

### API Reference:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // optional: log debug messages
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

### Events:

**From HubSpot:**

* `onReady`: HubSpot is ready.  Provides `engagementId`, `iframeLocation`, `ownerId`, `portalId`, `userId`.
* `onDialNumber`:  Outbound call initiated. Provides `phoneNumber`, `ownerId`, `subjectId`, `objectId`, `objectType`, `portalId`, `countryCode`, `calleeInfo`, `startTimestamp`, `toPhoneNumberSrc`.
* `onCreateEngagementSucceeded`: Engagement successfully created.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement successfully updated.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed (minimized/hidden).
* `onNavigateToRecordFailed`: Navigating to a record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publishing to a channel succeeded/failed.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match succeeded/failed.


**To HubSpot:**

* `initialized`: Softphone ready.  Requires `{ isLoggedIn: boolean, engagementId: number }`.
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started.  Requires `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`.
* `callAnswered`: Call answered.  Requires `{ externalCallId: string }`.
* `callEnded`: Call ended. Requires `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`.  `callEndStatus` is an enum (INTERNAL_COMPLETED, INTERNAL_FAILED, etc.).
* `callCompleted`: Call completed.  Requires `{ engagementId: number, hideWidget: boolean, engagementProperties: object, externalCallId: number }`.
* `sendError`:  Error occurred.  Requires `{ message: string }`.
* `resizeWidget`: Resize the widget.  Requires `{ height: number, width: number }`.


## Calling Settings Endpoint (API)

Use this API to configure your app's settings for each HubSpot account:

**Endpoint:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`

**Methods:** POST (create), PATCH (update), GET (retrieve), DELETE (delete).

**Request Body (example):**

```json
{
  "name": "My Calling App",
  "url": "https://my-calling-app.com",
  "height": 600,
  "width": 400,
  "isReady": false // Set to true for production
}
```

**Note:** The `isReady` flag indicates production readiness.  Set it to `false` during development.


## Overriding Settings with localStorage

For testing, you can override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production Deployment

1. Set `isReady` to `true` via the API.
2. Publish your app to the HubSpot Marketplace (optional).


## Frequently Asked Questions

Refer to the original document for FAQs on authentication, CDN hosting, engagement creation/updates, required scopes, and other common questions.


This Markdown documentation provides a concise and structured overview of the HubSpot Calling Extensions SDK.  Remember to consult the original document for complete details and the most up-to-date information.
