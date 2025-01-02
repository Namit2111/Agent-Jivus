# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling options into HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between a calling application and HubSpot, allowing users to initiate calls directly from CRM records.  The integration consists of three key components:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication between your app and HubSpot.  It handles event handling and message passing.
2. **Calling Settings Endpoints (API):**  Used to configure the calling app's settings for each connected HubSpot account.
3. **Calling iFrame:**  The iframe where your calling app's UI is displayed to HubSpot users.  Its configuration is managed via the calling settings endpoints.

**Note:** Currently, only outgoing calls are supported.

## Getting Started

### 1. Install the Demo App (Optional)

Two demo apps are available to test the SDK:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS.  SDK instantiation is in `index.js`.
* **`demo-react-ts`:**  More realistic implementation using React, TypeScript, and Styled Components.  SDK instantiation is in `useCti.ts`.

**Installation:**

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo app's directory (`demos/demo-minimal-js` or `demos/demo-react-ts`).
4. Run `npm i && npm start`.  This opens the app at `https://localhost:9025/`.  You might need to bypass a security warning.

### 2. Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Run one of the following commands in the console, depending on the demo app and whether you installed it locally:

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

4. Refresh the page.  Select the demo app from the "Call from" dropdown in the call switcher.

### 3. Install the Calling Extensions SDK

Add the SDK to your project using npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses events to exchange messages between your app and HubSpot.

### Events

**Sent to HubSpot:**

* `initialized`:  Notifies HubSpot that the softphone is ready.
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call initiated.
* `callAnswered`: Outgoing call answered.
* `callEnded`: Outgoing call ended.
* `callCompleted`: Call completed.
* `sendError`: An error occurred.
* `resizeWidget`: Request to resize the widget.


**Received from HubSpot:**

* `onReady`: HubSpot is ready.
* `onDialNumber`: Outbound call triggered by HubSpot user.
* `onEngagementCreated`: (Deprecated; use `onCreateEngagementSucceeded`) Engagement created.
* `onNavigateToRecordFailed`: Navigation to record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publish to channel success/failure.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match success/failure.
* `onCreateEngagementSucceeded`/`onCreateEngagementFailed`: Engagement creation success/failure.
* `onUpdateEngagementSucceeded`/`onUpdateEngagementFailed`: Engagement update success/failure.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Default event handler.


### Example: SDK Instantiation

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

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

### Example: Sending an `outgoingCall` Event

```javascript
const callInfo = {
  toNumber: "+15551234567",
  fromNumber: "+15559876543",
  createEngagement: true,
  callStartTime: Date.now()
};

extensions.outgoingCall(callInfo);
```


## API Endpoints (Calling Settings)

Use the following API endpoints to manage your app's settings:

* **URL:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`
* **Methods:** `POST`, `PATCH`, `GET`, `DELETE`

**Example (using `curl`):**

* **POST (Add/Update settings):**
  ```bash
  curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"My App","url":"https://my-app.com","height":600,"width":400,"isReady":false}'
  ```

* **PATCH (Update settings):**
  ```bash
  curl --request PATCH \
  --url '...' \
  --data '{"isReady": true}'
  ```

  Replace placeholders like `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values.  The `isReady` flag should be `false` during testing and `true` for production.


## Local Storage Override (for Testing)

You can override settings during testing using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Publishing to the Marketplace

Once your app is ready, publish it to the HubSpot marketplace [link to marketplace instructions].


## Frequently Asked Questions (FAQ)

The provided text contains a comprehensive FAQ section that is well-structured and answers many common questions regarding authentication, CDN hosting, engagement management, required scopes, integration with existing applications, multi-integration support, free user access, automatic updates, user permissions, custom properties, and custom object calls.  Refer to the original text for those answers.
