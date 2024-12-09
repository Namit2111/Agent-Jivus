# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK allows apps to offer custom calling options directly from CRM records.  It consists of three key components:

* **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
* **Calling Settings Endpoints:** Configure calling settings for each connected HubSpot account.
* **Calling iFrame:** Your app's user interface, configured via the settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](link-to-knowledge-base-article).  After connecting your app, it will appear in HubSpot's call switcher.

**Note:** Only outgoing calls are currently supported.  If you don't have an app, you can [create one from your HubSpot developer account](link-to-developer-account-creation).

## Getting Started

### Run the Demo Calling App

Two demo apps are available:

* **`demo-minimal-js`:** A minimal JavaScript, HTML, and CSS implementation.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more complete React, TypeScript, and Styled Components implementation. See `useCti.ts` for SDK instantiation.

**Note:** These demos use mock data.

### Install the Demo App

1. Install Node.js.
2. Clone, fork, or [download the ZIP](link-to-zip-download) of the repository.
3. Navigate to the project's root directory.
4. Run one of the following commands:

   * For `demo-minimal-js`:  `cd demos/demo-minimal-js && npm i && npm start`
   * For `demo-react-ts`:  `cd demos/demo-react-ts && npm i && npm start`

   This installs dependencies and starts the app at `https://localhost:9025/`. You might need to bypass a security warning.

### Launch the Demo App from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console and run one of the following commands:

   * **After Installation:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Without Installation:**
     * `demo-minimal-js`: `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
     * `demo-react-ts`: `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
3. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".


### Install the Calling Extensions SDK

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the Calling Extensions SDK

The SDK uses messages exchanged via methods and event handlers.  See the [Events section](#events) for a complete list.

### SDK Initialization

Create a `CallingExtensions` object, defining behavior using an options object with `eventHandlers`:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: boolean, // Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: event => { /* Dial number received */ },
    onCreateEngagementSucceeded: event => { /* Engagement created */ },
    onEngagementCreatedFailed: event => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: event => { /* Engagement updated */ },
    onUpdateEngagementFailed: event => { /* Engagement update failed */ },
    onVisibilityChanged: event => { /* Widget visibility changed */ }
  }
};

const extensions = new CallingExtensions(options);
```

###  Testing Your App

To launch the calling extensions iFrame, HubSpot requires these iFrame parameters:

```json
{
  "name": "string", // App name
  "url": "string",  // App URL
  "width": number, // iFrame width
  "height": number, // iFrame height
  "isReady": boolean, // Ready for production (defaults to true)
  "supportsCustomObjects": true // Supports calls from custom objects
}
```

### Using the Calling Settings Endpoint

Use your API tool (e.g., Postman) to send a payload to HubSpot's settings API. Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY`.  Set `isReady` to `false` during testing.

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"demo widget","url":"https://mywidget.com/widget","height":600,"width":400,"isReady":false}'
```

This endpoint also supports `PATCH`, `GET`, and `DELETE`.

### Override Extension Settings Using localStorage

For testing, override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Get Your App Ready for Production

Set `isReady` to `true` using the `PATCH` endpoint.

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"isReady":true}'
```

### Publish Your Calling App

[Publish your app to the HubSpot marketplace](link-to-marketplace-publishing).

## Events

### Sending Messages to HubSpot

The `extensions` object provides methods to send messages:

* **`initialized(payload)`:**  Indicates softphone readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
* **`userLoggedIn()`:** User login notification.
* **`userLoggedOut()`:** User logout notification.
* **`outgoingCall(callInfo)`:** Outgoing call started.  `callInfo`: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
* **`callAnswered(payload)`:** Call answered.  `payload`: `{ externalCallId: string }`
* **`callEnded(payload)`:** Call ended.  `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* **`callCompleted(data)`:** Call completed. `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* **`sendError(data)`:** Error notification. `data`: `{ message: string }`
* **`resizeWidget(data)`:** Resize request. `data`: `{ height: number, width: number }`


### Receiving Messages from HubSpot

The SDK provides event handlers for inbound messages:

* **`onReady(data)`:**  HubSpot is ready. `data`: `{ engagementId: number, iframeLocation: Enum, ownerId: String or Number, portalId: Number, userId: Number }`
* **`onDialNumber(data)`:** Outbound call initiated.  `data`: `{ phoneNumber: string, ownerId: number, subjectId: number, objectId: number, objectType: CONTACT | COMPANY, portalId: number, countryCode: string, calleeInfo: { calleeId: number, calleeObjectTypeId: string }, startTimestamp: number, toPhoneNumberSrc: string }`
* **`onEngagementCreated(data)`:** (Deprecated) Engagement created. `data`: `{ engagementId: number }`
* **`onNavigateToRecordFailed(data)`:** Navigation to a record failed. `data`: `{ engagementId: number, objectCoordinates: object coordinates }`
* **`onPublishToChannelSucceeded(data)`:** Publishing to a channel succeeded. `data`: `{ engagementId: number, externalCallId: string }`
* **`onPublishToChannelFailed(data)`:** Publishing to a channel failed. `data`: `{ engagementId: number, externalCallId: string }`
* **`onCallerIdMatchSucceeded(event)`:** Caller ID match succeeded.
* **`onCallerIdMatchFailed(event)`:** Caller ID match failed.
* **`onCreateEngagementSucceeded(event)`:** Engagement creation succeeded.
* **`onCreateEngagementFailed(event)`:** Engagement creation failed.
* **`onUpdateEngagementSucceeded(event)`:** Engagement update succeeded.
* **`onUpdateEngagementFailed(event)`:** Engagement update failed.
* **`onVisibilityChanged(data)`:** Widget visibility changed. `data`: `{ isMinimized: boolean, isHidden: boolean }`
* **`defaultEventHandler(event)`:** Default event handler.


## Frequently Asked Questions

* **Authentication:** Handled by the calling app.
* **CDN Hosting:** Yes, via jsDeliver.  Example: `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`
* **Engagement Creation vs. Update:** HubSpot creates engagements for calls from the HubSpot UI; the app updates them afterward.  For calls outside the HubSpot UI, the app creates the engagement.
* **Required Scopes:** `contacts` and `timeline`.
* **Existing Apps:** Functionality can be added to existing marketplace apps.
* **Softphone Integration:** Easily integrate existing softphones.
* **Multiple Integrations:** Users can use multiple integrations simultaneously.
* **Free Users:** All users can install the app.
* **Automatic Appearance:** Yes, for updated apps.
* **App Installation/Uninstallation:** Controlled by user permissions.
* **Custom Calling Properties:** Yes, using the properties API.
* **Calls from Custom Objects:** Yes, using the SDK.  Ensure `outgoingCall({ createEngagement: true })`.


## Feedback

[Share your feedback](link-to-feedback-form)


**(Remember to replace placeholder links with actual links.)**
