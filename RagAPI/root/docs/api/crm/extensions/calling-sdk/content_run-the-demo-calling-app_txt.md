# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK enables apps to provide a custom calling option directly from CRM records.  It consists of three key components:

* **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
* **Calling Settings Endpoints (API):** Configure calling settings for each connected HubSpot account.
* **Calling iFrame:**  Displays your app to HubSpot users; configured via the calling settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](link-to-knowledge-base-article).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.


## Getting Started

### 1.  Run the Demo Calling App

Test the SDK using two demo apps:

* **`demo-minimal-js`:** Minimal implementation (JavaScript, HTML, CSS).  SDK instantiation is in `index.js`.
* **`demo-react-ts`:**  More comprehensive implementation (React, TypeScript, Styled Components). SDK instantiation is in `useCti.ts`.

**Note:** Demo apps use mock data and aren't fully functional calling apps.


### 2. Install the Demo App

To install the demo app locally:

1. Install Node.js.
2. Clone, fork, or download the ZIP of the repository.
3. Navigate to the project's root directory.
4. Run the appropriate command:

   * **`demo-minimal-js`**: `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`**: `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### 3. Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console.
3. Run the appropriate `localStorage` command (choose one based on whether you installed the app):

   * **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page and select the demo app from the "Call from" dropdown in the call switcher.


### 4. Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  See the [Events](#events) section for a complete list.

### Creating an Instance

Create a `CallingExtensions` object, defining event handlers:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* HubSpot sends dial number */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created */ },
    onEngagementCreatedFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```


###  iFrame Parameters

To launch the calling extension iFrame, HubSpot requires these parameters:

```json
{
  "name": "string", // App name
  "url": "string", // App URL
  "width": number, // iFrame width
  "height": number, // iFrame height
  "isReady": boolean, // Ready for production?
  "supportsCustomObjects": true // Supports calls from custom objects?
}
```


## Using the Calling Settings Endpoint

Use the API to set your app's settings. Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  The `isReady` flag should be `false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint supports `PATCH`, `GET`, and `DELETE` as well.


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

### Production Readiness

Set `isReady` to `true` using the `PATCH` endpoint when ready for production.


### Publishing to the HubSpot Marketplace

Once configured, publish your app to the HubSpot marketplace [here](link-to-marketplace-docs).


## Events

### Sending Messages to HubSpot

* `initialized`: Softphone ready.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Outgoing call answered. Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`: App error. Payload: `{ message: string }`
* `resizeWidget`: Resize the widget. Payload: `{ height: number, width: number }`

### Receiving Messages from HubSpot

* `onReady`: HubSpot is ready.  Payload: `{ engagementId: number, iframeLocation: Enum, ownerId: String | Number, portalId: Number, userId: Number }`
* `onDialNumber`: Outbound call triggered.  Payload: `{ phoneNumber: string, ownerId: number, subjectId: number, objectId: number, objectType: CONTACT | COMPANY, portalId: number, countryCode: string, calleeInfo: { calleeId: number, calleeObjectTypeId: string }, startTimestamp: number, toPhoneNumberSrc: string }`
* `onEngagementCreated` (Deprecated): Use `onCreateEngagementSucceeded` instead. Payload: `{ engagementId: number }`
* `onNavigateToRecordFailed`: Navigation to a record failed.  Payload: `{ engagementId: number, objectCoordinates: object }`
* `onPublishToChannelSucceeded`: Publishing to a channel succeeded. Payload: `{ engagementId: number, externalCallId: string }`
* `onPublishToChannelFailed`: Publishing to a channel failed. Payload: `{ engagementId: number, externalCallId: string }`
* `onCallerIdMatchSucceeded`: Caller ID match successful.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement creation successful.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onVisibilityChanged`: Widget visibility changed. Payload: `{ isMinimized: boolean, isHidden: boolean }`
* `defaultEventHandler`: Default event handler.


## Frequently Asked Questions

* **User Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver.  Example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; apps update them afterward.  Apps create engagements for calls outside the HubSpot UI.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:** Functionality can be added to existing marketplace apps.
* **Softphone Integration:** Easily integrate existing softphones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free Users:** All users can install the app.
* **Automatic Updates:**  Integration automatically appears for existing users.
* **App Installation/Uninstallation:**  Restricted to users with appropriate permissions.
* **Custom Calling Properties:**  Create using the properties API.
* **Calls from Custom Objects:** Supported if using the SDK to create calls and notifying HubSpot via the `outgoingCall` event with `createEngagement: true`.


This markdown provides a comprehensive overview of the HubSpot CRM API Calling Extensions SDK. Remember to replace placeholder links with actual links as needed.
