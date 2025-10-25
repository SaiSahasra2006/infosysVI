# 🎵 Gesture-Based Volume Control using Hand Gestures

---

## 🧠 Project Overview

This project demonstrates a **real-time, contactless volume control system** using **computer vision** and **hand gesture recognition**.  
It utilizes **OpenCV** for webcam feed, **MediaPipe** for hand tracking, and **PyAutoGUI** for controlling system volume.  
The application runs on a **Streamlit web interface**, showing live video feed, hand tracking visuals, and real-time volume metrics.

---

## 🎯 Objective

To create a **gesture-controlled system volume manager** that allows users to adjust the audio level **without touching hardware**, providing an **interactive and hygienic** experience.

---

## ⚙️ Technologies Used

| Technology | Purpose |
|-------------|----------|
| 🐍 **Python** | Core programming language |
| 📸 **OpenCV** | Webcam video capture and frame processing |
| ✋ **MediaPipe** | Hand landmark detection and tracking |
| 🔊 **PyAutoGUI** | System volume control through simulated keypresses |
| 🌐 **Streamlit** | Web-based graphical user interface |
| 🖼️ **Pillow (PIL)** | Displaying processed images on Streamlit |

---

## 🧩 Project Modules

### 1️⃣ Webcam Input & Hand Detection
- Captures live video feed using OpenCV.
- Detects hand landmarks using MediaPipe.
- Draws connections between 21 detected hand points.

### 2️⃣ Gesture Recognition & Distance Calculation
- Identifies thumb tip (Landmark 4) and index fingertip (Landmark 8).
- Calculates **Euclidean distance** between them.
- Uses distance as input to map volume percentage.

### 3️⃣ Volume Mapping & Control
- Maps the distance range (20–200 px) to a **volume level (0–100%)**.
- Increases/decreases volume using PyAutoGUI’s “volumeup” and “volumedown”.
- Prevents flickering by adjusting only when change >5%.

### 4️⃣ Streamlit Interface
- Live webcam feed displayed on webpage.
- **Start** and **Pause** buttons for user control.
- Real-time metrics:
  - Volume Level (%)
  - Distance between fingertips (pixels)
- Includes a **line chart** for volume history and a **progress bar** for distance visualization.

---

## 📈 Working Principle

1. The webcam captures real-time video.
2. MediaPipe detects hand landmarks on each frame.
3. The distance between thumb and index fingertips is measured.
4. This distance is mapped to system volume level.
5. Streamlit interface updates:
   - Live feed with drawn hand landmarks.
   - Volume & distance metrics.
   - Visual progress bar and volume chart.

---

## 💡 Features

✅ Real-time hand tracking  
✅ Streamlit-based web UI  
✅ Contactless volume control  
✅ Smooth and dynamic volume scaling  
✅ Visual feedback (chart + progress bar)  
✅ Works on any system with a webcam  

---

## 🚀 Future Enhancements

- Add **mute/unmute gesture**.  
- Integrate with **media players** (Spotify, VLC, YouTube).  
- Add **AI-based gesture classification** for accuracy.  
- Enable **multi-hand gestures** for advanced control.  
- Host as an **online web app**.

---

## 🧠 How to Run

### 🔧 Requirements
Install dependencies:
```bash
pip install opencv-python mediapipe pyautogui streamlit pillow numpy
