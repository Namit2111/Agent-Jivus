# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into HubSpot.

## Overview

The Calling Extensions SDK enables apps to provide a custom calling option to HubSpot users directly from CRM records.  It consists of three parts:

1. **The SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:**  Your app's user interface, displayed within HubSpot.

**Note:** Only outgoing calls are currently supported.


## Getting Started

### 1. Install the Demo App (Optional):

This allows you to test the SDK before integrating it into your application.

**Prerequisites:** Node.js

1. Clone the demo repository (link provided in original text, omitted here).
2. Navigate to the demo directory (`cd demos/demo-minimal-js` or `cd demos/demo-react-ts`).
3. Install dependencies: `npm i`
4. Start the app: `npm start` (opens in browser at `https://localhost:9025/`)


### 2. Launch the Demo App from HubSpot:

1. Go to your HubSpot contacts or companies.
2. Open your browser's developer console.
3. Set the appropriate localStorage item:

   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **demo-minimal-js (Uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **demo-react-ts (Uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.  The demo app should appear in the call switcher.


### 3. Install the SDK in your App:

Use npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends events, and your app responds using event handlers.

###  API Reference

**`CallingExtensions(options)`:** Creates a new `CallingExtensions` instance.

**`options` object:**

* `debugMode: boolean` - Enables/disables verbose logging.

* `eventHandlers: object` - Defines how your app handles HubSpot events.  See the "Events" section for details on available events and their payloads.  Example:

```javascript
const options = {
  debugMode: true,
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  }
};
const extensions = new CallingExtensions(options);
```

**Methods to send messages to HubSpot:**

* **`extensions.initialized(payload)`:**  Notifies HubSpot that your app is ready.  `payload` includes `isLoggedIn: boolean` and `engagementId: number`.

* **`extensions.userLoggedIn()`:** Notifies HubSpot of user login.

* **`extensions.userLoggedOut()`:** Notifies HubSpot of user logout.

* **`extensions.outgoingCall(callInfo)`:** Notifies HubSpot of an outgoing call.  `callInfo` includes: `toNumber: string` (required), `fromNumber: string` (required), `callStartTime: number`, `createEngagement: boolean`.

* **`extensions.callAnswered(payload)`:**  Notifies HubSpot that a call was answered.  `payload` includes `externalCallId: string`.

* **`extensions.callEnded(payload)`:** Notifies HubSpot that a call ended.  `payload` includes `externalCallId: string`, `engagementId: number`, `callEndStatus: EndStatus` (enumeration).

* **`extensions.callCompleted(data)`:** Notifies HubSpot that a call is completed. `data` includes `engagementId: number`, `hideWidget: boolean`, `engagementProperties: object`, `externalCallId: number`.

* **`extensions.sendError(data)`:** Reports an error to HubSpot. `data` includes `message: string`.

* **`extensions.resizeWidget(data)`:** Requests a widget resize.  `data` includes `height: number`, `width: number`.


### Events Received from HubSpot

* **`onReady()`:** HubSpot is ready to receive messages.  Provides `engagementId`, `iframeLocation`, `ownerId`, `portalId`, and `userId`.

* **`onDialNumber(data)`:**  A user initiated an outbound call. `data` includes phone number, owner ID, subject ID, object ID, object type, portal ID, country code, callee info, start timestamp, and `toPhoneNumberSrc`.

* **`onEngagementCreated(data)`:** (Deprecated – use `onCreateEngagementSucceeded` instead). Provides `engagementId`.

* **`onNavigateToRecordFailed(data)`:** Navigation to a record failed. Provides `engagementId` and `objectCoordinates`.

* **`onPublishToChannelSucceeded(data)`:** Publishing to a channel succeeded. Provides `engagementId` and `externalCallId`.

* **`onPublishToChannelFailed(data)`:** Publishing to a channel failed. Provides `engagementId` and `externalCallId`.

* **`onCallerIdMatchSucceeded(event)`:** Caller ID match succeeded.

* **`onCallerIdMatchFailed(event)`:** Caller ID match failed.

* **`onCreateEngagementSucceeded(event)`:** Engagement creation succeeded.

* **`onCreateEngagementFailed(event)`:** Engagement creation failed.

* **`onUpdateEngagementSucceeded(event)`:** Engagement update succeeded.

* **`onUpdateEngagementFailed(event)`:** Engagement update failed.

* **`onVisibilityChanged(data)`:** Widget visibility changed.  `data` includes `isMinimized` and `isHidden`.

* **`defaultEventHandler(event)`:** Catches any unhandled events.


## Calling Settings Endpoint (API)

Use this API to configure your app's settings for each HubSpot account.

**Endpoint:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`

**Methods:** POST, PATCH, GET, DELETE

**Payload (example):**

```json
{
  "name": "My App",
  "url": "https://myapp.com/widget",
  "height": 600,
  "width": 400,
  "isReady": false, // Set to true for production
  "supportsCustomObjects": true
}
```

**Note:** `isReady: false` during testing.  Set to `true` for production.


## Overriding Settings with localStorage (for testing)

You can temporarily override settings using localStorage:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Frequently Asked Questions (FAQ)

Refer to the original text for the FAQ section.  It covers authentication, CDN hosting, engagement creation vs. updates, required scopes, integrating with existing apps, multiple integrations, free user access, automatic updates, user permissions, custom properties, and calling from custom objects.


## Publishing to the HubSpot Marketplace

Once ready, publish your app to the HubSpot Marketplace (details in the original text).


This documentation provides a comprehensive overview of the HubSpot Calling Extensions SDK.  Remember to consult the original text for specific details, links, and code snippets that were omitted for brevity.
