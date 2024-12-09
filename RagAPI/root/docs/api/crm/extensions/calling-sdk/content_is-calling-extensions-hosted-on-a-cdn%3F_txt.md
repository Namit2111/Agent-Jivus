# HubSpot CRM API Calling Extensions SDK Documentation

This document details the HubSpot CRM API Calling Extensions SDK, allowing developers to integrate custom calling options directly into HubSpot CRM records.

## Overview

The Calling Extensions SDK enables communication between your app and HubSpot, providing a custom calling experience for users within the CRM.  The system comprises three key parts:

1. **Calling Extensions SDK (JavaScript):**  Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Used to configure the settings for your calling app on a per-HubSpot account basis.
3. **Calling iFrame:** The interface displayed to HubSpot users, configured via the calling settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](link-to-knowledge-base-article).  Once integrated, your app will appear in the HubSpot call switcher.  If you don't have a HubSpot app, you can [create one here](link-to-create-hubspot-app).  If you need a HubSpot developer account, [sign up here](link-to-sign-up).


**Note:** Currently, only outgoing calls are supported.


## Getting Started

### Run the Demo Calling App

Two demo apps are available:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.

### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](link-to-zip) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`**:  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`**: `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.

### Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands based on your installation:

   * **Installed `demo-minimal-js` or `demo-react-ts`**: `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Uninstalled `demo-minimal-js`**: `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Uninstalled `demo-react-ts`**: `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Install the Calling Extensions SDK

Add the SDK to your app:

* **npm**: `npm i --save @hubspot/calling-extensions-sdk`
* **yarn**: `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends messages (events) to your app, and your app responds using methods provided by the SDK.

### Events

#### Sending Messages to HubSpot

* **`initialized`**: Notifies HubSpot that the softphone is ready.  Payload: `{isLoggedIn: boolean, engagementId: number}`.
* **`userLoggedIn`**: Notifies HubSpot of user login.
* **`userLoggedOut`**: Notifies HubSpot of user logout.
* **`outgoingCall`**: Notifies HubSpot of an outgoing call. Payload: `{phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string}`.
* **`callAnswered`**: Notifies HubSpot that a call has been answered. Payload: `{externalCallId: string}`.
* **`callEnded`**: Notifies HubSpot that a call has ended. Payload: `{externalCallID: string, engagementId: number, callEndStatus: EndStatus}`.  `callEndStatus` options: `INTERNAL_COMPLETED`, `INTERNAL_FAILED`, `INTERNAL_CANCELED`, `INTERNAL_BUSY`, `INTERNAL_NO_ANSWER`, `INTERNAL_REJECTED`, `INTERNAL_MISSED`.
* **`callCompleted`**: Notifies HubSpot that a call is complete. Payload: `{engagementId: number, hideWidget: boolean, engagementProperties: {[key: string]: string}, externalCallId: number}`.
* **`sendError`**: Sends an error message to HubSpot. Payload: `{message: string}`.
* **`resizeWidget`**: Requests a widget resize. Payload: `{height: number, width: number}`.

#### Receiving Messages from HubSpot

* **`onReady`**: HubSpot is ready for communication.
* **`onDialNumber`**: An outbound call is initiated.
* **`onEngagementCreated`**: *(Deprecated - use `onCreateEngagementSucceeded`)* Engagement created.
* **`onNavigateToRecordFailed`**: Navigation to a record failed.
* **`onPublishToChannelSucceeded`**: Publishing to a channel succeeded.
* **`onPublishToChannelFailed`**: Publishing to a channel failed.
* **`onCallerIdMatchSucceeded`**: Caller ID match successful.
* **`onCallerIdMatchFailed`**: Caller ID match failed.
* **`onCreateEngagementSucceeded`**: Engagement creation successful.
* **`onCreateEngagementFailed`**: Engagement creation failed.
* **`onUpdateEngagementSucceeded`**: Engagement update successful.
* **`onUpdateEngagementFailed`**: Engagement update failed.
* **`onVisibilityChanged`**: Widget visibility changed.
* **`defaultEventHandler`**: Default event handler.


### SDK Initialization

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // optional
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Testing Your App

To launch the calling extensions iFrame, HubSpot requires these iFrame parameters:

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

### Using the Calling Settings Endpoint

Use the API to configure your app's settings.  Remember to replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`. The `isReady` flag should be `false` during testing.


```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.


### Overriding Extension Settings using localStorage

For testing, you can override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Getting Your App Ready for Production

Set `isReady` to `true` using the `PATCH` endpoint.

### Publishing Your App to the HubSpot Marketplace

[Instructions here](link-to-marketplace-instructions)


## Frequently Asked Questions

* **Authentication:** Handled by your calling app.
* **CDN Hosting:** Yes, via jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them.  For calls outside the HubSpot UI, your app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:**  You can add this functionality to existing marketplace apps.
* **Softphone Integration:** Easily integrable.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free User Access:** Yes.
* **Automatic Appearance:** Yes, for updated apps.
* **User Installation/Uninstallation:** Controlled by user permissions.
* **Custom Calling Properties:** Yes, using the properties API.
* **Custom Object Calls:** Yes, if using the SDK to create calls and using `outgoingCall({ createEngagement: true })`.


## Feedback

[Feedback form](link-to-feedback-form)

