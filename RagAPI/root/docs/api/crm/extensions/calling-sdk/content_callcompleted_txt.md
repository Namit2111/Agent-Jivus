# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into their HubSpot apps.

## Overview

The Calling Extensions SDK facilitates communication between a calling app and HubSpot, enabling users to initiate calls directly from CRM records.  A calling extension comprises three key components:

1. **Calling Extensions SDK (JavaScript):** Enables communication between the app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure calling settings for each connected HubSpot account.
3. **Calling iFrame:**  The app's user interface within HubSpot, configured via the settings endpoints.


For details on the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE_HERE -  replace with actual link).  Once integrated, the app will appear in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.

If you lack an app, [create one through your HubSpot developer account](LINK_TO_DEVELOPER_ACCOUNT - replace with actual link).  If you need a developer account, sign up [here](LINK_TO_SIGNUP - replace with actual link).


## Getting Started

### 1. Run the Demo Calling App

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more realistic implementation using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and aren't fully functional calling apps.


### 2. Install the Demo App

To install locally:

1. Install Node.js.
2. Clone, fork, or download the ZIP of the repository.
3. Navigate to the project's root directory.
4. Run the appropriate command:

   * **`demo-minimal-js`**:  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`**: `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### 3. Launch the Demo App from HubSpot

1. Navigate to HubSpot contacts (`Contacts > Contacts`) or companies (`Contacts > Companies`).
2. Open your browser's developer console.
3. Run the appropriate `localStorage` command:

   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### 4. Install the Calling Extensions SDK

Add the SDK to your app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses events for communication.  See the [Events section](#events) for details.

### Creating an SDK Instance

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Log debug messages to the console
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

To launch the iFrame, HubSpot requires these parameters:

```json
{
  "name": "string", // App name
  "url": "string", // App URL
  "width": number, // iFrame width
  "height": number, // iFrame height
  "isReady": boolean, // Ready for production (false during testing)
  "supportsCustomObjects": true //Support calls from custom objects
}
```

### Using the Calling Settings Endpoint

Use the API (e.g., Postman) to set app settings. Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  Set `isReady` to `false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.


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

[Publish your app to the marketplace here](LINK_TO_MARKETPLACE - replace with actual link).


## Events

### Sending Messages to HubSpot

*   `initialized`: Notifies HubSpot that the softphone is ready.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
*   `userLoggedIn`: Notifies HubSpot of user login.
*   `userLoggedOut`: Notifies HubSpot of user logout.
*   `outgoingCall`: Notifies HubSpot of an outgoing call.  Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
*   `callAnswered`: Notifies HubSpot that a call has been answered. Payload: `{ externalCallId: string }`
*   `callEnded`: Notifies HubSpot that a call has ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
*   `callCompleted`: Notifies HubSpot that a call is complete. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
*   `sendError`: Reports an error to HubSpot. Payload: `{ message: string }`
*   `resizeWidget`: Requests a widget resize. Payload: `{ height: number, width: number }`


### Receiving Messages from HubSpot

*   `onReady`: HubSpot is ready to receive messages.
*   `onDialNumber`: An outbound call is initiated.
*   `onEngagementCreated` (Deprecated): Use `onCreateEngagementSucceeded`.
*   `onNavigateToRecordFailed`: Navigation to a record failed.
*   `onPublishToChannelSucceeded`: Publishing to a channel succeeded.
*   `onPublishToChannelFailed`: Publishing to a channel failed.
*   `onCallerIdMatchSucceeded`: Caller ID match succeeded.
*   `onCallerIdMatchFailed`: Caller ID match failed.
*   `onCreateEngagementSucceeded`: Engagement creation succeeded.
*   `onCreateEngagementFailed`: Engagement creation failed.
*   `onUpdateEngagementSucceeded`: Engagement update succeeded.
*   `onUpdateEngagementFailed`: Engagement update failed.
*   `onVisibilityChanged`: Widget visibility changed.
*   `defaultEventHandler`: Default event handler.


Detailed payloads for each event are described in the section above.


## Frequently Asked Questions

* **Authentication:** The calling app handles authentication.
* **CDN Hosting:** Yes, the SDK is hosted on jsDeliver.  Example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; the app updates them afterward.  For calls outside HubSpot, the app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Adding to Existing App:** Yes, add functionality to an existing app.  Existing users automatically get access.
* **Integrating Existing Softphone:**  Yes, easily integrate your existing softphone.
* **Multiple Integrations:** Yes, users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic Integration Appearance:** Yes, for updated apps.
* **User Installation/Uninstallation:** Only users with permissions can install/uninstall.
* **Custom Calling Property:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, if using the SDK and setting `createEngagement: true` in `outgoingCall`.



Remember to replace placeholder links with actual links where applicable.  This markdown provides a structured and comprehensive representation of the provided text.
