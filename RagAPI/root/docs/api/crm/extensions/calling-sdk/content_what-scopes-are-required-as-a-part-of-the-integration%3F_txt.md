# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK allows apps to offer custom calling options directly from CRM records within HubSpot.  It consists of three key components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:**  Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:** The interface displayed to HubSpot users, configured via the settings endpoints.

For a detailed understanding of the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE_REQUIRED).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.  If you don't have a HubSpot app, you can [create one here](LINK_TO_APP_CREATION_REQUIRED).  If you lack a HubSpot developer account, sign up [here](LINK_TO_SIGNUP_REQUIRED).


## Getting Started

### Running the Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  The SDK instantiation is shown in `index.js`.
* **`demo-react-ts`:** A more realistic implementation using React, TypeScript, and Styled Components. SDK instantiation is in `useCti.ts`.

**Note:** These demos use mock data and are not fully functional calling apps.

### Installing the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP_REQUIRED) of the repository.
3. Navigate to the project's root directory in your terminal.
4. Run the appropriate command:

   * **`demo-minimal-js`:**  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

   This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launching the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console and run one of the following commands, depending on your installation method:

   * **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

3. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Installing the Calling Extensions SDK

Add the SDK as a dependency to your calling app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses events for communication between your app and HubSpot.

### Events

**Sent to HubSpot:**

* `initialized`: Softphone ready.
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started.
* `callAnswered`: Outgoing call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`: Error encountered.
* `resizeWidget`: Widget resize request.

**Received from HubSpot:**

* `onReady`: HubSpot is ready.
* `onDialNumber`: Outbound call initiated.
* `onEngagementCreated` (deprecated, use `onCreateEngagementSucceeded` instead): Engagement created.
* `onNavigateToRecordFailed`: Navigation to record failed.
* `onPublishToChannelSucceeded`: Publish to channel succeeded.
* `onPublishToChannelFailed`: Publish to channel failed.
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement creation succeeded.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onUpdateEngagementSucceeded`: Engagement update succeeded.
* `onUpdateEngagementFailed`: Engagement update failed.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Default event handler.


### SDK API Example

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

### Testing Your App

HubSpot requires these iFrame parameters to launch the calling extension:

```json
{
  "name": "App Name",
  "url": "App URL",
  "width": 600,
  "height": 400,
  "isReady": false, // Set to false during testing
  "supportsCustomObjects": true
}
```

### Using the Calling Settings Endpoint

Use the HubSpot settings API (e.g., with `curl`) to manage your app's settings.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  The `isReady` flag should be `false` during testing and set to `true` for production using a PATCH request.

```bash
# POST (Add settings)
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'

# PATCH (Update settings)
curl --request PATCH \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"isReady":true}'
```

### Overriding Settings with localStorage

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

Set `isReady` to `true` using the PATCH endpoint.


### Publishing to the HubSpot Marketplace

[Details on publishing your app to the marketplace](LINK_TO_MARKETPLACE_PUBLISHING_REQUIRED).


## Frequently Asked Questions

This section provides answers to common questions regarding the HubSpot Calling Extensions SDK.  (Detailed answers are provided in the original text and should be incorporated here)


## Feedback

Please share your feedback on this documentation. (Link to feedback mechanism)

