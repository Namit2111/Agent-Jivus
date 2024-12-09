# HubSpot Calling Extensions SDK Documentation

## Overview

The HubSpot Calling Extensions SDK allows developers to integrate custom calling functionality directly into the HubSpot CRM.  This enables users to initiate calls from within contact or company records using a custom calling application.  The SDK facilitates communication between your app and HubSpot through a simple API and event-driven architecture.  Currently, only outgoing calls are supported.

The system consists of three main parts:

1. **Calling Extensions SDK (JavaScript):** A JavaScript SDK enabling communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Used to configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:**  The iframe where your calling app is displayed to HubSpot users.  It's configured using the calling settings endpoints.


## Getting Started

### Run the Demo Calling App

Two demo apps are provided to illustrate SDK usage:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS (see `index.js`).
* **`demo-react-ts`:** A more realistic implementation using React, TypeScript, and Styled Components (see `useCti.ts`).

**Note:** These demos use mock data and aren't fully functional calling apps.

### Install the Demo App

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app directory:
    * For `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
    * For `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
4. The app will open in your browser at `https://localhost:9025/`. You might need to bypass a security warning.

### Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Run one of the following commands (depending on which demo and whether you installed it):
    * **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".

### Install the Calling Extensions SDK

Use npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends messages (events) to your app, and your app responds using SDK methods.

### Events

#### HubSpot Sends to App:

* `onReady`: HubSpot is ready.
* `onDialNumber`: User initiates an outbound call.
* `onEngagementCreated`: (Deprecated; use `onCreateEngagementSucceeded`)  Engagement created.
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`: Publishing to a channel succeeded.
* `onPublishToChannelFailed`: Publishing to a channel failed.
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement created successfully.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement updated successfully.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Call widget visibility changed.
* `defaultEventHandler`: Default event handler.


#### App Sends to HubSpot:

* `initialized`: Softphone is ready.
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started.
* `callAnswered`: Outgoing call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`: An error occurred.
* `resizeWidget`: Resize the widget.

### SDK Initialization

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, //Optional
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    onCreateEngagementSucceeded: (event) => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

###  Calling Settings Endpoint

Use the API to configure your app's settings:  (Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`)

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"My App","url":"https://my-app.com","height":600,"width":400,"isReady":false}'
```

Use `PATCH` to update settings (e.g., set `isReady: true` for production).

### Overriding Settings with localStorage (for testing)

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

##  Production Deployment

1. Set `isReady` to `true` in your app settings via the API.
2. Publish your app to the HubSpot Marketplace.


## Frequently Asked Questions

Refer to the included FAQ section within the original document for answers to common questions.


This markdown documentation summarizes the provided text, improving readability and organization.  It also adds consistent formatting and heading structures for better navigation.
