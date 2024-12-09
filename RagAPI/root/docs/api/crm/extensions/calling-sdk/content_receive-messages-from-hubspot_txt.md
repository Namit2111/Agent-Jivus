# HubSpot Calling Extensions SDK Documentation

This document provides comprehensive information on the HubSpot Calling Extensions SDK, enabling developers to integrate custom calling options into their HubSpot apps.

## Overview

The Calling Extensions SDK allows apps to offer custom calling functionality directly from CRM records within HubSpot.  This integration consists of three key components:

1. **Calling Extensions SDK (JavaScript):** Facilitates communication between your app and HubSpot.
2. **Calling Settings Endpoints:** Used to configure calling settings for your app on a per-HubSpot account basis.
3. **Calling iFrame:**  The visual interface of your app displayed to HubSpot users; configured using the calling settings endpoints.

For details on the in-app calling experience, refer to [this knowledge base article](link_to_knowledge_base_article_here).  Once integrated, your app will appear in the HubSpot call switcher.

**Note:** Currently, only outgoing calls are supported.

## Getting Started

### Prerequisites

* A HubSpot developer account ([sign up here](link_to_signup_here)).
* An existing HubSpot app (or create one from your [HubSpot developer account](link_to_developer_account_here)).
* Node.js installed on your environment.

### Demo Apps

Two demo apps are available to test the SDK:

* **`demo-minimal-js`:** A minimal implementation using JavaScript, HTML, and CSS.  See `index.js` for SDK instantiation.
* **`demo-react-ts`:** A more comprehensive example using React, TypeScript, and Styled Components.  See `useCti.ts` for SDK instantiation.

**Note:** Demo apps use mock data and are not fully functional calling applications.

### Installing Demo Apps

1. Clone, fork, or download the ZIP of the repository.
2. Navigate to the demo app's root directory:
   * `demo-minimal-js`: `cd demos/demo-minimal-js`
   * `demo-react-ts`: `cd demos/demo-react-ts`
3. Install dependencies: `npm i`
4. Start the app: `npm start`  (Opens `https://localhost:9025/` in your browser; you may need to bypass a security warning).

### Launching Demo Apps from HubSpot

1. Navigate to HubSpot records (Contacts > Contacts or Contacts > Companies).
2. Open your browser's developer console and run one of the following commands:
   * **Installed Demo:** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'local');`
   * **`demo-minimal-js` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app:js');`
   * **`demo-react-ts` (uninstalled):** `localStorage.setItem('LocalSettings:Calling:installDemoWidget', 'app');`
3. Refresh the page.
4. Click the "Call" icon, select the demo app from the dropdown, and click "Call".

### Installing the SDK

Use npm or yarn to install the SDK:

* **npm:** `npm i --save @hubspot/calling-extensions-sdk`
* **yarn:** `yarn add @hubspot/calling-extensions-sdk`


## Using the Calling Extensions SDK

The SDK uses events for communication. See the [Events section](#events) for a complete list.  Key events and their purpose are outlined below:

* **Dial Number:** HubSpot initiates an outbound call.
* **Outbound Call Started:** App notifies HubSpot that the call has begun.
* **Create Engagement:** HubSpot creates a call engagement (minimal information if requested by the app).
* **Engagement Created:** HubSpot confirms engagement creation.
* **Engagement ID Sent to App:** HubSpot provides the `engagementId` to the app.
* **Call Ended:** App notifies HubSpot that the call has ended.
* **Call Completed:** App signals completion of the user experience.
* **Update Engagement:** App updates the engagement with detailed call information using the `engagementId` ([Learn more about updating call engagements](link_to_api_documentation_here)).


### SDK Initialization

Create a `CallingExtensions` object with event handlers:

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const options = {
  debugMode: true, //optional, logs messages to console
  eventHandlers: {
    onReady: () => { /* HubSpot is ready */ },
    onDialNumber: (event) => { /* HubSpot sends dial number */ },
    onCreateEngagementSucceeded: (event) => { /* Engagement created */ },
    // ... other event handlers
  },
};

const extensions = new CallingExtensions(options);
```

### Testing Your App

To launch the iFrame for end-users, HubSpot requires these iFrame parameters:

```javascript
{
  name: "My App Name", //String
  url: "My App URL", //String
  width: 400, //Number
  height: 600, //Number
  isReady: false, //Boolean (set to false during testing)
  supportsCustomObjects: true //Boolean
}
```

### Using the Calling Settings Endpoint

Use the HubSpot settings API (e.g., with `curl` or Postman) to configure your app:

```bash
curl --request POST \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"name":"My App","url":"My App URL","height":600,"width":400,"isReady":false}'
```
(Replace `APP_ID` and `DEVELOPER_ACCOUNT_API_KEY` with your values).  This endpoint supports `POST`, `PATCH`, `GET`, and `DELETE` methods.

### Overriding Settings with localStorage

For testing, override settings in your browser's developer console:

```javascript
const myExtensionSettings = {
  isReady: true,
  name: 'My App Name',
  url: 'My App URL',
};
localStorage.setItem('LocalSettings:Calling:CallingExtensions', JSON.stringify(myExtensionSettings));
```

### Preparing for Production

Set `isReady` to `true` using the `PATCH` endpoint once testing is complete.

### Publishing to the Marketplace

[Learn how to publish your app to the HubSpot marketplace here](link_to_marketplace_instructions_here).


## Events

### Sending Messages to HubSpot

*   `initialized`:  Signals app readiness.  Payload: `{ isLoggedIn: boolean, engagementId: number }`
*   `userLoggedIn`:  Indicates user login.
*   `userLoggedOut`: Indicates user logout.
*   `outgoingCall`:  Notifies HubSpot of an outgoing call. Payload: `{ phoneNumber: string, callStartTime: number, createEngagement: boolean, toNumber: string, fromNumber: string }`
*   `callAnswered`:  Signals call answer. Payload: `{ externalCallId: string }`
*   `callEnded`:  Notifies call termination. Payload: `{ externalCallID: string, engagementId: number, callEndStatus: EndStatus }`
*   `callCompleted`: Signals call completion. Payload: `{ engagementId: number, hideWidget: boolean, engagementProperties: { [key: string]: string }, externalCallId: number }`
*   `sendError`: Reports errors. Payload: `{ message: string }`
*   `resizeWidget`: Requests widget resizing. Payload: `{ height: number, width: number }`

### Receiving Messages from HubSpot

*   `onReady`: HubSpot readiness signal.  Payload includes: `engagementId`, `iframeLocation`, `ownerId`, `portalId`, `userId`
*   `onDialNumber`: Outbound call initiation.  Payload includes: `phoneNumber`, `ownerId`, `subjectId`, `objectId`, `objectType`, `portalId`, `countryCode`, `calleeInfo`, `startTimestamp`, `toPhoneNumberSrc`
*   `onEngagementCreated` (deprecated): Use `onCreateEngagementSucceeded` instead. Payload: `{ engagementId: number }`
*   `onNavigateToRecordFailed`: Failure to navigate to a record. Payload: `{ engagementId: number, objectCoordinates: object }`
*   `onPublishToChannelSucceeded`: Successful channel publishing. Payload: `{ engagementId: number, externalCallId: string }`
*   `onPublishToChannelFailed`: Failed channel publishing. Payload: `{ engagementId: number, externalCallId: string }`
*   `onCallerIdMatchSucceeded`: Successful caller ID match.
*   `onCallerIdMatchFailed`: Failed caller ID match.
*   `onCreateEngagementSucceeded`: Successful engagement creation.
*   `onCreateEngagementFailed`: Failed engagement creation.
*   `onUpdateEngagementSucceeded`: Successful engagement update.
*   `onUpdateEngagementFailed`: Failed engagement update.
*   `onVisibilityChanged`: Widget visibility change. Payload: `{ isMinimized: boolean, isHidden: boolean }`
*   `defaultEventHandler`: Default event handler.


## Frequently Asked Questions

*   **Authentication:**  Handled by the calling app.
*   **CDN Hosting:** Yes, using jsDeliver (e.g., `https://cdn.jsdelivr.net/npm/@hubspot/calling-extensions-sdk@0.2.2/dist/main.js`).
*   **Engagement Creation vs. Update:** HubSpot creates engagements for calls initiated within the HubSpot UI; apps update them with details afterward.  For calls initiated outside HubSpot, the app creates the engagement.
*   **Required Scopes:** `contacts` and `timeline`.
*   **Existing Marketplace Apps:** Functionality can be added to existing apps.
*   **Softphone Integration:** Easy integration is supported.
*   **Multiple Integrations:** Yes, users can use multiple integrations concurrently.
*   **Free User Access:** Yes.
*   **Automatic Integration Appearance:** Yes, for updates to existing apps.
*   **App Installation/Uninstallation:** Controlled by user permissions.
*   **Custom Calling Properties:** Creatable via the properties API.
*   **Calls from Custom Objects:** Possible using the SDK to create calls and notifying HubSpot in the `outgoingCall` event.


This markdown document provides a structured and comprehensive representation of the provided text, enhancing readability and searchability.  Remember to replace placeholder links (`link_to..._here`) with actual links.
