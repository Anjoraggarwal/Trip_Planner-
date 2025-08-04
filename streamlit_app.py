import streamlit as st
import requests

st.set_page_config(
    page_title="🌍 Travel Planner ",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Dark theme, moving waves, and visible input text color
st.markdown('''
<style>
.stApp {
    background: linear-gradient(135deg, #141E30 0%, #243B55 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #ddd;
}
.big-title {
    font-size: 42px;
    font-weight: 900;
    text-align: center;
    background: -webkit-linear-gradient(45deg, #5f87d0 0%, #105199 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
}
.stHeader {
    text-align: center;
    font-size: 20px;
    font-weight: 600;
    margin-top: 10px;
    margin-bottom: 20px;
    color: #5f87d0;
    letter-spacing: .5px;
}
#chat-container {
    min-height: 300px;
    margin-bottom: 40px;
}
.chat-bubble-user {
    background-color: #105199;
    color: white;
    border-radius: 22px 2px 22px 22px;
    padding: 15px 18px;
    margin: 16px 0 4px 80px;
    display: inline-block;
    max-width: 75%;
    font-size: 16px;
    box-shadow: 0 4px 10px rgba(16,81,153, 0.9);
    animation: fadeInLeft 0.8s ease forwards;
}
.chat-bubble-bot {
    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    color: #212121;
    border-radius: 2px 22px 22px 22px;
    padding: 15px 18px;
    margin: 2px 80px 16px 0;
    display: inline-block;
    max-width: 75%;
    font-size: 16px;
    box-shadow: 0 4px 12px rgba(250, 112, 154, 0.8);
    animation: fadeInRight 0.8s ease forwards;
}
@keyframes fadeInLeft {
  0% { opacity: 0; transform: translateX(-50px); }
  100% { opacity: 1; transform: translateX(0); }
}
@keyframes fadeInRight {
  0% { opacity: 0; transform: translateX(50px); }
  100% { opacity: 1; transform: translateX(0); }
}
.stTextInput > div > div > input {
    box-shadow: 0 1px 6px 1px #0f1930;
    border-radius: 10px;
    font-size: 16px;
    padding: 10px 15px;
    background: #f0f2f6 !important;
    color: #1a2332 !important;
    border: 1.5px solid #243B55 !important;
}
.stButton>button {
    background: linear-gradient(135deg, #105199 0%, #5f87d0 100%);
    color: #eee;
    font-weight: 700;
    padding: 10px 20px;
    border-radius: 15px;
    border: none;
    margin-top: 8px;
    cursor: pointer;
    transition: background 0.3s ease;
    font-size: 16px;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #5f87d0 0%, #105199 100%);
    color: #ffc;
}
/* Moving waves animation at bottom */
.waves {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100vw;
    height: 120px;
    pointer-events: none;
    background: url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/85486/wave.svg') repeat-x;
    background-size: 1600px 120px;
    animation: wave 9s linear infinite;
    opacity: 0.8;
    z-index: 0;
}
@keyframes wave {
    0% { background-position-x: 0; }
    100% { background-position-x: 1600px; }
}
</style>
''', unsafe_allow_html=True)

st.markdown(
    '<h1 class="big-title">🌍 Travel Planner </h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<h2 class="stHeader">Hello!! Where would you like to Travel?</h2>',
    unsafe_allow_html=True,
)

ss = st.session_state

if "messages" not in ss:
    ss["messages"] = []

with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input("User Input", placeholder="e.g. Plan a trip to Goa for 5 days")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input.strip():
    try:
        with st.spinner("Bot is thinking..."):
            BASE_URL = "http://localhost:8000"
            payload = {"question": user_input}
            response = requests.post(f"{BASE_URL}/query", json=payload)
        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            ss["messages"].append({"user": user_input, "bot": answer})
        else:
            st.error("Bot failed to respond: " + response.text)
    except Exception as e:
        st.error(f"The response failed due to {e}")

for msg in ss["messages"]:
    st.markdown(f'<div class="chat-bubble-user"><b>User:</b> {msg["user"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-bubble-bot"><b>Bot:</b> {msg["bot"]}</div>', unsafe_allow_html=True)

# Animated moving waves at the bottom
st.markdown("<div class='waves'></div>", unsafe_allow_html=True)
