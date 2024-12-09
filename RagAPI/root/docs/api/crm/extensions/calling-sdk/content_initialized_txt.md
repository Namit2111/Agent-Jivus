# HubSpot Calling Extensions SDK Documentation

This document provides comprehensive information on the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling options into their HubSpot apps.

## Overview

The Calling Extensions SDK allows apps to offer custom calling functionality directly from CRM records within HubSpot.  It consists of three primary components:

1. **Calling Extensions SDK (JavaScript SDK):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure calling settings for your app on a per-HubSpot account basis.
3. **Calling IFrame:**  Displays your app to HubSpot users; its configuration is managed via the calling settings endpoints.

For a detailed understanding of the in-app calling experience, refer to [this knowledge base article](link-to-knowledge-base-article-here).  Once integrated, your app will appear as a selectable option in HubSpot's call switcher.

**Note:** Currently, only outgoing calls are supported.

## Getting Started

### 1. Create or Use an Existing HubSpot App

If you don't have a HubSpot app, create one through your [HubSpot developer account](link-to-hubspot-developer-account-creation). If you already have an app and wish to add calling functionality, you can integrate the SDK into your existing application.

### 2. Demo Apps

Two demo apps are available for testing the SDK:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive example utilizing React, TypeScript, and Styled Components.  See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.

### 3. Install Demo App (Optional)

1. Install Node.js.
2. Clone, fork, or download the ZIP of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * For `demo-minimal-js`:  `cd demos/demo-minimal-js && npm i && npm start`
   * For `demo-react-ts`:  `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and launch the app at `https://localhost:9025/`. You might need to bypass a security warning.

### 4. Launch Demo App from HubSpot

1. Navigate to HubSpot contacts (`Contacts > Contacts`) or companies (`Contacts > Companies`).
2. Open your browser's developer console.
3. Run the appropriate `localStorage` command (depending on whether you installed the demo or not):

   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".

### 5. Install the Calling Extensions SDK

Add the SDK as a dependency to your app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses events for communication between your app and HubSpot.

### Events

**Outbound Messages (from your app to HubSpot):**

* `initialized`: Softphone ready.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn`: User logged in.
* `userLoggedOut`: User logged out.
* `outgoingCall`: Outgoing call started. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* `callAnswered`: Outgoing call answered. Payload: `{ externalCallId: string }`
* `callEnded`: Call ended. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted`: Call completed. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError`: Error encountered. Payload: `{ message: string }`
* `resizeWidget`: Resize widget. Payload: `{ height: number, width: number }`


**Inbound Messages (from HubSpot to your app):**

* `onReady`: HubSpot ready. Payload includes `engagementId`, `iframeLocation`, `ownerId`, `portalId`, `userId`.
* `onDialNumber`: Outbound call initiated from HubSpot. Payload includes detailed call information (phone number, owner ID, object ID, object type, portal ID, country code, callee info, timestamp, `toPhoneNumberSrc`).
* `onEngagementCreated` (Deprecated): Use `onCreateEngagementSucceeded` instead.
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


### SDK Instantiation

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

## Calling Settings Endpoint

Use this API endpoint to manage your app's settings: `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`  (Supports POST, PATCH, GET, DELETE).  The `isReady` flag indicates production readiness (set to `false` during testing).

## Local Storage Overrides

For testing, override settings using browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

## Production Deployment

Once testing is complete, set `isReady` to `true` using the PATCH endpoint.  Then, publish your app to the HubSpot marketplace [here](link-to-marketplace-publishing).

## Frequently Asked Questions

This section answers common questions about the SDK.  (Content from the original text included here.)


## Feedback

Share your feedback on this documentation.  (Content from the original text included here.)

**(Note:  Replace bracketed placeholders like `link-to-knowledge-base-article-here` with actual links.)**
