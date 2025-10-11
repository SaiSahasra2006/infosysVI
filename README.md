🎵 **VOLUME CONTROL USING HAND GESTURES**  

---

🧠 **PROJECT OVERVIEW**  

This project demonstrates **contactless system volume control** using computer vision and hand-tracking technology. The system recognizes hand gestures in real-time and adjusts the computer volume based on the distance between the thumb and index finger. It uses **MediaPipe** for hand landmark detection and **OpenCV** to visualize hand gestures on the webcam feed.  

---

🔍 **OBJECTIVE**  

To develop a **gesture-based volume control system** that allows users to adjust their computer’s audio without touching any hardware. This provides a **hygienic, modern, and interactive** way to control volume.  

---

⚙️ **TECHNOLOGIES USED**  

🐍 **Python**  
📸 **OpenCV** — for real-time webcam capture and image processing  
✋ **MediaPipe** — for detecting and tracking hand landmarks  
🔊 **PyAutoGUI / OS module** — to control system volume  
🖼️ **Tkinter & Pillow** — for GUI and displaying video feed  

---

🧩 **PROJECT MODULES**  

1️⃣ **Webcam Input & Hand Detection**  
- Captures live video from the webcam using OpenCV  
- Detects hands and extracts 21 landmarks in real-time using MediaPipe  

2️⃣ **Gesture Recognition & Distance Measurement**  
- Tracks thumb tip and index fingertip positions  
- Calculates the distance between these points  
- Classifies gestures into: Open Hand, Pinch, and Closed Hand  

3️⃣ **Volume Mapping & Control**  
- Converts gesture distance into a volume level (0%–100%)  
- Adjusts system volume dynamically  
- Smooth transitions to prevent sudden jumps  

4️⃣ **User Interface & Feedback**  
- Displays hand landmarks and gestures on the video feed  
- Shows real-time volume level via a progress bar and numeric display  

---

📈 **WORKING PRINCIPLE**  

- The webcam captures a **live video feed**  
- MediaPipe identifies **hand landmarks**  
- Distance between thumb and index fingertips is measured  
- Based on the distance:  
  - 🤏 Pinch → Lower volume  
  - ✋ Open hand → Higher volume  
- A visual progress bar reflects the current volume level  

---

💡 **FEATURES**  

✅ Real-time hand detection and gesture recognition  
✅ Contactless volume control  
✅ Smooth and dynamic volume adjustment  
✅ Visual feedback through GUI and progress bar  
✅ Works with only a standard webcam  
✅ Easily extendable for more gestures  

---

🧠 **FUTURE ENHANCEMENTS**  

- Gesture-based mute/unmute functionality  
- Integration with media apps like YouTube or Spotify  
- Support for multi-hand gestures for advanced controls  
- AI-based gesture classification for improved accuracy  

---



