# HubSpot CRM API: Calling Extensions SDK

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot CRM.

## Overview

The Calling Extensions SDK enables apps to offer a customized calling experience directly from CRM records.  This integration consists of three core elements:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:** The interface your app presents to HubSpot users, configured via the calling settings endpoints.

For a detailed understanding of the in-app calling experience, refer to [this knowledge base article](link_to_article_here).  Once integrated, your app will appear as an option in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.

## Getting Started

If you don't have a HubSpot app, you can [create one from your HubSpot developer account](link_to_create_app_here). If you need a developer account, sign up [here](link_to_signup_here).

### Run the Demo Calling App

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components.  See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling applications.

### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](link_to_zip_here) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * For `demo-minimal-js`:  `cd demos/demo-minimal-js && npm i && npm start`
   * For `demo-react-ts`:  `cd demos/demo-react-ts && npm i && npm start`

   This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console and run the following command, depending on your chosen demo and whether it was installed:

   * **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

3. Refresh the page. Click the "Call" icon, select the demo app from the dropdown, and click "Call".

### Install the Calling Extensions SDK

Add the SDK as a dependency to your calling app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends messages (events), and your app responds via event handlers.

### Events

**HubSpot Sends:**

* `initialized`: SDK is ready.
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `onDialNumber`: Outbound call initiated.
* `onEngagementCreated`: (Deprecated) Engagement created. Use `onCreateEngagementSucceeded` instead.
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`: Publishing to a channel succeeded.
* `onPublishToChannelFailed`: Publishing to a channel failed.
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement successfully created.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement successfully updated.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Call widget visibility changed.


**Your App Sends:**

* `initialized`: Softphone ready.
* `userLoggedIn`: User logged in (only if not logged in on `initialized`).
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started.
* `callAnswered`: Call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`: Error encountered.
* `resizeWidget`: Resize widget request.

(Detailed event descriptions and payloads are provided in the original text; they are too extensive to reproduce here completely).

### SDK Initialization

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Enable debug logging
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

To launch the calling extensions iFrame, HubSpot requires these iFrame parameters:

```javascript
{
  name: "Your App Name",
  url: "Your App URL",
  width: 400,
  height: 600,
  isReady: false, // Set to false during testing
  supportsCustomObjects: true //Optional
}
```

### Using the Calling Settings Endpoint

Use the HubSpot API to set your app's settings.  Remember to replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

(This endpoint also supports `PATCH`, `GET`, and `DELETE`.)

### Overriding Settings with localStorage

For testing, override settings in the browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production Readiness

Set `isReady` to `true` using the `PATCH` endpoint when your app is ready for production.

### Publishing to the Marketplace

Once ready, publish your app to the HubSpot marketplace [here](link_to_marketplace_here).


## Frequently Asked Questions

The original text includes a FAQ section which is too long to reproduce here completely.  It covers topics like authentication, CDN hosting, engagement creation/updates, required scopes, integrating with existing apps, multi-integration support, free user access, automatic updates, user permissions, custom calling properties, and making calls from custom objects.


This Markdown documentation provides a structured overview of the HubSpot Calling Extensions SDK, allowing developers to quickly grasp the key concepts and begin integration.  Remember to consult the original text for complete details on events, payloads, and API calls.
