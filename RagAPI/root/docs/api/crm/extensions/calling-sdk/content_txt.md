# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling functionality directly into the HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between a calling application and HubSpot.  It consists of three core components:

1. **The Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication.
2. **Calling Settings Endpoints (API):** Used to configure calling settings for each connected HubSpot account.
3. **Calling iFrame:**  The iframe where the calling app is displayed to HubSpot users; configured via the settings endpoints.

**Note:** Currently, only outgoing calls are supported.


## Getting Started

### 1. Demo Applications

Two demo applications are available for testing:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:** A more complete example using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:**  These demos use mock data and are not fully functional calling apps.

### 2. Installing the Demo App

1. Install Node.js.
2. Clone or download the demo repository.
3. Navigate to the demo directory (either `demos/demo-minimal-js` or `demos/demo-react-ts`).
4. Run:
   * `npm i && npm start` (for both demos)

This will install dependencies and start the app, opening a browser tab at `https://localhost:9025/`. You might need to bypass a security warning.

### 3. Launching the Demo from HubSpot

1. Navigate to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Run one of the following commands in the console, based on your chosen demo:

   * **`demo-minimal-js` (installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-react-ts` (installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
   * **`demo-minimal-js` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (not installed):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".

### 4. Installing the SDK

Add the SDK as a dependency to your calling app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses events for communication.

### Events

**HubSpot sends these events to your app:**

* `onReady`: HubSpot is ready.
* `onDialNumber`:  User initiates an outbound call (details in the section below).
* `onEngagementCreated`: (Deprecated; use `onCreateEngagementSucceeded`) HubSpot created a call engagement.
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publishing to a channel succeeded/failed.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match succeeded/failed.
* `onUpdateEngagementSucceeded`/`onUpdateEngagementFailed`: Engagement update succeeded/failed.
* `onVisibilityChanged`: Widget visibility changed.

**Your app sends these events to HubSpot:**

* `initialized`: Softphone is ready.
* `userLoggedIn`/`userLoggedOut`: User login/logout status.
* `outgoingCall`: Outgoing call started.
* `callAnswered`: Outgoing call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`: An error occurred.
* `resizeWidget`: Request to resize the widget.

### API Reference

#### `CallingExtensions` Object

The main SDK object.  Instantiation:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: { // Event handlers for inbound messages from HubSpot
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
    defaultEventHandler: (event) => { /* Handle unknown events */ }
  }
};

const extensions = new CallingExtensions(options);
```

#### Sending Events to HubSpot

Examples for some key methods:

**`extensions.initialized(payload)`:**

```javascript
const payload = {
  isLoggedIn: true,
  engagementId: 123 // Optional
};
extensions.initialized(payload);
```

**`extensions.outgoingCall(callInfo)`:**

```javascript
const callInfo = {
  toNumber: "+15551234567",
  fromNumber: "+15559876543",
  callStartTime: Date.now(),
  createEngagement: true // Tells HubSpot to create an engagement
};
extensions.outgoingCall(callInfo);
```

See the complete list of event methods and their parameters in the original text.


### `onDialNumber` Event Details

This event provides crucial call information:

| Property          | Type      | Description                                                                     |
|-------------------|-----------|---------------------------------------------------------------------------------|
| `phoneNumber`     | String    | Phone number to be dialed.                                                    |
| `ownerId`         | Number    | ID of the logged-in HubSpot user.                                             |
| `subjectId`       | Number    | ID of the subject (contact or company).                                        |
| `objectId`        | Number    | ID of the object (contact or company).                                         |
| `objectType`      | String    | `"CONTACT"` or `"COMPANY"`.                                                    |
| `portalId`        | Number    | ID of the HubSpot portal.                                                     |
| `countryCode`     | String    | Country code of the phone number.                                              |
| `calleeInfo`      | Object    | Contains `calleeId` and `calleeObjectTypeId`.                                  |
| `startTimestamp`  | Number    | Timestamp of the call start.                                                   |
| `toPhoneNumberSrc` | String    | Name of the HubSpot property containing the phone number (e.g., "Mobile"). |


### Calling Settings Endpoint (API)

Use this API endpoint to manage your app's settings:

`POST/PATCH/GET/DELETE https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Example Payload (POST/PATCH):**

```json
{
  "name": "My Calling App",
  "url": "https://my-calling-app.com",
  "height": 600,
  "width": 400,
  "isReady": true, // Set to false during development
  "supportsCustomObjects": true
}
```

### Local Storage Override

For testing, you can override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'http://localhost:3000'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production Deployment

1. Set `isReady` to `true` in your API settings.
2. Publish your app to the HubSpot marketplace (optional).


## Frequently Asked Questions

The original text contains a FAQ section.  Refer to that section for answers to common questions.


This markdown documentation provides a structured overview of the HubSpot Calling Extensions SDK.  Remember to consult the original text for more detailed information and specific code examples.
