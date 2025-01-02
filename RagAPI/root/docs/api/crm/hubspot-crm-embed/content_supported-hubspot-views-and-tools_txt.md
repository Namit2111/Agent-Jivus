# HubSpot CRM Embed Documentation

This document describes the HubSpot CRM Embed feature, allowing you to display interactive HubSpot interfaces within your application.  It details supported views, URL structure for embedding, and using the embed sandbox for testing.

## Supported HubSpot Views and Tools

The following tools can be embedded:

* **Object Timeline:** Displays activities related to a record (meetings, tasks), including an interactive sidebar with activity filters and association cards (contacts, companies, deals, etc.).
* **Workflows Tab:** Tracks workflow enrollment history, allows enrollment of records, and searches workflows by name.
* **Sequences Tab:** (Contact records only) Manages sequences, enrolls contacts, and tracks sequence progress.
* **Properties Tab:** Searches and filters properties, views property history, and hides blank fields.
* **Meetings Tab:** Schedules meetings and manages/reviews upcoming meetings.
* **Company & Deal Functionality:** (Company and Deal records only) Includes a "Target Accounts" tab with metrics like emails sent and meetings scheduled.


## Embedding a Specific View

To embed a specific view, construct a URL using this structure:

```
https://app.hubspot.com/embed/{hubId}/{objectType}/{recordId}/{view}
```

* **`hubId`:** Your HubSpot account's Hub ID.
* **`objectType`:** The object type (e.g., `contacts`, `companies`, `deals`).  Note that `0-1` is used in the example for contacts.  The specific numerical portion will vary depending on your HubSpot setup.
* **`recordId`:** The ID of the specific record.
* **`view`:** The view to embed (e.g., `timeline`, `workflows`, `sequences`).

**Example:**

To embed the timeline for a contact with ID `251` in Hub ID `12345`:

```
https://app.hubspot.com/embed/12345/0-1/251/timeline
```

**Important:**  The user must be logged into their HubSpot account to view the embedded content.  Unauthenticated users will be prompted to log in.


## Using the Embed Sandbox

HubSpot provides a sandbox environment to test embedded views:

1. Navigate to the embed sandbox environment for your account.  (Link not provided in source text).
2. Select the HubSpot account containing the data you want to embed.
3. Choose the `ObjectType ID` and `ObjectID` from the dropdown menus.
4. Preview the embedded view.  Interact with the timeline and tabs.
5. Click "Copy" to copy the embed URL.  Remember to append the `view` parameter to the copied URL to ensure correct loading (e.g., add `/sequences` to view sequences for a contact).


## API & Call Examples

The provided text focuses on embedding existing views; it does not directly describe an API for programmatic interaction with the embedded views. There is no API call example included in the source text.  Further documentation would be required to understand any underlying APIs used to implement the embed functionality.
