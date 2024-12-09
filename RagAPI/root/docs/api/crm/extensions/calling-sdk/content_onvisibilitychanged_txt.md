# HubSpot Calling Extensions SDK Documentation

This document provides comprehensive information on the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling options into their HubSpot apps.

## Overview

The Calling Extensions SDK allows apps to offer a customized calling experience directly from CRM records within HubSpot.  It consists of three core components:

* **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
* **Calling Settings Endpoints:**  Used to configure your app's calling settings for each connected HubSpot account.
* **Calling iFrame:** The interface displayed to HubSpot users, configured through the calling settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](<replace with actual link>).  Once integrated, your app will appear in HubSpot's call switcher.  If you lack an app, you can [create one via your HubSpot developer account](<replace with actual link>).  New HubSpot developer accounts can be created [here](<replace with actual link>).

**Note:** Currently, only outgoing calls are supported.


## Getting Started

### Run the Demo Calling App

Two demo apps are available:

* **`demo-minimal-js`:** A basic implementation using JavaScript, HTML, and CSS.  SDK instantiation is shown in `index.js`.
* **`demo-react-ts`:** A more realistic implementation using React, TypeScript, and Styled Components.  SDK instantiation is in `useCti.ts`.

**Note:** These demos use mock data and are not fully functional calling apps.


### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](<replace with actual link>) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`:**  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:**  `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app, opening a browser tab at `https://localhost:9025/`. You might need to bypass a security warning.


### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console and run one of these commands:

   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

3. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses a simple API for message exchange via methods and event handlers.  See the [Events section](#events) for a complete list.

Key interactions:

* **Dial Number:** HubSpot sends the dial number.
* **Outbound Call Started:** App notifies HubSpot.
* **Create Engagement:** HubSpot creates a call engagement (if requested).
* **Engagement Created:** HubSpot confirms engagement creation.
* **Engagement ID Sent:** HubSpot sends the `engagementId`.
* **Call Ended:** App notifies HubSpot.
* **Call Completed:** App signals completion.
* **Update Engagement:** App updates the engagement with details.  Learn more about updating engagements via the [API](<replace with actual link>) or [SDK](<replace with actual link>).


### SDK Instantiation

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Log debug messages
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

To launch the iFrame, HubSpot requires these parameters:

```javascript
{
  name: string, // App name
  url: string, // App URL
  width: number, // iFrame width
  height: number, // iFrame height
  isReady: boolean, // Ready for production (defaults to true)
  supportsCustomObjects: true // Support calls from custom objects
}
```


### Using the Calling Settings Endpoint

Use your API tool (e.g., Postman) and send a payload to HubSpot's settings API.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  `isReady: false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.


### Overriding Extension Settings with localStorage

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

Set `isReady` to `true` using the `PATCH` endpoint:

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"isReady":true}'
```


### Publishing to the HubSpot Marketplace

[Learn how to publish your app to the HubSpot marketplace here](<replace with actual link>).


## Events

### Sending Messages to HubSpot

The `extensions` object provides methods to send messages:

* **`initialized(payload)`:** Signals softphone readiness.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn()`:** User login notification.
* **`userLoggedOut()`:** User logout notification.
* **`outgoingCall(callInfo)`:** Outgoing call started.  `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered(payload)`:** Call answered. `payload`: `{ externalCallId: string }`
* **`callEnded(payload)`:** Call ended. `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`  `EndStatus`: `INTERNAL_COMPLETED`, `INTERNAL_FAILED`, `INTERNAL_CANCELED`, `INTERNAL_BUSY`, `INTERNAL_NO_ANSWER`, `INTERNAL_REJECTED`, `INTERNAL_MISSED`
* **`callCompleted(data)`:** Call completed. `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError(data)`:** Error notification. `data`: `{ message: string }`
* **`resizeWidget(data)`:** Resize request. `data`: `{ height: number, width: number }`


### Receiving Messages from HubSpot

* **`onReady(data)`:** HubSpot is ready. `data`: `{ engagementId: number, iframeLocation: Enum, ownerId: String | Number, portalId: Number, userId: Number }`  `iframeLocation`: `widget`, `remote`, `window`
* **`onDialNumber(data)`:** Outbound call triggered.  `data`: `{ phoneNumber: string, ownerId: number, subjectId: number, objectId: number, objectType: CONTACT | COMPANY, portalId: number, countryCode: string, calleeInfo: { calleeId: number, calleeObjectTypeId: string }, startTimestamp: number, toPhoneNumberSrc: string }`
* **`onEngagementCreated(data)`:** *(Deprecated, use `onCreateEngagementSucceeded`)* Engagement created. `data`: `{ engagementId: number }`
* **`onNavigateToRecordFailed(data)`:** Navigation to record failed. `data`: `{ engagementId: number, objectCoordinates: object }`
* **`onPublishToChannelSucceeded(data)`:** Publishing to channel succeeded. `data`: `{ engagementId: number, externalCallId: string }`
* **`onPublishToChannelFailed(data)`:** Publishing to channel failed. `data`: `{ engagementId: number, externalCallId: string }`
* **`onCallerIdMatchSucceeded(event)`:** Caller ID match succeeded.
* **`onCallerIdMatchFailed(event)`:** Caller ID match failed.
* **`onCreateEngagementSucceeded(event)`:** Engagement creation succeeded.
* **`onCreateEngagementFailed(event)`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded(event)`:** Engagement update succeeded.
* **`onUpdateEngagementFailed(event)`:** Engagement update failed.
* **`onVisibilityChanged(data)`:** Widget visibility changed. `data`: `{ isMinimized: boolean, isHidden: boolean }`
* **`defaultEventHandler(event)`:** Default event handler.


## Frequently Asked Questions

* **Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; apps update them.  For calls outside HubSpot, the app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:** Functionality can be added to existing marketplace apps.
* **Softphone Integration:** Easily integrate existing softphones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Appearance:** Yes, for updated apps.
* **User Installation/Uninstall:** Controlled by user permissions.
* **Custom Calling Properties:** Yes, via the properties API.
* **Calls from Custom Objects:** Yes, using the SDK.  Ensure `outgoingCall({ createEngagement: true });`


**(Remember to replace placeholders like `<replace with actual link>` with the correct URLs.)**
