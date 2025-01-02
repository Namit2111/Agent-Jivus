# HubSpot CRM API: Receive Calls in Calling Apps (BETA)

This document details the HubSpot CRM API's beta feature for receiving inbound calls within calling apps integrated with HubSpot.  This allows users to manage calls directly within HubSpot, eliminating the need to switch between applications.

## Overview

This feature allows developers to integrate their calling apps with HubSpot to receive and manage inbound calls directly within the HubSpot interface.  Calls are automatically logged in HubSpot's Call Index page, enabling real-time note-taking and post-call review.  The integration leverages the HubSpot Calling SDK and requires specific API calls and event handling.

## Preventing Dropped Calls and Simultaneous Ringing

Because HubSpot is a multi-page application, navigating between pages can cause the iframe containing the calling app to be removed and re-rendered. To prevent dropped calls, calling apps can maintain their call connection within a dedicated "calling window."

### Opting out of the Calling Window

While the calling window is enabled by default, apps that already handle page refreshes can opt out.  Use the following PATCH request to disable it:

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"usesCallingWindow":false}'
```

Replace `APP_ID` with your application ID and `DEVELOPER_ACCOUNT_API_KEY` with your API key.

### Using the Calling Window for Shared Calling State

If using the calling window, HubSpot notifies the app of the iframe location via the `onReady` SDK event.  Handle these locations as follows:

* **`iframeLocation: window`**: Create the call connection in the calling window and manage the shared calling state (using a `SharedWorker` is recommended for cross-tab communication).
* **`iframeLocation: remote`**: Subscribe to the shared calling state from the calling window.

This prevents simultaneous ringing across multiple HubSpot tabs.


## HubSpot Calling SDK Integration

1. **Installation:**

   * npm: `npm i -s @hubspot/calling-extensions-sdk@latest`
   * yarn: `yarn add @hubspot/calling-extensions-sdk@latest`

2. **Setting User Availability:**

   Use the following events to manage user availability:

   * **`initialized` event:** Send a payload to indicate user login status and availability.  Optional `sizeInfo` can specify widget dimensions.

     ```javascript
     const payload = {
       isLoggedIn: true, // Boolean
       isAvailable: true, // Boolean
       sizeInfo: { height: 300, width: 400 } // Object
     };
     extensions.initialized(payload);
     ```

   * **`userAvailable` event:**  Indicates user availability.

     ```javascript
     extensions.userAvailable();
     ```

   * **`userUnavailable` event:** Indicates user unavailability.

     ```javascript
     extensions.userUnavailable();
     ```

3. **Inbound Call Notification:**

   Send the `incomingCall` event when an inbound call starts:

   ```javascript
   const callInfo = {
     fromNumber: "+15551234567", // Required: Caller's number
     toNumber: "+15559876543", // Required: Recipient's number
     createEngagement: true // Whether HubSpot should create an engagement
   };
   extensions.incomingCall(callInfo);
   ```

   If `createEngagement` is `true`, subscribe to `onCreateEngagementSucceeded` and `onCreateEngagementFailed` events for handling success and failure.  This is recommended for supporting custom objects and future HubSpot integrations.

   ```javascript
   extensions.eventHandlers = {
     onCreateEngagementSucceeded: (data) => {
       const { engagementId } = data; // HubSpot-generated engagement ID
       // ... your code ...
     },
     onCreateEngagementFailed: (data) => {
       const { error: { message } } = data; // Error message
       // ... your code ...
     }
   };
   ```

4. **Caller ID Matching:**

   Subscribe to `onCallerIdMatchSucceeded` and `onCallerIdMatchFailed` to retrieve contact matching data.  This replaces the need for the Search API.

   ```javascript
   extensions.eventHandlers = {
     onCallerIdMatchSucceeded: (data) => {
       const { callerIdMatches } = data; // Array of ContactIdMatch or CompanyIdMatch
       // ... your code ...
     },
     onCallerIdMatchFailed: (data) => {
       const { error: { message } } = data; // Error message
       // ... your code ...
     }
   };
   ```

   `ContactIdMatch` and `CompanyIdMatch` structures:

   ```typescript
   type ObjectCoordinates = {
     portalId: number;
     objectTypeId: string;
     objectId: number;
   }
   type ContactIdMatch = {
     callerIdType: 'CONTACT';
     objectCoordinates: ObjectCoordinates;
     firstName: string;
     lastName: string;
     email: string;
   }
   type CompanyIdMatch = {
     callerIdType: 'COMPANY';
     objectCoordinates: ObjectCoordinates;
     name: string;
   }
   ```

5. **Navigating to Record Pages:**

   Use `navigateToRecord` to navigate to a contact or company record page after receiving caller ID matches.

   ```javascript
   const data = { objectCoordinates: callerIdMatch.objectCoordinates };
   extensions.navigateToRecord(data);
   ```

6. **`onReady` Event Handling:**

   The `onReady` event provides information about the iframe location and engagement ID (if any).  You'll likely need to re-initialize your app based on this information.

   ```javascript
   // ... within the onReady event handler ...
   extensions.initialized(payload); // Re-initialize with engagementId if present
   if (payload.engagementId) {
     // ... initialize calling state for existing inbound call ...
   }
   ```

## Ungating Your Account and Users

* **Ungate Account (Developer Test Accounts):**  Set `localStorage['LocalSettings:Calling:supportsInboundCalling'] = true;` in your browser's developer console.
* **Ungate Account (Other Accounts):** Join the beta program.
* **Ungate Users:** Use a PATCH request to set `supportsInboundCalling` to `true` in your app settings:

   ```bash
   curl --request PATCH \
   --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
   --header 'accept: application/json' \
   --header 'content-type: application/json' \
   --data '{"supportsInboundCalling":true}'
   ```

## Setting the Provider

Select your calling app as the preferred provider in your HubSpot call settings.  Only calls from the selected provider will be received.


## Receiving Incoming Calls

1. Integrate your calling app.
2. Log in to your app via the HubSpot call widget.
3. Set your availability to receive calls.
4. Answer calls from the call remote.
5. Completed calls (including missed calls) are logged in the Call Index page.


This documentation provides a comprehensive overview of the HubSpot CRM API's beta feature for receiving inbound calls in calling apps. Remember to consult the official HubSpot documentation for the most up-to-date information and details.
