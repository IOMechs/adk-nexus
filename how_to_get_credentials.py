import streamlit as st
import constants

def how_to_get_credentials():
    with st.expander(f"{constants.HELP_CENTER_ICON} How to get your credentials"):
        st.markdown(
            """
### Connecting to Your Vertex AI Agent

To connect to your Vertex AI Agent, you will need to find three key pieces of information:

*   **Location**: This is the specific Google Cloud region where your agent is located (for example, `us-central1`).
*   **Resource ID**: This is the unique ID number assigned to your agent.
*   **Service Account JSON**: This is a key file that allows the application to securely connect to your agent.

---

### **Part 1: Find Your Agent's Location and Resource ID**

1.  Open the **[Vertex AI Agent Engine](https://console.cloud.google.com/vertex-ai/agents/agent-engines)** in your web browser.
2.  Click on the name of your agent.
3.  Look at the URL in your browser's address bar. It will look something like this:
    `.../locations/us-central1/agent-engines/1234567891059626240`
    *   The **Location** is the part after `locations/` (e.g., `us-central1`).
    *   The **Resource ID** is the long number at the end (e.g., `1234567891059626240`).

---

### **Part 2: Get Your Service Account JSON Key**

You need to give the application permission to use your agent. You'll do this by creating a special account called a "Service Account" and downloading a key file.

**Step 1: Go to the Service Accounts Page**

*   Go to the **[Service Accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts)**.
*   Make sure the correct Google Cloud project is selected.

**Step 2: Create the New Service Account**

*   Click the **+ CREATE SERVICE ACCOUNT** button.
*   Enter a name for the account (like `my-chatbot-key`).
*   Click **CREATE AND CONTINUE**.

**Step 3: Give it the Right Permission**

*   Find the "Role" dropdown menu.
*   Type **Vertex AI User** in the search box and select it.
*   Click **CONTINUE**, and then click **DONE**.

**Step 4: Download the JSON Key File**

*   You will see your new service account in the list.
*   Click the three dots (⋮) on the right side of it and choose **Manage keys**.
*   Click **ADD KEY** and then select **Create new key**.
*   Choose **JSON** and click **CREATE**.
*   A JSON file will be downloaded to your computer. This is the file you need.
            """
        )
