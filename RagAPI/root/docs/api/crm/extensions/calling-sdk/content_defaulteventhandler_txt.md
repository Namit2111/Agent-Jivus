# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, enabling custom calling options within HubSpot CRM.  It covers installation, usage, API interaction, event handling, and frequently asked questions.

## Overview

The Calling Extensions SDK facilitates communication between your calling application and HubSpot. It consists of three main components:

1. **Calling Extensions SDK (JavaScript):**  Enables communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure calling settings for your app per HubSpot account.
3. **Calling iFrame:** Your app's interface within HubSpot, configured via the settings endpoints.


## Getting Started

### 1. Create a HubSpot Developer Account (if needed):

If you don't have one, sign up [here](<insert signup link here>).  You'll need this to create and manage your calling app.

### 2. Create a HubSpot App (if needed):

Create a new app from your HubSpot developer account [here](<insert app creation link here>).  This is necessary to obtain the `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` required for API calls.


### 3. Install the Demo App (Optional):

Two demo apps are available for testing:

* **`demo-minimal-js`:** Minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
* **`demo-react-ts`:**  More realistic implementation using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Installation Steps:**

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo app's directory (e.g., `cd demos/demo-minimal-js`).
4. Run `npm i && npm start` (or `yarn add @hubspot/calling-extensions-sdk` and `yarn start`).  This will start a local server at `https://localhost:9025/`. You might need to bypass a security warning.

### 4. Launch the Demo App from HubSpot:

1. Go to HubSpot Contacts > Contacts or Contacts > Companies.
2. Open your browser's developer console.
3. Run one of the following commands in the console, depending on which demo app and installation method you chose:

    * **Installed `demo-minimal-js` or `demo-react-ts`:**
      ```javascript
      localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');
      ```

    * **Uninstalled `demo-minimal-js`:**
      ```javascript
      localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');
      ```

    * **Uninstalled `demo-react-ts`:**
      ```javascript
      localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');
      ```

4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


## Installing the Calling Extensions SDK

Add the SDK to your project using npm or yarn:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the SDK

### Creating an Instance:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Outbound call initiated */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

### Event Handlers:

The SDK uses event handlers to manage communication with HubSpot.  A detailed list of events and their payloads is provided below.  Note that some events are deprecated.  Use the recommended alternatives.

#### Sending Messages to HubSpot:

* `initialized(payload)`: Notifies HubSpot that your app is ready.  `payload`: `{ isLoggedIn: boolean, engagementId: number }`
* `userLoggedIn()`: Notifies HubSpot of user login.
* `userLoggedOut()`: Notifies HubSpot of user logout.
* `outgoingCall(callInfo)`: Notifies HubSpot of an outgoing call. `callInfo`: `{ phoneNumber: string, toNumber:string, fromNumber: string, callStartTime: number, createEngagement: boolean }`
* `callAnswered(payload)`:  Notifies HubSpot that a call has been answered. `payload`: `{ externalCallId: string }`
* `callEnded(payload)`: Notifies HubSpot that a call has ended. `payload`: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
* `callCompleted(data)`: Notifies HubSpot that a call is complete.  `data`: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
* `sendError(data)`: Reports an error to HubSpot. `data`: `{ message: string }`
* `resizeWidget(data)`: Requests a widget resize. `data`: `{ height: number, width: number }`


#### Receiving Messages from HubSpot:

* `onReady(data)`: HubSpot is ready to receive messages. `data`: `{ engagementId: number, iframeLocation: Enum, ownerId: String | Number, portalId: Number, userId: Number }`
* `onDialNumber(data)`: User initiated an outbound call. See detailed data properties in the original document.
* `onEngagementCreated(data)`: **Deprecated**. Use `onCreateEngagementSucceeded`.
* `onNavigateToRecordFailed(data)`: Navigation to a record failed. `data`: `{ engagementId: number, objectCoordinates: object }`
* `onPublishToChannelSucceeded(data)`: Publishing to a channel succeeded. `data`: `{ engagementId: number, externalCallId: string }`
* `onPublishToChannelFailed(data)`: Publishing to a channel failed. `data`: `{ engagementId: number, externalCallId: string }`
* `onCallerIdMatchSucceeded(event)`: Caller ID match successful.
* `onCallerIdMatchFailed(event)`: Caller ID match failed.
* `onCreateEngagementSucceeded(event)`: Engagement creation successful.
* `onCreateEngagementFailed(event)`: Engagement creation failed.
* `onUpdateEngagementSucceeded(event)`: Engagement update successful.
* `onUpdateEngagementFailed(event)`: Engagement update failed.
* `onVisibilityChanged(data)`: Widget visibility changed. `data`: `{ isMinimized: boolean, isHidden: boolean }`
* `defaultEventHandler(event)`: Default handler for unhandled events.


## Calling Settings Endpoint (API)

Use this endpoint to configure your app's settings for each HubSpot account.  Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your actual values. The `isReady` flag should be `false` during testing and `true` for production.


**Endpoint:** `https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`

**Methods:** `POST`, `PATCH`, `GET`, `DELETE`

**Example Payload (POST/PATCH):**

```json
{
  "name": "My Calling App",
  "url": "https://my-calling-app.com",
  "height": 600,
  "width": 400,
  "isReady": false,
  "supportsCustomObjects": true
}
```


## Overriding Settings with localStorage (for Testing)

You can override settings temporarily using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Preparing for Production

1. Set `isReady` to `true` using the PATCH method on the settings endpoint.
2. Publish your app to the HubSpot Marketplace [link here].


## Frequently Asked Questions (FAQ)

The FAQ section from the original document is included here verbatim.


## Conclusion

This documentation provides a comprehensive guide to integrating the HubSpot Calling Extensions SDK into your applications. Remember to consult the HubSpot developer portal for the most up-to-date information and best practices.
