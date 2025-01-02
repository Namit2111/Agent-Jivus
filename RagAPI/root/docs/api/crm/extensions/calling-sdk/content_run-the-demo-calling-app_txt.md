# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, enabling custom calling options within the HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between your calling application and HubSpot.  It consists of three core components:

1. **Calling Extensions SDK (JavaScript):** Enables message exchange between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure settings for your app on a per-HubSpot account basis.
3. **Calling iFrame:** Your app's user interface, displayed within HubSpot.


**Note:** Currently, only outgoing calls are supported.

## Getting Started

### 1. Run the Demo App

Two demo apps are available for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:** More comprehensive example using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:**  Demo apps use mock data and aren't fully functional calling applications.


### 2. Install the Demo App (Optional)

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo app directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
4. Access the app at `https://localhost:9025/` (may require bypassing a security warning).


### 3. Launch the Demo App from HubSpot

1. Go to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Set `localStorage` based on your installation method:
   * **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page, click the "Call" icon, select the demo app from the dropdown, and click "Call".


### 4. Install the SDK

Add the SDK as a dependency:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

The SDK uses an event-driven architecture.  Your app sends messages to HubSpot via methods, and receives messages via event handlers.


### API

The `CallingExtensions` object provides methods for communication:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Dial number received */ },
    // ... other event handlers (see Events section)
  },
};

const extensions = new CallingExtensions(options);
```

### Events

**Messages Sent to HubSpot:**

| Method           | Description                                                              | Payload Example                                      |
|-------------------|--------------------------------------------------------------------------|------------------------------------------------------|
| `initialized`    | Softphone ready.                                                        | `{ isLoggedIn: true, engagementId: 123 }`             |
| `userLoggedIn`   | User logged in.                                                          | `{}`                                                |
| `userLoggedOut`  | User logged out.                                                         | `{}`                                                |
| `outgoingCall`   | Outgoing call started.                                                   | `{ toNumber: "+15551234567", fromNumber: "+15559876543", callStartTime: Date.now(), createEngagement: true }` |
| `callAnswered`   | Outgoing call answered.                                                  | `{ externalCallId: "abc123xyz" }`                   |
| `callEnded`      | Call ended.                                                             | `{ externalCallID: "abc123xyz", engagementId: 123, callEndStatus: "INTERNAL_COMPLETED" }` |
| `callCompleted`  | Call completed.                                                         | `{ engagementId: 123, hideWidget: true, engagementProperties: {property1: 'value1'} }` |
| `sendError`      | Error occurred.                                                          | `{ message: "An error occurred." }`                  |
| `resizeWidget`   | Resize the widget.                                                      | `{ height: 600, width: 400 }`                         |


**Messages Received from HubSpot:**

| Event                 | Description                                                                          | Payload Example (partial)                               |
|-----------------------|--------------------------------------------------------------------------------------|-------------------------------------------------------|
| `onReady`             | HubSpot is ready.                                                                   | `{ engagementId: 123, iframeLocation: "widget" }`       |
| `onDialNumber`        | Outbound call initiated.                                                           | `{ phoneNumber: "+15551234567", objectType: "CONTACT", objectId: 123 }` |
| `onCreateEngagementSucceeded` | Engagement successfully created by HubSpot.                                     | `{ engagementId: 456 }`                              |
| `onCreateEngagementFailed`  | Engagement creation failed.                                                        | `{ error: "Error creating engagement" }`              |
| `onUpdateEngagementSucceeded` | Engagement successfully updated by HubSpot.                                     | `{}`                                                |
| `onUpdateEngagementFailed`  | Engagement update failed.                                                        | `{ error: "Error updating engagement" }`              |
| `onNavigateToRecordFailed` | Navigation to record failed.                                                       | `{ engagementId: 123, objectCoordinates: { ... } }`     |
| `onPublishToChannelSucceeded` | Publishing to channel succeeded.                                                   | `{ engagementId: 123, externalCallId: "abc123xyz" }`   |
| `onPublishToChannelFailed`  | Publishing to channel failed.                                                        | `{ engagementId: 123, externalCallId: "abc123xyz" }`   |
| `onCallerIdMatchSucceeded` | Caller ID match successful.                                                       | `{}`                                                |
| `onCallerIdMatchFailed`  | Caller ID match failed.                                                           | `{}`                                                |
| `onVisibilityChanged` | Widget visibility changed.                                                         | `{ isMinimized: false, isHidden: true }`              |
| `defaultEventHandler` | Default handler for unhandled events.                                                | `{ event: { ... } }`                                 |



### Calling Settings Endpoint (API)

Use the API to configure your app's settings for each HubSpot account.  The endpoint supports `POST`, `PATCH`, `GET`, and `DELETE`.

**Endpoint:** `https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Example Payload (POST/PATCH):**

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

### Overriding Settings with localStorage (for testing)

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Production Deployment

1. Set `isReady` to `true` via the settings API.
2. Publish your app to the HubSpot marketplace (optional).


## Frequently Asked Questions

See the original document for the FAQs.


This markdown provides a structured and more concise version of the provided text.  Remember to replace placeholders like `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values.
