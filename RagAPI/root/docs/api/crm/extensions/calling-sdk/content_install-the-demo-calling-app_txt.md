# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling functionalities into their HubSpot applications.

## Overview

The Calling Extensions SDK allows apps to offer a custom calling experience directly from CRM records within HubSpot.  It consists of three key parts:

* **Calling Extensions SDK (JavaScript SDK):** Facilitates communication between your app and HubSpot.
* **Calling Settings Endpoints:** Used to configure your app's calling settings for each connected HubSpot account.
* **Calling iFrame:**  The interface displayed to HubSpot users, configured via the settings endpoints.


For details on the in-app calling experience, refer to [this knowledge base article](LINK_TO_KNOWLEDGE_BASE_ARTICLE).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.  If you don't have a HubSpot app, you can [create one here](LINK_TO_CREATE_APP).  If you need a HubSpot developer account, sign up [here](LINK_TO_SIGN_UP).


## Getting Started

### Run the Demo Calling App

Two demo apps illustrate SDK usage:

* **`demo-minimal-js`:** A minimal JavaScript, HTML, and CSS implementation.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more robust example using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.

### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP) of the repository.
3. Navigate to the project's root directory in your terminal.
4. Run one of the following commands:

   * **`demo-minimal-js`**:  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`**: `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app.  The app should open in your browser at `https://localhost:9025/`. You might need to bypass a security warning.

### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console and run one of these commands:

   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

3. Refresh the page. Click the "Call" icon, select the demo app from the "Call from" dropdown, and click "Call".


### Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses events for communication.  See the [Events section](#events) for a complete list.

### SDK API

Begin by creating a `CallingExtensions` object.  You can define custom behavior using an options object:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Log debug messages to the console
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

To display the calling extension iFrame, HubSpot requires these iFrame parameters:

```javascript
{
  name: "Your App Name",
  url: "Your App URL",
  width: 400,
  height: 600,
  isReady: false, // Set to false during testing
  supportsCustomObjects: true
}
```

### Using the Calling Settings Endpoint

Use your API tool (e.g., Postman) to send a POST request to HubSpot's settings API. Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your app's details.  The `isReady` flag should be `false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports PATCH, GET, and DELETE.

### Override Extension Settings using `localStorage`

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

Set `isReady` to `true` using the PATCH endpoint:

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"isReady":true}'
```

### Publish to the HubSpot Marketplace

[Learn how to publish your app to the HubSpot Marketplace here](LINK_TO_MARKETPLACE_PUBLISHING).


## Events

### Sending Messages to HubSpot

The `extensions` object provides methods to send messages:

* **`initialized(payload)`:**  Signals softphone readiness.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn()`:**  User login notification.
* **`userLoggedOut()`:** User logout notification.
* **`outgoingCall(callInfo)`:**  Outgoing call started. `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered(payload)`:** Outgoing call answered. `payload`: `{ externalCallId: string }`
* **`callEnded(payload)`:** Call ended. `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted(data)`:** Call completed. `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError(data)`:** Error occurred. `data`: `{ message: string }`
* **`resizeWidget(data)`:** Resize the widget. `data`: `{ height: number, width: number }`


### Receiving Messages from HubSpot

The `extensions` object's event handlers receive messages:

* **`onReady()`:** HubSpot is ready.
* **`onDialNumber(data)`:** Outbound call initiated.  (See detailed data properties below)
* **`onEngagementCreated(data)`:** (Deprecated; use `onCreateEngagementSucceeded`) Engagement created.
* **`onNavigateToRecordFailed(data)`:** Navigation to a record failed.
* **`onPublishToChannelSucceeded(data)`:** Publishing to a channel succeeded.
* **`onPublishToChannelFailed(data)`:** Publishing to a channel failed.
* **`onCallerIdMatchSucceeded(event)`:** Caller ID match succeeded.
* **`onCallerIdMatchFailed(event)`:** Caller ID match failed.
* **`onCreateEngagementSucceeded(event)`:** Engagement creation succeeded.
* **`onCreateEngagementFailed(event)`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded(event)`:** Engagement update succeeded.
* **`onUpdateEngagementFailed(event)`:** Engagement update failed.
* **`onVisibilityChanged(data)`:** Widget visibility changed.
* **`defaultEventHandler(event)`:** Default event handler.


**`onDialNumber` Data Properties:**

| Property          | Type     | Description                                                                                                    |
|-------------------|----------|----------------------------------------------------------------------------------------------------------------|
| `phoneNumber`     | String   | Phone number dialed.                                                                                             |
| `ownerId`         | Number   | ID of the logged-in user.                                                                                       |
| `subjectId`       | Number   | ID of the subject.                                                                                             |
| `objectId`        | Number   | ID of the object.                                                                                             |
| `objectType`      | String   | Object type ("CONTACT" or "COMPANY").                                                                           |
| `portalId`        | Number   | ID of the HubSpot portal.                                                                                       |
| `countryCode`     | String   | Country code.                                                                                                |
| `calleeInfo`      | Object   | `{ calleeId: number, calleeObjectTypeId: string }`                                                             |
| `startTimestamp`  | Number   | Call start timestamp.                                                                                           |
| `toPhoneNumberSrc` | String   | Name of the phone number property in HubSpot.                                                                  |


## Frequently Asked Questions

* **User Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls from the HubSpot UI; apps update them. Apps create engagements for calls originating outside the HubSpot UI.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:** Functionality can be added to existing marketplace apps.
* **Softphone Integration:** Easily integrate existing softphones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Integration Appearance:** Yes, for updated apps.
* **App Installation/Uninstallation:** Controlled by user permissions.
* **Custom Calling Properties:** Yes, via the properties API.
* **Calls from Custom Objects:** Yes, if using the SDK to create calls and setting `createEngagement: true` in the `outgoingCall` event.


This markdown provides a structured and comprehensive documentation of the HubSpot Calling Extensions SDK.  Remember to replace placeholder links (`LINK_TO_...`) with the actual URLs.
