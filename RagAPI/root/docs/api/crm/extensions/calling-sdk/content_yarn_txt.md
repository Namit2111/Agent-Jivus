# HubSpot CRM API Calling Extensions SDK

This document provides a comprehensive guide to the HubSpot CRM API Calling Extensions SDK.  It covers installation, usage, event handling, and frequently asked questions.

## Overview

The Calling Extensions SDK allows developers to integrate custom calling functionality into HubSpot, providing users with a seamless calling experience directly from CRM records.  The SDK facilitates communication between your calling application and HubSpot.  Currently, only outgoing calls are supported.

A calling extension comprises three core components:

1. **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure the settings for your calling app on a per-HubSpot account basis.
3. **Calling iFrame:** The interface displayed to HubSpot users, configured via the calling settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE_HERE - replace with actual link).  Once integrated, your app will appear in HubSpot's call switcher.

If you need to create a HubSpot developer account, you can do so [here](LINK_TO_SIGNUP_HERE - replace with actual link).  If you don't have an app, you can create one from your [HubSpot developer account](LINK_TO_DEVELOPER_ACCOUNT_HERE - replace with actual link).


## Getting Started

### Run the Demo Calling App

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  The SDK instantiation is shown in `index.js`.
* **`demo-react-ts`:** A more realistic implementation using React, TypeScript, and Styled Components. The SDK instantiation is in `useCti.ts`.

**Note:** These demos use mock data and aren't fully functional calling applications.

### Install the Demo App

1. Install Node.js.
2. Clone, fork, or download the ZIP of the repository.
3. Navigate to the project's root directory.
4. Run the appropriate command:

   * **`demo-minimal-js`:**  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`. You may need to bypass a security warning.

### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console and run the following command (choose the appropriate option based on whether you installed the app locally):

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

3. Refresh the page.  Select the demo app from the "Call from" dropdown in the call switcher.


## Installing the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends messages via events, and your app responds using event handlers.

### Events

#### Sending Messages to HubSpot

* **`initialized`:**  Indicates softphone readiness. Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn`:**  User login notification.
* **`userLoggedOut`:** User logout notification.
* **`outgoingCall`:** Outgoing call initiation. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`  `phoneNumber` is deprecated; use `toNumber`.
* **`callAnswered`:** Outgoing call answered. Payload: `{ externalCallId: string }`
* **`callEnded`:** Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`  `EndStatus` is an enumeration (INTERNAL_COMPLETED, INTERNAL_FAILED, etc.).
* **`callCompleted`:** Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError`:** Error notification. Payload: `{ message: string }`
* **`resizeWidget`:** Widget resize request. Payload: `{ height: number, width: number }`

#### Receiving Messages from HubSpot

* **`onReady`:** HubSpot is ready. Payload includes `engagementId`, `iframeLocation` (widget, remote, window), `ownerId`, `portalId`, and `userId`.
* **`onDialNumber`:** Outbound call initiated in HubSpot.  Payload includes detailed call information (phoneNumber, ownerId, subjectId, objectId, objectType, portalId, countryCode, calleeInfo, startTimestamp, toPhoneNumberSrc).
* **`onEngagementCreated`:** (Deprecated) Use `onCreateEngagementSucceeded` instead. Payload: `{ engagementId: number }`
* **`onNavigateToRecordFailed`:** Navigation to record failed. Payload: `{ engagementId: number, objectCoordinates: object }`
* **`onPublishToChannelSucceeded`:** Publishing to channel succeeded. Payload: `{ engagementId: number, externalCallId: string }`
* **`onPublishToChannelFailed`:** Publishing to channel failed. Payload: `{ engagementId: number, externalCallId: string }`
* **`onCallerIdMatchSucceeded`:** Caller ID match successful.
* **`onCallerIdMatchFailed`:** Caller ID match failed.
* **`onCreateEngagementSucceeded`:** Engagement creation succeeded.
* **`onCreateEngagementFailed`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded`:** Engagement update succeeded.
* **`onUpdateEngagementFailed`:** Engagement update failed.
* **`onVisibilityChanged`:** Widget visibility changed (minimized or hidden). Payload: `{ isMinimized: boolean, isHidden: boolean }`
* **`defaultEventHandler`:** Default event handler.

### SDK Instantiation

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Log debug messages
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
  "name": string,
  "url": string,
  "width": number,
  "height": number,
  "isReady": boolean,
  "supportsCustomObjects": true
}
```

### Calling Settings Endpoint

Use the HubSpot settings API (e.g., with `curl`) to manage your app's settings.  Remember to replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values.  The `isReady` flag should be `false` during testing and `true` for production.

```bash
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports PATCH, GET, and DELETE.

### Overriding Settings with localStorage

For testing, override settings using the browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Getting Your App Ready for Production

Set `isReady` to `true` using the PATCH endpoint.

### Publishing to the HubSpot Marketplace

Publish your app to the HubSpot marketplace [here](LINK_TO_MARKETPLACE_HERE - replace with actual link).


## Frequently Asked Questions

* **User Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, using jsDeliver (example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them.  For calls initiated outside HubSpot, your app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:** You can add this functionality to existing marketplace apps.
* **Integrating Existing Softphones:** Easily integrable.
* **Multiple Integrations:** Yes, users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Appearance:** Yes, for updates to existing installations.
* **User Installation/Uninstallation:**  Only permitted users can install/uninstall.
* **Custom Calling Properties:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, using the SDK and setting `createEngagement: true` in the `outgoingCall` event.


This markdown documentation provides a structured and easily readable version of the provided text.  Remember to replace the placeholder links with the actual links.
