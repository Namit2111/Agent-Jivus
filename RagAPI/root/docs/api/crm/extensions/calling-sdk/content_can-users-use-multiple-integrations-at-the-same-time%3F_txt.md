# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK enables apps to provide a custom calling option directly from CRM records.  It consists of three main components:

* **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
* **Calling Settings Endpoints (API):** Configure calling settings for each connected HubSpot account.
* **Calling iFrame:**  Displays your app to HubSpot users; configured using the settings endpoints.

For the in-app calling experience details, refer to [this knowledge base article](link_to_knowledge_base_article).  After connecting, your app will appear in the HubSpot call switcher.

If you need to create a HubSpot app, you can do so from your [HubSpot developer account](link_to_hubspot_developer_account). If you don't have one, sign up [here](link_to_signup).  **Note:** Currently, only outgoing calls are supported.

## Getting Started

### Running the Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and aren't fully functional calling apps.

#### Installation (Optional)

1. Install Node.js.
2. Clone or download the repository's ZIP file.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`**: `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`**: `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launching the Demo App from HubSpot

1. Navigate to HubSpot contacts (`Contacts > Contacts`) or companies (`Contacts > Companies`).
2. Open your browser's developer console.
3. Run one of the following commands, depending on whether you installed the demo:

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (Uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (Uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page and select the demo app from the "Call from" dropdown in the call switcher.


## Installing the Calling Extensions SDK

Add the SDK as a dependency:

* **npm**: `npm i --save @hubspot/calling-extensions-sdk`
* **yarn**: `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses events for communication. See the [Events](#events) section for a complete list.

### SDK Initialization

Create a `CallingExtensions` object, defining behavior with an options object and `eventHandlers`:

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

To display your app's iFrame to users, HubSpot requires these iFrame parameters:

```json
{
  "name": "Your App Name",
  "url": "Your App URL",
  "width": 400,
  "height": 600,
  "isReady": false, // Set to false during testing, true for production
  "supportsCustomObjects": true
}
```

### Using the Calling Settings Endpoint (API)

Use the following API call to set your app's settings (replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`):

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.  Remember to set `isReady` to `true` for production.

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

### Production Readiness

Set `isReady` to `true` using the `PATCH` endpoint after testing.

### Publishing to the Marketplace

Publish your app to the HubSpot marketplace [here](link_to_marketplace).


## Events

### Sending Messages to HubSpot

* **`initialized`**: Notifies HubSpot the app is ready.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn`**: User logged in.
* **`userLoggedOut`**: User logged out.
* **`outgoingCall`**: Outgoing call started. Payload: `{ phoneNumber: string (deprecated, use toNumber), callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered`**: Outgoing call answered. Payload: `{ externalCallId: string }`
* **`callEnded`**: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted`**: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError`**: Error occurred. Payload: `{ message: string }`
* **`resizeWidget`**: Resize the widget. Payload: `{ height: number, width: number }`


### Receiving Messages from HubSpot

* **`onReady`**: HubSpot is ready. Payload: `{ engagementId: number, iframeLocation: Enum, ownerId: String | Number, PortalId: Number, userId: Number }`
* **`onDialNumber`**: Outbound call triggered.  Payload includes `phoneNumber`, `ownerId`, `subjectId`, `objectId`, `objectType`, `portalId`, `countryCode`, `calleeInfo`, `startTimestamp`, `toPhoneNumberSrc`.
* **`onEngagementCreated`**: *(Deprecated)* Use `onCreateEngagementSucceeded` instead.
* **`onNavigateToRecordFailed`**: Navigation to record failed. Payload: `{ engagementId: number, objectCoordinates: object }`
* **`onPublishToChannelSucceeded`**: Publishing to channel succeeded. Payload: `{ engagementId: number, externalCallId: string }`
* **`onPublishToChannelFailed`**: Publishing to channel failed. Payload: `{ engagementId: number, externalCallId: string }`
* **`onCallerIdMatchSucceeded`**: Caller ID match succeeded.
* **`onCallerIdMatchFailed`**: Caller ID match failed.
* **`onCreateEngagementSucceeded`**: Engagement creation succeeded.
* **`onCreateEngagementFailed`**: Engagement creation failed.
* **`onVisibilityChanged`**: Widget visibility changed. Payload: `{ isMinimized: boolean, isHidden: boolean }`
* **`defaultEventHandler`**: Default event handler.


## Frequently Asked Questions

* **Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls from the HubSpot UI; apps update them.  Apps create engagements for calls initiated outside the HubSpot UI.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:** Functionality can be added to existing marketplace apps.
* **Soft Phone Integration:** Easily integrate existing soft phones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free Users:** All users can install the app.
* **Automatic Appearance:** Integration automatically appears for existing users.
* **User Installation/Uninstallation:** Only users with the necessary permissions can install/uninstall.
* **Custom Calling Properties:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, if the SDK is used to create calls and `outgoingCall({ createEngagement: true })` is used.


This markdown provides a structured and comprehensive overview of the HubSpot Calling Extensions SDK.  Remember to replace placeholder links with actual URLs.
