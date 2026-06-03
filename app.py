import streamlit as st
import os
from assistant import listen_command, speak, get_weather, get_news, set_reminder

# Page configuration
st.set_page_config(page_title="AI Voice Assistant", page_icon="🎙️", layout="centered")

# FORCE DEEP DARK GREEN THEME (Overriding Streamlit defaults)
st.markdown("""
    <style>
    /* Force main app canvas background */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0d1b15 !important;
    }
    
    /* Make all standard text readable and bright */
    .stMarkdown, p, span, label, div {
        color: #e0efe9 !important;
    }
    
    /* Custom Header Design */
    h1 {
        color: #52b788 !important;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        padding-bottom: 10px;
        text-shadow: 0 0 15px rgba(82, 183, 136, 0.3);
    }
    
    /* Input Labels */
    div[data-testid="stWidgetLabel"] p {
        color: #52b788 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }

    /* Text Input Boxes */
    input {
        background-color: #1b4332 !important;
        color: #e0efe9 !important;
        border: 1px solid #2d6a4f !important;
    }
    
    /* Custom Green Buttons */
    .stButton>button {
        background-color: #2d6a4f !important;
        color: white !important;
        border-radius: 8px !important;
        width: 100% !important;
        border: 1px solid #40916c !important;
        font-weight: 600 !important;
        padding: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background-color: #40916c !important;
        color: white !important;
        box-shadow: 0 0 15px rgba(82, 183, 136, 0.5) !important;
        border: 1px solid #52b788 !important;
    }
    
    /* Deep Green Output Panel Box */
    .response-box {
        background-color: #1b4332 !important;
        color: #e0efe9 !important;
        padding: 22px;
        border-radius: 10px;
        border-left: 6px solid #52b788;
        margin-top: 15px;
        font-size: 1.1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎙️ Voice Assistant Dashboard</h1>", unsafe_allow_html=True)
st.write("Interact with your smart assistant using voice commands or text inputs directly below.")

# Preserve states across actions
if "assistant_text" not in st.session_state:
    st.session_state.assistant_text = "Hello! How can I assist you today?"
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

# UI columns layout
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🎤 Trigger Voice Input"):
        st.write("Listening... Speak clearly into your mic.")
        user_speech = listen_command()
        if user_speech:
            st.info(f"Captured Speech: '{user_speech}'")
            
            if "weather" in user_speech:
                st.session_state.assistant_text = get_weather()
            elif "news" in user_speech:
                st.session_state.assistant_text = get_news()
            elif "reminder" in user_speech:
                st.session_state.assistant_text = set_reminder("Voice Task", 5)
            else:
                st.session_state.assistant_text = f"You said: '{user_speech}'. I am processing this request."
            
            st.session_state.audio_path = speak(st.session_state.assistant_text)
        else:
            st.error("Could not capture any speech. Please try again.")

with col2:
    text_input = st.text_input("Or Type a Command:", placeholder="e.g., weather in Hyderabad")
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

# Central Output Section
st.markdown("### Assistant Output")
st.markdown(f'<div class="response-box"><b>Response:</b> {st.session_state.assistant_text}</div>', unsafe_allow_html=True)

# Direct browser audio playback (Bypasses headless server crashes)
if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
    with open(st.session_state.audio_path, "rb") as f:
        audio_bytes = f.read()
    st.audio(audio_bytes, format="audio/mp3", autoplay=True)