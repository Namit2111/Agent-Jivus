# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK facilitates communication between a calling app and HubSpot, providing a custom calling experience directly from CRM records.  It comprises three main components:

1. **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure calling settings for each connected HubSpot account.
3. **Calling iFrame:** The app's user interface within HubSpot, configured via the settings endpoints.

**Note:** Only outgoing calls are currently supported.


## Getting Started

### 1. Run the Demo App

Two demo apps are available:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS (see `index.js` for SDK instantiation).
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components (see `useCti.ts` for SDK instantiation).

**Note:** Demo apps use mock data and aren't fully functional calling apps.

### 2. Install the Demo App (Optional)

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
4. Access the app at `https://localhost:9025/` (may require bypassing a security warning).

### 3. Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Set the `localStorage` item:
   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page and select the demo app from the call switcher.

### 4. Install the SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends messages (events) to the app, and the app responds using SDK methods.

### SDK API

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
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

### Events

#### Sending Messages to HubSpot

* **`initialized(payload)`:**  Notifies HubSpot the app is ready.  `payload` includes `isLoggedIn` (boolean) and `engagementId` (number).
* **`userLoggedIn()`:** Notifies HubSpot of user login (only needed if not logged in during `initialized`).
* **`userLoggedOut()`:** Notifies HubSpot of user logout.
* **`outgoingCall(callInfo)`:** Notifies HubSpot of an outgoing call. `callInfo` includes `callStartTime` (number, milliseconds), `createEngagement` (boolean), `toNumber` (string), and `fromNumber` (string).
* **`callAnswered(payload)`:** Notifies HubSpot the call was answered. `payload` includes `externalCallId` (string).
* **`callEnded(payload)`:** Notifies HubSpot the call ended. `payload` includes `externalCallID` (string), `engagementId` (number), and `callEndStatus` (enum).
* **`callCompleted(data)`:** Notifies HubSpot the call is complete. `data` includes `engagementId`, `hideWidget` (boolean), `engagementProperties` (object), and `externalCallId`.
* **`sendError(data)`:** Reports an error to HubSpot. `data` includes `message` (string).
* **`resizeWidget(data)`:** Requests a widget resize. `data` includes `height` and `width` (numbers).


#### Receiving Messages from HubSpot

* **`onReady(data)`:** HubSpot is ready. `data` includes `engagementId`, `iframeLocation`, `ownerId`, `portalId`, and `userId`.
* **`onDialNumber(data)`:** Outbound call initiated.  `data` includes `phoneNumber`, `ownerId`, `subjectId`, `objectId`, `objectType`, `portalId`, `countryCode`, `calleeInfo`, `startTimestamp`, and `toPhoneNumberSrc`.
* **`onCreateEngagementSucceeded(event)`:** Engagement created successfully.
* **`onCreateEngagementFailed(event)`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded(event)`:** Engagement updated successfully.
* **`onUpdateEngagementFailed(event)`:** Engagement update failed.
* **`onVisibilityChanged(data)`:** Widget visibility changed. `data` includes `isMinimized` and `isHidden` (booleans).
* **`defaultEventHandler(event)`:**  Handles any unhandled events.


## Calling Settings Endpoint (API)

Use this API endpoint to manage your app's settings:

`https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`

* **Methods:** POST (create/update), PATCH (update), GET (retrieve), DELETE (delete).
* **Payload:**  `{ name: string, url: string, width: number, height: number, isReady: boolean, supportsCustomObjects: boolean }`
* **Example (curl):**

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"My App","url":"https://myapp.com","height":600,"width":400,"isReady":false,"supportsCustomObjects":true}'
```

## Local Storage Override (for testing)

You can override settings using browser's local storage:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'https://myapp.com',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

## Production Readiness

Set `isReady` to `true` in the settings endpoint to mark your app as production-ready.

## Publishing to the Marketplace

Once ready, publish your app to the HubSpot marketplace.


## Frequently Asked Questions (FAQ)

Refer to the original document for FAQs on authentication, CDN hosting, engagement creation/updates, required scopes, integrating existing apps, multiple integrations, free user access, automatic updates, user permissions, custom properties, and custom object calls.


This markdown documentation provides a structured overview of the HubSpot Calling Extensions SDK. Remember to consult the original document for complete details and the most up-to-date information.
