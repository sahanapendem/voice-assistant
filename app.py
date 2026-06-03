import streamlit as st
import os
from assistant import listen_command, speak, get_weather, get_news, set_reminder

# Page Layout configuration
st.set_page_config(page_title="AI Voice Assistant", page_icon="🎙️", layout="centered")

# Custom Dark Green Dashboard Styling
st.markdown("""
    <style>
    .main { background-color: #0d1b15; color: #e0efe9; }
    h1 { color: #52b788; text-align: center; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #2d6a4f; color: white; border-radius: 8px; width: 100%; border: none;}
    .stButton>button:hover { background-color: #40916c; border: none; color: white;}
    .response-box { background-color: #1b4332; padding: 20px; border-radius: 10px; border-left: 5px solid #52b788; margin-top: 20px;}
    </style>
""", unsafe_allow_html=True)

st.title("🎙️ Voice Assistant Dashboard")
st.write("Interact with your smart assistant using voice commands or text inputs directly below.")

# Persistent Interface Session states
if "assistant_text" not in st.session_state:
    st.session_state.assistant_text = "Hello! How can I assist you today?"
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🎤 Trigger Voice Input"):
        st.write("Listening... Speak into your microphone.")
        user_speech = listen_command()
        if user_speech:
            st.info(f"Captured Speech: '{user_speech}'")
            
            # Text Processing Routing
            if "weather" in user_speech:
                st.session_state.assistant_text = get_weather()
            elif "news" in user_speech:
                st.session_state.assistant_text = get_news()
            elif "reminder" in user_speech:
                st.session_state.assistant_text = set_reminder("Voice Task", 5)
            else:
                st.session_state.assistant_text = f"You said: {user_speech}. I am processing this task."
            
            # Generate Audio
            st.session_state.audio_path = speak(st.session_state.assistant_text)
        else:
            st.error("Could not capture any clear speech. Please try again.")

with col2:
    text_input = st.text_input("Or Type a Command:", placeholder="e.g., weather in New York")
    if st.button("Submit Text"):
        if text_input:
            cmd = text_input.lower()
            if "weather" in cmd:
                st.session_state.assistant_text = get_weather()
            elif "news" in cmd:
                st.session_state.assistant_text = get_news()
            elif "reminder" in cmd:
                st.session_state.assistant_text = set_reminder("Text Task", 10)
            else:
                st.session_state.assistant_text = f"Processing text input query for: '{text_input}'"
            
            st.session_state.audio_path = speak(st.session_state.assistant_text)

# Centralized Response & Audio Playback Output
st.markdown("### Assistant Output")
st.markdown(f'<div class="response-box"><b>Response:</b> {st.session_state.assistant_text}</div>', unsafe_allow_html=True)

if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
    with open(st.session_state.audio_path, "rb") as f:
        audio_bytes = f.read()
    st.audio(audio_bytes, format="audio/mp3", autoplay=True)