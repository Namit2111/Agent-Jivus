# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, enabling custom calling options within the HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between your calling app and HubSpot, providing a custom calling experience directly from CRM records.  It consists of three main parts:

* **Calling Extensions SDK (JavaScript):**  Enables communication between your app and HubSpot.
* **Calling Settings Endpoints:** Used to configure your app's settings for each connected HubSpot account.
* **Calling iFrame:**  Your app's interface within HubSpot, configured via the settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE_REQUIRED).  Once integrated, your app appears in HubSpot's call switcher.

**Note:** Currently, only outgoing calls are supported.  If you don't have a HubSpot app, you can [create one here](LINK_TO_CREATION_REQUIRED).  If you lack a HubSpot developer account, sign up [here](LINK_TO_SIGNUP_REQUIRED).

## Getting Started

### Run the Demo Calling App

Two demo apps illustrate the SDK:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:**  A more comprehensive example using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.

### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP_REQUIRED) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`**: `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`**: `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console.
3. Run one of these commands (depending on whether you installed the demo or not):

   * **Installed (`demo-minimal-js` or `demo-react-ts`):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Uninstalled (`demo-minimal-js`):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Uninstalled (`demo-react-ts`):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".

### Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses an event-driven API for message exchange.  See the **Events** section for a complete list.

### Creating an SDK Instance

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: event => { /* Dial number received */ },
    onCreateEngagementSucceeded: event => { /* Engagement created */ },
    onEngagementCreatedFailed: event => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: event => { /* Engagement updated */ },
    onUpdateEngagementFailed: event => { /* Engagement update failed */ },
    onVisibilityChanged: event => { /* Widget visibility changed */ }
  }
};

const extensions = new CallingExtensions(options);
```

###  iFrame Parameters

To launch the iFrame, HubSpot requires these parameters:

```json
{
  "name": "string", // App name
  "url": "string", // App URL
  "width": number, // iFrame width
  "height": number, // iFrame height
  "isReady": boolean, // Production-ready?
  "supportsCustomObjects": true // Support calls from custom objects?
}
```

### Calling Settings Endpoint

Use this API endpoint (e.g., with Postman) to manage your app's settings. Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  `isReady: false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.

### Overriding Settings with localStorage

For testing, override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Getting Your App Ready for Production

Set `isReady` to `true` using the `PATCH` endpoint:

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"isReady":true}'
```

### Publishing to the HubSpot Marketplace

[Details on publishing your app to the marketplace](LINK_TO_MARKETPLACE_REQUIRED).


## Events

### Sending Messages to HubSpot

* `initialized`:  Signals softphone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User login notification.
* `userLoggedOut`: User logout notification.
* `outgoingCall`: Outgoing call started.  Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Outgoing call answered. Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`: Error notification. Payload: `{ message: string }`
* `resizeWidget`: Widget resize request. Payload: `{ height: number, width: number }`

### Receiving Messages from HubSpot

* `onReady`: HubSpot is ready.
* `onDialNumber`: Outbound call triggered.
* `onEngagementCreated`: (Deprecated; use `onCreateEngagementSucceeded`)
* `onNavigateToRecordFailed`: Record navigation failure.
* `onPublishToChannelSucceeded`: Successful channel publishing.
* `onPublishToChannelFailed`: Channel publishing failure.
* `onCallerIdMatchSucceeded`: Caller ID match success.
* `onCallerIdMatchFailed`: Caller ID match failure.
* `onCreateEngagementSucceeded`: Engagement creation success.
* `onCreateEngagementFailed`: Engagement creation failure.
* `onUpdateEngagementSucceeded`: Engagement update success.
* `onUpdateEngagementFailed`: Engagement update failure.
* `onVisibilityChanged`: Widget visibility change.
* `defaultEventHandler`: Default event handler.


## Frequently Asked Questions

* **Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls from the HubSpot UI; apps update them.  Apps create engagements for calls outside the HubSpot UI.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:**  Add functionality to existing apps; existing users get automatic access.
* **Softphone Integration:**  Easily integrate existing softphones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free Users:** All users can install.
* **Automatic App Appearance:** Yes, for updates to existing installations.
* **User Installation/Uninstallation:** Only users with necessary permissions.
* **Custom Calling Properties:** Create via the properties API.
* **Calls from Custom Objects:** Supported if only using the SDK to create calls and sending `outgoingCall` events with `createEngagement: true`.


This documentation provides a comprehensive guide to using the HubSpot Calling Extensions SDK. Remember to replace placeholder links with actual links.
