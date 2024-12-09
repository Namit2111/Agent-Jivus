# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK enables apps to offer a custom calling experience directly from CRM records within HubSpot.  It consists of three key components:

* **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
* **Calling Settings Endpoints:** Used to configure calling settings for your app on a per-HubSpot account basis.
* **Calling iframe:**  The interface your app presents to HubSpot users, configured via the calling settings endpoints.

For a detailed understanding of the in-app calling experience, refer to [this knowledge base article](LINK_TO_KNOWLEDGE_BASE_ARTICLE).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Only outgoing calls are currently supported.  If you need an app, you can [create one from your HubSpot developer account](LINK_TO_HUBSPOT_DEVELOPER_ACCOUNT).  If you don't have a developer account, sign up [here](LINK_TO_SIGNUP).

## Getting Started

### Run the Demo Calling App

Two demo apps are available to test the SDK:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.

### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

   This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console and run one of the following commands:

   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

3. Refresh the page. Click the "Call" icon, select the demo app from the dropdown, and click "Call".

### Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends messages via events, and your app responds through event handlers.


### Events

#### Sending Messages to HubSpot

* **`initialized`:**  Indicates soft phone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn`:** User login notification (needed only if not logged in during initialization).
* **`userLoggedOut`:** User logout notification.
* **`outgoingCall`:** Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered`:** Outgoing call answered. Payload: `{ externalCallId: string }`
* **`callEnded`:** Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted`:** Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError`:** App error. Payload: `{ message: string }`
* **`resizeWidget`:** Resize request. Payload: `{ height: number, width: number }`

#### Receiving Messages from HubSpot

* **`onReady`:** HubSpot is ready.
* **`onDialNumber`:** Outbound call initiated in HubSpot.
* **`onEngagementCreated` (Deprecated):** Use `onCreateEngagementSucceeded` instead.
* **`onNavigateToRecordFailed`:** Record navigation failure.
* **`onPublishToChannelSucceeded`:** Successful channel publishing.
* **`onPublishToChannelFailed`:** Failed channel publishing.
* **`onCallerIdMatchSucceeded`:** Successful caller ID match.
* **`onCallerIdMatchFailed`:** Failed caller ID match.
* **`onCreateEngagementSucceeded`:** Successful engagement creation.
* **`onCreateEngagementFailed`:** Failed engagement creation.
* **`onUpdateEngagementSucceeded`:** Successful engagement update.
* **`onUpdateEngagementFailed`:** Failed engagement update.
* **`onVisibilityChanged`:** Widget visibility changed.
* **`defaultEventHandler`:** Default event handler.

### SDK Instantiation

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean,
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: event => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Testing Your App

HubSpot requires these iframe parameters: `{ name: string, url: string, width: number, height: number, isReady: boolean, supportsCustomObjects: boolean }`

### Using the Calling Settings Endpoint

Use the API (e.g., Postman) to manage settings.  Remember to use your `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`.  Example cURL command:

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports PATCH, GET, and DELETE.  Set `isReady` to `false` during testing.

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

### Getting Your App Ready for Production

Set `isReady` to `true` using the PATCH endpoint.

### Publishing to the HubSpot Marketplace

[Instructions for publishing your app to the HubSpot Marketplace](LINK_TO_MARKETPLACE_INSTRUCTIONS).


## Frequently Asked Questions

* **Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, using jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them.  For calls outside HubSpot, your app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Adding to Existing App:** Yes, possible. Existing users automatically get the update.
* **Integrating Existing Softphone:** Yes, easily integrated.
* **Multiple Integrations:** Yes, users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Integration Appearance:** Yes, for existing users of an updated app.
* **User Installation/Uninstallation:** Only users with necessary permissions.
* **Custom Calling Property:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, if using the SDK to create calls and setting `createEngagement: true` in the `outgoingCall` event.


**(Remember to replace placeholder links with the actual links.)**
