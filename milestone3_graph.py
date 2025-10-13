import os
import warnings

# -------------------- Suppress logs --------------------
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['ABSL_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore", category=UserWarning, module='google.protobuf')

import cv2
import mediapipe as mp
import math
import pyautogui
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ------------------------ Constants ------------------------
MAX_HISTORY = 50

# ------------------------ Hand Detection ------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# ------------------------ Tkinter GUI ------------------------
class VolumeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture-Based Volume Control")
        self.root.geometry("1300x700")
        self.root.configure(bg="white")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.running = False  # Camera paused initially
        self.prev_level = None
        self.volume_history = deque(maxlen=MAX_HISTORY)
        self.dist_val = 0

        # ---------------- Left Panel ----------------
        self.left_frame = tk.Frame(root, width=800, height=700, bg="black")
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Header with buttons
        header = tk.Frame(self.left_frame, bg="#7C4DFF", height=50)
        header.pack(side=tk.TOP, fill=tk.X)
        tk.Label(header, text="Gesture-Based Volume Control",
                 font=("Helvetica", 18, "bold"), bg="#7C4DFF", fg="white").pack(side=tk.LEFT, padx=20)
        btn_frame = tk.Frame(header, bg="#7C4DFF")
        btn_frame.pack(side=tk.RIGHT, padx=20)
        ttk.Style().configure("TButton", font=("Helvetica", 12, "bold"), padding=5)
        self.start_btn = ttk.Button(btn_frame, text="▶ Start", command=self.start_camera)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.pause_btn = ttk.Button(btn_frame, text="⏸ Pause", command=self.pause_camera)
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        # Video Label
        self.video_label = tk.Label(self.left_frame)
        self.video_label.pack()
        self.volume_label = tk.Label(self.left_frame, text="Vol: 0%", font=("Arial", 16, "bold"),
                                     bg="black", fg="white")
        self.volume_label.pack(pady=5)

        # ---------------- Right Panel ----------------
        self.right_frame = tk.Frame(root, width=450, height=700, bg="#7C4DFF")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        tk.Label(self.right_frame, text="Volume Graph & Distance", font=("Helvetica", 18, "bold"),
                 bg="#7C4DFF", fg="white").pack(pady=10)

        # Distance Meter
        self.distance_label = tk.Label(self.right_frame, text="Distance: 0 px",
                                       font=("Helvetica", 20, "bold"), bg="#7C4DFF", fg="yellow")
        self.distance_label.pack(pady=10)
        self.distance_progress = ttk.Progressbar(self.right_frame, orient="horizontal", length=300,
                                                 mode="determinate", maximum=100)
        self.distance_progress.pack(pady=10)

        # Matplotlib Graph
        self.fig, self.ax = plt.subplots(figsize=(4.5, 5))
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, MAX_HISTORY)
        self.ax.set_xlabel("Frames")
        self.ax.set_ylabel("Volume (%)")
        self.ax.set_facecolor('#EDE7F6')
        self.line, = self.ax.plot([], [], 'b-', linewidth=3)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(pady=20)

        # Video capture
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Camera Error", "Cannot open webcam. Check connection.")

        self.hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

    # ---------------- Distance ----------------
    def calculate_distance(self, p1, p2):
        return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

    # ---------------- Start / Pause ----------------
    def start_camera(self):
        if not self.running:
            self.running = True
            self.update_frame()

    def pause_camera(self):
        self.running = False

    # ---------------- Update Loop ----------------
    def update_frame(self):
        if not self.running or not self.root.winfo_exists():
            return

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb)

            volume_level = 0

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    x1, y1 = int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h)
                    x2, y2 = int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h)

                    cv2.circle(frame, (x1, y1), 10, (255, 0, 0), -1)
                    cv2.circle(frame, (x2, y2), 10, (0, 255, 0), -1)
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)

                    dist = self.calculate_distance((x1, y1), (x2, y2))
                    self.dist_val = int(dist)

                    volume_level = int(((dist - 20) / (200 - 20)) * 100)
                    volume_level = max(0, min(volume_level, 100))

                    if self.prev_level is None or abs(volume_level - self.prev_level) > 5:
                        if self.prev_level is not None:
                            if volume_level > self.prev_level:
                                pyautogui.press("volumeup")
                            else:
                                pyautogui.press("volumedown")
                        self.prev_level = volume_level

            # Update UI
            self.volume_label.config(text=f"Vol: {volume_level}%")
            self.distance_label.config(text=f"Distance: {self.dist_val} px")
            self.distance_progress['value'] = min(self.dist_val, 100)

            self.volume_history.append(volume_level)
            self.line.set_data(range(len(self.volume_history)), self.volume_history)
            self.ax.set_xlim(0, max(MAX_HISTORY, len(self.volume_history)))
            self.canvas.draw()

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.config(image=imgtk)

        self.root.after(10, self.update_frame)

    # ---------------- Safe Close ----------------
    def on_close(self):
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

# ------------------------ Run App ------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = VolumeApp(root)
    root.mainloop()
