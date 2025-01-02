# HubSpot CRM API: Receive Calls in Calling Apps (BETA)

This document details the HubSpot CRM API's beta feature for receiving inbound calls within HubSpot using calling apps.  It outlines the process of integrating inbound calling functionality, handling call states, and managing user availability.

## Overview

This beta feature allows developers to integrate their calling apps with HubSpot so that inbound calls are received and managed directly within the HubSpot interface. Call records are automatically logged in the Call Index Page, providing a unified call history.  The integration leverages the HubSpot Calling SDK and requires adherence to HubSpot's Developer Terms and Developer Beta Terms.


## Preventing Dropped Calls and Simultaneous Ringing

Because HubSpot is a multi-page application, page navigation can interrupt the calling app iframe. To prevent dropped calls, calling apps can use a "calling window" to maintain the call connection.

**Opting out of the Calling Window:**

Apps that already handle dropped calls can opt out.  Use the following PATCH request to the calling settings endpoint to set `usesCallingWindow` to `false`:

```bash
curl --request PATCH \
--url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data '{"usesCallingWindow":false}'
```

Replace `APP_ID` with your app's ID and `DEVELOPER_ACCOUNT_API_KEY` with your API key.


**Using the Calling Window:**

The `onReady` SDK event provides the `iframeLocation`.  Manage the call connection and shared calling state as follows:

* **`iframeLocation: window`**: Create the call connection in the calling window and use a `SharedWorker` for cross-tab communication.
* **`iframeLocation: remote`**: Subscribe to the shared calling state from the calling window.

This prevents dropped calls and simultaneous ringing across multiple HubSpot tabs.


## HubSpot Calling SDK Integration

1. **Installation:**

   * npm: `npm i -s @hubspot/calling-extensions-sdk@latest`
   * yarn: `yarn add @hubspot/calling-extensions-sdk@latest`

2. **User Availability:**

   Set user availability using one of the following events:

   * **`initialized` event:**

     ```javascript
     const payload = {
       isLoggedIn: true, // Optional: Whether a user is logged in
       isAvailable: true, // Optional: Whether a user is available for inbound calls
       sizeInfo: { height: 300, width: 400 } // Optional: Widget size
     };
     extensions.initialized(payload);
     ```

   * **`userAvailable` event:** `extensions.userAvailable();`

   * **`userUnavailable` event:** `extensions.userUnavailable();`

3. **Incoming Call Notification:**

   Send the `incomingCall` event when an inbound call starts:

   ```javascript
   const callInfo = {
     fromNumber: "+15551234567", // Required: Caller's number
     toNumber: "+15559876543", // Required: Recipient's number
     createEngagement: true // Whether to create a HubSpot engagement
   };
   extensions.incomingCall(callInfo);
   ```

   If `createEngagement` is `true`, subscribe to `onCreateEngagementSucceeded` and `onCreateEngagementFailed` for custom object support:

   ```javascript
   onCreateEngagementSucceeded(data) {
     const { engagementId } = data; // HubSpot-created engagement ID
     // ...
   }

   onCreateEngagementFailed(data) {
     const { error: { message } } = data;
     // ...
   }
   ```

4. **Caller ID Matching:**

   Subscribe to `onCallerIdMatchSucceeded` and `onCallerIdMatchFailed` to receive contact matching data:

   ```javascript
   onCallerIdMatchSucceeded: data => {
     const { callerIdMatches } = data; // Array of ContactIdMatch or CompanyIdMatch
     // ...
   }

   onCallerIdMatchFailed: data => {
     const { error: { message } } = data;
     // ...
   }
   ```

   `ContactIdMatch` and `CompanyIdMatch` types:

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

   Use `navigateToRecord` to navigate to a contact or company record page after receiving caller ID matches:

   ```javascript
   const data = { objectCoordinates }; // From onCallerIdMatchSucceeded
   extensions.navigateToRecord(data);
   ```

   After engagement creation, HubSpot redirects to the specified page, and the SDK re-initializes in the `onReady` event.


6. **`onReady` Event Handling (Example):**

   ```javascript
   onReady(payload) {
     extensions.initialized(payload);
     if (payload.engagementId) {
       // Initialize calling state for existing inbound call
       // ...
     }
     // ...
   }
   ```

##  Ungating Your Account and Users

1. **Ungate Account (Developer Test Account):**  In your browser's developer console, set:  `localStorage['LocalSettings:Calling:supportsInboundCalling'] = true;`

2. **Ungate Account (Other Accounts):** Join the beta program.

3. **Ungate Users:** Use a PATCH request to set `supportsInboundCalling` to `true` in the calling settings endpoint:

   ```bash
   curl --request PATCH \
   --url 'https://api.hubapi.com/crm/v3/extensions/calling/APP_ID/settings?hapikey=DEVELOPER_ACCOUNT_API_KEY' \
   --header 'accept: application/json' \
   --header 'content-type: application/json' \
   --data '{"supportsInboundCalling":true}'
   ```

## Setting the Provider

Select your calling app as the preferred provider in your HubSpot call settings (Settings > General > Calling).  Only calls from the selected provider will be received.


## Receiving Incoming Calls

1. Integrate with a calling app.
2. Log in to your calling app through the HubSpot call widget.
3. Set your availability to "Available" in HubSpot.
4. Answer inbound calls.
5. Completed and missed calls are logged in the Call Index page.


##  Additional Notes:

* The specific behavior might vary slightly depending on the calling app's implementation.
* Minimizing the call widget while available does not prevent call reception; closing the call tab during a call will disconnect it.


This documentation provides a comprehensive guide for integrating inbound calling into your HubSpot-based calling application. Remember to consult the HubSpot developer documentation for the most up-to-date information and API specifications.
