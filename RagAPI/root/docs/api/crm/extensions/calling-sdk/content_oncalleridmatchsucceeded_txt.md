# HubSpot CRM API: Calling Extensions SDK

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK enables apps to offer a custom calling experience directly from CRM records.  It consists of three core components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:**  Used to configure your app's calling settings for each connected HubSpot account.
3. **Calling iframe:**  The visual representation of your app within HubSpot, controlled via the calling settings endpoints.

For a detailed understanding of the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE_NEEDED).  After integration, your app will appear in HubSpot's call switcher.

**Note:** Currently, only outgoing calls are supported.  If you need an app, create one from your [HubSpot developer account](LINK_TO_DEVELOPER_ACCOUNT_NEEDED).  If you don't have an account, sign up [here](LINK_TO_SIGNUP_NEEDED).


## Getting Started

### Run the Demo Calling App

Two demo apps are available:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more realistic implementation using React, TypeScript, and Styled Components. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data and aren't fully functional calling apps.

### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](LINK_TO_ZIP_NEEDED) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * **`demo-minimal-js`:** `cd demos/demo-minimal-js && npm i && npm start`
   * **`demo-react-ts`:** `cd demos/demo-react-ts && npm i && npm start`

This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console and run one of these commands (depending on whether you installed the demo app):
    * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    * **`demo-minimal-js` (Uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    * **`demo-react-ts` (Uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
3. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".

### Install the Calling Extensions SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends messages (events) to your app, and your app responds with appropriate actions.

### Events

#### Sending Messages to HubSpot

* `initialized`:  Signals soft phone readiness (payload: `isLoggedIn`, `engagementId`).
* `userLoggedIn`: Notifies HubSpot of user login.
* `userLoggedOut`: Notifies HubSpot of user logout.
* `outgoingCall`:  Notifies HubSpot of an outgoing call (payload: `phoneNumber` (deprecated, use `toNumber`), `callStartTime`, `createEngagement`, `toNumber`, `fromNumber`).
* `callAnswered`: Notifies HubSpot that a call was answered (payload: `externalCallId`).
* `callEnded`: Notifies HubSpot that a call ended (payload: `externalCallID`, `engagementId`, `callEndStatus`).
* `callCompleted`: Notifies HubSpot that the call is complete (payload: `engagementId`, `hideWidget`, `engagementProperties`, `externalCallId`).
* `sendError`: Sends an error message to HubSpot (payload: `message`).
* `resizeWidget`: Requests a widget resize (payload: `height`, `width`).


#### Receiving Messages from HubSpot

* `onReady`: HubSpot is ready for communication.
* `onDialNumber`:  An outbound call is initiated (payload: `phoneNumber`, `ownerId`, `subjectId`, `objectId`, `objectType`, `portalId`, `countryCode`, `calleeInfo`, `startTimestamp`, `toPhoneNumberSrc`).
* `onEngagementCreated` (deprecated, use `onCreateEngagementSucceeded`): Engagement created.
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`: Publishing to a channel succeeded.
* `onPublishToChannelFailed`: Publishing to a channel failed.
* `onCallerIdMatchSucceeded`: Caller ID match succeeded.
* `onCallerIdMatchFailed`: Caller ID match failed.
* `onCreateEngagementSucceeded`: Engagement creation succeeded.
* `onCreateEngagementFailed`: Engagement creation failed.
* `onVisibilityChanged`: Widget visibility changed.
* `defaultEventHandler`: Default event handler.


### SDK Initialization

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Enable debug logging
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  }
};

const extensions = new CallingExtensions(options);
```

### Testing Your App

To launch the calling extensions iframe, HubSpot requires these iframe parameters:

```javascript
{
  name: string, // App name
  url: string, // App URL
  width: number, // IFrame width
  height: number, // IFrame height
  isReady: boolean, // Is the app ready for production? (Defaults to true)
  supportsCustomObjects: true // Whether calls can be placed from a custom object
}
```

### Using the Calling Settings Endpoint

Use the following API call (replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values) to set app settings:

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint supports `PATCH`, `GET`, and `DELETE` methods as well.  Set `isReady` to `false` during testing.

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

### Preparing for Production

Once testing is complete, use the `PATCH` endpoint to set `isReady` to `true`.

### Publishing to the Marketplace

Publish your app to the HubSpot marketplace [here](LINK_NEEDED).


## Frequently Asked Questions

* **Authentication:** Your app handles authentication.
* **CDN Hosting:** Yes, via jsDeliver (example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; your app updates them.  For calls outside HubSpot, your app creates engagements.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:** You can add this functionality to existing apps.
* **Soft Phone Integration:** Easily integrate existing soft phones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free User Access:** All users can install the app.
* **Automatic Updates:** Yes, for existing app users.
* **Install/Uninstall Permissions:** Restricted by user permissions.
* **Custom Calling Properties:** Yes, via the properties API.
* **Calls from Custom Objects:** Yes, using the SDK.  Ensure `outgoingCall({ createEngagement: true });`


This Markdown documentation provides a comprehensive guide to the HubSpot CRM API Calling Extensions SDK. Remember to replace placeholder links with the actual links.
