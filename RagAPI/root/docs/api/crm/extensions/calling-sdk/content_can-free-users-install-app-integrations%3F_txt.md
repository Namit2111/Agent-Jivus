# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot directly from CRM records.

## Overview

The Calling Extensions SDK facilitates communication between your application and HubSpot, providing a custom calling experience for HubSpot users.  The integration consists of three key components:

1. **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:**  Displays your app to HubSpot users; its configuration is managed via the calling settings endpoints.

For details on the in-app calling experience, see [this knowledge base article](link_to_knowledge_base_article).  After connecting your app, it will appear in HubSpot's call switcher.

**Note:** Currently, only outgoing calls are supported.  If you don't have a HubSpot app, you can [create one here](link_to_create_hubspot_app).  If you need a developer account, sign up [here](link_to_developer_signup).


## Getting Started

### Run the Demo Calling App

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.

### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](link_to_zip) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app at `https://localhost:9025/`. You may need to bypass a security warning.

### Launch the Demo App from HubSpot

1. Navigate to HubSpot contacts (Contacts > Contacts) or companies (Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands, depending on your installation method:

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call."


### Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends messages (events) to your app, and your app can send messages back.

### Events

#### Sending Messages to HubSpot

* `initialized`: Softphone ready status.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User login notification.
* `userLoggedOut`: User logout notification.
* `outgoingCall`: Outgoing call started.  Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Outgoing call answered.  Payload: `{ externalCallId: string }`
* `callEnded`: Call ended.  Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`  `callEndStatus` options: `INTERNAL_COMPLETED`, `INTERNAL_FAILED`, `INTERNAL_CANCELED`, `INTERNAL_BUSY`, `INTERNAL_NO_ANSWER`, `INTERNAL_REJECTED`, `INTERNAL_MISSED`
* `callCompleted`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`:  Error notification. Payload: `{ message: string }`
* `resizeWidget`: Resize request. Payload: `{ height: number, width: number }`


#### Receiving Messages from HubSpot

* `onReady`: HubSpot is ready.
* `onDialNumber`: Outbound call initiated.
* `onEngagementCreated`: (Deprecated. Use `onCreateEngagementSucceeded`.) Engagement created.
* `onNavigateToRecordFailed`: Record navigation failure.
* `onPublishToChannelSucceeded`: Channel publishing success.
* `onPublishToChannelFailed`: Channel publishing failure.
* `onCallerIdMatchSucceeded`: Caller ID match success.
* `onCallerIdMatchFailed`: Caller ID match failure.
* `onCreateEngagementSucceeded`: Engagement creation success.
* `onCreateEngagementFailed`: Engagement creation failure.
* `onUpdateEngagementSucceeded`: Engagement update success.
* `onUpdateEngagementFailed`: Engagement update failure.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Default event handler.


### SDK Instantiation

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Log debug messages
  eventHandlers: {
    onReady: () => { /*...*/ },
    onDialNumber: (event) => { /*...*/ },
    onCreateEngagementSucceeded: (event) => { /*...*/ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Testing Your App

To launch the calling extensions iFrame, HubSpot requires these iFrame parameters:

```json
{
  "name": "string",
  "url": "string",
  "width": number,
  "height": number,
  "isReady": boolean,
  "supportsCustomObjects": true
}
```

### Calling Settings Endpoint

Use the API (e.g., Postman) to manage app settings.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  `isReady: false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.

### Overriding Settings with localStorage

For testing, override settings using the browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production Readiness

Set `isReady` to `true` using the `PATCH` endpoint once testing is complete.

### Publishing to the Marketplace

[Learn how to publish your app to the HubSpot marketplace](link_to_marketplace_publishing).


## Frequently Asked Questions

* **User Authentication:** Handled by your app.
* **CDN Hosting:** Yes, via jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them.  For calls outside HubSpot, your app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:** You can add this functionality to existing marketplace apps.
* **Softphone Integration:**  Easily integrate your existing softphone.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free User Access:** Yes, all users can install the app.
* **Automatic Appearance:** Yes, for updated apps.
* **Installation/Uninstallation:** Controlled by user permissions.
* **Custom Calling Properties:** Yes, via the properties API.
* **Calls from Custom Objects:** Yes, if using the SDK to create calls and setting `createEngagement: true` in the `outgoingCall` event.


This markdown provides a comprehensive documentation of the HubSpot CRM API Calling Extensions SDK. Remember to replace placeholder links with actual links.
