# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options directly into HubSpot CRM records.

## Overview

The Calling Extensions SDK facilitates communication between your application and HubSpot, enabling a custom calling experience for HubSpot users.  It comprises three key components:

1. **Calling Extensions SDK (JavaScript):**  The core SDK enabling communication.
2. **Calling Settings Endpoints (API):**  Used to configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:**  The interface displayed to HubSpot users, configured via the settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](link-to-knowledge-base-article-here).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Only outgoing calls are currently supported.  If you don't have a HubSpot app, you can [create one here](link-to-create-app-here).  If you need a HubSpot developer account, sign up [here](link-to-signup-here).


## Getting Started

### Run the Demo Calling App

Two demo apps are available:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more robust implementation using React, TypeScript, and Styled Components.  See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling applications.


### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](link-to-zip-here) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * For `demo-minimal-js`:  `cd demos/demo-minimal-js && npm i && npm start`
   * For `demo-react-ts`:  `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands, depending on whether you installed the demo app:

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page and select the demo app from the "Call from" dropdown in the call switcher.


### Install the Calling Extensions SDK

Add the SDK to your app as a Node.js dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  Events are sent and received via methods and event handlers.


### Events

#### Sending Messages to HubSpot

* **`initialized`:**  Indicates softphone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn`:**  Notifies HubSpot of user login.
* **`userLoggedOut`:**  Notifies HubSpot of user logout.
* **`outgoingCall`:**  Notifies HubSpot of an outgoing call.  Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered`:**  Notifies HubSpot that a call was answered.  Payload: `{ externalCallId: string }`
* **`callEnded`:**  Notifies HubSpot that a call ended.  Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted`:**  Notifies HubSpot that a call is complete. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError`:** Reports errors.  Payload: `{ message: string }`
* **`resizeWidget`:** Requests widget resizing.  Payload: `{ height: number, width: number }`


#### Receiving Messages from HubSpot

* **`onReady`:** HubSpot is ready.  Payload: `{ engagementId: number, iframeLocation: Enum, ownerId: String | Number, portalId: Number, userId: Number }`
* **`onDialNumber`:** Outbound call initiated.
* **`onEngagementCreated` (deprecated):** Use `onCreateEngagementSucceeded` instead.
* **`onNavigateToRecordFailed`:**  Navigation to a record failed.
* **`onPublishToChannelSucceeded`:** Publishing to a channel succeeded.
* **`onPublishToChannelFailed`:** Publishing to a channel failed.
* **`onCallerIdMatchSucceeded`:** Caller ID match successful.
* **`onCallerIdMatchFailed`:** Caller ID match failed.
* **`onCreateEngagementSucceeded`:** Engagement creation successful.
* **`onCreateEngagementFailed`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded`:** Engagement update successful.
* **`onUpdateEngagementFailed`:** Engagement update failed.
* **`onVisibilityChanged`:** Widget visibility changed.
* **`defaultEventHandler`:** Default event handler.


### SDK Initialization

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, //Optional
  eventHandlers: {
    onReady: () => { /*...*/ },
    onDialNumber: event => { /*...*/ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```


### Test Your App

To launch the calling iFrame, HubSpot requires these parameters:

```json
{
  "name": string,
  "url": string,
  "width": number,
  "height": number,
  "isReady": boolean,
  "supportsCustomObjects": true
}
```

### Using the Calling Settings Endpoint

Use the API to manage your app's settings.  Remember to use your `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`. The `isReady` flag should be `false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.


### Override Settings Using localStorage

For testing, you can override settings in your browser's developer console:

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

[Instructions for publishing](link-to-marketplace-publishing-instructions-here).


## Frequently Asked Questions

* **User Authentication:** Handled by your app.
* **CDN Hosting:** Yes, via jsDeliver (example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them.  For calls outside HubSpot, your app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Adding to Existing App:** Yes, possible.
* **Integrating Existing Softphone:** Yes, straightforward integration.
* **Multiple Integrations:** Yes, users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Integration Appearance:** Yes, for updates to existing installations.
* **User Installation/Uninstallation:** Controlled by user permissions.
* **Custom Calling Properties:** Yes, via the properties API.
* **Calls from Custom Objects:** Yes, using the SDK.  Ensure `createEngagement: true` in `outgoingCall`.


## Feedback

[Link to feedback form](link-to-feedback-form-here)
