import cv2
import mediapipe as mp
import math
import pyautogui
import streamlit as st
import numpy as np
from collections import deque
from PIL import Image

# -------------------- Constants --------------------
MAX_HISTORY = 50

# -------------------- Hand Detection --------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="Gesture-Based Volume Control", layout="wide")

st.title("🎛 Gesture-Based Volume Control")

col1, col2 = st.columns([2, 1])

# Left column: video
video_display = col1.empty()

# Right column: controls and graphs
start_btn = col2.button("▶ Start")
pause_btn = col2.button("⏸ Pause")
vol_text = col2.empty()
dist_text = col2.empty()
vol_chart = col2.line_chart(np.zeros(MAX_HISTORY))
dist_progress = col2.progress(0)

# -------------------- Variables --------------------
running = False
prev_level = None
volume_history = deque(maxlen=MAX_HISTORY)
dist_val = 0

# -------------------- Distance Function --------------------
def calculate_distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

# -------------------- Start / Pause --------------------
if start_btn:
    running = True

if pause_btn:
    running = False

# -------------------- OpenCV Capture --------------------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    st.error("Cannot open webcam")
    st.stop()

# -------------------- Main Loop --------------------
while running:
    ret, frame = cap.read()
    if not ret:
        st.warning("Failed to capture frame")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    volume_level = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            x1, y1 = int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h)
            x2, y2 = int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h)

            cv2.circle(frame, (x1, y1), 10, (255, 0, 0), -1)
            cv2.circle(frame, (x2, y2), 10, (0, 255, 0), -1)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)

            dist = calculate_distance((x1, y1), (x2, y2))
            dist_val = int(dist)

            volume_level = int(((dist - 20) / (200 - 20)) * 100)
            volume_level = max(0, min(volume_level, 100))

            if prev_level is None or abs(volume_level - prev_level) > 5:
                if prev_level is not None:
                    if volume_level > prev_level:
                        pyautogui.press("volumeup")
                    else:
                        pyautogui.press("volumedown")
                prev_level = volume_level

    # -------------------- Update Streamlit UI --------------------
    vol_text.markdown(f"**Volume:** {volume_level}%")
    dist_text.markdown(f"**Distance:** {dist_val} px")
    dist_progress.progress(min(dist_val, 100))

    volume_history.append(volume_level)
    vol_chart.line_chart(np.array(volume_history))

    # Show frame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame_rgb)
    video_display.image(image)

    # Stop button check
    if pause_btn:
        running = False
        break

# -------------------- Cleanup --------------------
cap.release()
st.info("Camera stopped")
