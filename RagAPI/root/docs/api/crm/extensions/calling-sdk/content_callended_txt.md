# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, a JavaScript SDK allowing apps to integrate custom calling options directly into HubSpot CRM records.

## Overview

The Calling Extensions SDK facilitates communication between your app and HubSpot, enabling a seamless calling experience for HubSpot users.  A calling extension comprises three key components:

1. **Calling Extensions SDK:** A JavaScript SDK for app-HubSpot communication.
2. **Calling Settings Endpoints:** Used to configure calling settings for each connected HubSpot account.
3. **Calling iFrame:**  Your app's user interface, configured via the calling settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](link-to-knowledge-base-article).  Once integrated, your app will appear in HubSpot's call switcher.

**Note:** Only outgoing calls are currently supported.  If you need an app, [create one here](link-to-create-app).  If you lack a HubSpot developer account, [sign up here](link-to-signup).


## Getting Started

### Run the Demo Calling App

Two demo apps illustrate SDK usage:

* **`demo-minimal-js`:** A minimal implementation (JavaScript, HTML, CSS).  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more realistic implementation (React, TypeScript, Styled Components).  See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling applications.

### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](link-to-zip) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app, opening a browser tab at `https://localhost:9025/`. You might need to bypass a security warning.


### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands, depending on whether you installed the demo app:

   * **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses methods and event handlers for message exchange.  See the [Events](#events) section for a complete event list.

**SDK Initialization:**

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: event => { /* Dial number received from HubSpot */ },
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

To launch the calling extensions iFrame, HubSpot requires these iFrame parameters:

```javascript
{
  name: string, // App name
  url: string, // App URL
  width: number, // iFrame width
  height: number, // iFrame height
  isReady: boolean, // Ready for production (false during testing)
  supportsCustomObjects: true // Support for calls from custom objects
}
```

### Using the Calling Settings Endpoint

Use your API tool (e.g., Postman) to send a payload to HubSpot's settings API.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your app's information.  Set `isReady` to `false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports PATCH, GET, and DELETE.


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

Use the PATCH endpoint to set `isReady` to `true` after testing:

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"isReady":true}'
```

### Publish Your Calling App to the HubSpot Marketplace

[Details here](link-to-marketplace-details).


## Events

### Sending Messages to HubSpot

The `extensions` object provides methods to send messages:

* **`initialized(payload)`:**  Indicates softphone readiness.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn()`:** User logged in.
* **`userLoggedOut()`:** User logged out.
* **`outgoingCall(callInfo)`:** Outgoing call started.  `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered(payload)`:** Call answered. `payload`: `{ externalCallId: string }`
* **`callEnded(payload)`:** Call ended. `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted(data)`:** Call completed. `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError(data)`:** Error encountered. `data`: `{ message: string }`
* **`resizeWidget(data)`:** Resize the widget. `data`: `{ height: number, width: number }`

Detailed descriptions of each event's properties are provided within the original text.


### Receiving Messages from HubSpot

* **`onReady()`:** HubSpot is ready.
* **`onDialNumber(data)`:** Outbound call triggered.  Data includes `phoneNumber`, `ownerId`, `subjectId`, `objectId`, `objectType`, `portalId`, `countryCode`, `calleeInfo`, `startTimestamp`, `toPhoneNumberSrc`.
* **`onEngagementCreated(data)`:** *(Deprecated. Use `onCreateEngagementSucceeded` instead.)* Engagement created. Data includes `engagementId`.
* **`onNavigateToRecordFailed(data)`:** Navigation to record failed. Data includes `engagementId` and `objectCoordinates`.
* **`onPublishToChannelSucceeded(data)`:** Publishing to channel succeeded. Data includes `engagementId` and `externalCallId`.
* **`onPublishToChannelFailed(data)`:** Publishing to channel failed. Data includes `engagementId` and `externalCallId`.
* **`onCallerIdMatchSucceeded(event)`:** Caller ID match succeeded.
* **`onCallerIdMatchFailed(event)`:** Caller ID match failed.
* **`onCreateEngagementSucceeded(event)`:** Engagement creation succeeded.
* **`onCreateEngagementFailed(event)`:** Engagement creation failed.
* **`onVisibilityChanged(data)`:** Widget visibility changed. Data includes `isMinimized` and `isHidden`.
* **`defaultEventHandler(event)`:** Default event handler.


## Frequently Asked Questions

The original text contains a comprehensive FAQ section covering authentication, CDN hosting, engagement creation/updates, required scopes, app integration (existing vs. new), softphone integration, multiple integrations, free user access, automatic integration display, user installation/uninstallation, custom calling properties, and calls from custom objects.  This section is too extensive to reproduce here but is present in the original text.


Remember to replace placeholder links (`link-to-knowledge-base-article`, `link-to-create-app`, `link-to-signup`, `link-to-zip`, `link-to-marketplace-details`) with the actual links.
