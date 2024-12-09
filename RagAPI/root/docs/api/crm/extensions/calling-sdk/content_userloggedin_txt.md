# HubSpot Calling Extensions SDK Documentation

This document provides a comprehensive guide to the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling functionality into their HubSpot apps.

## Overview

The Calling Extensions SDK allows apps to offer a custom calling experience directly from CRM records within HubSpot.  This involves three key components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints (API):** Configure settings for your app on a per-HubSpot account basis.
3. **Calling iFrame:**  The user interface of your app within HubSpot, configured via the settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](LINK_TO_ARTICLE_HERE -  replace with actual link).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.

## Getting Started

### Prerequisites

*   A HubSpot developer account ([Sign up here](LINK_TO_SIGNUP_HERE - replace with actual link) if you don't have one).
*   A HubSpot app (create one from your developer account if needed).
*   Node.js installed on your development environment.

### Demo Apps

Two demo apps are available to test the SDK:

*   **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS (`index.js` shows SDK instantiation).
*   **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components (`useCti.ts` shows SDK instantiation).

**Note:** Demo apps use mock data and are not fully functional calling applications.

### Installing the Demo App

1.  Clone or download the demo app repository (ZIP download available).
2.  Navigate to the demo app's root directory in your terminal.
3.  Run the appropriate command:

    *   `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
    *   `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`

    This installs dependencies and starts the app at `https://localhost:9025/`.  You might need to bypass a security warning.

### Launching the Demo App from HubSpot

1.  Go to either **Contacts > Contacts** or **Contacts > Companies** in your HubSpot account.
2.  Open your browser's developer console.
3.  Run one of the following `localStorage` commands, depending on your demo app and whether you installed it locally:

    *   **Installed `demo-minimal-js` or `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
    *   **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
    *   **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`

4.  Refresh the HubSpot page.
5.  Click the "Call" icon, select the demo app from the dropdown, and click "Call".

### Installing the SDK

Add the SDK to your project using npm or yarn:

*   **npm:** `npm i --save @hubspot/calling-extensions-sdk`
*   **yarn:** `yarn add @hubspot/calling-extensions-sdk`

## Using the SDK

The SDK uses an event-driven architecture.  HubSpot sends messages (events) to your app, and your app can send messages back.

### Events

#### HubSpot sends these messages:

*   `onReady`
*   `onDialNumber`
*   `onEngagementCreated` (Deprecated; use `onCreateEngagementSucceeded`)
*   `onNavigateToRecordFailed`
*   `onPublishToChannelSucceeded`
*   `onPublishToChannelFailed`
*   `onCallerIdMatchSucceeded`
*   `onCallerIdMatchFailed`
*   `onCreateEngagementSucceeded`
*   `onCreateEngagementFailed`
*   `onUpdateEngagementSucceeded`
*   `onUpdateEngagementFailed`
*   `onVisibilityChanged`
*   `defaultEventHandler`


#### Your app sends these messages:

*   `initialized`
*   `userLoggedIn`
*   `userLoggedOut`
*   `outgoingCall`
*   `callAnswered`
*   `callEnded`
*   `callCompleted`
*   `sendError`
*   `resizeWidget`

Each event has a specific payload; see the detailed descriptions in the original text for specifics.

### SDK Initialization

Create a `CallingExtensions` instance and define event handlers:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Set to true for debugging
  eventHandlers: {
    onReady: () => { /* ... */ },
    onDialNumber: (event) => { /* ... */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

### iFrame Parameters

To launch the calling extension iFrame, HubSpot requires these parameters:

```json
{
  "name": "My App Name",
  "url": "My App URL",
  "width": 400,
  "height": 600,
  "isReady": true, // Set to false during development
  "supportsCustomObjects": true //Indicates support for custom object calls
}
```


### Calling Settings Endpoint

Use the HubSpot API to manage your app's settings:

```bash
# Example (replace APP_ID and API_KEY)
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"My App","url":"https://myapp.com","height":600,"width":400,"isReady":false}'
```

This endpoint supports `POST`, `PATCH`, `GET`, and `DELETE`.  Use `PATCH` to update settings (e.g., setting `isReady` to `true` for production).

### LocalStorage Override

For testing, you can override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'My App URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Production Deployment

Set `isReady` to `true` via the API to make your app ready for production.  Then, publish your app to the HubSpot Marketplace ([instructions here](LINK_TO_MARKETPLACE_INSTRUCTIONS)).

## Frequently Asked Questions

The FAQs section from the original text is included here verbatim for completeness.  Refer to the original for details.

##  Share your feedback

Include a feedback mechanism here.


This markdown document provides a structured and readable version of the provided text, making it easier to navigate and understand the HubSpot Calling Extensions SDK.  Remember to replace the placeholder links with the actual links.
