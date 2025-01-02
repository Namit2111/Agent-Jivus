# HubSpot CRM Embed Documentation

## Overview

The HubSpot CRM Embed feature allows you to display interactive HubSpot interfaces within your application.  This enables users to access key HubSpot functionality, such as object timelines, workflows, sequences, properties, and meetings, directly from your app.  This is distinct from the content embed and content timeline embed features.

## Supported Views and Tools

The following HubSpot tools can be embedded:

* **Object Timeline:** Displays activities, upcoming meetings, and tasks related to a record. Includes an interactive sidebar, activity filters, and association cards (related contacts, companies, deals, etc.).
* **Workflows Tab:** Tracks workflow enrollment history, allows enrollment of records into workflows, and enables workflow searching.
* **Sequences Tab (Contacts Only):** Manages sequences, enrolls contacts, and tracks sequence progress.
* **Properties Tab:** Searches, filters, and displays property history; allows hiding unused blank fields.
* **Meetings Tab:** Schedules, manages, and reviews meeting details.
* **Target Accounts Tab (Companies & Deals Only):** Provides metrics such as emails, meetings, and other aggregate data.


## Embedding a HubSpot View

To embed a specific HubSpot view, construct a URL using the following format:

```
https://app.hubspot.com/embed/{hubId}/{objectType}/{recordId}/{view}
```

* **`hubId`:** Your HubSpot account's Hub ID.
* **`objectType`:** The type of object (e.g., `contacts`, `companies`, `deals`).  Note: The example uses `0-1` for contacts,  you should determine the correct value for your object type.
* **`recordId`:** The ID of the specific record.
* **`view`:** The view to embed:  `timeline`, `workflows`, `sequences`, etc.


**Example:**

To embed the timeline view for a contact with ID 251 in Hub ID 12345:

```
https://app.hubspot.com/embed/12345/0-1/251/timeline
```

**Important:** Users must be logged into their HubSpot account to view the embedded content.  Unauthenticated users will be prompted to log in.


## Using the Embed Sandbox

HubSpot provides an embed sandbox to test and preview embedded views:

1. Navigate to the embed sandbox environment for your account.
2. Select the HubSpot account containing the data you want to embed.
3. Choose the `Object Type ID` and `Object ID` from the dropdown menus.
4. Preview the embedded view and interact with it.
5. Click "Copy" to copy the `Embed URL` to your clipboard.
6. Append the desired `view` parameter to the URL (e.g., `/sequences` to view sequences for a contact).


**Example from Sandbox:**

The sandbox might provide a base URL like:

```
https://app.hubspot.com/embed/12345/0-1/251
```

To view the sequences for this contact, append `/sequences`:

```
https://app.hubspot.com/embed/12345/0-1/251/sequences
```

## API (Not Explicitly Defined in Provided Text)

The provided text does not describe a formal API for interacting with the embed feature.  The embedding functionality relies solely on constructing and using the specific URL format described above.  There's no mention of API calls or methods for programmatic control beyond this URL construction.
