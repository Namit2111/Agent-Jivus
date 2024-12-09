# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into HubSpot.

## Overview

The Calling Extensions SDK enables apps to provide a custom calling experience directly from CRM records.  It consists of three core components:

* **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
* **Calling Settings Endpoints (API):** Configure calling settings for each connected HubSpot account.
* **Calling iframe:**  Displays your app to HubSpot users; configured via the settings endpoints.


For details on the in-app calling experience, see [this knowledge base article](link-to-knowledge-base-article).  Once integrated, your app appears in HubSpot's call switcher.

Only outgoing calls are currently supported.  If you need an app, [create one via your HubSpot developer account](link-to-hubspot-developer-account).  If you lack a developer account, [sign up here](link-to-signup).

## Getting Started

### Demo Apps

Two demo apps illustrate SDK usage:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:**  More realistic implementation using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** Demo apps use mock data and aren't fully functional calling applications.

### Installing the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](link-to-zip) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app (accessing it may require bypassing a security warning at `https://localhost:9025/`).

### Launching the Demo App from HubSpot

1. Navigate to HubSpot contacts (Contacts > Contacts) or companies (Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands, depending on whether you installed the demo app:

   * **Installed (`demo-minimal-js` or `demo-react-ts`):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call."

### Installing the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses messages exchanged via methods and event handlers.  See the [Events section](#events) for a complete list.

### SDK Initialization

Create a `CallingExtensions` instance:

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

To launch the iframe, provide these parameters to HubSpot:

```javascript
{
  name: string, // App name
  url: string, // App URL
  width: number, // IFrame width
  height: number, // IFrame height
  isReady: boolean, // Ready for production (false during testing)
  supportsCustomObjects: true // Whether calls from custom objects are supported
}
```


### Calling Settings Endpoint

Use your API tool (e.g., Postman) to send a payload to HubSpot's settings API. Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  `isReady` should be `false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports PATCH, GET, and DELETE.

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

### Getting Your App Ready for Production

Set `isReady` to `true` using the PATCH endpoint:

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"isReady":true}'
```

### Publishing to the Marketplace

[Publish your app to the HubSpot marketplace](link-to-marketplace-publishing).


## Events

### Sending Messages to HubSpot

The `extensions` object provides methods to send messages:

* **`initialized(payload)`:**  Indicates softphone readiness.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn()`:** User login notification.
* **`userLoggedOut()`:** User logout notification.
* **`outgoingCall(callInfo)`:** Outgoing call started.  `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered(payload)`:** Call answered. `payload`: `{ externalCallId: string }`
* **`callEnded(payload)`:** Call ended. `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted(data)`:** Call completed. `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: {[key: string]: string}, externalCallId: number }`
* **`sendError(data)`:** Error encountered. `data`: `{ message: string }`
* **`resizeWidget(data)`:** Resize the widget. `data`: `{ height: number, width: number }`


### Receiving Messages from HubSpot

Event handlers receive messages from HubSpot:

* **`onReady()`:** HubSpot is ready.
* **`onDialNumber(data)`:** Outbound call triggered.
* **`onEngagementCreated(data)`:** (Deprecated) Engagement created.
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


Detailed descriptions of event payloads are provided within the document.


## Frequently Asked Questions

This section answers common questions about the SDK.  Refer to the provided document for detailed answers.


## Appendix:  Data Structures and Types

Detailed descriptions of data types used throughout the API and SDK are included within the original document.  For example,  `EndStatus` enumeration,  `CONTACT | COMPANY` object types, and parameters for individual event handlers are described.
