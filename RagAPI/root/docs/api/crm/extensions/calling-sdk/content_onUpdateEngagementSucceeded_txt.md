# HubSpot Calling Extensions SDK Documentation

## Overview

The HubSpot Calling Extensions SDK allows developers to integrate custom calling functionality into their HubSpot apps.  This enables users to initiate calls directly from HubSpot CRM records.  The SDK facilitates communication between the app and HubSpot, handling call events and engagement management.

**Key Components:**

* **Calling Extensions SDK (JavaScript):**  The core library enabling communication.
* **Calling Settings Endpoints (API):** Configure your app's settings within HubSpot.
* **Calling iFrame:** The interface displayed to the HubSpot user.


## Getting Started

### 1. Install the SDK:

**npm:**

```bash
npm i --save @hubspot/calling-extensions-sdk
```

**yarn:**

```bash
yarn add @hubspot/calling-extensions-sdk
```

### 2.  Demo Apps:

Two demo apps are provided for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS.  (`index.js` shows SDK instantiation).
* **`demo-react-ts`:**  More comprehensive example using React, TypeScript, and Styled Components. (`useCti.ts` shows SDK instantiation).


To run the demos (requires Node.js and npm/yarn):

1. Clone the repository.
2. Navigate to the demo directory (`cd demos/demo-minimal-js` or `cd demos/demo-react-ts`).
3. Run `npm i && npm start` (or `yarn install && yarn start`).
4. Access the app at `https://localhost:9025/`.  You might need to bypass a security warning.

### 3. Launch Demo from HubSpot:

1. Navigate to Contacts > Contacts or Contacts > Companies in your HubSpot account.
2. Open your browser's developer console.
3. Set the appropriate `localStorage` item:

   * **Installed Demo (local):**  `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and initiate a call.


## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends events to your app, and your app sends events back to HubSpot.

### Creating an SDK Instance:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* HubSpot sends dial number */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created */ },
    // ... other event handlers (see below)
  },
};

const extensions = new CallingExtensions(options);
```

### Events

**Sent from HubSpot:**

* `onReady`: HubSpot is ready for communication.
* `onDialNumber`: User initiates an outbound call.  Provides phone number, contact/company ID, etc.
* `onCreateEngagementSucceeded`:  Engagement successfully created by HubSpot.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement successfully updated.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Call widget visibility changes (minimized/hidden).
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publish to channel success/failure.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match success/failure.


**Sent to HubSpot:**

* `initialized`: App initialization status.
* `userLoggedIn`: User logs in.
* `userLoggedOut`: User logs out.
* `outgoingCall`: Outgoing call initiated.  Provides call start time, phone number, etc.
* `callAnswered`: Outgoing call answered.
* `callEnded`: Outgoing call ended.
* `callCompleted`: Call completed (Engagement properties are managed by HubSpot).
* `sendError`: An error occurred in the app.
* `resizeWidget`: Request to resize the widget.

**Example: Handling `onDialNumber` event:**

```javascript
options.eventHandlers.onDialNumber = (data) => {
  const { phoneNumber, ownerId, objectId, objectType } = data;
  console.log("Dialing:", phoneNumber, "for contact/company:", objectId, objectType);
  // Initiate your call using phoneNumber
};
```


**Example: Sending `outgoingCall` event:**

```javascript
const callInfo = {
  toNumber: "+15551234567",
  fromNumber: "+15559876543",
  createEngagement: true, // HubSpot will create the engagement
  callStartTime: Date.now(),
};
extensions.outgoingCall(callInfo);
```

### API Endpoints (Calling Settings)

Use the HubSpot API to configure your app's settings. Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.

* **GET:**  Retrieve settings: `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`
* **POST:** Create settings:  Same URL as GET.
* **PATCH:** Update settings: Same URL as GET.
* **DELETE:** Delete settings: Same URL as GET.

**Example (using curl to POST settings):**

```bash
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"My App","url":"https://my-app.com/widget","height":600,"width":400,"isReady":false}'
```


### LocalStorage Override (for testing):

You can override settings using `localStorage` in your browser's developer console:

```javascript
const mySettings = { isReady: true, name: 'My App', url: 'http://localhost:3000' };
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(mySettings));
```

## Frequently Asked Questions

Refer to the original document for FAQs regarding authentication, CDN hosting, engagement creation/updates, required scopes, and other common questions.


## Publishing to the Marketplace

Once your app is ready, publish it to the HubSpot Marketplace.  (See the original document for details).


This markdown documentation provides a more structured and concise overview of the HubSpot Calling Extensions SDK.  Remember to consult the original document for complete details and the most up-to-date information.
