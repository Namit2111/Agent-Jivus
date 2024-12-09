# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality directly into HubSpot's CRM.  Only outgoing calls are currently supported.

## Overview

The Calling Extensions SDK enables apps to provide a custom calling experience for HubSpot users, directly from CRM records.  It consists of three main components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:**  Displays your app to HubSpot users; configured via the calling settings endpoints.


For details on the in-app calling experience, see [this knowledge base article](link_to_knowledge_base_article).  Once integrated, your app will appear in HubSpot's call switcher.

If you don't have a HubSpot app, you can [create one here](link_to_hubspot_developer_account_creation).  If you lack a HubSpot developer account, sign up [here](link_to_hubspot_developer_signup).


## Getting Started

### Run the Demo Calling App

Two demo apps are available:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** More comprehensive example using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and aren't fully functional calling apps.


### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](link_to_zip_download) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`:**  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

   This installs dependencies and starts the app (access it at `https://localhost:9025/`). You may need to bypass a security warning.


### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console and run one of these commands (depending on which demo you installed):

   * **`demo-minimal-js` (installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-react-ts` (installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

3. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Install the Calling Extensions SDK

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses messages exchanged via methods and event handlers. See the [Events](#events) section for a complete list.

**Key Events:**

* **Dial Number:** HubSpot sends the dial number.
* **Outbound Call Started:** App notifies HubSpot.
* **Create Engagement:** HubSpot creates a call engagement (minimal info).
* **Engagement Created:** HubSpot confirms engagement creation.
* **EngagementId Sent to App:** HubSpot sends the `engagementId`.
* **Call Ended:** App notifies HubSpot.
* **Call Completed:** App signals completion.
* **Update Engagement:** App updates the engagement with call details.


**Creating an Instance:**

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: event => { /* Dial number received */ },
    onCreateEngagementSucceeded: event => { /* Engagement created successfully */ },
    onEngagementCreatedFailed: event => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: event => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: event => { /* Engagement update failed */ },
    onVisibilityChanged: event => { /* Widget visibility changed */ },
  }
};

const extensions = new CallingExtensions(options);
```


## Test Your App

To launch the iFrame, HubSpot requires these parameters:

```json
{
  "name": "string", // App name
  "url": "string", // App URL
  "width": number, // iFrame width
  "height": number, // iFrame height
  "isReady": boolean, // Ready for production (false during testing)
  "supportsCustomObjects": true // Support calls from custom objects
}
```

## Using the Calling Settings Endpoint

Use your API tool (e.g., Postman) to send a payload to HubSpot's settings API.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  Set `isReady` to `false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint supports `POST`, `PATCH`, `GET`, and `DELETE`.


## Override Extension Settings (localStorage)

For testing, override settings using your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

## Get Your App Ready for Production

Set `isReady` to `true` using the `PATCH` endpoint:

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"isReady":true}'
```

## Publish to the HubSpot Marketplace

[Learn how to publish your app to the marketplace here](link_to_marketplace_publishing).


## Events

### Sending Messages to HubSpot

* **`initialized`:**  Indicates softphone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn`:** User login.
* **`userLoggedOut`:** User logout.
* **`outgoingCall`:** Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered`:** Call answered. Payload: `{ externalCallId: string }`
* **`callEnded`:** Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted`:** Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError`:** App error. Payload: `{ message: string }`
* **`resizeWidget`:** Resize request. Payload: `{ height: number, width: number }`

### Receiving Messages from HubSpot

* **`onReady`:** HubSpot is ready.
* **`onDialNumber`:** Outbound call initiated.
* **`onEngagementCreated`:** (Deprecated; use `onCreateEngagementSucceeded`)
* **`onNavigateToRecordFailed`:** Navigation to record failed.
* **`onPublishToChannelSucceeded`:** Publishing to channel succeeded.
* **`onPublishToChannelFailed`:** Publishing to channel failed.
* **`onCallerIdMatchSucceeded`:** Caller ID match succeeded.
* **`onCallerIdMatchFailed`:** Caller ID match failed.
* **`onCreateEngagementSucceeded`:** Engagement created successfully.
* **`onCreateEngagementFailed`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded`:** Engagement updated successfully.
* **`onUpdateEngagementFailed`:** Engagement update failed.
* **`onVisibilityChanged`:** Widget visibility changed.
* **`defaultEventHandler`:** Default event handler.


## Frequently Asked Questions

* **Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:**  HubSpot creates engagements for calls from the HubSpot UI; apps create them for calls outside the UI and update them afterward.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:** Functionality can be added to existing marketplace apps.
* **Softphone Integration:** Easily integrate existing softphones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free Users:** All users can install the app.
* **Automatic Appearance:** Integration automatically appears for existing app users.
* **User Permissions:** Only users with appropriate permissions can install/uninstall.
* **Custom Calling Properties:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, if using the SDK for call creation and setting `createEngagement: true` in the `outgoingCall` event.


Remember to replace placeholder links (`link_to_...`) with the actual URLs.
