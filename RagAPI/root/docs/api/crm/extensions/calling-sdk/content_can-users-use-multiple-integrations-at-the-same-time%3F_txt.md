# HubSpot Calling Extensions SDK Documentation

This document provides comprehensive information on the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling functionalities within HubSpot CRM.

## Overview

The HubSpot Calling Extensions SDK allows developers to provide a custom calling option to HubSpot users directly from CRM records.  It consists of three key components:

1. **Calling Extensions SDK (JavaScript):**  Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):**  Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:** Your app's user interface, displayed to HubSpot users and configured via the settings endpoints.

**Note:** Only outgoing calls are currently supported.

## Getting Started

### 1. Demo Apps

Two demo applications are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS (see `index.js`).
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components (see `useCti.ts`).

**Note:** These demos use mock data.

### 2. Installing Demo Apps

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
4. Access the app at `https://localhost:9025/`.  You might need to bypass a security warning.

### 3. Launching Demo Apps from HubSpot

1. Navigate to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Set the `localStorage` item:
   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (Uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (Uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.
5. Select the demo app from the "Call from" dropdown in the call switcher.


## Installing the SDK

Use npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses events for communication:

**Events sent from HubSpot:**

* `onReady`: HubSpot is ready.
* `onDialNumber`: User initiates an outbound call.  Provides phone number, owner ID, object ID, object type (`CONTACT` or `COMPANY`), portal ID, country code, callee info, timestamp, and phone number source property.
* `onEngagementCreated`: (Deprecated - use `onCreateEngagementSucceeded`)  Engagement created.
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publish to channel success/failure.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match success/failure.
* `onUpdateEngagementSucceeded`/`onUpdateEngagementFailed`: Engagement update success/failure.
* `onVisibilityChanged`: Widget visibility changed.

**Events sent to HubSpot:**

* `initialized`: Softphone ready (includes `isLoggedIn` and `engagementId`).
* `userLoggedIn`/`userLoggedOut`: User login/logout status.
* `outgoingCall`: Outgoing call started (includes `callStartTime`, `createEngagement`, `toNumber`, `fromNumber`).
* `callAnswered`: Call answered (includes `externalCallId`).
* `callEnded`: Call ended (includes `externalCallID`, `engagementId`, `callEndStatus`).
* `callCompleted`: Call completed (includes `engagementId`, `hideWidget`, `engagementProperties`, `externalCallId`).
* `sendError`: Error occurred (includes `message`).
* `resizeWidget`: Resize widget (includes `height`, `width`).


### Example: SDK Initialization

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: enable debug logging
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```


## API Endpoints (Calling Settings)

Use the HubSpot API to manage your app's settings:

* **URL:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`
* **Methods:** `POST`, `PATCH`, `GET`, `DELETE`
* **Payload (Example):**

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

**Example using `curl`:**

```bash
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```


### Overriding Settings with localStorage (for testing)

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

## Production & Publishing

1. Set `isReady` to `true` using the API.
2. Publish your app to the HubSpot Marketplace (see HubSpot documentation for details).


## Frequently Asked Questions (FAQs)

* **Authentication:** Handled by the calling app.
* **CDN:** Yes, hosted on jsDeliver.  Example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; the app updates them.  For calls outside HubSpot, the app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:**  Can be updated to include this functionality.
* **Softphone Integration:** Easily integrable.
* **Multiple Integrations:** Supported.
* **Free Users:** Can install the app.
* **Automatic Appearance:** Yes, for existing app updates.
* **User Permissions:** Only permitted users can install/uninstall.
* **Custom Calling Properties:**  Createable via the properties API.
* **Custom Object Calls:** Supported if using the SDK and `outgoingCall({ createEngagement: true })`.


This documentation provides a comprehensive overview of the HubSpot Calling Extensions SDK. Refer to the HubSpot Developer documentation for further details and updates.
