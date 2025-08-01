import streamlit as st
import requests
import datetime

BASE_URL = "http://localhost:8000"  # Backend endpoint

st.set_page_config(
    page_title="🌍 Travel Planner Agentic Application",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("🌍 Travel Planner Agentic Application")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
st.header("How can I help you in planning a trip? Let me know where do you want to visit.")

# Chat input box at bottom
with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input("User Input", placeholder="e.g. Plan a trip to Goa for 5 days")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input.strip():
    try:
        with st.spinner("Bot is thinking..."):
            payload = {"question": user_input}
            response = requests.post(f"{BASE_URL}/query", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            # Append to chat history
            st.session_state.messages.append({"user": user_input, "bot": answer})
        else:
            st.error(" Bot failed to respond: " + response.text)
    except Exception as e:
        st.error(f"The response failed due to {e}")

# Display conversation history
for msg in st.session_state.messages:
    st.markdown(f"**User:** {msg['user']}")
    st.markdown(f"**Bot:** {msg['bot']}")
