import streamlit as st
import datetime
import os

# Import everything from our fixed assistant backend
from assistant import listen_command, speak, get_weather, get_news, set_reminder

# --- Theme Configuration & Custom CSS Injection ---
st.set_page_config(page_title="Home Assistant AI", page_icon="🎙️", layout="wide")

# Custom CSS styling matching your glassmorphism theme image
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1c2e24 0%, #2b4c3f 50%, #15221b 100%);
        color: #e0e0e0;
    }
    .ha-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    .ha-card h2, .ha-card h3 {
        color: #ffffff;
        font-weight: 600;
        margin-top: 0px;
    }
    .status-badge {
        background: rgba(255, 255, 255, 0.1);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85em;
        color: #a0c4b2;
    }
    /* Simple styling fix for Streamlit text boxes on dark backgrounds */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize background app states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "status" not in st.session_state:
    st.session_state.status = "Idle"

def process_voice(text_fallback=None):
    """Processes pipeline updates whether triggered by voice button or keyboard."""
    if text_fallback:
        query = text_fallback.lower()
    else:
        st.session_state.status = "Listening..."
        query = listen_command()
    
    if query == "hardware_missing":
        st.session_state.status = "Cloud Mode active. Please type your command below!"
        return
        
    if query == "none" or not query:
        st.session_state.status = "Idle"
        return

    st.session_state.status = f"Processing: '{query}'"
    response_text = ""

    # Process Action commands
    if "weather" in query:
        response_text = get_weather()
    elif "news" in query:
        response_text = get_news()
    elif "remind me to" in query or "reminder" in query:
        response_text = set_reminder(query)
    elif "time" in query:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        response_text = f"The current time is {time_now}."
    else:
        response_text = "I can help you with the weather, news, time, or reminders. What would you like to try?"

    # Attempt to speak back out loud (fails safely if running on cloud server logs)
    try:
        speak(response_text)
    except Exception:
        pass

    # Save to history logs
    st.session_state.chat_history.append({"user": query, "assistant": response_text})
    st.session_state.status = "Idle"

# --- LAYOUT DASHBOARD GRID ---
st.markdown("<h1 style='color: white; margin-bottom: 0px;'>Be Smart, Go Local!</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #8da399;'>Voice-Activated Home Dashboard</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.2, 1.5, 1])

with col1:
    # Card 1: Climate Panel
    st.markdown(
        f"""
        <div class="ha-card">
            <h3>🌤️ Climate Overview</h3>
            <p style='font-size: 2.2em; font-weight: bold; margin-bottom: 0px; color: white;'>19.4 °C</p>
            <p style='color: #8da399; margin-bottom: 15px;'>Partly Cloudy • Forecast Home</p>
            <span class="status-badge">Living Room Temperature: 23°C</span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Card 2: Voice Action Panel
    st.markdown('<div class="ha-card"><h3>🎙️ System Control</h3>', unsafe_allow_html=True)
    st.write(f"System State: `{st.session_state.status}`")
    
    if st.button("🎤 Activate Assistant Voice", use_container_width=True, type="primary"):
        process_voice()
        st.rerun()
        
    st.write("")
    user_text = st.text_input("⌨️ Cloud input (Type if no mic):", key="text_cmd")
    if user_text:
        process_voice(text_fallback=user_text)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Card 3: Interactive Feed Log
    st.markdown('<div class="ha-card" style="min-height: 360px;"><h3>💬 Voice Activity Feed</h3>', unsafe_allow_html=True)
    if not st.session_state.chat_history:
        st.markdown("<p style='color: #6a8276;'>No commands processed yet. Click the voice input microphone to communicate.</p>", unsafe_allow_html=True)
    else:
        for chat in reversed(st.session_state.chat_history):
            st.markdown(f"<p style='color: #a0c4b2; margin-bottom:2px;'><b>You:</b> {chat['user']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: white; margin-bottom:12px;'><b>Assistant:</b> {chat['assistant']}</p>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 8px 0; border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    # Card 4: Hardware Statistics
    st.markdown(
        """
        <div class="ha-card">
            <h3>⚡ Energy & Automation</h3>
            <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
                <span>Solar Pump</span><b style='color: #4caf50;'>66 W</b>
            </div>
            <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
                <span>Home Power Grid</span><b style='color: #ff9800;'>209 W</b>
            </div>
            <div style='display: flex; justify-content: space-between;'>
                <span>Boiler Temp</span><b style='color: #2196f3;'>25.5 °C</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Card 5: Live Database Reminders
    st.markdown('<div class="ha-card"><h3>📌 Live Reminders</h3>', unsafe_allow_html=True)
    if os.path.exists("reminders.txt"):
        with open("reminders.txt", "r") as f:
            reminders = f.readlines()
        if reminders:
            for r in reminders[-4:]:  
                st.markdown(f"• <span style='color: #cbdad2; font-size: 0.9em;'>{r.strip()}</span>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #6a8276;'>No reminders found.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: #6a8276;'>No reminders logged yet.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)