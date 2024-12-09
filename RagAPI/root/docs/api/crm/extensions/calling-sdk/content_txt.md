# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot CRM records.

## Overview

The Calling Extensions SDK facilitates communication between your calling application and HubSpot.  It consists of three key components:

1. **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:** The interface displayed to HubSpot users, configured via the settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE_HERE).  Once integrated, your app will appear in HubSpot's call switcher.  Only outgoing calls are currently supported.

If you need to create a HubSpot developer account, you can sign up [here](LINK_TO_SIGNUP_HERE).

## Getting Started

### Demo Apps

Two demo applications showcase the SDK's functionality:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive implementation using React, TypeScript, and Styled Components.  See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.

### Installing the Demo App

1. Install Node.js.
2. Clone, fork, or download the ZIP of the repository.
3. Navigate to the project's root directory in your terminal.
4. Run one of the following commands:

   * **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launching the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands, depending on the demo app and whether you installed it locally:

   * **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Installing the Calling Extensions SDK

Add the SDK as a dependency to your app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses events for communication.  See the "Events" section for a complete list.

### Creating an SDK Instance

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Whether to log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: event => { /* HubSpot sends a dial number */ },
    onCreateEngagementSucceeded: event => { /* Engagement created */ },
    onEngagementCreatedFailed: event => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: event => { /* Engagement updated */ },
    onUpdateEngagementFailed: event => { /* Engagement update failed */ },
    onVisibilityChanged: event => { /* Widget visibility changed */ },
  }
};

const extensions = new CallingExtensions(options);
```

### Testing Your App

To launch the calling extension iFrame, HubSpot requires these iFrame parameters:

```json
{
  "name": "string", // App name
  "url": "string", // App URL
  "width": number, // iFrame width
  "height": number, // iFrame height
  "isReady": boolean, // Whether the widget is ready for production (defaults to true)
  "supportsCustomObjects": true // Whether calls can be placed from custom objects
}
```

### Using the Calling Settings Endpoint

Use your API tool (e.g., Postman) to send a payload to HubSpot's settings API:

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

(Remember to replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`.)  This endpoint also supports `PATCH`, `GET`, and `DELETE`.  Set `isReady` to `false` during testing.


### Overriding Extension Settings (localStorage)

For testing, override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Preparing for Production

Set `isReady` to `true` using the `PATCH` endpoint.


### Publishing to the HubSpot Marketplace

Once ready, publish your app to the HubSpot marketplace [here](LINK_TO_MARKETPLACE_HERE).


## Events

### Sending Messages to HubSpot

* `initialized`:  Indicates soft phone readiness. Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User login notification.
* `userLoggedOut`: User logout notification.
* `outgoingCall`: Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Outgoing call answered. Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`: Error notification. Payload: `{ message: string }`
* `resizeWidget`: Widget resize request. Payload: `{ height: number, width: number }`


### Receiving Messages from HubSpot

* `onReady`: HubSpot is ready.
* `onDialNumber`: Outbound call triggered.
* `onEngagementCreated`: (Deprecated; use `onCreateEngagementSucceeded`) Engagement created.
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


## Frequently Asked Questions

* **User Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver.
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; the app updates them.  For calls outside the HubSpot UI, the app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Marketplace Apps:** Functionality can be added to existing apps.
* **Integrating Existing Soft Phones:** Easily integrated; follow the documentation.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Integration Display:** Yes, for updated apps.
* **User Installation/Uninstallation:**  Only users with necessary permissions.
* **Custom Calling Properties:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, if using the SDK to create calls and setting `createEngagement: true` in the `outgoingCall` event.


This markdown documentation provides a comprehensive overview and detailed instructions for using the HubSpot Calling Extensions SDK. Remember to replace placeholder links with the actual URLs.
