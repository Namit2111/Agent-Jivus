# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot CRM records.  The SDK facilitates communication between a calling application and HubSpot, enabling features like initiating calls and managing call engagements.

## Overview

The Calling Extensions SDK consists of three main components:

1. **JavaScript SDK:** Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Configure settings for your app on a per-HubSpot account basis.
3. **Calling iFrame:** The user interface of your app within HubSpot.


**Note:** Currently, only outgoing calls are supported.

## Getting Started

### 1. Run the Demo App

Two demo apps are available:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (see `index.js`).
* **`demo-react-ts`:**  More comprehensive example using React, TypeScript, and Styled Components (see `useCti.ts`).

**Note:** Demo apps use mock data.


### 2. Install the Demo App (Optional)

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app directory (`demos/demo-minimal-js` or `demos/demo-react-ts`).
4. Run: `npm i && npm start`

This starts the app at `https://localhost:9025/`. You might need to bypass a security warning.


### 3. Launch the Demo App from HubSpot

1. Go to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Run one of the following commands in the console, depending on which demo app and installation method you chose:

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
4. Refresh the page. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### 4. Install the SDK

Add the SDK as a dependency to your app:

**npm:**

```bash
npm i --save @hubspot/calling-extensions-sdk
```

**yarn:**

```bash
yarn add @hubspot/calling-extensions-sdk
```


## Using the SDK

The SDK uses events for communication.

### Events

**HubSpot sends:**

* `onReady`: HubSpot is ready.
* `onDialNumber`: User initiates an outbound call.  Provides phone number, owner ID, subject ID, object ID, object type, portal ID, country code, callee info, timestamp, and phone number source.
* `onEngagementCreated`: (Deprecated, use `onCreateEngagementSucceeded`) Engagement created.
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`: Publishing to a channel succeeded.
* `onPublishToChannelFailed`: Publishing to a channel failed.
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement creation succeeded.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement update succeeded.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed.

**Your app sends:**

* `initialized`: Softphone is ready (includes `isLoggedIn` and `engagementId`).
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started (includes `callStartTime`, `createEngagement`, `toNumber`, `fromNumber`).
* `callAnswered`: Call answered (includes `externalCallId`).
* `callEnded`: Call ended (includes `externalCallID`, `engagementId`, `callEndStatus`).
* `callCompleted`: Call completed (includes `engagementId`, `hideWidget`, `engagementProperties`, `externalCallId`).
* `sendError`: Error occurred (includes `message`).
* `resizeWidget`: Resize the widget (includes `height`, `width`).


### API Example (Creating an instance of `CallingExtensions`)

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Set to true for debugging
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    onCreateEngagementSucceeded: (event) => { /* ... */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

### Sending Messages to HubSpot (Examples)

See the original text for detailed examples of each event handler's usage and payload structures.


## Calling Settings Endpoint

Use this API endpoint to manage your app's settings:

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your app's ID and API key.  The endpoint supports `POST`, `PATCH`, `GET`, and `DELETE` methods.  Set `isReady` to `true` when your app is ready for production.


## Local Storage Override

For testing, override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production and Marketplace Publishing

Set `isReady` to `true` via the settings API.  Then, publish your app to the HubSpot marketplace (see the original text for details).


## Frequently Asked Questions (FAQs)

The original text includes a comprehensive FAQ section.


This Markdown documentation provides a structured overview of the HubSpot Calling Extensions SDK, making it easier to understand and utilize.  Remember to consult the original text and HubSpot's official documentation for the most up-to-date information.
