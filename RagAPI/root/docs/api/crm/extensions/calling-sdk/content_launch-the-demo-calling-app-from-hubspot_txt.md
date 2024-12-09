# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK facilitates communication between your app and HubSpot, enabling custom calling options directly from CRM records.  It comprises three key components:

1. **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Configure calling settings for your app on a per-HubSpot account basis.
3. **Calling iFrame:** Displays your app to HubSpot users; configured via the calling settings endpoints.

For details on the in-app calling experience, see [this knowledge base article](LINK_TO_ARTICLE_HERE).  After connection, your app will appear in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.  If you don't have a HubSpot app, you can [create one here](LINK_TO_APP_CREATION).  If you lack a HubSpot developer account, [sign up here](LINK_TO_SIGNUP).


## Getting Started

### Run the Demo Calling App

Two demo apps are available:

* **`demo-minimal-js`:** A minimal JavaScript, HTML, and CSS implementation.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive React, TypeScript, and Styled Components implementation. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.


### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP_HERE) of the repository.
3. Navigate to the project's root directory.
4. Run the appropriate command:

   * **`demo-minimal-js`:**  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

   This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console and run the following command (choose the appropriate one based on your installation method):

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

3. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".

### Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses message passing via methods and event handlers.  See the [Events section](#events) for a complete list.

**Key Events:**

* **Dial number:** HubSpot sends the dial number.
* **Outbound call started:** App notifies HubSpot.
* **Create engagement:** HubSpot creates a call engagement (if requested).
* **Engagement created:** HubSpot confirms engagement creation.
* **EngagementId sent to App:** HubSpot sends the `engagementId`.
* **Call ended:** App notifies HubSpot.
* **Call completed:** App notifies HubSpot (HubSpot now handles engagement updates).
* **Update engagement:** App updates the engagement with call details.

**Creating an Instance:**

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: event => { /* HubSpot sends dial number */ },
    onCreateEngagementSucceeded: event => { /* Engagement created */ },
    onEngagementCreatedFailed: event => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: event => { /* Engagement updated */ },
    onUpdateEngagementFailed: event => { /* Engagement update failed */ },
    onVisibilityChanged: event => { /* Widget visibility changed */ },
  }
};

const extensions = new CallingExtensions(options);
```


### Test Your App

To launch the iFrame, HubSpot requires these parameters:

```javascript
{
  name: string, // App name
  url: string, // App URL
  width: number, // iFrame width
  height: number, // iFrame height
  isReady: boolean, // Ready for production? (false during testing)
  supportsCustomObjects: true // Support calls from custom objects?
}
```


### Using the Calling Settings Endpoint

Use your API tool (e.g., Postman) to send a payload to HubSpot's settings API. Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  `isReady` should be `false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.


### Override Extension Settings Using localStorage

For testing, override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


### Get Your App Ready for Production

Set `isReady` to `true` using the `PATCH` endpoint:

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"isReady":true}'
```


### Publish Your Calling App

[Publish your app to the HubSpot marketplace here](LINK_TO_MARKETPLACE_HERE).


## Events

### Sending Messages to HubSpot

The `extensions` object provides methods to send messages:

* **`initialized(payload)`:** Soft phone ready.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn()`:** User logged in.
* **`userLoggedOut()`:** User logged out.
* **`outgoingCall(callInfo)`:** Outgoing call started.  Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered(payload)`:** Call answered. Payload: `{ externalCallId: string }`
* **`callEnded(payload)`:** Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted(data)`:** Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError(data)`:** Error encountered. Payload: `{ message: string }`
* **`resizeWidget(data)`:** Resize widget. Payload: `{ height: number, width: number }`


### Receiving Messages from HubSpot

The SDK provides event handlers for incoming messages:

* **`onReady()`:** HubSpot is ready.
* **`onDialNumber(data)`:** Outbound call initiated.  (See detailed data properties in the original text.)
* **`onEngagementCreated(data)`:** (Deprecated; use `onCreateEngagementSucceeded`) Engagement created.
* **`onNavigateToRecordFailed(data)`:** Navigation to record failed.
* **`onPublishToChannelSucceeded(data)`:** Publishing to channel succeeded.
* **`onPublishToChannelFailed(data)`:** Publishing to channel failed.
* **`onCallerIdMatchSucceeded(event)`:** Caller ID match succeeded.
* **`onCallerIdMatchFailed(event)`:** Caller ID match failed.
* **`onCreateEngagementSucceeded(event)`:** Engagement creation succeeded.
* **`onCreateEngagementFailed(event)`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded(event)`:** Engagement update succeeded.
* **`onUpdateEngagementFailed(event)`:** Engagement update failed.
* **`onVisibilityChanged(data)`:** Widget visibility changed.
* **`defaultEventHandler(event)`:** Default event handler.


## Frequently Asked Questions

* **User Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver (example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls from the HubSpot UI; apps update them.  Apps create engagements for calls outside the HubSpot UI.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:** Functionality can be added to existing marketplace apps.
* **Soft Phone Integration:** Easily integrate existing soft phones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free Users:** All users can install the app.
* **Automatic Updates:** Yes, for existing users.
* **User Installation/Uninstallation:** Restricted by user permissions.
* **Custom Calling Properties:** Yes, via the properties API.
* **Calls from Custom Objects:** Yes, using the SDK and setting `createEngagement: true` in `outgoingCall`.


Remember to replace placeholder links (`LINK_TO_ARTICLE_HERE`, etc.) with the actual URLs.  Also, consider adding more detailed descriptions and examples for each event and function as needed.
