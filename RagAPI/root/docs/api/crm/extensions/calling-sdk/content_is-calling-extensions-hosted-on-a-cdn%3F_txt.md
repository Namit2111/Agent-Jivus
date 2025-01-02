# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling custom calling options within the HubSpot CRM.

## Overview

The Calling Extensions SDK facilitates communication between your calling application and HubSpot, offering a customized calling experience directly from CRM records.  It consists of three core components:

1. **Calling Extensions SDK (JavaScript):** Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure settings for your app on a per-HubSpot account basis.
3. **Calling iFrame:** The interface displayed to HubSpot users, configured via the settings endpoints.

**Note:** Currently, only outgoing calls are supported.

## Getting Started

### 1. Run the Demo Apps

Two demo apps are available to test the SDK:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:** A more realistic implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** These demos use mock data and are not fully functional calling apps.

**Installation (optional):**

1. Install Node.js.
2. Clone or download the repository.
3. Navigate to the demo directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   * `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
   This will install dependencies and start the app at `https://localhost:9025/`.  You might need to bypass a security warning.

### 2. Launch the Demo from HubSpot

1. Go to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Run one of the following commands in the console, depending on the demo app and whether you installed it:
   * **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page. Click the "Call" icon, select the demo app from the dropdown, and click "Call".

### 3. Install the SDK

Add the SDK to your app:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends messages via events, and your app responds using event handlers.

### API

The `CallingExtensions` object is the core of the SDK.  It's instantiated with an options object, including `eventHandlers`:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Dial number event received */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    // ... other event handlers (see Events section)
  },
};

const extensions = new CallingExtensions(options);
```

### Events

**Outbound Messages (from your app to HubSpot):**

| Event Name       | Description                                                                  | Payload                                                              |
|-------------------|------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| `initialized`     | Signals app readiness.                                                        | `{ isLoggedIn: boolean, engagementId: number }`                     |
| `userLoggedIn`    | User logged in.                                                              | None                                                                 |
| `userLoggedOut`   | User logged out.                                                             | None                                                                 |
| `outgoingCall`    | Outgoing call started.                                                        | `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }` |
| `callAnswered`    | Outgoing call answered.                                                       | `{ externalCallId: string }`                                         |
| `callEnded`       | Outgoing call ended.                                                          | `{ externalCallId: string, engagementId: number, callEndStatus: EndStatus }` |
| `callCompleted`   | Outgoing call completed.                                                      | `{ engagementId: number, hideWidget: boolean, engagementProperties: object, externalCallId: number }` |
| `sendError`       | Error occurred.                                                              | `{ message: string }`                                               |
| `resizeWidget`    | Resize the widget.                                                            | `{ height: number, width: number }`                                   |


**Inbound Messages (from HubSpot to your app):**

| Event Name                      | Description                                                              | Payload                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| `onReady`                        | HubSpot is ready.                                                        | `{ engagementId: number, iframeLocation: Enum, ownerId: string\|number, portalId: number, userId: number }` |
| `onDialNumber`                   | Outbound call initiated.                                                 |  See detailed payload description in the document.                                                            |
| `onCreateEngagementSucceeded`   | Engagement created successfully.                                         | `{ engagementId: number }`                                                                                 |
| `onCreateEngagementFailed`      | Engagement creation failed.                                              | `{ error: string }`                                                                                         |
| `onUpdateEngagementSucceeded`   | Engagement updated successfully.                                          | `{ engagementId: number }`                                                                                 |
| `onUpdateEngagementFailed`      | Engagement update failed.                                               | `{ error: string }`                                                                                         |
| `onNavigateToRecordFailed`     | Navigation to record failed.                                             | `{ engagementId: number, objectCoordinates: object }`                                                       |
| `onPublishToChannelSucceeded`   | Publishing to channel succeeded.                                           | `{ engagementId: number, externalCallId: string }`                                                        |
| `onPublishToChannelFailed`      | Publishing to channel failed.                                            | `{ engagementId: number, externalCallId: string }`                                                        |
| `onCallerIdMatchSucceeded`     | Caller ID match succeeded.                                               |  `{}`                                                                                                       |
| `onCallerIdMatchFailed`        | Caller ID match failed.                                                | `{}`                                                                                                        |
| `onVisibilityChanged`           | Widget visibility changed (minimized/hidden).                             | `{ isMinimized: boolean, isHidden: boolean }`                                                              |
| `defaultEventHandler`           | Default handler for unhandled events.                                    | `{ event: object }`                                                                                       |


**Enum:** `iframeLocation` can be `widget`, `remote`, or `window`.  `callEndStatus` can be `INTERNAL_COMPLETED`, `INTERNAL_FAILED`, `INTERNAL_CANCELED`, `INTERNAL_BUSY`, `INTERNAL_NO_ANSWER`, `INTERNAL_REJECTED`, or `INTERNAL_MISSED`.


### Calling Settings Endpoint (API)

Use this API endpoint to configure your app's settings:

* **Endpoint:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`
* **Methods:** `POST`, `PATCH`, `GET`, `DELETE`
* **Payload (example):**

```json
{
  "name": "My Calling App",
  "url": "https://my-app.com/widget",
  "height": 600,
  "width": 400,
  "isReady": false, // Set to true for production
  "supportsCustomObjects": true
}
```

Replace `{APP_ID}` with your app's ID and `{DEVELOPER_ACCOUNT_API_KEY}` with your API key.  The `isReady` flag indicates production readiness.


### Local Storage Override (for testing)

You can override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'My URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

## Production & Publishing

1. Set `isReady` to `true` in the API settings using `PATCH`.
2. Publish your app to the HubSpot Marketplace (optional).


## Frequently Asked Questions (FAQ)

Refer to the original document for the FAQ section.


This markdown documentation provides a structured and concise overview of the HubSpot Calling Extensions SDK.  Remember to refer to the original text for complete details and nuanced information.
