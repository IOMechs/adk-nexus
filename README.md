
# ADK Chatbot for Vertex AI

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.47.0-red.svg)](https://www.streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![ADK Nexus Demo](./public/ADK-Nexus-Demo.gif)

A turnkey, open-source Streamlit chatbot interface designed for seamless integration with agents deployed on Google Cloud's Vertex AI Agent Engine. This project empowers developers to effortlessly connect their custom agents, deploy them, and share them with the world.

## ✨ Features

*   **Rapid Deployment:** Go from a deployed Vertex AI agent to a shareable web application in minutes.
*   **Streamlit Powered:** Built on the popular and easy-to-use Streamlit framework for a smooth user experience.
*   **Customizable:** Easily extend and customize the chatbot's appearance and functionality.
*   **Secure Authentication:** Straightforward setup for Google Cloud authentication using service accounts.
*   **Cloud Agnostic Deployment:** Deploy with ease to Streamlit Cloud or any other preferred platform.

## ⚡ Instantly Test Your Agent
To see how your agent performs right now, use our hosted version here: [adk-nexus.dev.iomechs.com](http://adk-nexus.dev.iomechs.com). A modal will prompt for your agent's credentials.

## ▶️ Video Tutorial
[![Watch the video](https://img.youtube.com/vi/y7damsm8Qos/maxresdefault.jpg)](https://youtu.be/y7damsm8Qos)


## 🚀 Getting Started

Follow these instructions to get a local copy of the chatbot up and running.

### Prerequisites

*   Python 3.9 or higher
*   A deployed agent on [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/docs/agent-engine/overview)

### 1. Set up your environment variables

To configure your application, you'll need to create a `secrets.toml` file within a `.streamlit` directory.

First, copy the example secrets file:

```bash
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
```

Next, open `.streamlit/secrets.toml` and populate it with your specific Google Cloud and agent information:

```toml
# .streamlit/secrets.toml

# --- Required Configuration ---
RESOURCE_ID = "your-agent-engine-resource-id"
LOCATION = "your-gcp-region"

# --- Optional Configuration ---
CHATBOT_NAME = "your-chatbot-name" # Defaults to "ADK Chatbot"
```

### 2. Configure Google Cloud authentication

To securely connect to your Vertex AI agent, you need to create a Google Cloud service account.

1.  **Navigate to Service Accounts:** In the Google Cloud Console, go to **IAM & Admin → Service Accounts** for your project.
2.  **Create Service Account:** Click on **+ CREATE SERVICE ACCOUNT**.
3.  **Details:** Give your service account a descriptive name (e.g., "ADK Chatbot Service Account").
4.  **Permissions:** Grant the "Vertex AI User" role to this service account.
5.  **Create Key:**
    *   Find your newly created service account in the list.
    *   Click the three-dot menu on the right and select **Manage keys**.
    *   Click on **ADD KEY** → **Create new key**.
    *   Choose **JSON** as the key type and click **Create**. A JSON key file will be downloaded to your computer.
6.  **Convert and Add to Secrets:**
    *   Open the downloaded JSON file.
    *   You will need to convert the content of this JSON file into a TOML-compatible format for Streamlit. You can use an online converter for this.
    *   Paste the resulting TOML content into your `.streamlit/secrets.toml` file under the `[gcp_service_account]` section, ensuring there are no line breaks in the private key.

Your completed `secrets.toml` should look like this:

```toml
# .streamlit/secrets.toml

RESOURCE_ID = "your-agent-engine-resource-id"
LOCATION = "your-gcp-region"
CHATBOT_NAME = "your-chatbot-name" # Optional, defaults to "ADK Chatbot"

[gcp_service_account]
type = "service_account"
project_id = "xxx"
private_key_id = "xxx"
...
```

## 💻 Running the App Locally

### Activate virtual environment

It is recommended to use a virtual environment to manage project dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

Your chatbot should now be running locally!

## ☁️ Deploy to Streamlit Cloud

1.  **Push to GitHub:** Ensure your code, including the `requirements.txt` file, is pushed to a GitHub repository.
2.  **New App on Streamlit Cloud:** Go to [Streamlit Cloud](https://streamlit.io/cloud) and click on **New app**.
3.  **Connect Your Repo:** Select your GitHub repository and the correct branch.
4.  **Configure App:** Set the "Main file path" to `app.py`.
5.  **Add Secrets:** In the "Advanced settings," copy the entire content of your local `secrets.toml` file and paste it into the "Secrets" section.
6.  **Deploy:** Click **Deploy**. Streamlit Cloud will handle the rest, and your chatbot will be live at a shareable URL.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 🏢 About IOMechs

This open-source project is proudly maintained by IOMechs. We specialize in creating intelligent automation and AI-powered solutions to drive business efficiency and innovation.

For inquiries about AI Automation or custom AI-Powered Solutions, please reach out to us at [info@iomechs.com](mailto:info@iomechs.com).

## 📄 License

MIT License

Copyright © 2025 [IOMechs](https://iomechs.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.