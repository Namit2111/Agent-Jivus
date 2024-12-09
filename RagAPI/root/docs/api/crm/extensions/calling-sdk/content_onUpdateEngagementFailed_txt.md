# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot CRM.

## Overview

The Calling Extensions SDK enables apps to provide a customized calling experience directly from CRM records.  It consists of three main components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Configure settings for your app on a per-HubSpot account basis.
3. **Calling iFrame:** Your app's visual representation within HubSpot, configured via the settings endpoints.

For a detailed understanding of the in-app calling experience, refer to [this knowledge base article](LINK_TO_KNOWLEDGE_BASE_ARTICLE).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.  If you don't have a HubSpot app, you can [create one here](LINK_TO_APP_CREATION).  If you lack a HubSpot developer account, sign up [here](LINK_TO_SIGN_UP).


## Getting Started

### Run the Demo Calling App

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  SDK instantiation is shown in `index.js`.
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components. SDK instantiation is in `useCti.ts`.

**Note:** These demos use mock data and are not fully functional calling apps.


### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP) of the repository.
3. Navigate to the project's root directory.
4. Run the appropriate command:

   * **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

   This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands, depending on your installation method:

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.  Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Install the Calling Extensions SDK

Add the SDK to your app as a Node.js dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses events for communication.  See the [Events section](#events) for a complete list.

### SDK Initialization

Create a `CallingExtensions` instance with options, including `eventHandlers`:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: event => { /* HubSpot sends dial number */ },
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

HubSpot requires these iFrame parameters:

```json
{
  "name": "string", // App name
  "url": "string", // App URL
  "width": number, // Width
  "height": number, // Height
  "isReady": boolean, // Ready for production (false during testing)
  "supportsCustomObjects": true // Support calls from custom objects
}
```

### Using the Calling Settings Endpoint

Use your API tool (e.g., Postman) to send a payload to HubSpot's settings API:

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

(Remember to replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`.)  This endpoint also supports `PATCH`, `GET`, and `DELETE`.  Set `isReady` to `true` for production.


### Overriding Extension Settings (localStorage)

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

Use the `PATCH` endpoint to set `isReady` to `true` in your calling settings.


### Publish to the HubSpot Marketplace

[Learn how to publish your app to the HubSpot Marketplace here](LINK_TO_MARKETPLACE_PUBLISHING).


## Events

### Sending Messages to HubSpot

* `initialized`:  Indicates softphone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User login notification.
* `userLoggedOut`: User logout notification.
* `outgoingCall`: Outgoing call started.  Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Outgoing call answered.  Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`:  Error notification. Payload: `{ message: string }`
* `resizeWidget`: Resize request. Payload: `{ height: number, width: number }`

### Receiving Messages from HubSpot

* `onReady`: HubSpot readiness notification. Payload: `{ engagementId: number, iframeLocation: Enum, ownerId: String | Number, portalId: number, userId: number }`
* `onDialNumber`: Outbound call triggered in HubSpot.  Payload: `{ phoneNumber: string, ownerId: number, subjectId: number, objectId: number, objectType: CONTACT | COMPANY, portalId: number, countryCode: string, calleeInfo: { calleeId: number, calleeObjectTypeId: string }, startTimestamp: number, toPhoneNumberSrc: string }`
* `onEngagementCreated`: (Deprecated) Use `onCreateEngagementSucceeded` instead.  Payload: `{ engagementId: number }`
* `onNavigateToRecordFailed`: Navigation to record failed. Payload: `{ engagementId: number, objectCoordinates: object }`
* `onPublishToChannelSucceeded`: Publishing to channel succeeded. Payload: `{ engagementId: number, externalCallId: string }`
* `onPublishToChannelFailed`: Publishing to channel failed. Payload: `{ engagementId: number, externalCallId: string }`
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement creation succeeded.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onVisibilityChanged`: Widget visibility changed. Payload: `{ isMinimized: boolean, isHidden: boolean }`
* `defaultEventHandler`: Default event handler.


## Frequently Asked Questions

* **Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver (example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; apps update them afterward.  For calls outside the HubSpot UI, the app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Marketplace Apps:**  Functionality can be added to existing apps.
* **Soft Phone Integration:** Easily integrable.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Integration Appearance:** Yes, for existing app updates.
* **User Installation/Uninstallation:** Controlled by user permissions.
* **Custom Calling Properties:** Creatable via the properties API.
* **Calls from Custom Objects:** Supported if the SDK is used for call creation and the `outgoingCall` event is used to notify HubSpot (`outgoingCall({ createEngagement: true });`).


## Feedback

[Share your feedback here](LINK_TO_FEEDBACK)


**(Remember to replace the placeholder links with the actual links.)**
