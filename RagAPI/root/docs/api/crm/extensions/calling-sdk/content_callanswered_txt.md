# HubSpot CRM API: Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, enabling custom calling options within the HubSpot CRM.  It covers installation, usage, event handling, API interactions, and frequently asked questions.

## Overview

The Calling Extensions SDK allows developers to integrate their calling applications directly into the HubSpot CRM interface.  Users can initiate calls from contact or company records, leveraging your app's calling features. The integration comprises three main parts:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:**  The user interface of your app displayed within HubSpot.

**Note:** Only outgoing calls are currently supported.

## Getting Started

### 1. Prerequisites

* Node.js installed on your development environment.
* A HubSpot developer account (sign up [here](link-to-hubspot-signup)).  An app must be created within your developer account.


### 2. Demo Apps

Two demo applications are provided to illustrate SDK usage:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:**  More comprehensive implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** Demo apps use mock data and aren't fully functional calling applications.


### 3. Installing the Demo App

1. Clone or download the demo repository (link to repo).
2. Navigate to the demo app's directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js`
   * `demo-react-ts`: `cd demos/demo-react-ts`
3. Install dependencies: `npm i`
4. Start the app: `npm start` (opens in browser at `https://localhost:9025/`)

### 4. Launching the Demo App from HubSpot

1. Navigate to HubSpot contacts (`Contacts > Contacts`) or companies (`Contacts > Companies`).
2. Open your browser's developer console.
3. Set the `localStorage` variable to install the demo:
   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.  The demo app should appear in the call switcher.

### 5. Installing the Calling Extensions SDK

Add the SDK to your project:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses events for communication between your app and HubSpot.

### Events

**Outbound Events (from your app to HubSpot):**

| Event Name      | Description                                                                   | Payload                                                              |
|-----------------|-------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| `initialized`   | Notifies HubSpot your app is ready.                                          | `{ isLoggedIn: boolean, engagementId: number }`                     |
| `userLoggedIn`  | User logged in.                                                              | None                                                                  |
| `userLoggedOut` | User logged out.                                                              | None                                                                  |
| `outgoingCall`  | Outgoing call started.                                                       | `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }` |
| `callAnswered`  | Outgoing call answered.                                                      | `{ externalCallId: string }`                                        |
| `callEnded`     | Call ended.                                                                  | `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }` |
| `callCompleted` | Call completed.  HubSpot handles engagement updates automatically.           | `{ engagementId: number, hideWidget: boolean, engagementProperties: object, externalCallId: number }` |
| `sendError`     | Error encountered.                                                            | `{ message: string }`                                               |
| `resizeWidget`  | Resize the calling widget.                                                  | `{ height: number, width: number }`                                  |


**Inbound Events (from HubSpot to your app):**

| Event Name                    | Description                                                                                             | Payload                                                                                                                               |
|--------------------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `onReady`                      | HubSpot is ready.                                                                                       | `{ engagementId: number, iframeLocation: Enum, ownerId: string\|number, portalId: number, userId: number }`                              |
| `onDialNumber`                 | Outbound call initiated in HubSpot.                                                                      | `{ phoneNumber: string, ownerId: number, subjectId: number, objectId: number, objectType: CONTACT \| COMPANY, portalId: number, countryCode: string, calleeInfo: { calleeId: number, calleeObjectTypeId: string }, startTimestamp: number, toPhoneNumberSrc: string }` |
| `onEngagementCreated`          | **Deprecated.** Use `onCreateEngagementSucceeded` instead.                                              | `{ engagementId: number }`                                                                                                                |
| `onNavigateToRecordFailed`     | Navigating to a record failed.                                                                         | `{ engagementId: number, objectCoordinates: object }`                                                                                     |
| `onPublishToChannelSucceeded` | Publishing to a channel succeeded.                                                                        | `{ engagementId: number, externalCallId: string }`                                                                                     |
| `onPublishToChannelFailed`    | Publishing to a channel failed.                                                                         | `{ engagementId: number, externalCallId: string }`                                                                                     |
| `onCallerIdMatchSucceeded`    | Caller ID match succeeded.                                                                           | `{}`                                                                                                                                      |
| `onCallerIdMatchFailed`       | Caller ID match failed.                                                                            | `{}`                                                                                                                                      |
| `onCreateEngagementSucceeded`  | HubSpot successfully created an engagement.                                                              | `{}`                                                                                                                                      |
| `onCreateEngagementFailed`     | HubSpot failed to create an engagement.                                                                | `{}`                                                                                                                                      |
| `onUpdateEngagementSucceeded`  | HubSpot successfully updated an engagement.                                                              | `{}`                                                                                                                                      |
| `onUpdateEngagementFailed`    | HubSpot failed to update an engagement.                                                                | `{}`                                                                                                                                      |
| `onVisibilityChanged`         | Call widget visibility changed (minimized/hidden).                                                    | `{ isMinimized: boolean, isHidden: boolean }`                                                                                           |
| `defaultEventHandler`         | Default event handler.                                                                                 | `{ event }`                                                                                                                               |


### SDK Initialization

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: (event) => { /* Handle onReady event */ },
    onDialNumber: (event) => { /* Handle onDialNumber event */ },
    // ... other event handlers
    defaultEventHandler: (event) => { console.log('Unhandled event:', event); } //Handle unknown events
  }
};

const extensions = new CallingExtensions(options);
```

### API Interactions

#### Calling Settings Endpoint

Use this endpoint to configure your app's settings for each HubSpot account.  Replace `APP_ID` with your app's ID and `DEVELOPER_ACCOUNT_API_KEY` with your API key.

**POST/PATCH/GET/DELETE:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Request Body (example):**

```json
{
  "name": "My Calling App",
  "url": "https://my-calling-app.com",
  "height": 600,
  "width": 400,
  "isReady": true, // Set to false during testing
  "supportsCustomObjects": true
}
```

#### Overriding Settings using localStorage (for testing)

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My app name',
  url: 'My local/qa/prod URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

## Production Deployment

1. Set `isReady` to `true` in your app settings using the API.
2. Publish your app to the HubSpot marketplace (link to marketplace instructions).


## Frequently Asked Questions (FAQs)

See the original text for the FAQs section.


This markdown documentation provides a more structured and easily navigable overview of the HubSpot Calling Extensions SDK. Remember to replace placeholder values like `APP_ID` and API keys with your actual values.  The original text contains additional details and examples which should be integrated here for completeness.
