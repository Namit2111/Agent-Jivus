# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into HubSpot CRM.

## Overview

The Calling Extensions SDK enables apps to provide a custom calling experience directly from CRM records.  It consists of three main components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Configure settings for your app on a per-HubSpot account basis.
3. **Calling iFrame:** The interface your app presents to HubSpot users, configured via the settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](replace_with_actual_link).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Only outgoing calls are currently supported.  To build an app, create one from your [HubSpot developer account](replace_with_actual_link). If you need an account, sign up [here](replace_with_actual_link).

## Getting Started

### Demo Apps

Test the SDK using two demo apps:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more robust example using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:**  These demos use mock data and aren't fully functional calling apps.

### Installing the Demo App

1. Install Node.js.
2. Clone, fork, or download the ZIP of the repository.
3. Navigate to the project's root directory.
4. Run:
    * For `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
    * For `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launching the Demo App from HubSpot

1. Go to your HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands, depending on your installation method:
    * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page and select the demo app from the "Call from" dropdown in the call switcher.

### Installing the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses a simple API for message exchange via methods and event handlers.  See the [Events section](#events) for a full list.

### SDK Initialization

Create a `CallingExtensions` instance, defining behavior via an options object and `eventHandlers`:

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
    onVisibilityChanged: event => { /* Widget visibility changed */ },
  }
};

const extensions = new CallingExtensions(options);
```

### Testing Your App

To launch the calling extension iframe, HubSpot requires these iframe parameters:

```json
{
  "name": "string", // App name
  "url": "string", // App URL
  "width": number, // iFrame width
  "height": number, // iFrame height
  "isReady": boolean, // Ready for production (false during testing)
  "supportsCustomObjects": true //Support calls from custom objects
}
```

### Calling Settings Endpoint

Use the settings API (e.g., with Postman) to set your app's settings.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  Set `isReady` to `false` during testing.

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

### Preparing for Production

Set `isReady` to `true` using the `PATCH` endpoint once your app is ready.

### Publishing to the HubSpot Marketplace

Publish your app to the marketplace [here](replace_with_actual_link).  This step is optional if the app is for internal use only.

## Events

### Sending Messages to HubSpot

The `extensions` object provides methods to send messages:

* **`initialized(payload)`:**  Indicates the softphone is ready.  `payload` includes `isLoggedIn` (boolean) and `engagementId` (number).
* **`userLoggedIn()`:** User logged in.
* **`userLoggedOut()`:** User logged out.
* **`outgoingCall(callInfo)`:** Outgoing call started.  `callInfo` includes `callStartTime` (number), `createEngagement` (boolean), `toNumber` (string), and `fromNumber` (string).
* **`callAnswered(payload)`:** Outgoing call answered.  `payload` includes `externalCallId` (string).
* **`callEnded(payload)`:** Call ended.  `payload` includes `externalCallId` (string), `engagementId` (number), and `callEndStatus` (enumeration).
* **`callCompleted(data)`:** Call completed.  `data` includes `engagementId`, `hideWidget` (boolean), `engagementProperties` (object), and `externalCallId`.
* **`sendError(data)`:** Error encountered.  `data` includes `message` (string).
* **`resizeWidget(data)`:** Resize the widget.  `data` includes `height` and `width` (numbers).

### Receiving Messages from HubSpot

The SDK provides event handlers for inbound messages:

* **`onReady()`:** HubSpot is ready.
* **`onDialNumber(data)`:** Outbound call triggered.  `data` includes detailed call information.
* **`onEngagementCreated(data)`:** (Deprecated) Engagement created. Use `onCreateEngagementSucceeded` instead.
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

* **Authentication:** The calling app handles authentication.
* **CDN Hosting:** Yes, via jsDeliver.  Example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; apps update them afterward.  Apps create engagements for calls initiated outside the UI.
* **Required Scopes:** `contacts` and `timeline`.
* **Adding to Existing Apps:** Yes, you can add this functionality to existing marketplace apps.
* **Integrating Existing Softphones:** Yes, integration is straightforward.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Appearance:** Yes, if the app is already installed.
* **User Installation/Uninstallation:** Only users with appropriate permissions.
* **Custom Calling Properties:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, if the SDK is used to create calls and `outgoingCall({ createEngagement: true })` is used.


This markdown provides a comprehensive overview of the HubSpot Calling Extensions SDK.  Remember to replace placeholder links with the actual links.
