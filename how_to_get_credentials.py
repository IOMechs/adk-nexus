import streamlit as st
import constants

def how_to_get_credentials():
    with st.expander(f"{constants.HELP_CENTER_ICON} How to get your credentials"):
        st.markdown(
            """
            To connect to your Vertex AI Agent, you need three pieces of information:
            1.  **Location**: The GCP region where your agent is deployed (e.g., `us-central1`).
            2.  **Resource ID**: The unique identifier for your agent.
            3.  **Service Account JSON**: A key file to authenticate with Google Cloud.

            ---

            #### 1. Finding your Location and Resource ID
            - Navigate to your agent in the [Vertex AI Agent Engine](https://console.cloud.google.com/vertex-ai/agents/agent-engines).
            - Select your agent.
            - Your **Location** and **Resource ID** can be found in your browser's URL. For example:
              `.../locations/us-central1/agent-engines/1234567891059626240`
              - **Location**: `us-central1`
              - **Resource ID**: `1234567891059626240`

            ---

            #### 2. Creating a Service Account and JSON Key
            You need to grant this application permission to access your agent.

            **Step 1: Go to the Service Accounts page**
            - Go to the [Service Accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts) in the Google Cloud Console.
            - Make sure you have selected the correct project.

            **Step 2: Create the Service Account**
            - Click **+ CREATE SERVICE ACCOUNT**.
            - Give it a name (e.g., `adk-chatbot-service-account`) and an optional description.
            - Click **CREATE AND CONTINUE**.

            **Step 3: Grant Permissions**
            - In the "Grant this service account access to project" section, click the **Role** dropdown.
            - Search for and select the **Vertex AI User** role.
            - Click **CONTINUE**, then **DONE**.

            **Step 4: Create and Download the JSON Key**
            - Find your new service account in the list.
            - Click the three-dot menu (⋮) on the right and select **Manage keys**.
            - Click **ADD KEY** → **Create new key**.
            - Select **JSON** as the key type and click **CREATE**.
            - A JSON file will be downloaded. **This is the file you need to upload below.**
            """
        )
