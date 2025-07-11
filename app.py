import streamlit as st, os, constants
from vertexai import agent_engines # type: ignore
from load_chat_history import load_chat_history
from sidebar import populate_sessions_in_sidebar
from utils import load_custom_css
from dotenv import load_dotenv
from uuid import uuid4
from streamlit_local_storage import LocalStorage # type: ignore

# Browser's local storage
localS = LocalStorage()

# Load environment variables
load_dotenv()

def main():
	# Set title on browser tab
	st.set_page_config(
		page_title=os.getenv("CHATBOT_NAME", constants.DEFAULT_CHATBOT_NAME),
	)

	st.html(load_custom_css())

	resource_id_is_from_local_storage = False
	resource_id = os.getenv("AGENT_ENGINE_RESOURCE_ID")
	if not resource_id:
		resource_id = localS.getItem("agent_engine_resource_id")
		resource_id_is_from_local_storage = True

	if not resource_id:
		agent_engine_resource_id_dialog()

	try:
		engine = agent_engines.get(resource_id)
	except Exception as e:
		agent_engine_resource_id_dialog(e)

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

	if resource_id_is_from_local_storage:
		if st.sidebar.button(
			f"{constants.ROBOT_ICON} Change Resource ID",
			key="change_resource_id_btn",
			help="Change the Agent Engine resource ID"
		):
			agent_engine_resource_id_dialog()

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

@st.dialog("Enter your Agent Engine's resource ID")
def agent_engine_resource_id_dialog(error=None):
	if error:
		st.error(f"Error retrieving agent engine: {error}")

	resource_id = st.text_input(
		label="Resource ID",
		value=localS.getItem("agent_engine_resource_id")
	)
	
	if st.button("Retrieve"):
		localS.setItem("agent_engine_resource_id", resource_id)
		st.success("Resource ID saved!")
		st.rerun()
	else:
		st.stop()

if __name__ == "__main__":
	main()
