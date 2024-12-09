# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options directly into HubSpot CRM records.

## Overview

The Calling Extensions SDK facilitates communication between your calling app and HubSpot, providing a custom calling experience for users within the CRM.  The system consists of three key components:

1. **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:**  The interface displayed to HubSpot users, configured via the calling settings endpoints.

For details on the in-app calling experience, see [this knowledge base article](LINK_TO_ARTICLE_HERE).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Only outgoing calls are currently supported.  If you need to create a new app, you can [create one from your HubSpot developer account](LINK_TO_CREATION_PAGE_HERE).  If you don't have a developer account, sign up [here](LINK_TO_SIGNUP_PAGE_HERE).


## Getting Started

### Demo Apps

Two demo apps are available for testing the SDK:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.

### Installing the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP_HERE) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * For `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * For `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launching the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands, depending on your installation method:

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Installing the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses methods and event handlers for message exchange.  See the [Events section](#events) for a complete list.

### SDK Initialization

Create a `CallingExtensions` instance with options, including `eventHandlers`:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Set to true for debugging
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Dial number received */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```


### iFrame Parameters

To launch the calling extensions iFrame, HubSpot requires these parameters:

```json
{
  "name": "Your App Name",
  "url": "Your App URL",
  "width": 400,
  "height": 600,
  "isReady": true, // Set to false during testing
  "supportsCustomObjects": true
}
```

### Calling Settings Endpoint

Use the API to manage your app's settings.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values:

```bash
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.  Set `isReady` to `true` for production.

### Local Storage Override (for testing)

Override settings using the browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production Readiness

Set `isReady` to `true` via the API's PATCH endpoint once testing is complete.


### Publishing to the Marketplace

[Learn how to publish your app to the HubSpot Marketplace](LINK_TO_MARKETPLACE_PAGE_HERE).


## Events

### Sending Messages to HubSpot

* `initialized`: Softphone ready.
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started.
* `callAnswered`: Outgoing call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`: Error occurred.
* `resizeWidget`: Resize widget request.


### Receiving Messages from HubSpot

* `onReady`: HubSpot is ready.
* `onDialNumber`: Outbound call triggered in HubSpot.
* `onEngagementCreated`: (Deprecated. Use `onCreateEngagementSucceeded`.) Engagement created.
* `onNavigateToRecordFailed`: Navigation to record failed.
* `onPublishToChannelSucceeded`: Publishing to channel succeeded.
* `onPublishToChannelFailed`: Publishing to channel failed.
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement creation succeeded.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement update succeeded.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Default event handler.


Detailed descriptions and parameters for each event are provided in the original text.  Refer to the original for complete details on each event's payload.

## Frequently Asked Questions (FAQs)

The FAQs section of the original text contains answers to common questions regarding authentication, CDN hosting, engagement creation/updates, required scopes, app integration, multiple integrations, free user access, automatic updates, user permissions, custom properties, and custom object calls.  Refer to the original text for the complete answers.


Remember to replace placeholder links (`LINK_TO_ARTICLE_HERE`, etc.) with the actual URLs.
