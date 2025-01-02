# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, enabling custom calling options within the HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between your calling application and HubSpot.  It consists of three key parts:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication between your app and HubSpot.  Installed via npm or yarn.
2. **Calling Settings Endpoints (API):**  Used to configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:** The iframe where your app is displayed to HubSpot users. Configured via the calling settings endpoints.

**Note:** Only outgoing calls are currently supported.

## Getting Started

### 1. Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS.  SDK instantiation in `index.js`.
* **`demo-react-ts`:**  More realistic implementation using React, TypeScript, and Styled Components. SDK instantiation in `useCti.ts`.

**Note:** Demo apps use mock data.

### 2. Installing Demo Apps

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo app directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`.  You might need to bypass a security warning.

### 3. Launching Demo Apps from HubSpot

1. Navigate to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Set `localStorage` value:
   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".

### 4. Installing the SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses events for communication:

### Events

**HubSpot sends:**

* `onReady`: HubSpot is ready.
* `onDialNumber`: Outbound call initiated.
* `onCreateEngagementSucceeded`: Engagement successfully created.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement successfully updated.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed.
* `onNavigateToRecordFailed`: Navigation to record failed.
* `onPublishToChannelSucceeded`: Publishing to channel succeeded.
* `onPublishToChannelFailed`: Publishing to channel failed.
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.

**Your app sends:**

* `initialized`: Softphone ready.
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started.
* `callAnswered`: Call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`: Error encountered.
* `resizeWidget`: Resize request.


### SDK API

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);

// Example: Sending an outgoing call event
extensions.outgoingCall({
  toNumber: "+15551234567",
  fromNumber: "+15559876543",
  createEngagement: true, // Tells HubSpot to create an engagement
  callStartTime: Date.now()
});
```

### Calling Settings Endpoint (API)

Use the API to configure your app's settings.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.

**POST/PATCH:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Request Body (JSON):**

```json
{
  "name": "My App",
  "url": "https://myapp.com",
  "width": 400,
  "height": 600,
  "isReady": false // Set to true for production
  "supportsCustomObjects": true //Indicates if calls can be placed from custom objects
}
```

**GET/DELETE:** Same endpoint, but use appropriate HTTP method.


### Overriding Settings with localStorage

For testing, override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production

Set `isReady` to `true` in the API settings to make your app available to users.  Publish your app to the HubSpot marketplace.


## Frequently Asked Questions

Refer to the original text for the FAQ section.


This Markdown documentation provides a more structured and easily navigable guide to the HubSpot Calling Extensions SDK.  Remember to consult the original text and HubSpot's official documentation for the most up-to-date information.
