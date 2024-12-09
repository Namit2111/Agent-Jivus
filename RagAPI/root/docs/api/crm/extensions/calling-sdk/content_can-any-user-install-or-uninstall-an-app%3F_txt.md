# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality directly into the HubSpot CRM.

## Overview

The Calling Extensions SDK enables apps to provide a custom calling option to HubSpot users from within CRM records.  This integration consists of three key components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:**  The user interface of your app displayed within HubSpot. Configured via the calling settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE_HERE -  Replace with actual link).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.

## Getting Started

### 1.  Create a HubSpot App (if needed)

If you don't have a HubSpot app, create one from your [HubSpot developer account](LINK_TO_DEVELOPER_ACCOUNT_HERE - Replace with actual link). If you lack a developer account, sign up [here](LINK_TO_SIGNUP_HERE - Replace with actual link).


### 2.  Demo Apps

Test the SDK using two demo apps:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive implementation using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demo apps use mock data and aren't fully functional calling applications.

### 3. Install the Demo App (Optional)

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP_HERE - Replace with actual link) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.

### 4. Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands, depending on whether you installed the demo app:

   * **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.  Select the demo app from the "Call from" dropdown in the call switcher.

### 5. Install the Calling Extensions SDK

Add the SDK as a dependency to your app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  Events are sent and received via methods and event handlers.

### Events

#### Sending Messages to HubSpot

* `initialized`:  Indicates softphone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User login notification.
* `userLoggedOut`: User logout notification.
* `outgoingCall`: Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Outgoing call answered. Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`  `callEndStatus` is an enumeration: `INTERNAL_COMPLETED`, `INTERNAL_FAILED`, `INTERNAL_CANCELED`, `INTERNAL_BUSY`, `INTERNAL_NO_ANSWER`, `INTERNAL_REJECTED`, `INTERNAL_MISSED`
* `callCompleted`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`: Error notification. Payload: `{ message: string }`
* `resizeWidget`: Resize request. Payload: `{ height: number, width: number }`

#### Receiving Messages from HubSpot

* `onReady`: HubSpot is ready.
* `onDialNumber`: Outbound call initiated from HubSpot.
* `onEngagementCreated`: (Deprecated; use `onCreateEngagementSucceeded`) Engagement created.
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`: Publishing to a channel succeeded.
* `onPublishToChannelFailed`: Publishing to a channel failed.
* `onCallerIdMatchSucceeded`: Caller ID match successful.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement creation successful.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Default event handler.

### SDK Instantiation

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

### iFrame Parameters

To launch the calling extensions iframe, HubSpot requires these parameters:

```json
{
  "name": "App Name",
  "url": "App URL",
  "width": 400,
  "height": 600,
  "isReady": true, // Set to false during testing
  "supportsCustomObjects": true // Optional. Set true if calls are made from custom objects
}
```

### Calling Settings Endpoint

Use the API to manage app settings:

```bash
# Example (replace APP_ID and API_KEY)
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"My App","url":"https://myapp.com","height":600,"width":400,"isReady":false}'
```

This endpoint supports `POST`, `PATCH`, `GET`, and `DELETE`.


### Overriding Settings with localStorage

For testing, override settings using the browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'My URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production Readiness

Set `isReady` to `true` via the API's PATCH endpoint once testing is complete.


### Publishing to the Marketplace

Publish your app to the HubSpot marketplace [here](LINK_TO_MARKETPLACE_HERE - Replace with actual link).


## Frequently Asked Questions

* **User Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver (example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; the app updates them afterward.  For calls outside the UI, the app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:**  Functionality can be added to existing marketplace apps.
* **Softphone Integration:** Easily integrate existing softphones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free Users:** All users can install the app.
* **Automatic Appearance:** Yes, for updates to existing installations.
* **Installation/Uninstallation:** Controlled by user permissions.
* **Custom Calling Properties:** Yes, via the properties API.
* **Calls from Custom Objects:** Yes, using the SDK and setting `createEngagement: true` in `outgoingCall`.


## Feedback

[Share your feedback here](LINK_TO_FEEDBACK_HERE - Replace with actual link)

