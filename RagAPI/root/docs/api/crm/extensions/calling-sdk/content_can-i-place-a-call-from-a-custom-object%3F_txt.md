# HubSpot Calling Extensions SDK Documentation

This document provides comprehensive information on using the HubSpot Calling Extensions SDK to integrate custom calling functionality into your HubSpot applications.

## Overview

The HubSpot Calling Extensions SDK enables apps to offer a custom calling experience directly from CRM records.  It consists of three key components:

* **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
* **Calling Settings Endpoints:** Configure calling settings for each connected HubSpot account.
* **Calling iFrame:**  The user interface displayed within HubSpot, configured using the settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](link-to-knowledge-base-article).  Once integrated, your app will appear in HubSpot's call switcher.

**Note:** Currently, only outgoing calls are supported.

## Getting Started

### 1. Create a HubSpot App (If Necessary)

If you don't have an existing HubSpot app, you can [create one from your HubSpot developer account](link-to-create-hubspot-app). If you need a developer account, sign up [here](link-to-signup).

### 2. Run the Demo Calling App

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive implementation using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.

### 3. Install the Demo App (Optional)

To install the demo locally:

1. Install Node.js.
2. Clone, fork, or [download the ZIP](link-to-zip) of the repository.
3. Navigate to the project's root directory.
4. Run the appropriate command:

   * **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### 4. Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console.
3. Run the appropriate `localStorage` command:

   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".

### 5. Install the Calling Extensions SDK

Add the SDK as a dependency to your calling app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses events for communication between your app and HubSpot.

### Events

**Send Messages to HubSpot:**

* `initialized`: Softphone ready.
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started.
* `callAnswered`: Outgoing call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`: Error encountered.
* `resizeWidget`: Resize request.

**Receive Messages from HubSpot:**

* `onReady`: HubSpot ready.
* `onDialNumber`: Outbound call triggered.
* `onEngagementCreated` (Deprecated, use `onCreateEngagementSucceeded` instead): Engagement created.
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


Each event has associated data;  see the detailed descriptions in the original text for specifics.  Example code snippets demonstrating the use of these events are also included in the original text.

### SDK Instantiation

Create a `CallingExtensions` instance with options defining `eventHandlers`:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, //Optional
  eventHandlers: {
    onReady: () => { /*...*/ },
    onDialNumber: (event) => { /*...*/ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Testing Your App

HubSpot requires these iFrame parameters for launching the calling extension:

```json
{
  "name": "Your App Name",
  "url": "Your App URL",
  "width": 600,
  "height": 400,
  "isReady": false, // Set to true for production
  "supportsCustomObjects": true
}
```

### Using the Calling Settings Endpoint

Use the HubSpot API to manage your app settings.  The provided `curl` examples demonstrate how to use POST and PATCH requests to add and update settings respectively. Remember to replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values.

### Overriding Settings with localStorage

For testing, override settings using `localStorage`:

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

### Publishing to the Marketplace

[Follow these instructions](link-to-marketplace-instructions) to publish your app to the HubSpot marketplace.


## Frequently Asked Questions (FAQ)

The original text includes a comprehensive FAQ section addressing common questions about authentication, CDN hosting, engagement creation/updates, required scopes, integration with existing apps, multiple integrations, free user access, automatic updates, user permissions, custom properties, and calling from custom objects.  Refer to the original text for these answers.


This Markdown documentation summarizes the provided text, making it easier to navigate and understand.  Remember to replace the placeholder links (`link-to...`) with the actual URLs from the original text.
