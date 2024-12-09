# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling options into their HubSpot apps.

## Overview

The Calling Extensions SDK allows apps to offer a custom calling experience directly from CRM records.  It consists of three key components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:**  The interface displayed to HubSpot users, configured via the calling settings endpoints.

For a detailed understanding of the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE_REPLACE_WITH_ACTUAL_LINK).  After connecting your app, it will appear in HubSpot's call switcher.

**Note:** Only outgoing calls are currently supported.  If you don't have a HubSpot app, you can [create one here](LINK_TO_CREATE_APP_REPLACE_WITH_ACTUAL_LINK).  If you lack a HubSpot developer account, sign up [here](LINK_TO_SIGN_UP_REPLACE_WITH_ACTUAL_LINK).


## Getting Started

### Run the Demo Calling App

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive implementation using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and are not fully functional calling apps.

### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP_REPLACE_WITH_ACTUAL_LINK) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`:**  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:**  `cd demos/demo-react-ts && npm i && npm start`

This will install dependencies and start the app at `https://localhost:9025/`. You might need to bypass a security warning.


### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands, depending on whether you installed the demo app:

   * **Installed (`demo-minimal-js` or `demo-react-ts`):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Not Installed (`demo-minimal-js`):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Not Installed (`demo-react-ts`):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  Events are sent and received via methods and `eventHandlers`.

### Events

**Outbound Events (Sent to HubSpot):**

* `initialized`:  Indicates softphone readiness.
* `userLoggedIn`: User login notification.
* `userLoggedOut`: User logout notification.
* `outgoingCall`: Outgoing call initiation.
* `callAnswered`: Outgoing call answered.
* `callEnded`: Outgoing call ended.
* `callCompleted`: Outgoing call completed.
* `sendError`: Error notification.
* `resizeWidget`: Widget resizing request.

**Inbound Events (Received from HubSpot):**

* `onReady`: HubSpot is ready.
* `onDialNumber`: Dial number received.
* `onEngagementCreated`: Engagement created (deprecated; use `onCreateEngagementSucceeded`).
* `onNavigateToRecordFailed`: Navigation to record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publish to channel success/failure.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match success/failure.
* `onCreateEngagementSucceeded`/`onCreateEngagementFailed`: Engagement creation success/failure.
* `onUpdateEngagementSucceeded`/`onUpdateEngagementFailed`: Engagement update success/failure.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Default event handler.


Each event has specific parameters; see the detailed descriptions below.


### SDK Instantiation and Event Handlers

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```


### Detailed Event Descriptions and Parameters (See original text for complete details)


**(Detailed event descriptions, parameters and data structures are available in the original text.  This markdown omits them for brevity but they should be included in a complete documentation.)**



##  Calling Settings Endpoint

Use the API to configure your app's settings.  The `isReady` flag indicates production readiness (set to `false` during testing).

**Example (using `curl`):**

```bash
curl --request POST \
     --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.


### Overriding Settings using `localStorage`

For testing, override settings in the browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production and Publishing

Set `isReady` to `true` using the `PATCH` endpoint to deploy to production.  Finally, publish your app to the HubSpot marketplace ([details here](LINK_TO_MARKETPLACE_DETAILS_REPLACE_WITH_ACTUAL_LINK)).


## Frequently Asked Questions (FAQs)

**(FAQs are detailed in the original text and should be included here.)**


## Feedback

Please provide feedback on this documentation.


**(Keep the original links and replace the placeholder links above with the actual links from the original text.)**
