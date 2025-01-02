# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between your application and HubSpot, enabling a custom calling experience directly from CRM records.  It consists of three core parts:

1. **Calling Extensions SDK (JavaScript):** A JavaScript SDK enabling communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):**  Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:**  The iframe where your app displays within HubSpot, configured using the settings endpoints.

**Note:** Only outgoing calls are currently supported.

## Getting Started

### 1. Run the Demo App

Two demo apps are available to test the SDK:

* **`demo-minimal-js`:**  A minimal JavaScript, HTML, and CSS implementation.  SDK instantiation is shown in `index.js`.
* **`demo-react-ts`:** A more realistic React, TypeScript, and Styled Components implementation. SDK instantiation is in `useCti.ts`.

**Note:** Demo apps use mock data and aren't fully functional calling applications.

### 2. Install the Demo App (Optional)

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app's directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
4. This will install dependencies and start the app at `https://localhost:9025/`.  You might need to bypass a security warning.

### 3. Launch the Demo App from HubSpot

1. Go to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Run one of the following commands in the console, depending on your installation method:
    * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.  Click the "Call" icon, select the demo app from the dropdown, and click "Call".

### 4. Install the SDK

Add the SDK as a dependency to your app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends messages (events) to your app, and your app responds with messages using specific methods.

### Events

**HubSpot sends these events:**

* `onReady`: HubSpot is ready.
* `onDialNumber`: User initiates an outbound call.
* `onEngagementCreated`: (Deprecated; use `onCreateEngagementSucceeded`) An engagement is created.
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publishing to a channel succeeded/failed.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID matching succeeded/failed.
* `onCreateEngagementSucceeded`/`onCreateEngagementFailed`: Engagement creation succeeded/failed.
* `onUpdateEngagementSucceeded`/`onUpdateEngagementFailed`: Engagement update succeeded/failed.
* `onVisibilityChanged`: Call widget visibility changed.

**Your app sends these events:**

* `initialized`: Softphone ready.
* `userLoggedIn`/`userLoggedOut`: User login/logout status.
* `outgoingCall`: Outgoing call started.
* `callAnswered`: Call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`: An error occurred.
* `resizeWidget`: Resize the widget.


### API

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);

// Example: Sending an outgoing call event
extensions.outgoingCall({
  toNumber: "+15551234567",
  fromNumber: "+15559876543",
  createEngagement: true, // Tells HubSpot to create an engagement
  callStartTime: Date.now()
});

// Example: Handling onDialNumber event
extensions.eventHandlers.onDialNumber = (data) => {
  console.log("Dial Number Event:", data);
  // ... your logic to handle the call ...
};
```


### Calling Settings Endpoint (API)

This API endpoint allows you to manage your app's settings in HubSpot.  Use `APP_ID` and your `DEVELOPER_ACCOUNT_API_KEY`.

**Endpoint:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`

**Methods:** `POST`, `PATCH`, `GET`, `DELETE`

**Example (cURL):**

```bash
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"My App","url":"https://myapp.com","height":600,"width":400,"isReady":false}'
```

### Local Storage Override (for Testing)

You can override settings during development using localStorage:

```javascript
const mySettings = { isReady: true, name: 'My App', url: 'http://localhost:3000' };
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(mySettings));
```

### Production Readiness

Set `isReady` to `true` via the settings endpoint to mark your app as production-ready.

### Publishing to the Marketplace

Once ready, publish your app to the HubSpot marketplace.  See the HubSpot marketplace documentation for details.


## Frequently Asked Questions

Refer to the original document for FAQs on authentication, CDN hosting, engagement creation/updates, required scopes, integration with existing apps, and more.


This expanded markdown documentation provides a more structured and detailed overview of the HubSpot Calling Extensions SDK, including code examples and API details.  Remember to replace placeholders like `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values.
