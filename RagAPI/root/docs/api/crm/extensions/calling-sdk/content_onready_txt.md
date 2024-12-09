# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into HubSpot CRM.

## Overview

The Calling Extensions SDK enables apps to provide a custom calling option directly from CRM records.  It consists of three main components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Configure calling settings for your app on a per-HubSpot account basis.
3. **Calling iFrame:**  Your app's interface within HubSpot, configured using the settings endpoints.

For a detailed understanding of the in-app calling experience, refer to [this knowledge base article](placeholder_link_to_knowledge_base).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Only outgoing calls are currently supported.  If you need an app, you can [create one here](placeholder_link_to_create_app).  If you don't have a HubSpot developer account, sign up [here](placeholder_link_to_signup).


## Getting Started

### Run the Demo Calling App

Two demo apps are available:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive implementation using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.

### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](placeholder_link_to_zip) of the repository.
3. Navigate to the project root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`:**  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

   This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.

### Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands based on your installation method:

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.  Select the demo app from the "Call from" dropdown in the call switcher.

### Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses events for communication.  See the [Events section](#events) for a complete list.

**SDK Initialization:**

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: event => { /* Dial number event */ },
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

To launch the calling iFrame, HubSpot requires these parameters:

```json
{
  "name": "Your App Name",
  "url": "Your App URL",
  "width": 400,
  "height": 600,
  "isReady": false, // Set to false during testing
  "supportsCustomObjects": true
}
```

### Using the Calling Settings Endpoint

Use the following API call to configure your app (replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`):

```bash
curl --request POST \
     --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`. Set `isReady` to `true` for production.

### Override Extension Settings (localStorage)

For testing, override settings using your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Get Your App Ready for Production

Set `isReady` to `true` using the `PATCH` endpoint.

### Publish to the HubSpot Marketplace

[Learn how to publish your app](placeholder_link_to_marketplace_publishing).


## Events

### Sending Messages to HubSpot

* **`initialized`**:  Indicates softphone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn`**: User login notification.
* **`userLoggedOut`**: User logout notification.
* **`outgoingCall`**: Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered`**: Outgoing call answered. Payload: `{ externalCallId: string }`
* **`callEnded`**: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted`**: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: object, externalCallId: number }`
* **`sendError`**: Error notification. Payload: `{ message: string }`
* **`resizeWidget`**: Resize request. Payload: `{ height: number, width: number }`


### Receiving Messages from HubSpot

* **`onReady`**: HubSpot is ready.
* **`onDialNumber`**: Outbound call initiated.
* **`onEngagementCreated`**: (Deprecated. Use `onCreateEngagementSucceeded`) Engagement created.
* **`onNavigateToRecordFailed`**: Navigation to record failed.
* **`onPublishToChannelSucceeded`**: Publishing to channel succeeded.
* **`onPublishToChannelFailed`**: Publishing to channel failed.
* **`onCallerIdMatchSucceeded`**: Caller ID match succeeded.
* **`onCallerIdMatchFailed`**: Caller ID match failed.
* **`onCreateEngagementSucceeded`**: Engagement creation succeeded.
* **`onCreateEngagementFailed`**: Engagement creation failed.
* **`onUpdateEngagementSucceeded`**: Engagement update succeeded.
* **`onUpdateEngagementFailed`**: Engagement update failed.
* **`onVisibilityChanged`**: Widget visibility changed.
* **`defaultEventHandler`**: Default event handler.


## Frequently Asked Questions

* **Authentication:** The calling app handles authentication.
* **CDN Hosting:** Yes, via jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the UI; apps update them afterward.  Apps create engagements for calls initiated outside the UI.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Marketplace Apps:**  Functionality can be added to existing apps.
* **Softphone Integration:** Easily integrate existing softphones.
* **Multiple Integrations:** Yes, users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Integration Display:** Yes, for updated apps.
* **User Installation/Uninstallation:**  Only users with necessary permissions.
* **Custom Calling Properties:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, if using the SDK and setting `createEngagement: true` in `outgoingCall`.


Remember to replace placeholder links with the actual links.  This comprehensive markdown document provides a structured and detailed explanation of the HubSpot Calling Extensions SDK.
