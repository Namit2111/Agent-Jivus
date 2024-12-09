# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling functionalities into their HubSpot apps.

## Overview

The Calling Extensions SDK allows apps to offer custom calling options directly from CRM records within HubSpot.  It consists of three main components:

* **Calling Extensions SDK (JavaScript):**  Facilitates communication between your app and HubSpot.
* **Calling Settings Endpoints:** Configure calling settings for each connected HubSpot account.
* **Calling iFrame:**  Displays your app to HubSpot users; configured via the calling settings endpoints.

For detailed information on the in-app calling experience, refer to [this knowledge base article](link-to-knowledge-base-article).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.

## Getting Started

### Prerequisites

* A HubSpot developer account ([sign up here](link-to-signup)).
* If you don't have an app, [create one from your HubSpot developer account](link-to-developer-account).
* Node.js installed on your development environment.

### Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS.  SDK instantiation is shown in `index.js`.
* **`demo-react-ts`:** Real-world implementation using React, TypeScript, and Styled Components. SDK instantiation is in `useCti.ts`.

**Note:** These demos use mock data and are not fully functional calling apps.


### Installing the Demo App

1. Clone or download the demo app repository (link-to-repository).
2. Navigate to the demo app's directory (`demos/demo-minimal-js` or `demos/demo-react-ts`).
3. Run `npm i && npm start`.  This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launching the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following `localStorage` commands, depending on which demo and installation method you chose:

    * **`demo-minimal-js` (installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **`demo-react-ts` (installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **`demo-minimal-js` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **`demo-react-ts` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.
5. Click the "Call" icon, select the demo app from the "Call from" dropdown, and click "Call".


### Installing the Calling Extensions SDK

Use npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends messages (events), and your app responds via event handlers.

### Events

**Sent to HubSpot:**

* `initialized`:  Softphone ready.
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started.
* `callAnswered`: Outgoing call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`: App error.
* `resizeWidget`: Resize request.


**Received from HubSpot:**

* `onReady`: HubSpot ready.
* `onDialNumber`: Outbound call initiated.
* `onEngagementCreated`: (Deprecated - use `onCreateEngagementSucceeded`) Engagement created.
* `onNavigateToRecordFailed`: Navigation to record failed.
* `onPublishToChannelSucceeded`: Publishing to channel succeeded.
* `onPublishToChannelFailed`: Publishing to channel failed.
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement created successfully.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement updated successfully.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Default event handler.


### SDK Initialization and Event Handlers

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, //Optional
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Sending Messages to HubSpot (Example: `outgoingCall`)

```javascript
const callInfo = {
  toNumber: '+15551234567',
  fromNumber: '+15559876543',
  createEngagement: true,
  callStartTime: Date.now()
};
extensions.outgoingCall(callInfo);
```

See the detailed descriptions of each event for the required parameters.

### Calling Settings Endpoint

Use this API endpoint (e.g., with `curl` or Postman) to configure your app's settings:

```bash
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"My App","url":"https://myapp.com","height":600,"width":400,"isReady":false}'
```

Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your app's ID and API key.  The `isReady` flag should be `false` during testing and `true` for production.  Use PATCH to update settings.

### LocalStorage Override (for testing)

You can override settings in the browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'my-local-url'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production Readiness

Once testing is complete, set `isReady` to `true` via the settings endpoint.

### Publishing to the Marketplace

After setup, publish your app to the HubSpot marketplace ([details here](link-to-marketplace-details)).

## Frequently Asked Questions

See the included FAQ section in the original document.


This markdown documentation provides a structured and easily readable version of the provided text, improving its organization and accessibility.  Remember to replace the bracketed placeholders (`[]`) with the actual links.
