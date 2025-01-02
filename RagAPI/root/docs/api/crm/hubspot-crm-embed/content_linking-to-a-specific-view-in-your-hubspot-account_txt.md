# HubSpot CRM Embed Documentation

## Overview

The HubSpot CRM Embed feature allows you to display interactive HubSpot interfaces within your application.  This enables users to access various tools and views directly from your app, eliminating the need to switch between platforms.  This is distinct from the content embed and content timeline embed features.

## Supported Views and Tools

The following tools can be embedded:

* **Object Timeline:** View activities, upcoming meetings, tasks, and associated records (contacts, companies, deals, etc.) with interactive filtering and association cards.
* **Workflows Tab:** Track workflow enrollment history, enroll records, and search workflows.
* **Sequences Tab (Contacts Only):** Manage sequences, enroll contacts, and track sequence progress.
* **Properties Tab:** Search, filter, view history, and hide properties.
* **Meetings Tab:** Schedule, manage, and review meeting details.
* **Target Accounts Tab (Companies & Deals Only):** View metrics like emails sent and meetings scheduled, along with other aggregate data.


## Embedding URLs

To embed a specific view, use a customized URL with the following structure:

```
https://app.hubspot.com/embed/{hubId}/{objectType}/{recordId}/{view}
```

Where:

* **`hubId`**: Your HubSpot account's Hub ID.
* **`objectType`**: The object type (e.g., `contacts`, `companies`, `deals`).  Note that `contacts` is often represented as `0-1`.
* **`recordId`**: The ID of the specific record.
* **`view`**: The desired view: `timeline`, `workflows`, `sequences` (contacts only).


**Example:**  Embedding the timeline view for a contact with ID 251 in Hub ID 12345:

```
https://app.hubspot.com/embed/12345/0-1/251/timeline
```

**Important:** Users must be logged into their HubSpot account to view the embedded content.  Unauthenticated users will be prompted to log in.


## Embed Sandbox

HubSpot provides an embed sandbox to test different views:

1. Navigate to the embed sandbox environment for your account.
2. Select the HubSpot account containing the data you want to embed.
3. Choose the `Object Type ID` and `Object ID`.
4. Preview the embedded view, interacting with the timeline and tabs.
5. Click "Copy" to copy the embed URL.  Remember to append the `view` parameter (e.g., `/sequences`) to the copied URL for correct functionality.


**Example using the Sandbox and appending the view:**

The sandbox might initially provide a URL like: `https://app.hubspot.com/embed/12345/0-1/251`.  To view the sequences, you would modify this to: `https://app.hubspot.com/embed/12345/0-1/251/sequences`.


##  Error Handling and Considerations

* **Authentication:**  Ensure users are logged into HubSpot.  Handle authentication failures gracefully in your application.
* **Hub ID:**  Correctly identify and use your Hub ID.
* **View Parameter:**  Always append the appropriate `view` parameter to the base URL.
* **Object Type:** Use the correct `objectType` identifier.


This documentation provides a comprehensive guide to using the HubSpot CRM Embed feature.  Refer to the HubSpot developer documentation for more detailed information and updates.
