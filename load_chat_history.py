import streamlit as st
import constants

def get_message_role(event: dict) -> str:
    """
    Determines the role of a chat message.
    """
    role = event["content"]["role"]
    _parts = event["content"]["parts"]
    # if functionResponse, the role is "user" that is coming from the Agent Engine (seems like a bug)
    if role == "model" or _parts[0].get("functionResponse"):
        return "ai"
    return role

def load_chat_history(events: list[dict], show_function_calls: bool) -> None:
    """
    Load chat history from the current session and display it in the Streamlit app.
    Args:
        events (list[dict]): The list of chat events to display.
    """
    for event in events:
        _parts = event["content"]["parts"]

        if not show_function_calls and (_parts[0].get("functionCall") or _parts[0].get("functionResponse")):
            continue

        parts: list[dict] = []

        role = get_message_role(event)

        with st.chat_message(role):
            for _part in _parts:
                part = {}
                if _part.get("text"):
                    part["text"] = _part["text"]
                    st.markdown(part["text"])
                elif _part.get("functionCall"):
                    part["function_call"] = _part["functionCall"]
                    st.badge(
                        label=part["function_call"]["name"],
                        color="gray",
                        icon=constants.FUNCTION_CALL_ICON
                    )
                elif _part.get("functionResponse"):
                    part["function_response"] = _part["functionResponse"]
                    st.badge(
                        label=part["function_response"]["name"],
                        color="green",
                        icon=constants.FUNCTION_RESPONSE_ICON
                    )
                parts.append(part)

        st.session_state.messages.append({
            "role": event["content"]["role"],
            "parts": parts,
        })