import streamlit as st
import base64

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Gesture Volume Control",
    page_icon="✋",
    layout="centered",
)

# ---- CUSTOM CSS ----
st.markdown("""
<style>
/* Dark Theme */
body {
    background-color: #0e1117;
    color: #ffffff;
}

/* Center content */
.main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-top: 80px;
}

/* Title styling */
.title {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00ffe0, #0078ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 10px;
}

/* Subtitle */
.subtitle {
    color: #c0c0c0;
    font-size: 1.2rem;
    text-align: center;
    margin-bottom: 40px;
    max-width: 600px;
}

/* Features Section */
.features {
    display: flex;
    justify-content: center;
    gap: 40px;
    margin-bottom: 40px;
}

.feature-box {
    background-color: #1c1f26;
    border-radius: 16px;
    padding: 25px;
    width: 200px;
    text-align: center;
    box-shadow: 0px 0px 10px #0078ff20;
    transition: transform 0.3s, box-shadow 0.3s;
}

.feature-box:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 15px #00ffe060;
}

/* Button */
.start-btn {
    background: linear-gradient(90deg, #0078ff, #00ffe0);
    color: black;
    font-size: 1.1rem;
    font-weight: bold;
    padding: 14px 40px;
    border-radius: 30px;
    border: none;
    cursor: pointer;
    transition: all 0.3s;
    text-decoration: none;
}

.start-btn:hover {
    background: linear-gradient(90deg, #00ffe0, #0078ff);
    transform: scale(1.08);
    box-shadow: 0px 0px 20px #00ffe080;
}

/* Illustration */
.illustration {
    width: 180px;
    margin-bottom: 30px;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}
</style>
""", unsafe_allow_html=True)

# ---- MAIN CONTENT ----
st.markdown('<div class="main">', unsafe_allow_html=True)

# Hand icon illustration (emoji or image)
st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/2721/2721299.png" class="illustration">', unsafe_allow_html=True)

st.markdown('<div class="title">Gesture-Based Volume Control</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Control your system volume effortlessly using simple hand gestures through AI-powered computer vision.</div>', unsafe_allow_html=True)

# Features Section
st.markdown("""
<div class="features">
    <div class="feature-box">✋ Real-time Hand Tracking</div>
    <div class="feature-box">🎵 Smooth & Responsive Control</div>
    <div class="feature-box">⚙️ Contactless Volume Adjustment</div>
</div>
""", unsafe_allow_html=True)

# Start button
if st.button("🚀 Start App"):
    st.switch_page("pages/milestone4.py")


st.markdown('</div>', unsafe_allow_html=True)
