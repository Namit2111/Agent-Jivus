# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, enabling custom calling options within the HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between your application and HubSpot, providing a custom calling experience for HubSpot users directly from CRM records.  It consists of three main parts:

* **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
* **Calling Settings Endpoints:** Configure calling settings for your app on a per-HubSpot account basis.
* **Calling iFrame:** Your app's interface within HubSpot, configured via the settings endpoints.

Only outgoing calls are currently supported.  For more information on the in-app calling experience, see [this knowledge base article](link-to-knowledge-base-article).  Once integrated, your app will appear in the HubSpot call switcher.


## Getting Started

### Prerequisites

* A HubSpot developer account ([sign up here](link-to-signup)).
* [Node.js](https://nodejs.org/) installed.

### Demo Applications

Two demo applications are available for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS.  SDK instantiation is shown in `index.js`.
* **`demo-react-ts`:**  More comprehensive implementation using React, TypeScript, and Styled Components. SDK instantiation is in `useCti.ts`.

**Note:** Demo apps use mock data and aren't fully functional calling applications.


### Installing the Demo App

1. Clone or download the repository's ZIP file.
2. Navigate to the demo app's directory (`demos/demo-minimal-js` or `demos/demo-react-ts`).
3. Run:
   * For `demo-minimal-js`: `npm i && npm start`
   * For `demo-react-ts`: `npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launching the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following `localStorage` commands, depending on whether you installed the demo app:
   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.
5. Click the "Call" icon, select the demo app from the "Call from" dropdown, and click "Call".

### Installing the Calling Extensions SDK

Add the SDK to your project using npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses message passing between your app and HubSpot via event handlers.

### Events

#### Sending Messages to HubSpot

* `initialized`: Soft phone ready for interaction. Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Outgoing call answered. Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`  `callEndStatus` is an enum: `INTERNAL_COMPLETED`, `INTERNAL_FAILED`, `INTERNAL_CANCELED`, `INTERNAL_BUSY`, `INTERNAL_NO_ANSWER`, `INTERNAL_REJECTED`, `INTERNAL_MISSED`.
* `callCompleted`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`: Error encountered. Payload: `{ message: string }`
* `resizeWidget`: Resize the widget. Payload: `{ height: number, width: number }`


#### Receiving Messages from HubSpot

* `onReady`: HubSpot ready to receive messages.  Payload: `{ engagementId: number, iframeLocation: Enum, ownerId: String or Number, PortalId: Number, userId: Number }`  `iframeLocation` is an enum: `widget`, `remote`, `window`.
* `onDialNumber`: Outbound call triggered.  Payload: `{ phoneNumber: string, ownerId: number, subjectId: number, objectId: number, objectType: CONTACT | COMPANY, portalId: number, countryCode: string, calleeInfo: { calleeId: number, calleeObjectTypeId: string }, startTimestamp: number, toPhoneNumberSrc: string }`
* `onEngagementCreated`: **Deprecated.** Use `onCreateEngagementSucceeded` instead. Payload: `{ engagementId: number }`
* `onNavigateToRecordFailed`: Navigation to a record failed. Payload: `{ engagementId: number, objectCoordinates: object }`
* `onPublishToChannelSucceeded`: Publishing to a channel succeeded. Payload: `{ engagementId: number, externalCallId: string }`
* `onPublishToChannelFailed`: Publishing to a channel failed. Payload: `{ engagementId: number, externalCallId: string }`
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement creation succeeded.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement update succeeded.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed. Payload: `{ isMinimized: boolean, isHidden: boolean }`
* `defaultEventHandler`: Default event handler.


###  Creating a CallingExtensions Instance

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Log debug messages to console
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: event => { /* ... */ },
    onCreateEngagementSucceeded: event => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### iFrame Parameters

To launch the calling extensions iFrame, HubSpot requires these parameters:

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


### Calling Settings Endpoint

Use this API endpoint to manage your app's settings (e.g., using `curl` or Postman):

`https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

This endpoint supports `POST`, `PATCH`, `GET`, and `DELETE` methods.  The `isReady` flag should be `false` during testing and `true` for production.


### Overriding Settings with localStorage

For testing, you can override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


### Getting Your App Ready for Production

Set `isReady` to `true` using the `PATCH` method on the settings endpoint.


### Publishing to the HubSpot Marketplace

[Details on publishing](link-to-marketplace-publishing).


## Frequently Asked Questions

* **User Authentication:** Handled by your application.
* **CDN Hosting:** Yes, via jsDeliver (example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them and creates engagements for calls initiated outside the UI.
* **Required Scopes:** `contacts` and `timeline`.
* **Adding to Existing App:** Yes, possible.
* **Integrating Existing Softphone:**  Yes, easily integrable.
* **Multiple Integrations:** Yes, users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Integration Appearance:** Yes, for existing users.
* **User Installation/Uninstallation:** Controlled by user permissions.
* **Custom Calling Properties:** Yes, via the properties API.
* **Calling from Custom Objects:** Yes, if using the SDK to create calls and setting `createEngagement: true` in `outgoingCall`.


## Feedback

[Link to feedback form]


This markdown documentation provides a comprehensive overview and detailed reference for the HubSpot Calling Extensions SDK. Remember to replace placeholder links (e.g., `link-to-knowledge-base-article`) with actual URLs.
