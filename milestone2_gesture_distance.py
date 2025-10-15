import streamlit as st
import cv2
import mediapipe as mp
import math
from PIL import Image
import numpy as np
import time

# ---------------------- Gesture Detection Setup ----------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def calculate_distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

# ---------------------- Thresholds ----------------------
PINCH_THRESHOLD = (20, 50)
OPEN_THRESHOLD = 50
CLOSED_THRESHOLD = 20

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title="Gesture Recognition Interface", layout="wide")

st.markdown("<h2 style='text-align: center; color: #7C4DFF;'>Gesture Recognition Interface</h2>", unsafe_allow_html=True)

start_btn = st.button("▶ Start")
stop_btn = st.button("⏸ Pause")

col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### Gesture States")
    st.markdown("🟢 **Open Hand (✋)**")
    st.markdown("🟠 **Pinch (🤏)**")
    st.markdown("🔴 **Closed (✊)**")
    
    st.markdown("### Distance Meter")
    distance_placeholder = st.empty()
    progress_bar = st.progress(0)

# Camera + MediaPipe
cap = cv2.VideoCapture(0)
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

frame_placeholder = col1.empty()

running = start_btn

while running:
    ret, frame = cap.read()
    if not ret:
        st.error("Failed to access camera.")
        break
    
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture_state = "None"
    distance_val = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            h, w, _ = frame.shape
            thumb = (int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h))
            index = (int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h))
            
            cv2.line(frame, thumb, index, (255, 0, 255), 3)
            cv2.circle(frame, thumb, 10, (0, 0, 255), -1)
            cv2.circle(frame, index, 10, (0, 255, 0), -1)

            distance_val = int(calculate_distance(thumb, index))
            gesture_state = "Pinch" if PINCH_THRESHOLD[0] <= distance_val <= PINCH_THRESHOLD[1] else \
                            "Open Hand" if distance_val > OPEN_THRESHOLD else "Closed"

    # Display Distance
    distance_placeholder.markdown(f"**Distance:** {distance_val} px")
    progress_bar.progress(min(distance_val, 100) / 100)

    # Show Frame
    frame_placeholder.image(frame, channels="BGR")

    # Stop logic
    if stop_btn:
        running = False

cap.release()
