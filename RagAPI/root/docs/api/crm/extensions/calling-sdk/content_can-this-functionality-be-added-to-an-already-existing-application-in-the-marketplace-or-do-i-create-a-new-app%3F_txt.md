# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality directly into HubSpot's CRM.

## Overview

The Calling Extensions SDK enables apps to provide a custom calling experience to HubSpot users from within CRM records.  It consists of three main components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:**  Displays your app to HubSpot users; its configuration is managed through the calling settings endpoints.

For a detailed understanding of the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE_HERE -  Replace with actual link).  After connecting your app, it will appear in HubSpot's call switcher.

**Note:** Currently, only outgoing calls are supported.  If you don't have a HubSpot app, you can [create one here](LINK_TO_APP_CREATION_HERE - Replace with actual link).  If you lack a HubSpot developer account, sign up [here](LINK_TO_SIGN_UP_HERE - Replace with actual link).

## Getting Started

### Run the Demo Calling App

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive implementation using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and aren't fully functional calling apps.

### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP_HERE - Replace with actual link) of the repository.
3. Navigate to the project's root directory.
4. Run the appropriate command:

   * **`demo-minimal-js`**:  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`**: `cd demos/demo-react-ts && npm i && npm start`

   This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts (`Contacts > Contacts`) or Companies (`Contacts > Companies`).
2. Open your browser's developer console and run the following command (choose one based on your installation method):

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

3. Refresh the page, click the "Call" icon, select the demo app from the "Call from" dropdown, and click "Call."


### Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses methods and event handlers for message exchange.  See the "Events" section for a complete list.

### SDK Initialization

Create a `CallingExtensions` object, defining behavior through an options object with `eventHandlers`:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Set to true for debugging messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Dial number event */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created */ },
    onEngagementCreatedFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
  },
};

const extensions = new CallingExtensions(options);
```

###  Testing Your App

To launch the calling extensions iFrame, HubSpot requires these iFrame parameters:

```json
{
  "name": "Your App Name",
  "url": "Your App URL",
  "width": 600,
  "height": 400,
  "isReady": false, // Set to false during testing, true for production
  "supportsCustomObjects": true
}
```

### Using the Calling Settings Endpoint

Use your API tool (e.g., Postman) to send a payload to HubSpot's settings API. Replace `APP_ID` with your app's ID and `DEVELOPER_ACCOUNT_API_KEY` with your key.  The `isReady` flag indicates production readiness (set to `false` during testing).

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.

### Overriding Extension Settings using localStorage

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

Set `isReady` to `true` using the `PATCH` endpoint:

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"isReady":true}'
```

### Publish to the HubSpot Marketplace

[Learn how to publish your app to the HubSpot marketplace here](LINK_TO_MARKETPLACE_PUBLISHING_HERE - Replace with actual link).


## Events

### Sending Messages to HubSpot

The `extensions` object provides methods to send messages:

* **`initialized(payload)`:**  Indicates softphone readiness.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn()`:** User login notification.
* **`userLoggedOut()`:** User logout notification.
* **`outgoingCall(callInfo)`:** Outgoing call started. `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered(payload)`:** Outgoing call answered. `payload`: `{ externalCallId: string }`
* **`callEnded(payload)`:** Call ended. `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted(data)`:** Call completed. `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError(data)`:**  Error notification. `data`: `{ message: string }`
* **`resizeWidget(data)`:** Resize request. `data`: `{ height: number, width: number }`

### Receiving Messages from HubSpot

* **`onReady()`:** HubSpot is ready.
* **`onDialNumber(data)`:** Outbound call initiated.  `data` contains call details.
* **`onEngagementCreated(data)`:** (Deprecated; use `onCreateEngagementSucceeded`) Engagement created.
* **`onNavigateToRecordFailed(data)`:** Record navigation failed.
* **`onPublishToChannelSucceeded(data)`:** Channel publishing succeeded.
* **`onPublishToChannelFailed(data)`:** Channel publishing failed.
* **`onCallerIdMatchSucceeded(event)`:** Caller ID match succeeded.
* **`onCallerIdMatchFailed(event)`:** Caller ID match failed.
* **`onCreateEngagementSucceeded(event)`:** Engagement creation succeeded.
* **`onCreateEngagementFailed(event)`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded(event)`:** Engagement update succeeded.
* **`onUpdateEngagementFailed(event)`:** Engagement update failed.
* **`onVisibilityChanged(data)`:** Widget visibility changed. `data`: `{isMinimized: boolean, isHidden: boolean}`
* **`defaultEventHandler(event)`:** Default event handler.


## Frequently Asked Questions

* **Authentication:** The calling app handles authentication.
* **CDN Hosting:** Yes, via jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the UI; the app updates them afterward. For calls outside the UI, the app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:** Functionality can be added to existing marketplace apps.
* **Soft Phone Integration:** Easily integrate existing soft phones.
* **Multiple Integrations:** Yes, users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Integration Appearance:** Yes, for updated apps.
* **User Installation/Uninstallation:** Only users with appropriate permissions.
* **Custom Calling Properties:** Yes, via the properties API.
* **Calls from Custom Objects:** Yes, using the SDK.  Ensure `createEngagement: true` in `outgoingCall`.


Remember to replace placeholder links with the actual links from the HubSpot documentation.  This markdown provides a comprehensive structured overview of the provided text.
