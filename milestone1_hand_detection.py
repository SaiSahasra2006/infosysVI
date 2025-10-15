import streamlit as st
import cv2
import mediapipe as mp
from PIL import Image

# Streamlit Page Config
st.set_page_config(page_title="Hand Detection - Streamlit", layout="wide")
st.title("🖐 Hand Detection - Milestone 1 (Streamlit Version)")

# Start/Stop Buttons
run = st.checkbox("Start Camera")

# Setup MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Camera Frame Placeholder
frame_placeholder = st.empty()

# OpenCV Capture
cap = cv2.VideoCapture(0)

while run:
    success, img = cap.read()
    if not success:
        st.write("⚠️ Failed to access camera.")
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    frame_placeholder.image(img, channels="BGR")

cap.release()
