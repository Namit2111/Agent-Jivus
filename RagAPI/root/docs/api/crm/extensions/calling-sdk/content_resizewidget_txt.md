# HubSpot Calling Extensions SDK Documentation

## Overview

The HubSpot Calling Extensions SDK allows developers to integrate custom calling functionality into HubSpot.  This enables users to initiate calls directly from HubSpot records (Contacts, Companies, and potentially custom objects), enhancing the user experience.  The SDK facilitates communication between the calling application and HubSpot via events and API calls.  Currently, only *outgoing* calls are supported.

## Key Components

A calling extension comprises three main components:

1. **Calling Extensions SDK (JavaScript):** A JavaScript SDK enabling communication between your app and HubSpot.  It's installed as a Node.js dependency (`@hubspot/calling-extensions-sdk`).

2. **Calling Settings Endpoints (API):**  Used to configure your app's settings (name, URL, dimensions, etc.) for each connected HubSpot account.  These settings determine how your app appears within HubSpot's call interface.

3. **Calling iFrame:** The iframe where your calling app is displayed to HubSpot users.  Its configuration is managed via the calling settings endpoints.


## Getting Started

### 1. Install the Demo App (Optional)

The HubSpot documentation provides two demo apps: `demo-minimal-js` (JavaScript, HTML, CSS) and `demo-react-ts` (React, TypeScript, Styled Components).  These use mock data for testing purposes.  To install:

1. Install Node.js.
2. Clone the repository (or download the ZIP).
3. Navigate to the demo app's directory:
   - `cd demos/demo-minimal-js` (for the minimal JS app)
   - `cd demos/demo-react-ts` (for the React/TypeScript app)
4. Run `npm i && npm start`.  This will install dependencies and start the app at `https://localhost:9025/`.


### 2. Launch the Demo App from HubSpot

1. Navigate to HubSpot Contacts or Companies.
2. Open your browser's developer console.
3. Run one of the following `localStorage` commands, depending on the demo app and whether you installed it locally:
   - **Installed `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   - **Installed `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   - **Uninstalled `demo-minimal-js`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   - **Uninstalled `demo-react-ts`:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
4. Refresh the page. The demo app should appear in the call switcher.


### 3. Install the SDK in Your App

Add the SDK to your project:

```bash
npm i --save @hubspot/calling-extensions-sdk
# or
yarn add @hubspot/calling-extensions-sdk
```


## Using the SDK

The SDK uses events to communicate between HubSpot and your app.

### Sending Messages to HubSpot (Events)

The `extensions` object exposes methods to send events to HubSpot:

- `initialized(payload)`:  Indicates app readiness.  `payload` includes `isLoggedIn` (boolean) and `engagementId` (number).
- `userLoggedIn()`: User login event.
- `userLoggedOut()`: User logout event.
- `outgoingCall(callInfo)`: Outgoing call initiated.  `callInfo` includes `toNumber` (string, required), `fromNumber` (string, required), `callStartTime` (number), and `createEngagement` (boolean, defaults to `true`).
- `callAnswered(payload)`: Call answered. `payload` includes `externalCallId` (string).
- `callEnded(payload)`: Call ended. `payload` includes `externalCallId` (string), `engagementId` (number), and `callEndStatus` (enum).
- `callCompleted(data)`: Call completed. `data` includes `engagementId`, `hideWidget` (boolean), `engagementProperties` (object), and `externalCallId`.
- `sendError(data)`:  Reports an error. `data` includes `message` (string).
- `resizeWidget(data)`:  Resizes the widget. `data` includes `height` and `width` (numbers).

**Example (`outgoingCall`):**

```javascript
const callInfo = {
  toNumber: '+15551234567',
  fromNumber: '+15559876543',
  createEngagement: true,
  callStartTime: Date.now()
};
extensions.outgoingCall(callInfo);
```

### Receiving Messages from HubSpot (Event Handlers)

Your app listens for HubSpot events using event handlers:

- `onReady()`: HubSpot is ready.
- `onDialNumber(data)`: Outbound call initiated by HubSpot. `data` includes various call details (phone number, owner ID, object type, etc.).
- `onCreateEngagementSucceeded(event)`: Engagement successfully created by HubSpot.
- `onCreateEngagementFailed(event)`: Engagement creation failed.
- `onUpdateEngagementSucceeded(event)`: Engagement successfully updated.
- `onUpdateEngagementFailed(event)`: Engagement update failed.
- `onVisibilityChanged(data)`: Widget visibility changed (minimized/hidden).
- `defaultEventHandler(event)`:  A catch-all for unhandled events.

**Example (`onDialNumber`):**

```javascript
extensions.eventHandlers = {
  onDialNumber: (data) => {
    console.log("Dial number event received:", data);
    // Process call data
  }
};
```


## API Endpoints (Calling Settings)

Use the following API endpoint to manage your app's settings:

`https://api.hubapi.com/crm/v3/extensions/calling/{APP_ID}/settings?hapikey={DEVELOPER_ACCOUNT_API_KEY}`

- **POST:** Creates or updates settings.
- **PATCH:** Updates existing settings.
- **GET:** Retrieves settings.
- **DELETE:** Deletes settings.


**Example (using `curl` to POST settings):**

```bash
curl --request POST \
  --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"name":"My App","url":"https://myapp.com","height":600,"width":400,"isReady":false}'
```

The `isReady` flag indicates whether the app is ready for production. Set it to `false` during development and `true` when ready.


##  Local Storage Overrides (for Testing)

For testing purposes, you can override settings using `localStorage`:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App',
  url: 'http://localhost:3000'
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```


## Frequently Asked Questions (FAQs)

The documentation includes a comprehensive FAQ section covering authentication, CDN hosting, engagement creation/updates, required scopes, compatibility with existing apps, handling multiple integrations, free user access, automatic updates, user permissions, custom properties, and calling from custom objects.  Refer to the original documentation for detailed answers.


This markdown documentation provides a structured overview of the HubSpot Calling Extensions SDK.  Always refer to the official HubSpot documentation for the most up-to-date information and detailed explanations.
