# HubSpot Calling Extensions SDK Documentation

This document provides comprehensive information on the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling options into their HubSpot apps.

## Overview

The Calling Extensions SDK facilitates communication between your app and HubSpot, allowing users to make calls directly from CRM records.  A calling extension comprises three core components:

1. **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure calling settings for your app on a per-HubSpot account basis.
3. **Calling iframe:**  Displays your app to HubSpot users; its configuration is managed via the calling settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE_HERE).  Once integrated, your app will appear in HubSpot's call switcher.

**Note:** Currently, only outgoing calls are supported.


## Getting Started

### Prerequisites:

* A HubSpot developer account ([Sign up here](LINK_TO_SIGN_UP_HERE)).
* A HubSpot app (create one from your [HubSpot developer account](LINK_TO_DEVELOPER_ACCOUNT_HERE) if needed).
* Node.js installed on your environment.


### 1. Run the Demo Calling App

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more realistic implementation using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** Demo apps use mock data and are not fully functional calling applications.


### 2. Install the Demo App

1. Clone, fork, or [download the ZIP](LINK_TO_ZIP_HERE) of the repository.
2. Navigate to the project's root directory in your terminal.
3. Run the appropriate command:

   * **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

   This installs dependencies and starts the app (access it at `https://localhost:9025/`). You might need to bypass a security warning.


### 3. Launch the Demo App from HubSpot

1. Go to either **Contacts > Contacts** or **Contacts > Companies** in your HubSpot account.
2. Open your browser's developer console.
3. Run the appropriate `localStorage` command:

   * **Installed demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.
5. Click the "Call" icon, select the demo app from the "Call from" dropdown, and click "Call."


### 4. Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends messages via events, and your app responds via event handlers.

### Events

#### Sending Messages to HubSpot

* **`initialized`**:  Signals softphone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn`**:  Indicates user login.
* **`userLoggedOut`**: Indicates user logout.
* **`outgoingCall`**:  Notifies HubSpot of an outgoing call.  Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered`**: Notifies HubSpot that a call has been answered. Payload: `{ externalCallId: string }`
* **`callEnded`**: Notifies HubSpot that a call has ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted`**: Notifies HubSpot that a call is completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError`**: Reports errors to HubSpot. Payload: `{ message: string }`
* **`resizeWidget`**: Requests a widget resize. Payload: `{ height: number, width: number }`

#### Receiving Messages from HubSpot

* **`onReady`**: HubSpot is ready for communication.
* **`onDialNumber`**: User initiates an outbound call.
* **`onEngagementCreated`**: (Deprecated; use `onCreateEngagementSucceeded`) HubSpot creates an engagement.
* **`onNavigateToRecordFailed`**: Navigation to a record fails.
* **`onPublishToChannelSucceeded`**: Publishing to a channel succeeds.
* **`onPublishToChannelFailed`**: Publishing to a channel fails.
* **`onCallerIdMatchSucceeded`**: Caller ID match succeeds.
* **`onCallerIdMatchFailed`**: Caller ID match fails.
* **`onCreateEngagementSucceeded`**: Engagement creation succeeds.
* **`onCreateEngagementFailed`**: Engagement creation fails.
* **`onUpdateEngagementSucceeded`**: Engagement update succeeds.
* **`onUpdateEngagementFailed`**: Engagement update fails.
* **`onVisibilityChanged`**: Widget visibility changes.
* **`defaultEventHandler`**: Default event handler.


### SDK Instantiation Example

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

###  Testing Your App

To launch the calling extensions iframe, HubSpot requires these iframe parameters:

```json
{
  "name": "App Name",
  "url": "App URL",
  "width": 400,
  "height": 600,
  "isReady": false, // Set to false during testing
  "supportsCustomObjects": true
}
```

### Using the Calling Settings Endpoint

Use your API tool (e.g., Postman) to manage app settings via these endpoints: `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY` (supports POST, PATCH, GET, DELETE).  Remember to set `isReady` to `true` for production.

### Overriding Settings with localStorage

For testing, you can override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Getting Your App Ready for Production

Set `isReady` to `true` using the PATCH endpoint.

### Publishing to the HubSpot Marketplace

[Learn how to publish your app to the HubSpot marketplace](LINK_TO_MARKETPLACE_INFO_HERE).

## Frequently Asked Questions

* **User Authentication:** Handled by your app.
* **CDN Hosting:** Yes, via jsDeliver ([example](https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js)).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them and creates engagements for calls initiated outside the UI.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:**  You can add this functionality to existing apps; existing users will automatically have access.
* **Softphone Integration:** Easily integrate existing softphones.
* **Multiple Integrations:** Yes, users can use multiple integrations simultaneously.
* **Free User Access:** Yes.
* **Automatic Integration Appearance:** Yes, for updated apps.
* **User Installation/Uninstallation:** Only users with appropriate permissions.
* **Custom Calling Properties:** Yes, via the properties API.
* **Calls from Custom Objects:** Yes, if using the SDK to create engagements (`outgoingCall({ createEngagement: true })`).


This markdown file provides a structured and well-formatted documentation for the HubSpot Calling Extensions SDK.  Remember to replace placeholder links (`LINK_TO_ARTICLE_HERE`, etc.) with the actual URLs.
