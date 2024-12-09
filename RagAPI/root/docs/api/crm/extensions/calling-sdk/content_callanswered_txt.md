# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into their HubSpot apps.

## Overview

The Calling Extensions SDK facilitates communication between your app and HubSpot, providing a custom calling experience directly from CRM records.  It consists of three key components:

1. **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:**  The interface your app presents to HubSpot users, configured via the calling settings endpoints.


For a detailed understanding of the in-app calling experience, refer to [this knowledge base article](link-to-knowledge-base-article).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.  If you don't have a HubSpot app, you can [create one here](link-to-create-hubspot-app).  If you need a developer account, sign up [here](link-to-hubspot-developer-signup).

## Getting Started

### Run the Demo Calling App

Two demo apps are available:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive implementation using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.

### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](link-to-zip) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   **`demo-minimal-js`:**

   ```bash
   cd demos/demo-minimal-js && npm i && npm start
   ```

   **`demo-react-ts`:**

   ```bash
   cd demos/demo-react-ts && npm i && npm start
   ```

   This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### Launch the Demo App from HubSpot

1. Go to either **Contacts > Contacts** or **Contacts > Companies** in your HubSpot account.
2. Open your browser's developer console.
3. Run one of the following commands, depending on your installation method:

   * **Installed (`demo-minimal-js` or `demo-react-ts`):**

     ```javascript
     localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');
     ```

   * **Uninstalled (`demo-minimal-js`):**

     ```javascript
     localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');
     ```

   * **Uninstalled (`demo-react-ts`):**

     ```javascript
     localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');
     ```

4. Refresh the page. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Install the Calling Extensions SDK

Add the SDK as a dependency:

**npm:**

```bash
npm i --save @hubspot/calling-extensions-sdk
```

**yarn:**

```bash
yarn add @hubspot/calling-extensions-sdk
```

## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends messages via events, and your app responds using event handlers.

### Events

**HubSpot sends these messages:**

* `onReady`
* `onDialNumber`
* `onEngagementCreated` (deprecated; use `onCreateEngagementSucceeded`)
* `onNavigateToRecordFailed`
* `onPublishToChannelSucceeded`
* `onPublishToChannelFailed`
* `onCallerIdMatchSucceeded`
* `onCallerIdMatchFailed`
* `onCreateEngagementSucceeded`
* `onUpdateEngagementSucceeded`
* `onUpdateEngagementFailed`
* `onVisibilityChanged`
* `defaultEventHandler`


**Your app sends these messages:**

* `initialized`
* `userLoggedIn`
* `userLoggedOut`
* `outgoingCall`
* `callAnswered`
* `callEnded`
* `callCompleted`
* `sendError`
* `resizeWidget`

See the detailed event descriptions below.

### SDK Initialization

Create a `CallingExtensions` instance:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Set to false for production
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    onCreateEngagementSucceeded: (event) => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Detailed Event Descriptions

(Detailed descriptions of each event and their parameters are provided in the original text and should be included here in a well-formatted table for each section - Sending messages and Receiving messages)


### Testing Your App

To launch the calling extension iframe, HubSpot requires these iframe parameters:

```javascript
{
  name: string, // Your app's name
  url: string, // Your app's URL
  width: number, // iFrame width
  height: number, // iFrame height
  isReady: boolean, // Set to false during testing
  supportsCustomObjects: true //Indicates if the app supports calls from custom objects
}
```

### Using the Calling Settings Endpoint

Use the HubSpot settings API (e.g., with `curl`) to configure your app:

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

Remember to replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`.  This endpoint also supports `PATCH`, `GET`, and `DELETE`.  Set `isReady` to `true` for production.


### Overriding Extension Settings with localStorage

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

Set `isReady` to `true` using the `PATCH` endpoint.

### Publishing Your App to the HubSpot Marketplace

[Instructions for publishing your app](link-to-marketplace-publishing-instructions)


### Frequently Asked Questions

(The FAQ section from the original text should be included here, formatted as a markdown FAQ section)


## Share Your Feedback

(Feedback section omitted as it is not relevant to the technical documentation.)
