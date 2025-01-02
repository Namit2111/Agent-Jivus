# HubSpot CRM API: Receive Calls in Calling Apps (BETA)

This document describes the HubSpot CRM API's beta feature for receiving inbound calls within HubSpot using calling apps.  It outlines the process of integrating your calling app to handle inbound calls, manage call states, and leverage HubSpot's features for call logging and contact management.

## Overview

This beta feature allows developers to integrate their calling apps with HubSpot so that inbound calls received through the app are automatically logged in HubSpot.  This eliminates the need for users to switch between the calling app and HubSpot.  Key features include:

* **Automatic Call Logging:** Inbound calls are automatically logged in the HubSpot Call Index page.
* **Real-time Notes:** Users can take notes during and after calls directly within HubSpot.
* **Prevent Dropped Calls:** Techniques are provided to prevent calls from being dropped when navigating within HubSpot.
* **Prevent Simultaneous Ringing:**  Methods are provided to ensure calls only ring in one browser tab.
* **Caller ID Matching:**  The API provides contact and company matching data for incoming calls, eliminating reliance on the Search API.
* **Navigation to Records:** Direct navigation to contact or company records from the incoming call data.


## API Endpoints

The primary API endpoint used is for managing calling app settings:

**PATCH `/crm/v3/extensions/calling/APP_ID/settings`**

This endpoint uses the following parameters:

* **`APP_ID`**: Your calling app's ID.
* **`hapikey`**: Your developer account's API key.

The request body is a JSON object.  The following parameters are relevant:

* **`usesCallingWindow` (boolean):**  Indicates whether your app uses a dedicated calling window to prevent dropped calls.  Defaults to `true`.  Set to `false` to opt out.

**Example (cURL): Opting out of the calling window**

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"usesCallingWindow":false}'
```

**PATCH `/crm/v3/extensions/calling/APP_ID/settings`**

This endpoint is also used to enable inbound calling:


* **`supportsInboundCalling` (boolean):**  Indicates whether your app supports inbound calling.  Defaults to `false`. Set to `true` to enable.


**Example (cURL): Enabling inbound calling**

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"supportsInboundCalling":true}'
```


## SDK and Event Handling

The HubSpot Calling Extensions SDK (`@hubspot/calling-extensions-sdk`) is required.

**Installation (npm):**

```bash
npm i -s @hubspot/calling-extensions-sdk@latest
```

**Installation (yarn):**

```bash
yarn add @hubspot/calling-extensions-sdk@latest
```

**Example Code (JavaScript):**

```javascript
import CallingExtensions from "@hubspot/calling-extensions-sdk";

const extensions = new CallingExtensions({
  eventHandlers: {
    onReady: ({ engagementId, iframeLocation, ownerId, portalId, userId }) => {
      // HubSpot is ready to receive messages.  Handle iframeLocation ('window', 'remote', 'widget') accordingly.
      console.log("HubSpot ready:", { engagementId, iframeLocation, ownerId, portalId, userId });
      // ... your logic to handle different iframe locations and manage call state ...
      extensions.initialized({ isLoggedIn: true, isAvailable: true }); //Set Availability
    },
    // ... other event handlers (see below) ...
  },
});
```

**Key SDK Events and Methods:**

* **`initialized(payload)`:**  Notifies HubSpot of the app's initialization status and user availability.  `payload` can include `isLoggedIn`, `isAvailable`, and `sizeInfo`.
* **`userAvailable()`:**  Indicates the user is available for calls.
* **`userUnavailable()`:** Indicates the user is unavailable for calls.
* **`incomingCall(callInfo)`:** Notifies HubSpot that an inbound call has started. Requires `fromNumber` and `toNumber`.  `createEngagement` (boolean) determines whether HubSpot creates an engagement record.
* **`onCreateEngagementSucceeded(data)`:**  Triggered after successful engagement creation.  `data` contains the `engagementId`.
* **`onCreateEngagementFailed(data)`:**  Triggered if engagement creation fails. `data` contains an error message.
* **`onCallerIdMatchSucceeded(data)`:** Triggered when caller ID matches are found. `data` contains `callerIdMatches` (array of `ContactIdMatch` or `CompanyIdMatch`).
* **`onCallerIdMatchFailed(data)`:** Triggered if caller ID matching fails. `data` contains an error message.
* **`navigateToRecord(data)`:** Navigates to a contact or company record in HubSpot.  Requires `objectCoordinates`.

**Data Types:**

```typescript
type ObjectCoordinates = {
  portalId: number;
  objectTypeId: string;
  objectId: number;
};

type ContactIdMatch = {
  callerIdType: 'CONTACT';
  objectCoordinates: ObjectCoordinates;
  firstName: string;
  lastName: string;
  email: string;
};

type CompanyIdMatch = {
  callerIdType: 'COMPANY';
  objectCoordinates: ObjectCoordinates;
  name: string;
};
```


##  Call State Management

To prevent dropped calls and simultaneous ringing, manage the call connection within a dedicated calling window (if `usesCallingWindow` is true) using techniques like SharedWorkers for cross-tab communication.  The `iframeLocation` in the `onReady` event determines whether the call should be initiated in the calling window or managed remotely.


## Ungating Your Account and Users

To use this beta feature, you might need to ungate your account and users:

* **Developer Test Accounts:** Set `localStorage['LocalSettings:Calling:supportsInboundCalling'] = true;` in your browser's developer console.
* **Other Accounts:** Join the beta program (instructions provided in the original text).
* **Ungating Users:** Set `supportsInboundCalling` to `true` using the PATCH endpoint (see API Endpoints section).


##  Receiving Incoming Calls

1.  Integrate your calling app.
2.  Set user availability using the SDK's events (`initialized`, `userAvailable`, `userUnavailable`).
3.  Handle inbound calls using the `incomingCall` event.
4.  Subscribe to `onCreateEngagementSucceeded`, `onCreateEngagementFailed`, `onCallerIdMatchSucceeded`, and `onCallerIdMatchFailed` events.
5.  Use `navigateToRecord` to navigate to relevant HubSpot records after caller ID matching.


This comprehensive guide should enable developers to integrate their calling apps with HubSpot's inbound call functionality. Remember that this is a beta feature, and some aspects might change.  Always refer to the latest HubSpot documentation for updates.
