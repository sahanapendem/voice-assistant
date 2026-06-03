import streamlit as st
import os
from assistant import listen_command, speak, get_weather, get_news, set_reminder, get_time

# Set configuration to wide mode to emulate landing page dashboard Layout
st.set_page_config(page_title="VOICE ASSES | AI Assistant", page_icon="🟢", layout="wide")

# PREMIUM SAAS GRADIENT & GLASSMORPHISM VISUAL INTERFACE THEME
st.markdown("""
    <style>
    /* 1. Global Reset & Futuristic Background (Aurora Glows) */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0b1210 !important;
        background-image: 
            radial-gradient(circle at 80% 20%, rgba(45, 106, 79, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 15% 80%, rgba(82, 183, 136, 0.12) 0%, transparent 45%) !important;
        background-attachment: fixed !important;
        font-family: 'Inter', 'Helvetica Neue', sans-serif !important;
    }
    
    /* Hide default Streamlit visual elements */
    [data-testid="stDecoration"], #MainMenu, footer {visibility: hidden;}

    /* 2. Custom Navbar Header Row Layout */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 2%;
        margin-bottom: 40px;
    }
    .brand-logo {
        font-size: 1.6rem;
        font-weight: 800;
        color: #e0efe9;
        letter-spacing: 1px;
    }
    .brand-logo span {
        color: #52b788;
    }

    /* 3. Hero Section Typography Styling */
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        line-height: 1.1 !important;
        margin-bottom: 10px !important;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        font-size: 1.1rem !important;
        color: #94a3b8 !important;
        max-width: 500px;
        line-height: 1.6;
        margin-bottom: 30px;
    }

    /* 4. Premium Glassmorphic Layout Components */
    .glass-card {
        background: rgba(17, 27, 24, 0.65) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(82, 183, 136, 0.15) !important;
        border-radius: 18px !important;
        padding: 25px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 20px;
    }
    
    /* Glowing Highlights for Main State Status Trackers */
    .glow-card {
        border: 1px solid rgba(82, 183, 136, 0.3) !important;
        background: linear-gradient(135deg, rgba(27, 67, 50, 0.4) 0%, rgba(13, 27, 21, 0.7) 100%) !important;
    }

    /* 5. Custom Form Labels and Dark Text Inputs */
    div[data-testid="stWidgetLabel"] p {
        color: #94a3b8 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        margin-bottom: 8px !important;
    }
    input {
        background-color: rgba(13, 27, 21, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(82, 183, 136, 0.25) !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }
    input:focus {
        border-color: #52b788 !important;
        box-shadow: 0 0 10px rgba(82, 183, 136, 0.2) !important;
    }

    /* 6. High-End SaaS Control Action Buttons Configuration */
    .stButton>button {
        background: linear-gradient(90deg, #2d6a4f 0%, #1b4332 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(82, 183, 136, 0.4) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 14px 28px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(45, 106, 79, 0.2) !important;
    }
    .stButton>button:hover {
        background: #52b788 !important;
        color: #0b1210 !important;
        border-color: #52b788 !important;
        box-shadow: 0 0 25px rgba(82, 183, 136, 0.6) !important;
        transform: translateY(-2px);
    }

    /* Target error and informational alert typography systems */
    .stAlert p {
        color: #0d1b15 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ─── NAVIGATION ROW HEADER ───
st.markdown("""
    <div class="nav-container">
        <div class="brand-logo">VOICE <span>ASSES</span></div>
        <div style="color: #94a3b8; font-size: 0.9rem; font-weight: 500;">
            Home &nbsp;&nbsp;&nbsp;&nbsp; Features &nbsp;&nbsp;&nbsp;&nbsp; Core &nbsp;&nbsp;&nbsp;&nbsp; Pricing
        </div>
    </div>
""", unsafe_allow_html=True)

# Application Stateful Caches
if "assistant_text" not in st.session_state:
    st.session_state.assistant_text = "Hi, I'm your personal artificial assistant. What would you like to ask or capture today?"
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

# ─── MAIN LANDING HERO & DASHBOARD SPLIT GRID LAYOUT ───
left_col, right_col = st.columns([1.1, 0.9], gap="large")

with left_col:
    st.markdown('<p class="hero-title">The Future of<br>Artificial Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Empowering the next generation of intelligent systems with seamless voice capture, real-time query tracking, and contextual automation feedback layouts.</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### 🎛️ System Automation Console")
    
    control_tab1, control_tab2 = st.tabs(["Voice Interface Control", "Keyboard Command String"])
    
    with control_tab1:
        st.write("")
        if st.button("🎤 Initialize Voice Stream Capture"):
            with st.spinner("Establishing secure voice node link..."):
                user_speech = listen_command()
                if user_speech:
                    st.success(f"Successfully Transcribed: \"{user_speech}\"")
                    
                    if "time" in user_speech:
                        st.session_state.assistant_text = get_time()
                    elif "weather" in user_speech or "temperature" in user_speech:
                        words = user_speech.split()
                        if "in" in words:
                            idx = words.index("in") + 1
                            st.session_state.assistant_text = get_weather(" ".join(words[idx:]))
                        else:
                            st.session_state.assistant_text = get_weather()
                    elif "news" in user_speech:
                        st.session_state.assistant_text = get_news()
                    elif "remind" in user_speech or "remain" in user_speech:
                        st.session_state.assistant_text = set_reminder("Voice Command Workflow", 5)
                    else:
                        st.session_state.assistant_text = f"Successfully parsed query: '{user_speech}'."
                    
                    st.session_state.audio_path = speak(st.session_state.assistant_text)
                else:
                    st.error("Connection timed out. No clear audio streams detected.")
                    
    with control_tab2:
        text_input = st.text_input("Input Operational Core Directive Query:", placeholder="e.g., weather in Paris")
        if st.button("Execute Terminal Frame"):
            if text_input:
                cmd = text_input.lower().strip()
                
                if "time" in cmd:
                    st.session_state.assistant_text = get_time()
                    
                elif "weather" in cmd or "temp" in cmd:
                    words = cmd.split()
                    if "in" in words:
                        city_index = words.index("in") + 1
                        city = " ".join(words[city_index:])
                        st.session_state.assistant_text = get_weather(city.title())
                    else:
                        st.session_state.assistant_text = get_weather()
                        
                elif "news" in cmd:
                    st.session_state.assistant_text = get_news()
                    
                elif "remind" in cmd or "remain" in cmd:
                    st.session_state.assistant_text = set_reminder("Manual Command Entry", 10)
                    
                else:
                    st.session_state.assistant_text = f"Custom tracking sequence initialized for: '{text_input}'"
                
                st.session_state.audio_path = speak(st.session_state.assistant_text)
                
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown("""
        <div class="glass-card glow-card">
            <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px; color: #52b788; font-weight: 700; margin-bottom: 5px;">Active Node Tracking</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: #ffffff; margin-bottom: 15px;">🎙️ Contextual Output Panel</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="glass-card" style="margin-top: -10px;">
            <p style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 5px;">Realtime Decoded Text Matrix:</p>
            <p style="font-size: 1.15rem; color: #e0efe9; font-weight: 500; line-height: 1.5; margin-bottom: 0;">
                {st.session_state.assistant_text}
            </p>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
        st.markdown('<div class="glass-card" style="padding: 15px !important;">', unsafe_allow_html=True)
        st.write("🔊 **Aural Generation Sync Active**")
        with open(st.session_state.audio_path, "rb") as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        st.markdown('</div>', unsafe_allow_html=True)