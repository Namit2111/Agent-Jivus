# HubSpot CRM API | Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options directly into HubSpot CRM records.

## Overview

The Calling Extensions SDK facilitates communication between a calling application and HubSpot.  It consists of three main parts:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication between your app and HubSpot.
2. **Calling Settings Endpoints:**  APIs used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:** The iframe where your app is displayed to HubSpot users, configured via the calling settings endpoints.

For a better understanding of the in-app calling experience, refer to [this knowledge base article](LINK_TO_KNOWLEDGE_BASE_ARTICLE).  After connecting your app, it will appear in HubSpot's call switcher.

**Note:** Currently, only outgoing calls are supported.

If you don't have a HubSpot app, you can [create one from your HubSpot developer account](LINK_TO_CREATE_APP).  If you need a developer account, sign up [here](LINK_TO_SIGN_UP).


## Getting Started

### Demo Apps

Two demo apps are available for testing the SDK:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  The SDK instantiation is shown in `index.js`.
* **`demo-react-ts`:** A more realistic implementation using React, TypeScript, and Styled Components. SDK instantiation is in `useCti.ts`.

**Note:** These demo apps use mock data and are not fully functional calling apps.

### Installing the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`:**  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### Launching the Demo App from HubSpot

1. Navigate to HubSpot Contacts (`Contacts > Contacts`) or Companies (`Contacts > Companies`).
2. Open your browser's developer console.
3. Run one of the following commands, depending on whether you installed the demo app:

   * **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page, click the "Call" icon, select the demo app from the "Call from" dropdown, and click "Call".

### Installing the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses events for communication. See the **Events** section for a complete list.

### Creating an SDK Instance

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Set to true for debugging messages
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

###  Testing Your App

To launch the calling extensions iframe, HubSpot requires these iframe parameters:

```javascript
{
  name: string, // App name
  url: string, // App URL
  width: number, // iFrame width
  height: number, // iFrame height
  isReady: boolean, // True for production, false for testing
  supportsCustomObjects: true // Whether calls can be made from custom objects
}
```


### Using the Calling Settings Endpoint

Use your API tool (e.g., Postman) to send a payload to HubSpot's settings API. Replace `APP_ID` with your app's ID and `DEVELOPER_ACCOUNT_API_KEY` with your API key.  Set `isReady` to `false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.


### Overriding Extension Settings (localStorage)

For testing, override settings using your browser's developer console:

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

[Learn how to publish your app to the HubSpot Marketplace](LINK_TO_MARKETPLACE_PUBLISHING).


## Events

### Sending Messages to HubSpot

* **`initialized`:**  Indicates softphone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn`:** User logged in.
* **`userLoggedOut`:** User logged out.
* **`outgoingCall`:** Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered`:** Outgoing call answered. Payload: `{ externalCallId: string }`
* **`callEnded`:** Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted`:** Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError`:**  Error occurred. Payload: `{ message: string }`
* **`resizeWidget`:** Resize the widget. Payload: `{ height: number, width: number }`

### Receiving Messages from HubSpot

* **`onReady`:** HubSpot is ready.
* **`onDialNumber`:** Outbound call initiated.
* **`onEngagementCreated` (deprecated):** Use `onCreateEngagementSucceeded` instead.
* **`onNavigateToRecordFailed`:** Navigation to a record failed.
* **`onPublishToChannelSucceeded`:** Publishing to a channel succeeded.
* **`onPublishToChannelFailed`:** Publishing to a channel failed.
* **`onCallerIdMatchSucceeded`:** Caller ID match succeeded.
* **`onCallerIdMatchFailed`:** Caller ID match failed.
* **`onCreateEngagementSucceeded`:** Engagement creation succeeded.
* **`onCreateEngagementFailed`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded`:** Engagement update succeeded.
* **`onUpdateEngagementFailed`:** Engagement update failed.
* **`onVisibilityChanged`:** Widget visibility changed.
* **`defaultEventHandler`:** Default event handler.


## Frequently Asked Questions

* **Authentication:** The calling app handles authentication.
* **CDN Hosting:** Yes, via jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:**  HubSpot creates engagements for calls initiated within the HubSpot UI; the app updates them afterward. For calls outside the HubSpot UI, the app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Adding to Existing App:** Yes, possible.
* **Integrating Existing Softphone:** Yes, easily integrable.
* **Multiple Integrations:** Yes, users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic App Appearance:** Yes, for updates to existing installations.
* **User Installation/Uninstallation:** Only users with necessary permissions.
* **Custom Calling Property:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, if using the SDK to create calls and notifying HubSpot via `outgoingCall` with `createEngagement: true`.


This markdown provides a comprehensive overview of the HubSpot Calling Extensions SDK. Remember to replace placeholder links with the actual links.  The code snippets are formatted for better readability.
