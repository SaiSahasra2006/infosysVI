import cv2
import mediapipe as mp
import math
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# ----------------------
# Gesture Detection Setup
# ----------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def calculate_distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

# ----------------------
# Thresholds
# ----------------------
PINCH_THRESHOLD = (20, 50)
OPEN_THRESHOLD = 50
CLOSED_THRESHOLD = 20

# ----------------------
# GUI App
# ----------------------
class GestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Recognition Interface")
        self.root.geometry("1200x650")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        self.running = False

        # Top Header
        header = tk.Frame(root, bg="#7C4DFF", height=50)
        header.pack(side=tk.TOP, fill=tk.X)
        tk.Label(header, text="Gesture Recognition Interface",
                 font=("Helvetica", 18, "bold"), bg="#7C4DFF", fg="white").pack(side=tk.LEFT, padx=20)
        btn_frame = tk.Frame(header, bg="#7C4DFF")
        btn_frame.pack(side=tk.RIGHT, padx=20)
        ttk.Style().configure("TButton", font=("Helvetica", 12, "bold"), padding=5)
        self.start_btn = ttk.Button(btn_frame, text="▶ Start", command=self.start_camera)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.pause_btn = ttk.Button(btn_frame, text="⏸ Pause", command=self.pause_camera)
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        # Left Panel
        self.left_frame = tk.Frame(root, bg="black", width=700, height=600)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.video_label = tk.Label(self.left_frame)
        self.video_label.pack()
        # Overlay labels
        self.left_gesture_label = tk.Label(self.left_frame, text="Gesture: None", font=("Helvetica", 14, "bold"),
                                           bg="black", fg="white")
        self.left_gesture_label.place(x=10, y=10)
        self.left_distance_label = tk.Label(self.left_frame, text="Distance: N/A", font=("Helvetica", 14, "bold"),
                                           bg="black", fg="white")
        self.left_distance_label.place(x=10, y=40)

        # Right Panel
        self.right_frame = tk.Frame(root, width=350, height=600, bg="#7C4DFF")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(self.right_frame, text="Gesture States", font=("Helvetica", 18, "bold"),
                 bg="#7C4DFF", fg="white").pack(pady=20)

        # Static gestures with white Unicode icons
        gestures = [
            ("Open Hand", "✋", "green"),
            ("Pinch", "🤏", "orange"),
            ("Closed", "✊", "red")
        ]

        for name, icon, color in gestures:
            frame = tk.Frame(self.right_frame, bg="white", pady=10, padx=10)
            frame.pack(pady=10, padx=15, fill=tk.X)

            canvas = tk.Canvas(frame, width=40, height=40, bg="white", highlightthickness=0)
            canvas.pack(side=tk.LEFT, padx=10)
            canvas.create_oval(5,5,35,35, fill=color)
            # Add white icon text, centered
            canvas.create_text(20, 20, text=icon, font=("Arial", 16), fill="black", anchor="center")

            tk.Label(frame, text=name, font=("Helvetica", 16, "bold"), bg="white").pack(side=tk.LEFT, padx=10)

        # Distance meter
        tk.Label(self.right_frame, text="Distance Meter", font=("Helvetica", 18, "bold"),
                 bg="#7C4DFF", fg="white").pack(pady=20)
        self.distance_value_label = tk.Label(self.right_frame, text="0 px", font=("Helvetica", 24, "bold"),
                                             bg="#7C4DFF", fg="white")
        self.distance_value_label.pack(pady=10)
        self.distance_progress = ttk.Progressbar(self.right_frame, orient="horizontal", length=250,
                                                 mode="determinate", maximum=100)
        self.distance_progress.pack(pady=10)

        # Camera
        self.cap = cv2.VideoCapture(0)
        self.hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

        self.update_frame()

    # Start / Pause
    def start_camera(self):
        self.running = True

    def pause_camera(self):
        self.running = False

    # Update loop
    def update_frame(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = self.hands.process(rgb)

                gesture_state = "None"
                distance_val = 0

                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        h, w, _ = frame.shape
                        thumb = (int(hand_landmarks.landmark[4].x * w),
                                 int(hand_landmarks.landmark[4].y * h))
                        index = (int(hand_landmarks.landmark[8].x * w),
                                 int(hand_landmarks.landmark[8].y * h))

                        # Magenta line
                        cv2.line(frame, thumb, index, (255, 0, 255), 4)
                        cv2.circle(frame, index, 5, (255, 0, 255), -1)

                        # Colored points
                        cv2.circle(frame, thumb, 10, (0, 0, 255), -1)
                        cv2.circle(frame, index, 10, (0, 255, 0), -1)

                        # Distance
                        distance_val = int(calculate_distance(thumb, index))
                        gesture_state = "Pinch" if PINCH_THRESHOLD[0] <= distance_val <= PINCH_THRESHOLD[1] else \
                                        "Open Hand" if distance_val > OPEN_THRESHOLD else "Closed"

                # Update overlays
                self.left_gesture_label.config(text=f"{gesture_state}")
                self.left_distance_label.config(text=f"Distance: {distance_val} px")
                self.distance_value_label.config(text=f"{distance_val} px")
                self.distance_progress['value'] = min(distance_val, 100)

                # Display video
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.config(image=imgtk)

        self.root.after(10, self.update_frame)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = GestureApp(root)
    root.mainloop()
