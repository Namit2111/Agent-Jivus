# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK enables apps to offer a custom calling experience directly from CRM records.  It consists of three core components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:**  Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iFrame:** The interface displayed to HubSpot users, customized via the calling settings endpoints.

For a detailed understanding of the in-app calling experience, refer to [this knowledge base article](LINK_TO_KNOWLEDGE_BASE_ARTICLE).  Once integrated, your app will appear in HubSpot's call switcher.  Only outgoing calls are currently supported.

If you lack an existing app, you can [create one via your HubSpot developer account](LINK_TO_HUBSPOT_DEVELOPER_ACCOUNT).  If you need a developer account, sign up [here](LINK_TO_SIGN_UP).


## Getting Started

### Demo Apps

Two demo apps are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  SDK instantiation is shown in `index.js`.
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components. SDK instantiation is in `useCti.ts`.

**Note:** These demos utilize mock data and aren't fully functional calling applications.


### Installing the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP) of the repository.
3. Navigate to the project's root directory in your terminal.
4. Run the appropriate command:

   * **`demo-minimal-js`:**  `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### Launching the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console.
3. Run one of the following commands, depending on your installation method:

   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.  Select the demo app from the "Call from" dropdown in the call switcher.


### Installing the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses message passing via methods and event handlers.  See the [Events section](#events) for a complete list.

### Key Events

* **Dial Number:** HubSpot sends the dial number.
* **Outbound Call Started:** App notifies HubSpot of call initiation.
* **Create Engagement:**  HubSpot creates a call engagement (if requested by the app).
* **Engagement Created:** HubSpot confirms engagement creation.
* **EngagementId Sent to App:** HubSpot provides the `engagementId`.
* **Call Ended:** App notifies HubSpot of call termination.
* **Call Completed:** App signals the end of the user experience.
* **Update Engagement:** App updates the engagement with call details.  Learn more about updating engagements via the [API](API_LINK) or [SDK](SDK_LINK).


### Creating an Instance

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: event => { /* Dial number received */ },
    onCreateEngagementSucceeded: event => { /* Engagement created successfully */ },
    onEngagementCreatedFailed: event => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: event => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: event => { /* Engagement update failed */ },
    onVisibilityChanged: event => { /* Widget visibility changed */ }
  }
};

const extensions = new CallingExtensions(options);
```

### Testing Your App

HubSpot requires these iFrame parameters:

```json
{
  "name": "string", // App name
  "url": "string", // App URL
  "width": number, // iFrame width
  "height": number, // iFrame height
  "isReady": boolean, // Ready for production (false during testing)
  "supportsCustomObjects": true //Support for custom objects
}
```


### Using the Calling Settings Endpoint

Use your API tool (e.g., Postman) to send a payload to HubSpot's settings API. Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values.  `isReady` should be `false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.


### Overriding Extension Settings (localStorage)

For testing, override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Preparing for Production

Set `isReady` to `true` using the `PATCH` endpoint:

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"isReady":true}'
```

### Publishing to the Marketplace

List your app in the HubSpot marketplace [here](MARKETPLACE_LINK).


## Events

### Sending Messages to HubSpot

* `initialized`: Softphone readiness.
* `userLoggedIn`: User login.
* `userLoggedOut`: User logout.
* `outgoingCall`: Outgoing call started.
* `callAnswered`: Outgoing call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`: App error.
* `resizeWidget`: Widget resize request.

(Detailed descriptions and parameters for each event are provided in the original text and should be included here.)

### Receiving Messages from HubSpot

* `onReady`: HubSpot readiness.
* `onDialNumber`: Outbound call triggered in HubSpot.
* `onEngagementCreated` (Deprecated): Use `onCreateEngagementSucceeded`.
* `onNavigateToRecordFailed`: Record navigation failure.
* `onPublishToChannelSucceeded`: Successful channel publishing.
* `onPublishToChannelFailed`: Failed channel publishing.
* `onCallerIdMatchSucceeded`: Successful caller ID match.
* `onCallerIdMatchFailed`: Failed caller ID match.
* `onCreateEngagementSucceeded`: Successful engagement creation.
* `onCreateEngagementFailed`: Failed engagement creation.
* `onUpdateEngagementSucceeded`: Successful engagement update.
* `onUpdateEngagementFailed`: Failed engagement update.
* `onVisibilityChanged`: Widget visibility change.
* `defaultEventHandler`: Default event handler.

(Detailed descriptions and parameters for each event are provided in the original text and should be included here.)



## Frequently Asked Questions (FAQ)

(The FAQ section from the original text should be included here.)


Remember to replace placeholder links (e.g., `LINK_TO_KNOWLEDGE_BASE_ARTICLE`, `API_LINK`, `SDK_LINK`, `MARKETPLACE_LINK`) with the actual URLs.  Also, add detailed parameter descriptions for each event from the original document.
