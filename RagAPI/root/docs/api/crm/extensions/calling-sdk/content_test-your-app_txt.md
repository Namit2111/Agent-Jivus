# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot directly from CRM records.

## Overview

The Calling Extensions SDK facilitates communication between your application and HubSpot, providing a custom calling experience for HubSpot users.  It comprises three key components:

* **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
* **Calling Settings Endpoints (API):** Configure calling settings for your app on a per-HubSpot account basis.
* **Calling iFrame:** The interface displayed to HubSpot users, configured via the calling settings endpoints.

For details on the in-app calling experience, see [this knowledge base article](LINK_TO_ARTICLE).  After integration, your app will appear in the HubSpot call switcher.

**Note:** Only outgoing calls are currently supported.


## Getting Started

### 1. Create a HubSpot App

If you don't have an app, [create one from your HubSpot developer account](LINK_TO_CREATION). If you lack a developer account, [sign up here](LINK_TO_SIGNUP).


### 2. Run the Demo Calling App

Test the SDK using two demo apps:

* **`demo-minimal-js`:** A minimal JavaScript, HTML, and CSS implementation. See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive implementation using React, TypeScript, and Styled Components.  See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling applications.

### 3. Install the Demo App (Optional)

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP) of the repository.
3. Navigate to the project's root directory.
4. Run the following command (replace with appropriate demo):

   For `demo-minimal-js`:  `cd demos/demo-minimal-js && npm i && npm start`
   For `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`

   This installs dependencies and starts the app at `https://localhost:9025/`. You may need to bypass a security warning.


### 4. Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console.
3. Run the following `localStorage` command (choose the appropriate option based on whether you installed the demo app):

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page, click the "Call" icon, select the demo app from the "Call from" dropdown, and click "Call".


### 5. Install the Calling Extensions SDK

Add the SDK as a dependency to your calling app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture for communication.

### Events

#### Sending Messages to HubSpot

* `initialized`: Softphone ready for interaction.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Outgoing call answered. Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`: Error encountered. Payload: `{ message: string }`
* `resizeWidget`: Resize the widget. Payload: `{ height: number, width: number }`

#### Receiving Messages from HubSpot

* `onReady`: HubSpot is ready.
* `onDialNumber`: Outbound call triggered in HubSpot.
* `onEngagementCreated` (Deprecated; use `onCreateEngagementSucceeded`): Engagement created.
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

### SDK Initialization

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, //optional
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Calling Settings Endpoint

Use the API to set your app's settings (e.g., using `curl`):

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

The `isReady` flag indicates production readiness (set to `false` during testing).  The endpoint also supports PATCH, GET, and DELETE.


### Local Storage Override (for testing)

Override settings using the browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production Deployment

Set `isReady` to `true` using the PATCH endpoint.

### Publishing to the Marketplace

[Learn how to publish your app to the HubSpot marketplace](LINK_TO_MARKETPLACE).


## Frequently Asked Questions

* **Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver.
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; the app updates them afterward.  For calls initiated outside HubSpot, the app should create the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:**  Functionality can be added to existing marketplace apps.
* **Softphone Integration:** Easily integrable.
* **Multiple Integrations:**  Users can use multiple integrations simultaneously.
* **Free User Access:** Yes.
* **Automatic Integration Appearance:** Yes, for updated apps.
* **User Installation/Uninstallation:** Restricted by user permissions.
* **Custom Calling Properties:** Creatable via the properties API.
* **Calls from Custom Objects:** Possible using the SDK and setting `createEngagement: true` in the `outgoingCall` event.

## Appendix:  Detailed Event Descriptions

[Include a table summarizing all the events, their parameters, and descriptions here.  This would be a large table and is best generated from a structured data source if possible.]


This markdown document provides a comprehensive overview of the HubSpot Calling Extensions SDK. Remember to replace placeholder links (`LINK_TO_ARTICLE`, `LINK_TO_CREATION`, `LINK_TO_SIGNUP`, `LINK_TO_ZIP`, `LINK_TO_MARKETPLACE`) with the actual links.  Also, create the detailed event table mentioned in the appendix.
