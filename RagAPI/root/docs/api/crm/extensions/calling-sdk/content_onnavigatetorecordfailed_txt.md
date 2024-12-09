# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, a JavaScript SDK enabling communication between your app and HubSpot, allowing you to provide custom calling options to HubSpot users directly from CRM records.


## Overview

The Calling Extensions SDK consists of three main components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:**  Your app's interface displayed to HubSpot users, configured via the calling settings endpoints.


For details on the in-app calling experience, refer to [this knowledge base article](link_to_knowledge_base_article).  Once integrated, your app will appear in the HubSpot call switcher.

If you lack an app, create one through your [HubSpot developer account](link_to_developer_account_creation).  If you don't have a developer account, sign up [here](link_to_developer_account_signup).


**Note:** Currently, only outgoing calls are supported.


## Getting Started

### Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS.  SDK instantiation is shown in `index.js`.
* **`demo-react-ts`:**  A more comprehensive implementation using React, TypeScript, and Styled Components.  SDK instantiation is in `useCti.ts`.

**Note:** These demos use mock data and are not fully functional calling apps.


### Installing the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](link_to_zip) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launching the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console and run one of these commands:
    * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
3. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Installing the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses a simple API for message exchange via methods and event handlers.  See the [Events section](#events) for a complete list.


### SDK Initialization and Event Handlers

Create a `CallingExtensions` object, defining behavior using an options object with `eventHandlers`:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: event => { /* Dial number received */ },
    onCreateEngagementSucceeded: event => { /* Engagement created successfully */ },
    onEngagementCreatedFailed: event => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: event => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: event => { /* Engagement update failed */ },
    onVisibilityChanged: event => { /* Widget visibility changed */ },
  }
};

const extensions = new CallingExtensions(options);
```


### Testing Your App

HubSpot requires these iFrame parameters to launch the calling extension:

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

Use your API tool (e.g., Postman) to send a payload to HubSpot's settings API. Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  The `isReady` flag should be `false` during testing.

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


### Preparing for Production

Set `isReady` to `true` using the `PATCH` endpoint:

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"isReady":true}'
```


### Publishing to the HubSpot Marketplace

List your app in the HubSpot marketplace [here](link_to_marketplace_publishing).  This step is optional for internal apps.


## Events

### Sending Messages to HubSpot

The `extensions` object provides methods to send messages:

* **`initialized(payload)`:**  Indicates soft phone readiness.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn()`:** User login notification.
* **`userLoggedOut()`:** User logout notification.
* **`outgoingCall(callInfo)`:** Outgoing call started. `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered(payload)`:** Outgoing call answered. `payload`: `{ externalCallId: string }`
* **`callEnded(payload)`:** Call ended. `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`  `EndStatus` is an enum (INTERNAL_COMPLETED, etc.)
* **`callCompleted(data)`:** Call completed. `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError(data)`:** Error encountered. `data`: `{ message: string }`
* **`resizeWidget(data)`:** Resize the widget. `data`: `{ height: number, width: number }`


### Receiving Messages from HubSpot

Event handlers receive messages from HubSpot:

* **`onReady(data)`:** HubSpot is ready. `data`: `{ engagementId: number, iframeLocation: Enum, ownerId: String | Number, PortalId: number, userId: number }`
* **`onDialNumber(data)`:** Outbound call triggered.  `data`: `{ phoneNumber, ownerId, subjectId, objectId, objectType, portalId, countryCode, calleeInfo, startTimestamp, toPhoneNumberSrc }`
* **`onEngagementCreated(data)`:** (Deprecated) Engagement created. `data`: `{ engagementId: number }`
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

* **User Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; the app updates them afterward.  For calls outside the UI, the app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Adding to Existing App:** Yes, possible. Existing users gain access automatically.
* **Integrating Existing Softphone:** Yes, easily.
* **Multiple Integrations:** Yes, users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Integration Appearance:** Yes, for updated apps.
* **User Installation/Uninstallation:** Only users with necessary permissions.
* **Custom Calling Property:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, if using the SDK to create calls and notifying HubSpot in the `outgoingCall` event (`outgoingCall({ createEngagement: true });`).


## Feedback

[Link to feedback form]


This markdown document provides a comprehensive overview of the HubSpot Calling Extensions SDK.  Remember to replace placeholder links (`link_to...`) with the actual URLs.  The code snippets are formatted for better readability.  The table structures are improved for clarity.  The deprecated functions are clearly marked as such.
