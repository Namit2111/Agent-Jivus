# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality directly into HubSpot's CRM.

## Overview

The Calling Extensions SDK enables apps to provide a customized calling experience for HubSpot users, directly from CRM records.  It consists of three main components:

* **Calling Extensions SDK (JavaScript):**  Facilitates communication between your app and HubSpot.
* **Calling Settings Endpoints:** Used to configure your app's calling settings for each connected HubSpot account.
* **Calling iFrame:**  The interface displayed to HubSpot users, configured via the calling settings endpoints.

For details on the in-app calling experience, see [this knowledge base article](link-to-knowledge-base-article-here).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.

## Getting Started

### 1. Create a HubSpot App

If you don't have an app, create one from your [HubSpot developer account](link-to-hubspot-developer-account-creation).  If you don't have a developer account, sign up [here](link-to-hubspot-developer-signup).

### 2. Run the Demo App

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.

#### Installation (Optional):

1. Install Node.js.
2. Clone, fork, or [download the ZIP](link-to-zip-download) of the repository.
3. Navigate to the demo app directory:
   * For `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * For `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.

### 3. Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console and run one of these commands:
    * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
3. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".


## Installing the SDK

Add the Calling Extensions SDK to your app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends messages, and your app responds via event handlers.


### Events

#### Sending Messages to HubSpot

* **`initialized`**: Notifies HubSpot the softphone is ready.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn`**:  Notifies HubSpot of user login.
* **`userLoggedOut`**: Notifies HubSpot of user logout.
* **`outgoingCall`**: Notifies HubSpot of an outgoing call. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`  `phoneNumber` is deprecated; use `toNumber`.
* **`callAnswered`**: Notifies HubSpot the call is answered. Payload: `{ externalCallId: string }`
* **`callEnded`**: Notifies HubSpot the call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`  `EndStatus` enum values: `INTERNAL_COMPLETED`, `INTERNAL_FAILED`, `INTERNAL_CANCELED`, `INTERNAL_BUSY`, `INTERNAL_NO_ANSWER`, `INTERNAL_REJECTED`, `INTERNAL_MISSED`
* **`callCompleted`**: Notifies HubSpot the call is complete. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError`**: Reports errors to HubSpot. Payload: `{ message: string }`
* **`resizeWidget`**: Requests a widget resize. Payload: `{ height: number, width: number }`


#### Receiving Messages from HubSpot

* **`onReady`**: HubSpot is ready. Payload: `{ engagementId: number, iframeLocation: Enum, ownerId: String | Number, portalId: Number, userId: Number }`  `iframeLocation` enum values: `widget`, `remote`, `window`.
* **`onDialNumber`**: Outbound call initiated.  Payload includes phone number, owner ID, subject ID, object ID, object type, portal ID, country code, callee info, start timestamp, and `toPhoneNumberSrc`.
* **`onEngagementCreated`**: *(Deprecated)* Use `onCreateEngagementSucceeded` instead. Payload: `{ engagementId: number }`
* **`onNavigateToRecordFailed`**: Navigation to record failed. Payload: `{ engagementId: number, objectCoordinates: object }`
* **`onPublishToChannelSucceeded`**: Publishing to channel succeeded. Payload: `{ engagementId: number, externalCallId: string }`
* **`onPublishToChannelFailed`**: Publishing to channel failed. Payload: `{ engagementId: number, externalCallId: string }`
* **`onCallerIdMatchSucceeded`**: Caller ID match succeeded.
* **`onCallerIdMatchFailed`**: Caller ID match failed.
* **`onCreateEngagementSucceeded`**: Engagement creation succeeded.
* **`onCreateEngagementFailed`**: Engagement creation failed.
* **`onVisibilityChanged`**: Widget visibility changed. Payload: `{ isMinimized: boolean, isHidden: boolean }`
* **`defaultEventHandler`**: Default event handler.


### Example SDK Initialization

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true,
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: event => { /* ... */ },
    onCreateEngagementSucceeded: event => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Calling Settings Endpoint

Use the API (e.g., `curl`) to manage settings:

```bash
# Example: POST (add settings)
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'

# Supports PATCH, GET, DELETE as well.
```

`isReady: false` during testing; set to `true` for production.

### Overriding Settings (for testing) using `localStorage`

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production & Marketplace

Set `isReady` to `true` using the PATCH endpoint.  For publishing to the HubSpot marketplace, see [this link](link-to-marketplace-publishing-guide).


## Frequently Asked Questions

* **Authentication:** Handled by the calling app.
* **CDN:** Yes, hosted on jsDeliver (example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; apps update them afterward.  For calls initiated outside, apps should create the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:** Functionality can be added to existing marketplace apps.
* **Softphone Integration:**  Easily integrate existing softphones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free Users:** All users can install the app.
* **Automatic Appearance:** The integration automatically appears for existing users.
* **User Permissions:** Only users with appropriate permissions can install/uninstall.
* **Custom Calling Properties:**  Creatable via the properties API.
* **Custom Object Calls:** Supported if the SDK is used to create calls and the `outgoingCall` event is used to notify HubSpot.  Ensure `outgoingCall({ createEngagement: true });`


## Appendix: Detailed Event Information (Tables)

*(The tables for each event's payload have been omitted for brevity, as they are already present and detailed within the provided text.  Including them here would result in significant redundancy.)*
