# HubSpot Calling Extensions SDK Documentation

This document provides comprehensive instructions and reference information for integrating the HubSpot Calling Extensions SDK into your calling application.

## Overview

The HubSpot Calling Extensions SDK allows developers to provide a custom calling experience directly within the HubSpot CRM.  Users can initiate calls from contact or company records, and the SDK facilitates communication between your application and HubSpot.  The integration consists of three key parts:

* **Calling Extensions SDK (JavaScript):** A JavaScript SDK enabling communication between your app and HubSpot.
* **Calling Settings Endpoints:**  Used to configure your app's settings for each connected HubSpot account.
* **Calling iFrame:** The iframe where your calling application is displayed to HubSpot users, configured via the settings endpoints.

**Note:** Only outgoing calls are currently supported.

## Getting Started

### 1. Run the Demo Calling App

Two demo applications are available to test the SDK:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  SDK instantiation is shown in `index.js`.
* **`demo-react-ts`:** A more realistic implementation using React, TypeScript, and Styled Components. SDK instantiation is in `useCti.ts`.

**Note:** These demos use mock data and are not fully functional calling applications.

### 2. Install the Demo App (Optional)

1. Install Node.js.
2. Clone, fork, or download the ZIP of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### 3. Launch the Demo App from HubSpot

1. Navigate to Contacts > Contacts or Contacts > Companies in your HubSpot account.
2. Open your browser's developer console.
3. Run one of the following commands in the console, depending on the demo app and whether you installed it:

   * **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".

### 4. Install the Calling Extensions SDK

Use npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses events to exchange messages between your app and HubSpot.

### Events

**Sent to HubSpot:**

* `initialized`: Soft phone ready.
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started.
* `callAnswered`: Outgoing call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`: Error encountered.
* `resizeWidget`: Resize widget request.

**Received from HubSpot:**

* `onReady`: HubSpot ready to receive messages.
* `onDialNumber`: Outbound call triggered.
* `onEngagementCreated` (deprecated - use `onCreateEngagementSucceeded`): Engagement created.
* `onNavigateToRecordFailed`: Navigation to record failed.
* `onPublishToChannelSucceeded`: Publishing to channel succeeded.
* `onPublishToChannelFailed`: Publishing to channel failed.
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement creation succeeded.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement update succeeded.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Default event handler.


Detailed event descriptions and payloads are provided in the full document.  Each event has a corresponding method on the `extensions` object.  Examples are provided in the original document.


### Creating an Instance

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```


###  iFrame Parameters

To launch the calling extensions iframe, HubSpot requires these parameters:

```json
{
  "name": "string",
  "url": "string",
  "width": number,
  "height": number,
  "isReady": boolean,
  "supportsCustomObjects": boolean
}
```

### Calling Settings Endpoint

Use this API endpoint to manage your app's settings:

`https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

(Use `POST`, `PATCH`, `GET`, or `DELETE` as needed. See the original document for example `curl` commands.)


### Overriding Settings with localStorage

For testing, you can override settings using localStorage:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Getting Your App Ready for Production

Set `isReady` to `true` using the PATCH endpoint.


### Publishing to the HubSpot Marketplace

Follow the instructions provided in the original document to publish your app.


## Frequently Asked Questions

The original document contains a comprehensive FAQ section covering authentication, CDN hosting, engagement creation/updates, required scopes, integrating with existing applications, multiple integrations, free user access, automatic updates, user permissions, custom properties, and calling from custom objects.


This markdown documentation summarizes the key aspects of the HubSpot Calling Extensions SDK.  Refer to the original text for detailed examples, code snippets, and further explanations.
