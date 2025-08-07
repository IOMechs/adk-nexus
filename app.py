import streamlit as st, os, constants
import vertexai
from vertexai import agent_engines # type: ignore
from load_chat_history import load_chat_history
from sidebar import populate_sessions_in_sidebar
from how_to_get_credentials import how_to_get_credentials
from utils import load_custom_css
from uuid import uuid4
from streamlit_local_storage import LocalStorage # type: ignore
from google.oauth2 import service_account
import json

# Browser's local storage
localS = LocalStorage()

def main():
	# Set title on browser tab
	st.set_page_config(
		page_title=os.getenv("CHATBOT_NAME", constants.DEFAULT_CHATBOT_NAME),
	)

	st.html(load_custom_css())

	# Get GCP credentials from Streamlit secrets or local storage
	# If not found, prompt the user to enter it
	credentials_source = "environment"
	service_account_info = None
	location = None
	resource_id = None

	try:
		# Try to get from Streamlit secrets first
		service_account_info = st.secrets["gcp_service_account"]
		location = st.secrets["LOCATION"]
		resource_id = st.secrets["RESOURCE_ID"]

		if not location or not resource_id or len(service_account_info) == 0:
			raise KeyError()
	except (KeyError):
		# Fall back to local storage
		gcp_credentials_str = localS.getItem("gcp_credentials")
		if gcp_credentials_str:
			try:
				gcp_credentials = json.loads(gcp_credentials_str)
				service_account_info = gcp_credentials.get("service_account_info")
				location = gcp_credentials.get("location")
				resource_id = gcp_credentials.get("resource_id")
				credentials_source = "local_storage"
			except json.JSONDecodeError as error:
				gcp_credentials_dialog(f"Invalid credentials data: {error}")

	if not service_account_info or not location or not resource_id:
		gcp_credentials_dialog()

	# Initialize Vertex AI with service account credentials
	try:
		credentials = service_account.Credentials.from_service_account_info(service_account_info)
	except Exception as e:
		gcp_credentials_dialog(f"Invalid service account credentials: {e}")

	vertexai.init(
		credentials=credentials,
		project=service_account_info["project_id"],
		location=location,
	)

	try:
		engine = agent_engines.get(resource_id)
	except Exception as e:
		gcp_credentials_dialog(e)

	user_id = localS.getItem("user_id")
	if not user_id:
		user_id = str(uuid4())
		localS.setItem("user_id", user_id)

	user_sessions = get_user_sessions(engine, user_id)
	current_session = None

	if len(user_sessions):
		# Sort by lastUpdateTime desc
		user_sessions.sort(key=lambda x: x['lastUpdateTime'], reverse=True)
		# if query parameter session_id is provided, load that session messages
		if st.query_params.get("session_id"):
			session_id = st.query_params["session_id"]
			current_session = engine.get_session(user_id=user_id, session_id=session_id)
			if current_session:
				# find current session in user_sessions list and add "is_current" flag
				for session in user_sessions:
					if session["id"] == current_session["id"]:
						session["is_current"] = True
			else:
				del st.query_params["session_id"]

	# Sidebar logic
	st.sidebar.header(f"_***{os.getenv('CHATBOT_NAME', constants.DEFAULT_CHATBOT_NAME)}***_", divider="rainbow")

	if credentials_source == "local_storage":
		st.sidebar.button(
			f"{constants.ROBOT_ICON} Change Credentials",
			key="change_resource_id_btn",
			help="Change the GCP credentials",
			on_click=gcp_credentials_dialog
		)

	show_tool_calls = st.sidebar.toggle(
		"Show Function Calls",
		value=False,
		key="function_calling_toggle",
		help="Enable to see function calls and response events in the chat messages. "
	)
	st.sidebar.subheader("User Sessions")
	if st.sidebar.button(f"{constants.PLUS_ICON} New Chat", key="new_session_btn"):
		# Trigger new session creation via query params
		if st.query_params.get("session_id"):
			del st.query_params["session_id"]
		st.rerun()

	sessions_container = st.sidebar.empty()  # single-item container to hold sessions list
	populate_sessions_in_sidebar(
		sessions_container,
		user_sessions
	)

	# Main chat area
	col1, col2 = st.columns([0.9, 0.1], gap="small", vertical_alignment="center")
	with col1:
		session_title = "New Chat"
		if current_session:
			session_title = f"Session ID: {current_session['id']}"
		st.subheader(session_title, anchor=False)

	if current_session:
		with col2:
			if st.button("🗑️", key="delete_session_button", help="Delete this chat"):
				engine.delete_session(
					user_id=user_id,
					session_id=current_session['id'],
				)
				if st.query_params.get("session_id"):
					del st.query_params["session_id"]
				get_user_sessions.clear()  # Clear the cache
				st.rerun()


	# Initialize chat history
	if "messages" not in st.session_state:
		st.session_state.messages = []

	# Display and save chat history
	if current_session:
		load_chat_history(current_session["events"], show_tool_calls)

	# React to user input
	if prompt := st.chat_input("Say something"):
		# Display user message in chat message container
		with st.chat_message("user"):
			st.markdown(prompt)

		# create new session if not exists
		if not current_session:
			current_session = engine.create_session(
				user_id=user_id,
			)
			current_session["is_new"] = True
			current_session["is_current"] = True
			st.query_params["session_id"] = current_session['id']
			get_user_sessions.clear() # Clear the cache
			user_sessions.insert(0, current_session) # Add new session to the list
			populate_sessions_in_sidebar(
				sessions_container,
				user_sessions,
			)

		# Add user message to chat history
		st.session_state.messages.append({"role": "user", "parts": [{"text": prompt}]})

		for event in engine.stream_query(
			user_id=user_id,
			session_id=current_session['id'],
			message=prompt
		):
			_parts = event["content"]["parts"]

			if show_tool_calls == False and ("function_call" in _parts[0] or "function_response" in _parts[0]):
				continue

			parts: list[dict] = []
			# Display agent response in chat message container
			with st.chat_message("ai"):
				for _part in _parts:
					part = {}
					if "text" in _part:
						part["text"] = _part["text"]
						st.markdown(part["text"])
					elif "function_call" in _part:
						part["function_call"] = _part["function_call"]
						st.badge(label=part["function_call"]["name"], color="grey", icon=constants.FUNCTION_CALL_ICON)
					elif "function_response" in _part:
						part["function_response"] = _part["function_response"]
						st.badge(label=part["function_response"]["name"], color="green", icon=constants.FUNCTION_RESPONSE_ICON)
					parts.append(part)

			# Add assistant response to chat history
			st.session_state.messages.append({"role": "model", "parts": parts})


@st.cache_data(show_spinner=False)
def get_user_sessions(_engine: agent_engines.AgentEngine, user_id: str) -> list:
	"""
	Get user sessions from the agent engine.
	
	Args:
		_engine: The agent engine instance (underscore indicates that this argument won't be cached by Streamlit)
		user_id: The user ID to fetch sessions for

	Returns:
		List of user sessions
	"""
	return _engine.list_sessions(user_id=user_id)['sessions']

@st.dialog("Enter your Agent's GCP credentials", width="large")
def gcp_credentials_dialog(error=None):
	how_to_get_credentials()
	if error:
		st.error(f"Error retrieving agent engine: {error}")

	# Try to get existing credentials from local storage
	existing_credentials = {}
	gcp_credentials_str = localS.getItem("gcp_credentials")
	if gcp_credentials_str:
		try:
			existing_credentials = json.loads(gcp_credentials_str)
		except json.JSONDecodeError:
			pass

	with st.form("agent_engine_resource_form"):
		location = st.text_input(
			label="Location",
			value=os.getenv("LOCATION") or existing_credentials.get("location", "us-central1"),
			placeholder="us-central1"
		)

		resource_id = st.text_input(
			label="Resource ID",
			value=existing_credentials.get("resource_id", ""),
		)

		service_account_json = st.file_uploader(
			label="Upload service account JSON file",
			type=["json"],
			help="""
				Upload your GCP service account JSON file to authenticate with Vertex AI.
				The contents of this file will only be stored in your browser's local storage.
			""",
			key="service_account_uploader",
		)

		submitted = st.form_submit_button("Submit")


		if submitted:
			if not resource_id:
				st.error("Resource ID is required.")
				return

			if not location:
				st.error("Location is required.")
				return

			if service_account_json is None:
				st.error("Service account JSON file is required.")
				return

			# Parse the service account JSON
			try:
				service_account_info = json.loads(service_account_json.read().decode('utf-8'))
			except json.JSONDecodeError as e:
				st.error(f"Invalid JSON file: {e}")
				return

			# Build credentials dictionary
			gcp_credentials = {
				"location": location,
				"resource_id": resource_id,
				"service_account_info": service_account_info
			}

			# Store as single JSON string in local storage
			localS.setItem("gcp_credentials", json.dumps(gcp_credentials), key="set_gcp_credentials")

			import time
			time.sleep(0.2)

			st.success("GCP credentials saved successfully!")

			if st.query_params.get("session_id"):
				del st.query_params["session_id"]
			st.rerun()
		else:
			st.stop()

if __name__ == "__main__":
	main()
