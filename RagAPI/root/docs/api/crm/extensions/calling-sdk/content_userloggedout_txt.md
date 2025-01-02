# HubSpot Calling Extensions SDK Documentation

## Overview

The HubSpot Calling Extensions SDK allows developers to integrate custom calling functionality into HubSpot.  This enables users to make calls directly from HubSpot records (Contacts, Companies, and potentially custom objects) using a third-party calling application.  The SDK facilitates communication between your calling application and HubSpot, handling call engagement creation and updates.

**Key Components:**

* **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication between your app and HubSpot.  This SDK is installed as a Node.js dependency (`@hubspot/calling-extensions-sdk`).
* **Calling Settings Endpoints (API):** Used to configure your calling app's settings within each HubSpot account that integrates with it.  These settings control aspects like the app's name, URL, dimensions, and readiness for production.
* **Calling iFrame:**  The iframe where your calling app's UI appears to the HubSpot user.  Configured using the calling settings endpoints.

**Important Notes:**

* Currently, only outgoing calls are supported.
* HubSpot handles call engagement creation and updates automatically; manual management is no longer required.


## Getting Started

### 1. Demo Apps

Two demo apps are available to test the SDK:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  SDK instantiation is in `index.js`.
* **`demo-react-ts`:** A more comprehensive implementation using React, TypeScript, and Styled Components. SDK instantiation is in `useCti.ts`.

**Installation (for either demo app):**

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app's directory (`demos/demo-minimal-js` or `demos/demo-react-ts`).
4. Run `npm i && npm start`.  This will open the app at `https://localhost:9025/`. You might need to bypass a security warning.


### 2. Launching the Demo App from HubSpot

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Run one of the following commands based on which demo and installation method was used:


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


### 3. Installing the SDK in Your App

Use npm or yarn:

**npm:**

```bash
npm i --save @hubspot/calling-extensions-sdk
```

**yarn:**

```bash
yarn add @hubspot/calling-extensions-sdk
```

## Using the SDK

### API

The SDK uses events for communication.

**Sending Messages to HubSpot:**

The `extensions` object exposes methods to send messages:

* `initialized(payload)`:  Indicates the softphone is ready.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`.
* `userLoggedIn()`: User logged in.
* `userLoggedOut()`: User logged out.
* `outgoingCall(callInfo)`: Outgoing call started. `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`.  `phoneNumber` is deprecated; use `toNumber`.
* `callAnswered(payload)`: Call answered. `payload`: `{ externalCallId: string }`.
* `callEnded(payload)`: Call ended. `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`.  `callEndStatus` is an enum (e.g., `INTERNAL_COMPLETED`, `INTERNAL_FAILED`).
* `callCompleted(data)`: Call completed. `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`.
* `sendError(data)`: Error occurred. `data`: `{ message: string }`.
* `resizeWidget(data)`: Resize the widget. `data`: `{ height: number, width: number }`.

**Receiving Messages from HubSpot:**

Event handlers receive messages from HubSpot:

* `onReady(data)`: HubSpot is ready.  `data` includes `engagementId`, `iframeLocation`, `ownerId`, `portalId`, and `userId`.
* `onDialNumber(data)`: Outbound call triggered. `data` includes phone number, owner ID, subject ID, object ID, object type, portal ID, country code, callee info, start timestamp, and `toPhoneNumberSrc`.
* `onEngagementCreated(data)`: (Deprecated) Engagement created. Use `onCreateEngagementSucceeded` instead.
* `onNavigateToRecordFailed(data)`: Navigation to a record failed.
* `onPublishToChannelSucceeded(data)`: Publishing to a channel succeeded.
* `onPublishToChannelFailed(data)`: Publishing to a channel failed.
* `onCallerIdMatchSucceeded(event)`: Caller ID match succeeded.
* `onCallerIdMatchFailed(event)`: Caller ID match failed.
* `onCreateEngagementSucceeded(event)`: Engagement creation succeeded.
* `onCreateEngagementFailed(event)`: Engagement creation failed.
* `onUpdateEngagementSucceeded(event)`: Engagement update succeeded.
* `onUpdateEngagementFailed(event)`: Engagement update failed.
* `onVisibilityChanged(data)`: Widget visibility changed.
* `defaultEventHandler(event)`: Default event handler.


### Example (SDK Instantiation):

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true,
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: event => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```


## Calling Settings Endpoints (API)

Use the API to manage your app's settings:

* **URL:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`
* **Methods:** POST (create), PATCH (update), GET (retrieve), DELETE (delete).
* **Payload (Example):**

```json
{
  "name": "My Calling App",
  "url": "https://my-app.com/widget",
  "height": 600,
  "width": 400,
  "isReady": false, // Set to true for production
  "supportsCustomObjects": true
}
```

Use `curl` or your preferred API client.  Remember to replace `{APP_ID}` and `{DEVELOPER_ACCOUNT_API_KEY}` with your actual values.


## Overriding Settings with localStorage

For testing, override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'my-local-url'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production and Marketplace

To prepare for production, set `isReady` to `true` in your API settings.  Finally, publish your app to the HubSpot marketplace (if desired).


## Frequently Asked Questions (FAQ)

Refer to the original document for the FAQ section.


This markdown documentation provides a more structured and concise overview of the HubSpot Calling Extensions SDK.  Remember to consult the original document for details not explicitly covered here.
