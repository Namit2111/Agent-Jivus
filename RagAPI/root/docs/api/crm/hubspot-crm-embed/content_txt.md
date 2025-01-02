# HubSpot CRM Embed Documentation

This document describes the HubSpot CRM Embed feature, allowing you to integrate interactive HubSpot interfaces within your application.  It details supported views, URL construction, and using the embed sandbox for testing.

## Supported Views and Tools

The CRM Embed feature supports embedding the following views and tools:

* **Object Timeline:** Displays activities, upcoming meetings, tasks, and association cards (related contacts, companies, deals, etc.) for a given object record. Includes an interactive sidebar and activity filters.
* **Workflows Tab:**  Tracks workflow enrollment history, allows enrolling records into workflows, and searching workflows by name.
* **Sequences Tab:** (Contact records only) Manages sequences, enrolls contacts, and tracks sequence progress.
* **Properties Tab:** Searches, filters, and displays property history. Allows hiding unused blank fields.
* **Meetings Tab:** Schedules meetings and manages/reviews upcoming meeting details.
* **Target Accounts Tab:** (Company & Deal records only) Displays metrics like emails sent and meetings scheduled, along with other aggregate metrics.


## Embedding URLs

To embed a specific HubSpot view, construct a URL using the following format:

```
https://app.hubspot.com/embed/{hubId}/{objectType}/{recordId}/{view}
```

Where:

* `hubId`: Your HubSpot account's Hub ID.
* `objectType`: The object type (e.g., `contacts`, `companies`, `deals`).  Note that the example uses `0-1` for contacts; this might vary slightly depending on your HubSpot setup.  Consult your HubSpot account for the correct object type code.
* `recordId`: The ID of the specific object record.
* `view`: The desired view: `timeline`, `workflows`, `sequences` (contacts only).

**Example:**

To embed the timeline view for a contact with `recordId` 251 in a HubSpot account with `hubId` 12345:

```
https://app.hubspot.com/embed/12345/0-1/251/timeline
```

**Important:** Users must be logged into their HubSpot account to view the embedded content.  Unauthenticated users will be prompted to log in.


## Using the Embed Sandbox

HubSpot provides a sandbox environment to test different views before embedding them in your application:

1. Navigate to the embed sandbox environment for your account.
2. Select the HubSpot account containing the data you want to embed.
3. Choose the `ObjectType` and `ObjectId` from the dropdown menus.
4. Preview the embedded view, interacting with the timeline and tabs.
5. Click "Copy" to copy the generated `Embed URL` to your clipboard.
6. Append the appropriate `view` parameter to the copied URL (if needed) to direct to a specific view within the embedded context (e.g., adding `/sequences` to view sequences for a contact).


## API Considerations (Not Explicitly Defined in Provided Text)

While the provided text focuses on embedding pre-built views,  interacting with the underlying HubSpot data would likely require using the HubSpot CRM API.  This API allows for programmatic access to create, read, update, and delete HubSpot objects and their properties.  The specific API calls would depend on the functionality you wish to integrate beyond simply embedding existing views.  Further investigation of the HubSpot CRM API documentation is recommended for advanced integration scenarios.
