# HubSpot Calling Extensions SDK Documentation

This document details the HubSpot Calling Extensions SDK, allowing developers to integrate custom calling options into HubSpot CRM records.

## Overview

The Calling Extensions SDK facilitates communication between your calling application and HubSpot.  It consists of three key components:

1. **Calling Extensions SDK (JavaScript):**  A JavaScript SDK enabling communication.
2. **Calling Settings Endpoints (API):**  Used to configure your app's settings for each connected HubSpot account.
3. **Calling iFrame:** The iframe where your app is displayed to HubSpot users, configured via the settings endpoints.


**Note:** Only outgoing calls are currently supported.

## Getting Started

### 1. Run the Demo App

Two demo apps are available:

* **`demo-minimal-js`:** A minimal implementation (JavaScript, HTML, CSS).  SDK instantiation in `index.js`.
* **`demo-react-ts`:** A more realistic implementation (React, TypeScript, Styled Components). SDK instantiation in `useCti.ts`.

**Note:** Demo apps use mock data.


### 2. Install the Demo App (Optional)

1. Install Node.js.
2. Clone/download the repository.
3. Navigate to the demo app directory:
   - For `demo-minimal-js`: `cd demos/demo-minimal-js && npm i && npm start`
   - For `demo-react-ts`: `cd demos/demo-react-ts && npm i && npm start`
4. Access the app at `https://localhost:9025/` (may require bypassing a security warning).


### 3. Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts (Contacts > Contacts) or Companies (Contacts > Companies).
2. Open your browser's developer console.
3. Set the `localStorage` item:
   - **Installed:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   - **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   - **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page.
5. Click the "Call" icon, select the demo app from the dropdown, and click "Call".


### 4. Install the Calling Extensions SDK

Use npm or yarn:

```bash
# npm
npm i --save @hubspot/calling-extensions-sdk

# yarn
yarn add @hubspot/calling-extensions-sdk
```

## Using the Calling Extensions SDK

The SDK uses an event-driven architecture.  HubSpot sends events; your app responds via event handlers.


### SDK API

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, // Optional: Log debug messages
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* Dial number event received */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created successfully */ },
    onCreateEngagementFailed: (event) => { /* Engagement creation failed */ },
    onUpdateEngagementSucceeded: (event) => { /* Engagement updated successfully */ },
    onUpdateEngagementFailed: (event) => { /* Engagement update failed */ },
    onVisibilityChanged: (event) => { /* Widget visibility changed */ },
    // ...other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

### Events

**HubSpot sends these events:**

* `onReady`: HubSpot is ready to receive messages.
* `onDialNumber`: User initiates an outbound call.
* `onCreateEngagementSucceeded`/`onCreateEngagementFailed`: Result of engagement creation.
* `onUpdateEngagementSucceeded`/`onUpdateEngagementFailed`: Result of engagement update.
* `onVisibilityChanged`: Widget visibility changes.


**Your app sends these messages:**

* `initialized`: Softphone ready.
* `userLoggedIn`/`userLoggedOut`: User login/logout status.
* `outgoingCall`: Outgoing call started.
* `callAnswered`: Call answered.
* `callEnded`: Call ended.
* `callCompleted`: Call completed.
* `sendError`: Error occurred.
* `resizeWidget`: Resize request.


See the detailed event descriptions and payloads in the original text for specifics on each event's data structure.


### Calling Settings Endpoint (API)

Use this API endpoint to configure your app's settings:

`POST/PATCH/GET/DELETE https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY`

**Payload Example (POST/PATCH):**

```json
{
  "name": "My App",
  "url": "https://myapp.com/widget",
  "height": 600,
  "width": 400,
  "isReady": false, // Set to true for production
  "supportsCustomObjects": true
}
```

Replace `APP_ID` with your app's ID and `DEVELOPER_ACCOUNT_API_KEY` with your API key.  The `isReady` flag indicates production readiness.


### Overriding Settings with localStorage (Testing)

For testing, override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


### Production Deployment

1. Set `isReady` to `true` using the API.
2. Publish your app to the HubSpot marketplace (optional).


## Frequently Asked Questions (FAQ)

The original text contains a comprehensive FAQ section addressing authentication, CDN hosting, engagement creation/updates, required scopes, integration with existing apps, multiple integrations, free user access, automatic updates, user permissions, custom properties, and calling from custom objects.  Refer to the original text for the answers.

This markdown documentation provides a structured and concise overview of the HubSpot Calling Extensions SDK, making it easier for developers to understand and use the API.  Remember to refer to the original text for detailed information on specific events, payloads, and API responses.
