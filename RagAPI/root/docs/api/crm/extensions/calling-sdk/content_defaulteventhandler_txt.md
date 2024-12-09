# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot CRM records.

## Overview

The Calling Extensions SDK enables communication between your application and HubSpot, providing a custom calling experience for HubSpot users directly from CRM records.  It consists of three key components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:**  The interface displayed to HubSpot users, configured via the calling settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](LINK_TO_KNOWLEDGE_BASE_ARTICLE).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Only outgoing calls are currently supported.

## Getting Started

### 1. Create a HubSpot App

If you don't have an existing app, create one in your HubSpot developer account. [Sign up for a developer account here](LINK_TO_DEVELOPER_SIGNUP).


### 2. Demo Applications

Test the SDK using two demo apps:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS.  SDK instantiation is in `index.js`.
* **`demo-react-ts`:**  A more comprehensive implementation using React, TypeScript, and Styled Components. SDK instantiation is in `useCti.ts`.

**Note:** Demo apps use mock data and are not fully functional calling applications.


### 3. Installing the Demo App

1. Install Node.js.
2. Clone, fork, or download the ZIP of the repository.
3. Navigate to the project's root directory.
4. Run the following command (replace with the appropriate demo app):

   * For `demo-minimal-js`:  `cd demos/demo-minimal-js && npm i && npm start`
   * For `demo-react-ts`:  `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app at `https://localhost:9025/`. You may need to bypass a security warning.


### 4. Launching the Demo App from HubSpot

1. Navigate to HubSpot Contacts (`Contacts > Contacts`) or Companies (`Contacts > Companies`).
2. Open your browser's developer console and run one of the following commands, depending on your installation method:

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

3. Refresh the page.  Select the demo app from the "Call from" dropdown in the call switcher.


### 5. Installing the Calling Extensions SDK

Add the SDK to your calling app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  Events are sent and received via methods and event handlers.

### Events

**Sending Messages to HubSpot:**

* `initialized`: Softphone readiness. Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User login notification.
* `userLoggedOut`: User logout notification.
* `outgoingCall`: Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Outgoing call answered. Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted`: Call completed.  Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`: Error notification. Payload: `{ message: string }`
* `resizeWidget`: Widget resize request. Payload: `{ height: number, width: number }`


**Receiving Messages from HubSpot:**

* `onReady`: HubSpot readiness notification. Payload: `{ engagementId: number, iframeLocation: Enum, ownerId: string | number, portalId: number, userId: number }`
* `onDialNumber`: Outbound call triggered.  Payload includes phone number, owner ID, subject ID, object ID, object type, portal ID, country code, callee info, start timestamp, and phone number source.
* `onEngagementCreated`: (Deprecated. Use `onCreateEngagementSucceeded`) Engagement created.
* `onNavigateToRecordFailed`: Record navigation failure.
* `onPublishToChannelSucceeded`: Channel publishing success.
* `onPublishToChannelFailed`: Channel publishing failure.
* `onCallerIdMatchSucceeded`: Caller ID match success.
* `onCallerIdMatchFailed`: Caller ID match failure.
* `onCreateEngagementSucceeded`: Engagement creation success.
* `onCreateEngagementFailed`: Engagement creation failure.
* `onVisibilityChanged`: Widget visibility change.
* `defaultEventHandler`: Default event handler.


### SDK Initialization

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Optional: Enable debug logging
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Testing Your App

HubSpot requires these iFrame parameters:

```javascript
{
  name: string, // App name
  url: string, // App URL
  width: number, // iFrame width
  height: number, // iFrame height
  isReady: boolean, // Production readiness (false for testing)
  supportsCustomObjects: true // Support for custom objects (optional)
}
```


### Calling Settings Endpoint

Use the API to manage your app's settings (POST, PATCH, GET, DELETE).  Example using `curl`:

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

Remember to replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`.  Set `isReady` to `true` for production.


### Local Storage Override

For testing, override settings using local storage:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


### Production Readiness

Set `isReady` to `true` in your app settings using the PATCH endpoint.


### Publishing to the Marketplace

Publish your app to the HubSpot marketplace [here](LINK_TO_MARKETPLACE_INFO).


## Frequently Asked Questions

* **Authentication:** Handled by your calling app.
* **CDN Hosting:** Yes, via jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them.  Create engagements for calls initiated outside the HubSpot UI.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Applications:** Add this functionality to existing apps; existing users will automatically get the update.
* **Softphone Integration:** Easily integrate existing softphones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free Users:** All users can install the app.
* **Automatic App Appearance:** Yes, for existing users.
* **User Installation/Uninstallation:** Controlled by user permissions.
* **Custom Calling Properties:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, using the SDK to create engagements (`outgoingCall({ createEngagement: true })`).



This markdown provides a comprehensive overview of the HubSpot Calling Extensions SDK. Remember to replace placeholder links (`LINK_TO_...`) with the actual URLs.
