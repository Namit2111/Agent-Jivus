# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot CRM records.

## Overview

The Calling Extensions SDK enables apps to provide a custom calling experience directly from CRM records.  It consists of three main parts:

* **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
* **Calling Settings Endpoints:** Used to configure your app's settings for each connected HubSpot account.
* **Calling IFrame:**  The interface your app presents to HubSpot users, configured via the settings endpoints.

**Note:** Only outgoing calls are currently supported.  HubSpot now handles call engagement creation and updates automatically; manual management is no longer required.  For more on the in-app calling experience, see [this knowledge base article](LINK_TO_KNOWLEDGE_BASE_ARTICLE).


## Getting Started

### Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal JavaScript, HTML, and CSS implementation.  SDK instantiation is shown in `index.js`.
* **`demo-react-ts`:** A more realistic implementation using React, TypeScript, and Styled Components. SDK instantiation is in `useCti.ts`.

**Note:** These demos use mock data and are not fully functional calling apps.


### Installing the Demo App

1. Install Node.js.
2. Clone, fork, or download the ZIP of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`:**  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

   This installs dependencies and starts the app, opening a browser tab at `https://localhost:9025/` (you may need to bypass a security warning).


### Launching the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console and run one of the following commands:

   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

3. Refresh the page, click the "Call" icon, select the demo app from the "Call from" dropdown, and click "Call".


### Installing the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses events for communication.  See the "Events" section for a complete list.

### SDK Initialization

Create a `CallingExtensions` object, defining behavior with an options object, including `eventHandlers`:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: event => { /* Dial number received from HubSpot */ },
    onCreateEngagementSucceeded: event => { /* Engagement created successfully */ },
    onEngagementCreatedFailed: event => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: event => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: event => { /* Engagement update failed */ },
    onVisibilityChanged: event => { /* Widget visibility changed */ }
  }
};

const extensions = new CallingExtensions(options);
```

### Testing Your App

To launch the calling extensions iFrame, provide these parameters to HubSpot:

```json
{
  "name": "string", // App name
  "url": "string", // App URL
  "width": number, // IFrame width
  "height": number, // IFrame height
  "isReady": boolean, // Ready for production (false during testing)
  "supportsCustomObjects": true // Whether calls can originate from custom objects
}
```

### Using the Calling Settings Endpoint

Use the API (e.g., Postman) to manage settings.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  `isReady: false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports PATCH, GET, and DELETE.


### Overriding Extension Settings (localStorage)

For testing, override settings in the browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Preparing for Production

Set `isReady` to `true` using the PATCH endpoint.


### Publishing to the HubSpot Marketplace

Once ready, publish your app to the HubSpot Marketplace.  Details are available [here](LINK_TO_MARKETPLACE_DETAILS).


## Events

### Sending Messages to HubSpot

* `initialized`:  Soft phone ready.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started.  Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Call answered.  Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`: Error encountered. Payload: `{ message: string }`
* `resizeWidget`: Resize the widget. Payload: `{ height: number, width: number }`


### Receiving Messages from HubSpot

* `onReady`: HubSpot is ready.
* `onDialNumber`: Outbound call initiated in HubSpot.
* `onEngagementCreated`: (Deprecated; use `onCreateEngagementSucceeded`) Engagement created.
* `onNavigateToRecordFailed`: Navigation to record failed.
* `onPublishToChannelSucceeded`: Publishing to channel succeeded.
* `onPublishToChannelFailed`: Publishing to channel failed.
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement creation succeeded.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Default event handler.


## Frequently Asked Questions

* **Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver (example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; apps update them.  Apps create engagements for calls outside the HubSpot UI.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:**  Functionality can be added to existing marketplace apps.
* **Integrating Existing Softphones:** Easily integrable.
* **Multiple Integrations:** Yes, users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Integration Appearance:** Yes, for updated apps.
* **User Installation/Uninstallation:** Only users with necessary permissions.
* **Custom Calling Properties:** Yes, via the properties API.
* **Calls from Custom Objects:** Yes, if using the SDK to create calls and setting `createEngagement: true` in the `outgoingCall` event.


This markdown documentation provides a comprehensive overview of the HubSpot CRM API Calling Extensions SDK, including setup, usage, event handling, and frequently asked questions.  Remember to replace placeholder links (`LINK_TO_KNOWLEDGE_BASE_ARTICLE`, `LINK_TO_MARKETPLACE_DETAILS`, etc.) with the actual URLs.
