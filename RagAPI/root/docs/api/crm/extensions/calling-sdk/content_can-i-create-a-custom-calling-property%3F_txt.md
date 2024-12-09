# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between your calling application and HubSpot.  It enables users to make calls directly from CRM records.  The SDK consists of three primary components:

* **Calling Extensions SDK (JavaScript):**  Enables communication between your app and HubSpot.
* **Calling Settings Endpoints (API):** Used to configure your app's settings for each connected HubSpot account.
* **Calling iFrame:**  The interface displayed to HubSpot users, configured via the calling settings endpoints.


For a detailed understanding of the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE_HERE -  replace with actual link).  Once integrated, your app will appear in HubSpot's call switcher.

**Note:** Currently, only outgoing calls are supported.

If you need to create a HubSpot developer account, you can do so [here](LINK_TO_SIGNUP_HERE - replace with actual link).  If you don't yet have an app, you can [create one from your HubSpot developer account](LINK_TO_APP_CREATION_HERE - replace with actual link).


## Getting Started

### Run the Demo Calling Apps

Two demo apps are available to test the SDK:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive implementation using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.


### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP_HERE - replace with actual link) of the repository.
3. Navigate to the project's root directory.
4. Run the appropriate command:

   * **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts (`Contacts > Contacts`) or Companies (`Contacts > Companies`).
2. Open your browser's developer console.
3. Run one of the following commands, depending on your installation and demo app:

   * **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses methods and event handlers for message exchange.  See the **Events** section for a complete list.

### SDK Initialization

Create a `CallingExtensions` instance with optional settings:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Dial number received */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

###  Events

#### Sending Messages to HubSpot

* **`initialized(payload)`:**  Signals softphone readiness.  `payload` includes `isLoggedIn` (boolean) and `engagementId` (number).
* **`userLoggedIn()`:**  Signals user login (only needed if not logged in during initialization).
* **`userLoggedOut()`:** Signals user logout.
* **`outgoingCall(callInfo)`:**  Notifies HubSpot of an outgoing call. `callInfo` includes `callStartTime` (number), `createEngagement` (boolean), `toNumber` (string), and `fromNumber` (string).  `phoneNumber` (string) is deprecated, use `toNumber` instead.
* **`callAnswered(payload)`:**  Signals call answered. `payload` includes `externalCallId` (string).
* **`callEnded(payload)`:** Signals call ended. `payload` includes `externalCallID` (string), `engagementId` (number), and `callEndStatus` (enumeration).
* **`callCompleted(data)`:** Signals call completion.  `data` includes `engagementId` (number), `hideWidget` (boolean), `engagementProperties` (object), and `externalCallId` (number).
* **`sendError(data)`:** Reports an error. `data` includes `message` (string).
* **`resizeWidget(data)`:** Requests widget resizing. `data` includes `height` (number) and `width` (number).


#### Receiving Messages from HubSpot

* **`onReady(data)`:** HubSpot is ready.  `data` includes `engagementId`, `iframeLocation`, `ownerId`, `portalId`, and `userId`.
* **`onDialNumber(data)`:** Outbound call triggered.  `data` includes various call details (see documentation for details).
* **`onEngagementCreated(data)`:** (Deprecated)  Engagement created.  `data` includes `engagementId`. Use `onCreateEngagementSucceeded` instead.
* **`onNavigateToRecordFailed(data)`:** Navigation to a record failed. `data` includes `engagementId` and `objectCoordinates`.
* **`onPublishToChannelSucceeded(data)`:** Publishing to a channel succeeded. `data` includes `engagementId` and `externalCallId`.
* **`onPublishToChannelFailed(data)`:** Publishing to a channel failed. `data` includes `engagementId` and `externalCallId`.
* **`onCallerIdMatchSucceeded(event)`:** Caller ID match succeeded.
* **`onCallerIdMatchFailed(event)`:** Caller ID match failed.
* **`onCreateEngagementSucceeded(event)`:** Engagement creation succeeded.
* **`onCreateEngagementFailed(event)`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded(event)`:** Engagement update succeeded.
* **`onUpdateEngagementFailed(event)`:** Engagement update failed.
* **`onVisibilityChanged(data)`:** Widget visibility changed. `data` includes `isMinimized` and `isHidden`.
* **`defaultEventHandler(event)`:**  Handles unhandled events.


###  Calling Settings Endpoint

Use the API (e.g., with `curl`) to manage your app's settings:

```bash
# Example: POST (add settings)
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'

# Example: PATCH (update settings)
curl --request PATCH \
--url '...'  --data '{"isReady":true}'
```

Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  `isReady` should be `false` during testing and `true` for production.


###  Override Settings with localStorage

For testing, override settings using the browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


### Get Your App Ready for Production

Set `isReady` to `true` using the PATCH endpoint.


### Publish to the HubSpot Marketplace

Once ready, publish your app to the HubSpot marketplace ([details here](LINK_TO_MARKETPLACE_DETAILS_HERE - replace with actual link)).


## Frequently Asked Questions

* **Authentication:** Your app handles authentication.
* **CDN Hosting:** Yes, hosted on jsDeliver (example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them and creates engagements for calls initiated outside HubSpot.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:**  You can add this functionality to existing marketplace apps.
* **Softphone Integration:** Easily integrate existing softphones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free Users:** Free users can install the app.
* **Automatic Appearance:** The integration automatically appears for existing users.
* **User Installation/Uninstallation:** Only users with necessary permissions can install/uninstall.
* **Custom Calling Property:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, if using the SDK to create calls and setting `createEngagement: true` in `outgoingCall`.



This markdown provides a comprehensive overview of the HubSpot Calling Extensions SDK.  Remember to replace the placeholder links with the correct URLs.
