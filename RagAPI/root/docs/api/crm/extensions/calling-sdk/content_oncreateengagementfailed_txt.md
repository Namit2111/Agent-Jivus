# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot directly from CRM records.

## Overview

The Calling Extensions SDK facilitates communication between your app and HubSpot, providing a custom calling experience for HubSpot users.  It consists of three main components:

1. **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:**  Displays your app to HubSpot users; configured via the calling settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.  If you don't have a HubSpot app, you can [create one here](LINK_TO_CREATE_APP). If you need a HubSpot developer account, [sign up here](LINK_TO_SIGN_UP).


## Getting Started

### 1. Run the Demo Calling App

Two demo apps are available:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.

### 2. Install the Demo App (Optional)

1. Install Node.js.
2. Clone, fork, or download the ZIP of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * For `demo-minimal-js`:  `cd demos/demo-minimal-js && npm i && npm start`
   * For `demo-react-ts`:  `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.

### 3. Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands, depending on your installation method:

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (Uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (Uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page. Click the "Call" icon, select the demo app from the "Call from" dropdown, and click "Call".


### 4. Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends messages via events, and your app responds through event handlers.

### Events

**Sent to HubSpot:**

* `initialized`:  Softphone ready status.
* `userLoggedIn`: User login notification.
* `userLoggedOut`: User logout notification.
* `outgoingCall`: Outgoing call initiated.
* `callAnswered`: Outgoing call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`:  Error encountered.
* `resizeWidget`: Request to resize the widget.

**Received from HubSpot:**

* `onReady`: HubSpot ready to receive messages.
* `onDialNumber`: Outbound call triggered.
* `onEngagementCreated` (Deprecated - use `onCreateEngagementSucceeded`): Engagement created.
* `onNavigateToRecordFailed`: Record navigation failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publishing to channel status.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match status.
* `onCreateEngagementSucceeded`/`onCreateEngagementFailed`: Engagement creation status.
* `onUpdateEngagementSucceeded`/`onUpdateEngagementFailed`: Engagement update status.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Default event handler.


### SDK Initialization

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    onCreateEngagementSucceeded: (event) => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Testing Your App

To display the calling iFrame, provide these parameters to HubSpot:

```javascript
{
  name: "Your App Name",
  url: "Your App URL",
  width: 400,
  height: 600,
  isReady: false, // Set to false during testing
  supportsCustomObjects: true
}
```

### Calling Settings Endpoint

Use your API tool (e.g., Postman) to manage app settings via the following API endpoint, replacing `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values:

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"Your App Name","url":"Your App URL","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.  Set `isReady` to `true` when your app is ready for production.


### Overriding Settings with localStorage

For testing, override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'My App URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production Readiness and Marketplace Publishing

Once your settings are configured, set `isReady` to `true` using the `PATCH` endpoint.  Finally, publish your app to the HubSpot Marketplace [here](LINK_TO_MARKETPLACE).


## Frequently Asked Questions

* **Authentication:** Your app handles authentication.
* **CDN Hosting:** Yes, via jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them. For calls outside the UI, your app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:**  Add this functionality to existing apps; existing users will automatically get the update.
* **Softphone Integration:** Easily integrate your existing softphone.
* **Multiple Integrations:** Yes, users can use multiple integrations simultaneously.
* **Free User Access:** Yes, all users can install the app.
* **Automatic App Appearance:** Yes, for existing users of updated apps.
* **User Installation/Uninstallation:** Only users with appropriate permissions can install/uninstall.
* **Custom Calling Properties:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, using only the SDK to create calls and notifying HubSpot via the `outgoingCall` event (`createEngagement: true`).


This documentation provides a comprehensive guide to using the HubSpot Calling Extensions SDK.  Remember to replace placeholder values with your actual data and consult the HubSpot API documentation for further details.
