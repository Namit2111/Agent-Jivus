# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK facilitates communication between a HubSpot account and a third-party calling application.  It allows users to initiate calls directly from HubSpot CRM records via a custom calling widget.  The SDK handles the exchange of events and data between the app and HubSpot.  HubSpot now handles engagement creation and updates automatically, simplifying the integration process.

**Key Components:**

* **Calling Extensions SDK (JavaScript):**  The core JavaScript library enabling communication.  Installed via npm or yarn.
* **Calling Settings Endpoints (API):**  Used to configure the calling app's settings (name, URL, dimensions, etc.) for each connected HubSpot account.
* **Calling iFrame:** The iframe displayed to the user within HubSpot, hosting the custom calling interface.

**Note:** Only outgoing calls are currently supported.


## Getting Started

### 1. Install the Demo App (Optional):

Two demo apps are provided: `demo-minimal-js` (JavaScript) and `demo-react-ts` (React/TypeScript).  These use mock data for testing purposes.

**Installation (using npm):**

1. Install Node.js.
2. Clone the repository.
3. Navigate to the demo app directory:
   ```bash
   cd demos/demo-minimal-js  # or cd demos/demo-react-ts
   ```
4. Install dependencies:
   ```bash
   npm install
   ```
5. Start the app:
   ```bash
   npm start
   ```
   This opens the app in your browser at `https://localhost:9025/`. You may need to bypass a security warning.


### 2. Launch the Demo App from HubSpot:

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Set the `localStorage` variable based on your chosen demo app:

   **`demo-minimal-js` (installed):**
   ```javascript
   localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');
   ```
   **`demo-minimal-js` (not installed):**
   ```javascript
   localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');
   ```
   **`demo-react-ts` (installed):**
   ```javascript
   localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');
   ```
   **`demo-react-ts` (not installed):**
   ```javascript
   localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');
   ```
4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and initiate a call.  Events will be logged to the console.


### 3. Install the Calling Extensions SDK:

Add the SDK to your project:

**npm:**
```bash
npm install --save @hubspot/calling-extensions-sdk
```

**yarn:**
```bash
yarn add @hubspot/calling-extensions-sdk
```


## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends events to your app, and your app sends events back to HubSpot.

### Creating an SDK Instance:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages to the console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* HubSpot initiates an outbound call */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    defaultEventHandler: (event) => { /* Handle any other events */ }
  }
};

const extensions = new CallingExtensions(options);
```

### Events

#### HubSpot-to-App Events:

* `onReady`: HubSpot is ready for communication.  Provides `engagementId`, `iframeLocation`, `ownerId`, `portalId`, and `userId`.
* `onDialNumber`:  User initiates a call from HubSpot. Provides phone number, contact/company ID, etc.
* `onCreateEngagementSucceeded`: HubSpot successfully created a call engagement. Provides `engagementId`.
* `onCreateEngagementFailed`: HubSpot failed to create a call engagement.
* `onUpdateEngagementSucceeded`: HubSpot successfully updated a call engagement.
* `onUpdateEngagementFailed`: HubSpot failed to update a call engagement.
* `onVisibilityChanged`:  Widget visibility changed (minimized/hidden).
* `onNavigateToRecordFailed`: Navigation to a record failed.
* `onPublishToChannelSucceeded`/`onPublishToChannelFailed`: Publish to channel success/failure.
* `onCallerIdMatchSucceeded`/`onCallerIdMatchFailed`: Caller ID match success/failure.


#### App-to-HubSpot Events:

* `initialized`: App is ready.  Provides `isLoggedIn` and `engagementId`.
* `userLoggedIn`: User logged into the app.
* `userLoggedOut`: User logged out of the app.
* `outgoingCall`: Outgoing call initiated.  Provides `toNumber`, `fromNumber`, `callStartTime`, and `createEngagement` (set to `true` to let HubSpot create the engagement).
* `callAnswered`: Outgoing call answered. Provides `externalCallId`.
* `callEnded`: Call ended. Provides `externalCallId`, `engagementId`, and `callEndStatus`.
* `callCompleted`: Call completed. Provides `engagementId`, `hideWidget` (optional), `engagementProperties` (optional), and `externalCallId`.
* `sendError`:  An error occurred. Provides `message`.
* `resizeWidget`: Request to resize the widget. Provides `height` and `width`.


### Calling Settings API

Use the following API endpoint to configure your app's settings:

```bash
curl --request POST \
     --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '{"name":"My App","url":"https://my-app.com/widget","height":600,"width":400,"isReady":false}'
```

* `APP_ID`: Your app's ID.
* `DEVELOPER_ACCOUNT_API_KEY`: Your developer API key.
* `isReady`: Set to `false` during testing, `true` for production.  Use PATCH to update this flag.


### LocalStorage Overrides (for testing):

You can override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

## Frequently Asked Questions

Refer to the original text for the FAQ section.


This markdown documentation provides a more structured and readable overview of the HubSpot Calling Extensions SDK, incorporating code examples and clarifying the event flow.  Remember to replace placeholder values like `APP_ID` and API keys with your actual values.
