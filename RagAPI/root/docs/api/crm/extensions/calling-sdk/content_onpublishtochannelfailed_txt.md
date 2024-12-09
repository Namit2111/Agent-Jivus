# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK enables apps to offer a customized calling experience directly from CRM records.  It consists of three core components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:**  The visual component of your app displayed to HubSpot users, configured via the calling settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE).  Once integrated, your app will appear in the HubSpot call switcher.  If you lack an app, you can [create one here](LINK_TO_CREATION).  If you don't have a HubSpot developer account, [sign up here](LINK_TO_SIGNUP).


**Note:** Currently, only outgoing calls are supported.


## Getting Started

### Run the Demo Calling App

Two demo apps are available:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and aren't fully functional calling apps.


### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * For `demo-minimal-js`:  `cd demos/demo-minimal-js && npm i && npm start`
   * For `demo-react-ts`:  `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app, opening a browser tab at `https://localhost:9025/`. You might need to bypass a security warning.


### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands (depending on your installation method):

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  See the "Events" section for a complete list.

### Creating an instance:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Logs debug messages to the console.
  eventHandlers: {
    onReady: () => { /* HubSpot is ready. */ },
    onDialNumber: event => { /* HubSpot sends a dial number. */ },
    onCreateEngagementSucceeded: event => { /* Engagement created successfully. */ },
    onEngagementCreatedFailed: event => { /* Engagement creation failed. */ },
    onUpdateEngagementSucceeded: event => { /* Engagement updated successfully. */ },
    onUpdateEngagementFailed: event => { /* Engagement update failed. */ },
    onVisibilityChanged: event => { /* Widget visibility changed. */ }
  }
};

const extensions = new CallingExtensions(options);
```

### iFrame Parameters

To launch the calling extensions iFrame, HubSpot requires these parameters:

```javascript
{
  name: string, // App name
  url: string, // App URL
  width: number, // iFrame width
  height: number, // iFrame height
  isReady: boolean, // Ready for production (defaults to true)
  supportsCustomObjects: true // Whether calls can be placed from custom objects
}
```

### Calling Settings Endpoint

Use your API tool (e.g., Postman) to manage settings via this API endpoint, replacing `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values:

```bash
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint supports `POST`, `PATCH`, `GET`, and `DELETE`.  Set `isReady` to `false` during testing.


### Overriding Extension Settings (localStorage)

For testing:

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

[Learn more here](LINK_TO_MARKETPLACE).


## Events

### Sending Messages to HubSpot

* `initialized`:  Indicates soft phone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Call answered. Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`  `EndStatus` options: `INTERNAL_COMPLETED`, `INTERNAL_FAILED`, `INTERNAL_CANCELED`, `INTERNAL_BUSY`, `INTERNAL_NO_ANSWER`, `INTERNAL_REJECTED`, `INTERNAL_MISSED`
* `callCompleted`: Call completed.  Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`: Error encountered. Payload: `{ message: string }`
* `resizeWidget`: Resize the widget. Payload: `{ height: number, width: number }`


### Receiving Messages from HubSpot

* `onReady`: HubSpot is ready.  Payload includes `engagementId`, `iframeLocation`, `ownerId`, `portalId`, and `userId`.
* `onDialNumber`: Outbound call triggered.  Payload includes `phoneNumber`, `ownerId`, `subjectId`, `objectId`, `objectType`, `portalId`, `countryCode`, `calleeInfo`, `startTimestamp`, and `toPhoneNumberSrc`.
* `onEngagementCreated` (Deprecated): Use `onCreateEngagementSucceeded` instead. Payload: `{ engagementId: number }`
* `onNavigateToRecordFailed`: Navigation to record failed. Payload: `{ engagementId: number, objectCoordinates: object }`
* `onPublishToChannelSucceeded`: Publishing to channel succeeded. Payload: `{ engagementId: number, externalCallId: string }`
* `onPublishToChannelFailed`: Publishing to channel failed. Payload: `{ engagementId: number, externalCallId: string }`
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement creation succeeded.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onVisibilityChanged`: Widget visibility changed. Payload: `{ isMinimized: boolean, isHidden: boolean }`
* `defaultEventHandler`: Default event handler.


## Frequently Asked Questions

* **Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver.  Example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; apps update them.  Apps create engagements for calls outside the HubSpot UI.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Marketplace Apps:** Functionality can be added to existing apps.
* **Existing Softphone Integration:** Easily integrated.
* **Multiple Integrations:** Yes.
* **Free User Installation:** Yes.
* **Automatic Integration Appearance:** Yes, for existing app users.
* **User Installation/Uninstallation:** Only users with necessary permissions.
* **Custom Calling Properties:** Yes, via the properties API.
* **Calls from Custom Objects:** Yes, using the SDK.  Ensure `createEngagement: true` in `outgoingCall`.


Remember to replace placeholder links (`LINK_TO_ARTICLE`, `LINK_TO_CREATION`, `LINK_TO_ZIP`, `LINK_TO_MARKETPLACE`) with the actual URLs.
