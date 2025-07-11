import streamlit as st
from utils import time_ago_from_epoch
import constants

def populate_sessions_in_sidebar(sidebar_container, user_sessions: list) -> None:
	with sidebar_container.container():
		# List existing sessions
		for session in user_sessions:
			#:grey[Last Updated: {time_ago_from_epoch(session['lastUpdateTime'])}]
			url = f"?session_id={session['id']}"
			new_icon, is_current = "", ""
			if session.get("is_new", False):
				new_icon = constants.NEW_ICON
			if session.get("is_current", False):
				is_current = "id='current_session'"
			st.html(
				f"<div>"
				f"	<a href='{url}' target='_parent' class='session-item' {is_current}>"
				f"		<span>Session ID: {session['id']} {new_icon}</span>"
				f"		<br><sup>Last Updated: {time_ago_from_epoch(session['lastUpdateTime'])}</sup>"
				f"	</a>"
				f"</div>"
			)


