# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling options into their HubSpot apps.

## Overview

The Calling Extensions SDK allows apps to offer a customized calling experience directly from CRM records within HubSpot.  It consists of three key components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling IFrame:** The interface displayed to HubSpot users, configured via the calling settings endpoints.

For a detailed understanding of the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE).  Once integrated, your app will appear in the HubSpot call switcher.  Only outgoing calls are currently supported.


## Getting Started

### Prerequisites

* A HubSpot developer account ([sign up here](LINK_TO_SIGNUP)).
* A HubSpot app (create one from your [HubSpot developer account](LINK_TO_DEVELOPER_ACCOUNT)).
* Node.js installed on your environment.


### Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:** A more advanced implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** Demo apps use mock data and are not fully functional calling applications.

### Installing the Demo App

1. Clone, fork, or [download the ZIP](LINK_TO_ZIP) of the demo repository.
2. Navigate to the demo app's root directory (`demos/demo-minimal-js` or `demos/demo-react-ts`).
3. Run the following command (replace with the appropriate directory):

   ```bash
   npm i && npm start
   ```

This installs dependencies and starts the app at `https://localhost:9025/`. You may need to bypass a security warning.

### Launching the Demo App from HubSpot

1. Navigate to HubSpot Contacts (`Contacts > Contacts`) or Companies (`Contacts > Companies`).
2. Open your browser's developer console.
3. Run one of the following commands based on your installation method:

   * **Installed Demo:**
     ```javascript
     localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');
     ```

   * **`demo-minimal-js` (uninstalled):**
     ```javascript
     localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');
     ```

   * **`demo-react-ts` (uninstalled):**
     ```javascript
     localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');
     ```

4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Installing the Calling Extensions SDK

Add the SDK to your app using npm or yarn:

* **npm:**
  ```bash
  npm i --save @hubspot/calling-extensions-sdk
  ```
* **yarn:**
  ```bash
  yarn add @hubspot/calling-extensions-sdk
  ```


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends messages (events), and your app responds via event handlers.

### Events

**Sent to HubSpot:**

* `initialized`: Softphone ready.
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started.
* `callAnswered`: Outgoing call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`: Error occurred.
* `resizeWidget`: Resize widget request.

**Received from HubSpot:**

* `onReady`: HubSpot ready.
* `onDialNumber`: Dial number event.
* `onEngagementCreated` (deprecated; use `onCreateEngagementSucceeded` instead): Engagement created.
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


### SDK API

Create a `CallingExtensions` instance with optional `eventHandlers` and `debugMode`:

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

Each event handler receives an event object with relevant data.  See the "Events" section for details on each event's payload.


### Calling Settings Endpoint

Use the settings API (e.g., with `curl` or Postman) to configure your app:

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"My App","url":"https://my-app.com","height":600,"width":400,"isReady":false}'
```

Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your app's ID and API key.  The `isReady` flag should be `false` during testing and `true` for production.  The endpoint also supports `PATCH`, `GET`, and `DELETE`.


### LocalStorage Override

For testing, override settings using localStorage:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


### Preparing for Production

Set `isReady` to `true` via the PATCH endpoint before publishing.


### Publishing to the Marketplace

Once ready, publish your app to the HubSpot marketplace ([more details here](LINK_TO_MARKETPLACE)).


## Frequently Asked Questions (FAQ)

* **Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver.
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them. For calls initiated outside, your app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:**  Functionality can be added to existing marketplace apps.
* **Softphone Integration:** Easily integrate existing softphones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free User Installation:** Yes.
* **Automatic App Update:** Yes, for existing users.
* **User Installation/Uninstallation:** Controlled by user permissions.
* **Custom Calling Properties:**  Yes, using the properties API.
* **Custom Object Calls:** Yes, if using the SDK and setting `createEngagement: true` in `outgoingCall`.


This markdown documentation provides a structured overview of the HubSpot Calling Extensions SDK. Remember to replace placeholder links with actual URLs.  Further details on specific events and API calls are included within the original text, which this markdown organizes and formats.
