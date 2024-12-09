# HubSpot Calling Extensions SDK Documentation

This document provides comprehensive information on the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into their HubSpot apps.

## Overview

The Calling Extensions SDK enables apps to offer custom calling functionality directly from CRM records. It consists of three core components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure calling settings for your app, applied to each connected HubSpot account.
3. **Calling iFrame:**  Displays your app to HubSpot users, customized via the calling settings endpoints.

For detailed information on the in-app calling experience, refer to [this knowledge base article](LINK_TO_KNOWLEDGE_BASE_ARTICLE).  After connecting your app, it will appear in the HubSpot call switcher.

To get started, you'll need a HubSpot developer account.  If you don't have one, sign up [here](LINK_TO_SIGN_UP).  If you don't have an app, [create one here](LINK_TO_CREATE_APP).

**Note:** Currently, only outgoing calls are supported.


## Getting Started

### Run the Demo Calling App

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal JavaScript, HTML, and CSS implementation.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive React, TypeScript, and Styled Components implementation.  See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.


### Install the Demo App

To install the demo apps locally:

1. Install Node.js.
2. Clone, fork, or download the ZIP of the repository [LINK_TO_REPOSITORY].
3. Navigate to the project's root directory in your terminal.
4. Run one of the following commands:

    * **`demo-minimal-js`**:  `cd demos/demo-minimal-js && npm i && npm start`
    * **`demo-react-ts`**: `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app.  The app will open in your browser at `https://localhost:9025/`. You may need to bypass a security warning.


### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console.
3. Run the appropriate `localStorage` command:

    * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **`demo-minimal-js` (no install):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **`demo-react-ts` (no install):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page and select the demo app from the "Call from" dropdown in the call switcher.


### Install the Calling Extensions SDK

Add the SDK to your app as a Node.js dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses messages exchanged via methods and event handlers.  See the [Events](#events) section for a complete list.

### Key SDK Events

* **Dial Number:** HubSpot sends the dial number.
* **Outbound Call Started:** App notifies HubSpot of call initiation.
* **Create Engagement:** HubSpot creates a call engagement (if requested by the app).
* **Engagement Created:** HubSpot confirms engagement creation.
* **Engagement ID Sent to App:** HubSpot provides the `engagementId`.
* **Call Ended:** App notifies HubSpot of call termination.
* **Call Completed:** App signals completion of the user experience.
* **Update Engagement:** App updates the engagement with call details.  Learn more about updating engagements via the [API](LINK_TO_API_DOCS) or the SDK.

### Creating a `CallingExtensions` Instance

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: event => { /* Dial number received */ },
    onCreateEngagementSucceeded: event => { /* Engagement created successfully */ },
    onEngagementCreatedFailed: event => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: event => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: event => { /* Engagement update failed */ },
    onVisibilityChanged: event => { /* Widget visibility changed */ }
  }
};

const extensions = new CallingExtensions(options);
```

### Testing Your App

To launch the calling extensions iFrame:

```json
{
  name: string, // App name
  url: string, // App URL
  width: number, // iFrame width
  height: number, // iFrame height
  isReady: boolean, // Ready for production (false for testing)
  supportsCustomObjects: true // Support calls from custom objects
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


### Overriding Extension Settings Using `localStorage`

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

To publish your app, follow the instructions [here](LINK_TO_MARKETPLACE_INSTRUCTIONS).


## Events

### Sending Messages to HubSpot

* **`initialized`**:  Signals softphone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn`**: Signals user login.
* **`userLoggedOut`**: Signals user logout.
* **`outgoingCall`**: Notifies HubSpot of an outgoing call. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered`**: Notifies HubSpot that a call has been answered. Payload: `{ externalCallId: string }`
* **`callEnded`**: Notifies HubSpot of call termination. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted`**: Signals call completion. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError`**: Reports an error. Payload: `{ message: string }`
* **`resizeWidget`**: Requests widget resizing. Payload: `{ height: number, width: number }`


### Receiving Messages from HubSpot

* **`onReady`**: HubSpot is ready to receive messages.  Payload: `{ engagementId: number, iframeLocation: Enum, ownerId: String | Number, portalId: Number, userId: Number }`
* **`onDialNumber`**: Outbound call initiated.  Payload includes phone number, owner ID, subject ID, object ID, object type, portal ID, country code, callee info, start timestamp, and phone number source.
* **`onEngagementCreated`**:  **(Deprecated)** Use `onCreateEngagementSucceeded` instead.
* **`onNavigateToRecordFailed`**: Navigation to a record failed. Payload: `{ engagementId: number, objectCoordinates: object }`
* **`onPublishToChannelSucceeded`**: Publishing to a channel succeeded. Payload: `{ engagementId: number, externalCallId: string }`
* **`onPublishToChannelFailed`**: Publishing to a channel failed. Payload: `{ engagementId: number, externalCallId: string }`
* **`onCallerIdMatchSucceeded`**: Caller ID match succeeded.
* **`onCallerIdMatchFailed`**: Caller ID match failed.
* **`onCreateEngagementSucceeded`**: Engagement creation succeeded.
* **`onCreateEngagementFailed`**: Engagement creation failed.
* **`onVisibilityChanged`**: Widget visibility changed. Payload: `{ isMinimized: boolean, isHidden: boolean }`
* **`defaultEventHandler`**: Default event handler.


## Frequently Asked Questions

* **User Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls from the HubSpot UI; apps create engagements for calls outside the UI and update existing engagements with call details.
* **Required Scopes:** `contacts` and `timeline`.
* **Adding to Existing App:**  Yes, possible.  Existing users will automatically gain access.
* **Integrating Existing Softphone:** Yes, easily integrable.
* **Multiple Integrations:** Yes, users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Integration Appearance:** Yes, for updated apps.
* **User Installation/Uninstallation:**  Only users with the necessary permissions.
* **Custom Calling Properties:** Yes, via the properties API.
* **Calls from Custom Objects:** Yes, if the SDK is used for call creation and the `outgoingCall` event is used.  Ensure `outgoingCall({ createEngagement: true });` is used.


## Copyright and Legal

Copyright © 2024 HubSpot, Inc.  [Privacy Policy](LINK_TO_PRIVACY_POLICY)  [Legal Stuff](LINK_TO_LEGAL_PAGE)


Remember to replace the bracketed placeholders (`LINK_TO_...`) with the actual URLs.
