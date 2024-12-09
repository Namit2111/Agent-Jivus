# HubSpot Calling Extensions SDK Documentation

This document provides comprehensive information on the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling functionalities within HubSpot.

## Overview

The Calling Extensions SDK facilitates communication between your application and HubSpot, offering users a custom calling option directly from CRM records.  It comprises three key components:

* **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
* **Calling Settings Endpoints (API):** Configure calling settings for your app on a per-HubSpot account basis.
* **Calling iFrame:**  Displays your app to HubSpot users; its configuration is managed via the calling settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE).  Once integrated, your app will appear in HubSpot's call switcher.

**Note:** Currently, only outgoing calls are supported.  If you lack an app, you can [create one from your HubSpot developer account](LINK_TO_CREATING_APP).  If you don't have a developer account, sign up [here](LINK_TO_SIGNUP).


## Getting Started

### Run the Demo Calling Apps

Two demo apps showcase the SDK:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more realistic implementation using React, TypeScript, and Styled Components.  See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling applications.


### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP) of the repository.
3. Navigate to the project's root directory in your terminal.
4. Run one of the following commands:

   * **`demo-minimal-js`:**  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

   This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console and run one of these commands:

   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

3. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Install the Calling Extensions SDK

Add the SDK as a dependency to your app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses methods and event handlers for message exchange.  See the **Events** section for a complete list.


### Events

#### Sending Messages to HubSpot

* **`initialized`**:  Signals softphone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn`**:  Signals user login.
* **`userLoggedOut`**: Signals user logout.
* **`outgoingCall`**: Notifies HubSpot of an outgoing call. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered`**: Notifies HubSpot that a call is answered. Payload: `{ externalCallId: string }`
* **`callEnded`**: Notifies HubSpot of call end. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted`**:  Notifies HubSpot of call completion.  Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError`**: Reports an error. Payload: `{ message: string }`
* **`resizeWidget`**: Requests widget resizing. Payload: `{ height: number, width: number }`

#### Receiving Messages from HubSpot

* **`onReady`**: HubSpot is ready to receive messages. Payload includes: `engagementId`, `iframeLocation`, `ownerId`, `portalId`, `userId`.
* **`onDialNumber`**:  Triggered by an outbound call from HubSpot.  Payload includes: `phoneNumber`, `ownerId`, `subjectId`, `objectId`, `objectType`, `portalId`, `countryCode`, `calleeInfo`, `startTimestamp`, `toPhoneNumberSrc`.
* **`onEngagementCreated`**: *(Deprecated)* Use `onCreateEngagementSucceeded` instead.
* **`onNavigateToRecordFailed`**: Called when record navigation fails. Payload includes: `engagementId`, `objectCoordinates`.
* **`onPublishToChannelSucceeded`**: Called when publishing to a channel succeeds. Payload includes: `engagementId`, `externalCallId`.
* **`onPublishToChannelFailed`**: Called when publishing to a channel fails. Payload includes: `engagementId`, `externalCallId`.
* **`onCallerIdMatchSucceeded`**: Called when caller ID match succeeds.
* **`onCallerIdMatchFailed`**: Called when caller ID match fails.
* **`onCreateEngagementSucceeded`**: HubSpot engagement creation succeeded.
* **`onCreateEngagementFailed`**: HubSpot engagement creation failed.
* **`onUpdateEngagementSucceeded`**: HubSpot engagement update succeeded.
* **`onUpdateEngagementFailed`**: HubSpot engagement update failed.
* **`onVisibilityChanged`**: Widget visibility changed. Payload: `{ isMinimized: boolean, isHidden: boolean }`
* **`defaultEventHandler`**: Default event handler.


###  Example SDK Instantiation

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // optional
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: event => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```


### Testing Your App

To launch the calling extensions iframe, HubSpot requires these iframe parameters:

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


### Using the Calling Settings Endpoint

Use your API tool (e.g., Postman) to send payloads to HubSpot's settings API.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  The `isReady` flag should be `false` during testing.

```bash
curl --request POST \
     --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports PATCH, GET, and DELETE.


### Overriding Extension Settings using localStorage

For testing, override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


### Getting Your App Ready for Production

Set `isReady` to `true` using the PATCH endpoint:

```bash
curl --request PATCH \
     --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '{"isReady":true}'
```


### Publishing to the HubSpot Marketplace

[Details on publishing your app to the HubSpot marketplace can be found here](LINK_TO_MARKETPLACE_DETAILS).


## Frequently Asked Questions

* **How is user authentication handled?**  Your app handles authentication.
* **Is Calling Extensions hosted on a CDN?** Yes, via jsDeliver. Example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`
* **When to create vs. update engagements?** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them.  For calls outside HubSpot, your app creates engagements.
* **Required scopes?** `contacts` and `timeline`.
* **Add to existing app or create new one?**  You can add this to an existing app.
* **Integrate existing softphone?** Yes.
* **Multiple integrations simultaneously?** Yes.
* **Can free users install?** Yes.
* **Automatic appearance after installation?** Yes.
* **Who can install/uninstall?** Only users with necessary permissions.  [Learn more about user permissions](LINK_TO_PERMISSIONS).
* **Custom calling properties?** Yes, using the properties API.
* **Calls from custom objects?** Yes, if using the SDK to create calls and notifying HubSpot via `outgoingCall` with `createEngagement: true`.


Remember to replace placeholder links (`LINK_TO_ARTICLE`, `LINK_TO_CREATING_APP`, `LINK_TO_SIGNUP`, `LINK_TO_ZIP`, `LINK_TO_MARKETPLACE_DETAILS`, `LINK_TO_PERMISSIONS`) with the actual links.
